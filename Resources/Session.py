"""Serial sessions and instance ownership, independent of wx and pyo."""

import copy
import json
import os
import tempfile
import uuid
from contextlib import contextmanager
from contextvars import ContextVar
from functools import wraps


INSTANCE_KEYS = frozenset((
    'currentCeciliaFile', 'builtinModule', 'currentModuleRef', 'currentModule',
    'currentModuleName', 'moduleDescription', 'interfaceWidgets', 'grapher',
    'userSliders', 'userTogglePopups', 'userSamplers', 'userInputs',
    'samplerSliders', 'samplerTogglePopup', 'initPreset', 'presetPanel',
    'presetToLoad',
))
active_instance = ContextVar('cecilia_module_instance', default=None)


@contextmanager
def instance_context(instance):
    token = active_instance.set(instance)
    try:
        yield instance
    finally:
        active_instance.reset(token)


def bind_instance(cls):
    """Bind Python methods (including deferred wx/pyo callbacks) to their owner.

    Ownership is captured at construction, never inferred from editor selection.
    Only classes belonging to Cecilia are decorated, not wx or pyo classes.
    """
    for name, method in list(vars(cls).items()):
        if not callable(method) or isinstance(method, type):
            continue
        if isinstance(method, (staticmethod, classmethod)):
            continue

        def bind(method, name):
            @wraps(method)
            def owned(self, *args, **kwargs):
                if name == '__init__' and '_cecilia_owner' not in self.__dict__:
                    self._cecilia_owner = active_instance.get()
                owner = self.__dict__.get('_cecilia_owner')
                if owner is None:
                    return method(self, *args, **kwargs)
                with instance_context(owner):
                    return method(self, *args, **kwargs)
            return owned

        setattr(cls, name, bind(method, name))
    return cls


def shared_effects(method):
    """Shared effects automation is hosted by the first module's editor."""
    @wraps(method)
    def wrapped(*args, **kwargs):
        from . import CeciliaLib
        modules = CeciliaLib.session.modules
        if not modules:
            return method(*args, **kwargs)
        with instance_context(modules[0]):
            return method(*args, **kwargs)
    return wrapped


class ModuleInstance:
    def __init__(self, path, module_class, interface, metadata=None, builtin=False,
                 instance_id=None):
        self.id = instance_id or uuid.uuid4().hex
        self.path = os.path.abspath(path)
        self.module_class = module_class
        self.interface = copy.deepcopy(interface)
        self.metadata = metadata
        self.embedded_presets = {}
        self.upstream = None
        self.inputs = None
        self.editor = None
        self.retired = False
        self.state = {
            'currentCeciliaFile': self.path, 'builtinModule': builtin,
            'currentModuleRef': module_class, 'currentModule': None,
            'currentModuleName': os.path.splitext(os.path.basename(path))[0],
            'moduleDescription': module_class.__doc__ or '',
            'interfaceWidgets': self.interface, 'grapher': None,
            'userSliders': [], 'userTogglePopups': [], 'userSamplers': [],
            'userInputs': {}, 'samplerSliders': [], 'samplerTogglePopup': [],
            'initPreset': None, 'presetPanel': None, 'presetToLoad': None,
        }

    @property
    def primary_input(self):
        inputs = [w for w in self.interface if w['type'] in ('csampler', 'cfilein')]
        if self.metadata is None:
            return inputs[0]['name'] if len(inputs) == 1 and inputs[0]['type'] == 'csampler' else None
        primary = self.metadata.get('primary_input')
        auxiliaries = self.metadata.get('auxiliary_inputs', [])
        if not isinstance(auxiliaries, list):
            return None
        names = {w['name']: w['type'] for w in inputs}
        if names.get(primary) != 'csampler':
            return None
        if set(names) != {primary, *auxiliaries}:
            return None
        if any(names.get(name) != 'cfilein' for name in auxiliaries):
            return None
        return primary

    @property
    def auxiliary_inputs(self):
        return self.metadata.get('auxiliary_inputs', []) if self.metadata else []


class ChainSession:
    def __init__(self):
        self.modules = []
        self.selected_id = None
        self.view = 'graph'
        self.path = None
        self.saved_snapshot = None

    @property
    def selected(self):
        return next((m for m in self.modules if m.id == self.selected_id), None)

    @staticmethod
    def validate_order(modules):
        ids = [m.id for m in modules]
        if len(set(ids)) != len(ids):
            raise ValueError('Module instance IDs must be unique.')
        for index, module in enumerate(modules[1:], 2):
            if module.primary_input is None:
                raise ValueError('Stage %d (%s) needs a compatible live stream input. '
                                 'Use this module first or by itself.' %
                                 (index, module.state['currentModuleName']))

    def append(self, module, first=False):
        proposed = [module] + self.modules if first else self.modules + [module]
        self.validate_order(proposed)
        self.modules = proposed
        self.selected_id = module.id

    def replace(self, old, new):
        proposed = [new if m is old else m for m in self.modules]
        self.validate_order(proposed)
        self.modules = proposed
        self.selected_id = new.id

    def remove(self, module):
        proposed = [m for m in self.modules if m is not module]
        self.validate_order(proposed)
        index = self.modules.index(module)
        self.modules = proposed
        if self.selected_id == module.id:
            self.selected_id = proposed[min(index, len(proposed)-1)].id if proposed else None
        if not proposed:
            self.view = 'chain'

    def move(self, module, direction):
        proposed = list(self.modules)
        index = proposed.index(module)
        target = index + direction
        if not 0 <= target < len(proposed):
            return
        proposed[index], proposed[target] = proposed[target], proposed[index]
        self.validate_order(proposed)
        self.modules = proposed


def encode_paths(data, base, encode):
    """Convert module and asset path fields, leaving widget strings untouched."""
    if isinstance(data, list):
        return [encode_paths(item, base, encode) for item in data]
    if not isinstance(data, dict):
        return data
    result = {}
    for key, value in data.items():
        if key in ('path', 'module_path', 'output_path') and isinstance(value, str) and value:
            if encode:
                try:
                    value = os.path.relpath(os.path.abspath(value), base)
                except ValueError:  # Different Windows drives.
                    value = os.path.abspath(value)
            else:
                value = os.path.abspath(os.path.join(base, value))
        else:
            value = encode_paths(value, base, encode)
        result[key] = value
    return result


def normalize_snapshot(value):
    """Canonicalize widget roundoff and tuples for stable saves/dirty checks."""
    if isinstance(value, float):
        return float(format(value, '.12g'))
    if isinstance(value, (list, tuple)):
        return [normalize_snapshot(item) for item in value]
    if isinstance(value, dict):
        return {key: normalize_snapshot(item) for key, item in value.items()}
    return value


def write_session(path, snapshot):
    base = os.path.dirname(os.path.abspath(path))
    document = encode_paths(snapshot, base, True)
    document['format'] = 'cecilia-chain'
    document['version'] = 1
    descriptor, temporary = tempfile.mkstemp(prefix='.c5chain-', dir=base)
    try:
        with os.fdopen(descriptor, 'w', encoding='utf-8') as stream:
            json.dump(document, stream, ensure_ascii=False, indent=2, allow_nan=False)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def read_session(path):
    with open(path, encoding='utf-8') as stream:
        document = json.load(stream)
    if document.get('format') != 'cecilia-chain' or document.get('version') != 1:
        raise ValueError('Unsupported Cecilia chain session format or version.')
    if not isinstance(document.get('modules'), list) or not isinstance(document.get('output'), dict):
        raise ValueError('Invalid chain session: modules and output settings are required.')
    return encode_paths(document, os.path.dirname(os.path.abspath(path)), False)
