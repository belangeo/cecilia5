"""Graph sessions and instance ownership, independent of wx and pyo."""

import copy
import json
import math
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
        self.source_id = None
        self.source_ids = []
        self.connections = []
        self.output_connections = []
        self.positions = {}
        self.selected_id = None
        self.view = 'graph'
        self.path = None
        self.saved_snapshot = None

    @property
    def selected(self):
        return next((m for m in self.modules if m.id == self.selected_id), None)

    @staticmethod
    def validate_order(modules, source_ids=None):
        ids = [m.id for m in modules]
        if len(set(ids)) != len(ids):
            raise ValueError('Module instance IDs must be unique.')
        sources = set(source_ids) if source_ids is not None else {modules[0].id} if modules else set()
        for index, module in enumerate(modules, 1):
            if module.id not in sources and module.primary_input is None:
                raise ValueError('Stage %d (%s) needs a compatible live stream input. '
                                 'Use this module first or by itself.' %
                                 (index, module.state['currentModuleName']))

    @property
    def source(self):
        return next((m for m in self.modules if m.id == self.source_id), None)

    @property
    def sources(self):
        return [m for m in self.modules if m.id in self.source_ids]

    def select(self, module, preserve_source=False):
        self.selected_id = module.id if module else None
        if module and module.id in self.source_ids and not preserve_source:
            self.source_id = module.id

    def routing_snapshot(self):
        return copy.deepcopy(dict(source_id=self.source_id, source_ids=self.source_ids, connections=self.connections,
                                  output_connections=self.output_connections, positions=self.positions))

    def restore_routing(self, routing):
        for key in ('source_id', 'source_ids', 'connections', 'output_connections', 'positions'):
            setattr(self, key, copy.deepcopy(routing[key]))

    def clear(self):
        self.modules = []
        self.selected_id = self.source_id = None
        self.source_ids = []
        self.connections = []
        self.output_connections = []
        self.positions = {}

    def validate_graph(self):
        ids = [m.id for m in self.modules]
        if not isinstance(self.source_ids, list) or len(set(self.source_ids)) != len(self.source_ids) or any(i not in ids for i in self.source_ids):
            raise ValueError('Invalid source modules.')
        if (ids and (not self.source_ids or self.source_id not in self.source_ids)) or (not ids and self.source_id is not None):
            raise ValueError('Select a valid reference source.')
        self.validate_order(self.modules, self.source_ids)
        if not isinstance(self.connections, list) or not isinstance(self.output_connections, list):
            raise ValueError('Invalid graph connections.')
        seen = set()
        for edge in self.connections:
            if not isinstance(edge, (list, tuple)) or len(edge) != 2:
                raise ValueError('Invalid graph connection.')
            a, b = edge
            if a not in ids or b not in ids or a == b or b in self.source_ids:
                raise ValueError('Connections must join different modules and cannot enter a source.')
            if (a, b) in seen:
                raise ValueError('Duplicate connection.')
            seen.add((a, b))
        if any(i not in ids for i in self.output_connections) or len(set(self.output_connections)) != len(self.output_connections):
            raise ValueError('Invalid or duplicate output connection.')
        if not isinstance(self.positions, dict):
            raise ValueError('Invalid node positions.')
        for node, point in self.positions.items():
            if node not in ids or not isinstance(point, (list, tuple)) or len(point) != 2 or any(
                    isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) or v < 0 for v in point):
                raise ValueError('Invalid node position.')
        self.topological_order()

    def topological_order(self):
        pending = list(self.modules)
        ordered = []
        done = set()
        while pending:
            ready = next((m for m in pending if all(a in done for a, b in self.connections if b == m.id)), None)
            if ready is None:
                raise ValueError('Feedback connections are not supported.')
            pending.remove(ready)
            ordered.append(ready)
            done.add(ready.id)
        return ordered

    def active_modules(self):
        self.validate_graph()
        reachable = set(self.source_ids)
        for module in self.topological_order():
            if any(a in reachable and b == module.id for a, b in self.connections):
                reachable.add(module.id)
        audible = set(self.output_connections) & reachable
        for module in reversed(self.topological_order()):
            if any(a == module.id and b in audible for a, b in self.connections):
                audible.add(module.id)
        return [m for m in self.topological_order() if m.id in audible & reachable]

    def connect(self, source, target=None):
        before = self.routing_snapshot()
        if target is None:
            self.output_connections.append(source)
        else:
            self.connections.append([source, target])
        try:
            self.validate_graph()
        except Exception:
            self.restore_routing(before)
            raise

    def disconnect(self, source, target=None):
        if target is None:
            self.output_connections.remove(source)
        else:
            self.connections.remove([source, target])

    def append(self, module, first=False, as_source=False):
        proposed = self.modules + [module]
        is_source = not self.modules or module.primary_input is None or as_source or first
        sources = self.source_ids + ([module.id] if is_source else [])
        self.validate_order(proposed, sources)
        self.modules = proposed
        self.source_ids = sources
        if len(proposed) == 1:
            self.output_connections = [module.id]
        self.select(module)

    def set_source(self, module, enabled):
        before = self.routing_snapshot()
        if enabled:
            if module.id not in self.source_ids:
                self.source_ids.append(module.id)
            self.source_id = module.id
        else:
            self.source_ids.remove(module.id)
            if self.source_id == module.id:
                self.source_id = self.source_ids[0] if self.source_ids else None
        try:
            self.validate_graph()
        except Exception:
            self.restore_routing(before)
            raise

    def replace(self, old, new):
        proposed = [new if m is old else m for m in self.modules]
        sources = [new.id if i == old.id else i for i in self.source_ids]
        self.validate_order(proposed, sources)
        self.modules = proposed
        self.source_ids = sources
        self.connections = [[new.id if i == old.id else i for i in edge] for edge in self.connections]
        self.output_connections = [new.id if i == old.id else i for i in self.output_connections]
        if old.id in self.positions:
            self.positions[new.id] = self.positions.pop(old.id)
        if old.id == self.source_id:
            self.source_id = new.id
        self.select(new)

    def remove(self, module):
        if module.id in self.source_ids and len(self.source_ids) == 1 and len(self.modules) > 1:
            raise ValueError('Keep at least one source while processing modules remain.')
        index = self.modules.index(module)
        self.modules.remove(module)
        self.source_ids = [i for i in self.source_ids if i != module.id]
        if self.source_id == module.id:
            self.source_id = self.source_ids[0] if self.source_ids else None
        self.connections = [edge for edge in self.connections if module.id not in edge]
        self.output_connections = [i for i in self.output_connections if i != module.id]
        self.positions.pop(module.id, None)
        if self.selected_id == module.id:
            self.selected_id = self.modules[min(index, len(self.modules)-1)].id if self.modules else None
        if not self.modules:
            self.source_id = None
            self.view = 'chain'

    def move(self, module, direction):
        raise ValueError('Use graph connections to change audio routing.')


def mix_signals(signals):
    """One cable is unity; each cable in a multiple-input mix contributes 0.707."""
    if not signals:
        raise ValueError('No connected audio signals.')
    if len(signals) == 1:
        return signals[0]
    result = signals[0] * 0.707
    for signal in signals[1:]:
        result = result + signal * 0.707
    return result


def serial_routing(modules):
    ids = [m['id'] for m in modules]
    return dict(source_id=ids[0] if ids else None, source_ids=ids[:1],
                connections=[list(edge) for edge in zip(ids, ids[1:])],
                output_connections=ids[-1:], positions={})


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
    document['version'] = 3
    if 'source_id' not in document:
        document.update(serial_routing(document['modules']))
    document.setdefault('source_ids', [document['source_id']] if document['source_id'] else [])
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
    if document.get('format') != 'cecilia-chain' or document.get('version') not in (1, 2, 3):
        raise ValueError('Unsupported Cecilia chain session format or version.')
    if not isinstance(document.get('modules'), list) or not isinstance(document.get('output'), dict):
        raise ValueError('Invalid chain session: modules and output settings are required.')
    if document['version'] == 1:
        document.update(serial_routing(document['modules']))
        document['version'] = 3
    if document['version'] == 2:
        document['source_ids'] = [document['source_id']] if document.get('source_id') else []
        document['version'] = 3
    for key in ('source_id', 'source_ids', 'connections', 'output_connections', 'positions'):
        if key not in document:
            raise ValueError('Missing graph field: ' + key)
    return encode_paths(document, os.path.dirname(os.path.abspath(path)), False)
