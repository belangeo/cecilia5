"""wx canvas for editing the session's directed audio graph."""

import math
import wx
from . import CeciliaLib
from .constants import BACKGROUND_COLOUR
from .PopupMenu import popup_menu


class RoutingGraph(wx.ScrolledWindow):
    NODE_W, NODE_H = 160, 82
    SOURCE_DIVIDER_X = 210

    def __init__(self, parent, frame):
        super().__init__(parent, style=wx.HSCROLL | wx.VSCROLL | wx.WANTS_CHARS)
        self.frame = frame
        self.running = False
        self.selected_edge = None
        self.drag = None
        self.cursor = (0, 0)
        self.rects = {}
        self.cables = []
        self.SetBackgroundColour(BACKGROUND_COLOUR)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.SetToolTip('Click a port, move to another port, and click to connect. Escape cancels. Select a cable and press Delete to disconnect. Double-click a module to edit. Right-click empty space to add a module.')
        self.SetScrollRate(10, 10)
        self.SetMinSize((100, 100))
        self.Bind(wx.EVT_PAINT, self.paint)
        self.Bind(wx.EVT_SIZE, self.resize)
        self.Bind(wx.EVT_LEFT_DOWN, self.press)
        self.Bind(wx.EVT_LEFT_UP, self.release)
        self.Bind(wx.EVT_MOTION, self.motion)
        self.Bind(wx.EVT_LEFT_DCLICK, self.edit)
        self.Bind(wx.EVT_RIGHT_UP, self.menu)
        self.Bind(wx.EVT_KEY_DOWN, self.key)
        self.Bind(wx.EVT_MOUSE_CAPTURE_LOST, self.capture_lost)

    def rebuild(self):
        session = CeciliaLib.session
        for index, module in enumerate(m for m in session.modules if m.id not in session.source_ids):
            # Keep new nodes clear of the direct source-to-Output cable.
            session.positions.setdefault(module.id, [280 + (index // 4) * 210, 150 + (index % 4) * 125])
        right = max([520] + [int(p[0]) + self.NODE_W + 80 for p in session.positions.values()])
        width = max(self.GetClientSize().width, right + self.NODE_W + 30)
        height = max([300, 150 + len(session.sources) * 125, self.GetClientSize().height] + [int(p[1]) + self.NODE_H + 60 for p in session.positions.values()])
        self.SetVirtualSize((width, height))
        self.rects = {m.id: wx.Rect(24, 40 + session.sources.index(m) * 125, self.NODE_W, self.NODE_H) if m.id in session.source_ids else
                      wx.Rect(int(session.positions[m.id][0]), int(session.positions[m.id][1]), self.NODE_W, self.NODE_H)
                      for m in session.modules}
        self.rects[None] = wx.Rect(width - self.NODE_W - 24, 40, self.NODE_W, self.NODE_H)
        edges = [tuple(edge) for edge in session.connections] + [(node, None) for node in session.output_connections]
        if self.selected_edge not in edges:
            self.selected_edge = None
        self.Refresh()

    def resize(self, event):
        self.rebuild()
        event.Skip()

    def point(self, event):
        return tuple(self.CalcUnscrolledPosition(event.GetPosition()))

    def port(self, node, output):
        rect = self.rects[node]
        return (rect.GetRight() if output else rect.x, rect.y + self.NODE_H // 2)

    def hit_port(self, point):
        for node in self.rects:
            for output in (False, True):
                if (node is None and output) or (node in CeciliaLib.session.source_ids and not output):
                    continue
                x, y = self.port(node, output)
                if math.hypot(point[0]-x, point[1]-y) <= 11:
                    return node, output
        return None

    def hit_node(self, point):
        return next((node for node, rect in reversed(list(self.rects.items())) if node is not None and rect.Contains(point)), None)

    @staticmethod
    def curve(start, end):
        reach = max(60, abs(end[0]-start[0]) * .5)
        c1, c2 = (start[0]+reach, start[1]), (end[0]-reach, end[1])
        points = []
        for step in range(33):
            t = step / 32
            points.append(tuple((1-t)**3*start[k] + 3*(1-t)**2*t*c1[k] + 3*(1-t)*t*t*c2[k] + t**3*end[k] for k in (0, 1)))
        return points

    def paint(self, event):
        dc = wx.AutoBufferedPaintDC(self)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        self.DoPrepareDC(dc)
        gc = wx.GraphicsContext.Create(dc)
        session = CeciliaLib.session
        active = {m.id for m in session.active_modules()}
        gc.SetPen(wx.Pen('#a0a0a0', 1))
        gc.StrokeLine(self.SOURCE_DIVIDER_X, 12, self.SOURCE_DIVIDER_X, self.GetVirtualSize().height - 12)
        self.cables = []
        edges = [tuple(edge) for edge in session.connections] + [(node, None) for node in session.output_connections]
        for edge in edges:
            if edge[0] not in self.rects or edge[1] not in self.rects:
                continue
            points = self.curve(self.port(edge[0], True), self.port(edge[1], False))
            self.cables.append((edge, points))
            gc.SetPen(wx.Pen('#ffd080' if edge == self.selected_edge else '#83b6d5', 3 if edge == self.selected_edge else 2))
            gc.StrokeLines(points)
        if self.drag and self.drag[0] == 'cable':
            node, output = self.drag[1]
            start, end = self.port(node, output), self.cursor
            if not output:
                start, end = end, start
            gc.SetPen(wx.Pen('#ffd080', 2))
            gc.StrokeLines(self.curve(start, end))
        dc.SetTextForeground(wx.WHITE)
        for node, rect in self.rects.items():
            selected = node is not None and node == session.selected_id
            gc.SetPen(wx.Pen('#e4bd80' if selected else '#777777', 2 if selected else 1))
            gc.SetBrush(wx.Brush('#38434b' if node in active or node is None else '#303030'))
            gc.DrawRoundedRectangle(rect.x, rect.y, rect.width, rect.height, 7)
            module = next((m for m in session.modules if m.id == node), None)
            title = module.state['currentModuleName'] if module else 'Output'
            dc.DrawText(title[:22], rect.x+12, rect.y+10)
            status = ('Source • selected' if node == session.source_id else 'Source') if node in session.source_ids else 'Final mix / effects' if node is None else 'Active' if node in active else 'Inactive'
            dc.DrawText(status, rect.x+12, rect.y+29)
            if node is not None:
                dc.DrawText('Edit', rect.x+12, rect.y+57)
                if self.can_remove(node):
                    dc.DrawText('Remove', rect.x+85, rect.y+57)
            for output in (False, True):
                if (node is None and output) or (node in session.source_ids and not output):
                    continue
                x, y = self.port(node, output)
                gc.SetBrush(wx.Brush('#83b6d5'))
                gc.DrawEllipse(x-5, y-5, 10, 10)
        if not session.modules:
            dc.DrawText('Add a module to start an audio graph.', 24, 150)

    @staticmethod
    def segment_distance(point, start, end):
        dx, dy = end[0]-start[0], end[1]-start[1]
        length = dx*dx + dy*dy
        t = max(0, min(1, ((point[0]-start[0])*dx + (point[1]-start[1])*dy) / length)) if length else 0
        return math.hypot(point[0]-start[0]-t*dx, point[1]-start[1]-t*dy)

    def press(self, event):
        self.SetFocus()
        point = self.point(event)
        self.cursor = point
        port = self.hit_port(point)
        if self.drag and self.drag[0] == 'cable':
            origin = self.drag[1]
            self.drag = None
            if port and port[1] != origin[1] and not self.running:
                source, destination = (origin[0], port[0]) if origin[1] else (port[0], origin[0])
                try:
                    CeciliaLib.session.connect(source, destination)
                    CeciliaLib.getVar('audioServer').cleanup_module()
                except ValueError as error:
                    CeciliaLib.showErrorDialog('Cannot connect modules', str(error))
            self.rebuild()
            return
        if port and not self.running:
            self.drag = ('cable', port)
        else:
            node = self.hit_node(point)
            if node:
                module = next(m for m in CeciliaLib.session.modules if m.id == node)
                rect = self.rects[node]
                if point[1] >= rect.y + 53:
                    if point[0] < rect.x + 75:
                        self.open_editor(module)
                    elif not self.running and self.can_remove(node):
                        CeciliaLib.removeChainModule(module)
                    return
                from . import ChainUI
                ChainUI.select(self.frame, module, change_view=False)
                self.selected_edge = None
                if not self.running and (node not in CeciliaLib.session.source_ids or self.can_move_source(module)):
                    self.drag = ('node', node, (point[0]-rect.x, point[1]-rect.y))
            else:
                self.selected_edge = None
                for edge, points in reversed(self.cables):
                    if any(self.segment_distance(point, a, b) < 9 for a, b in zip(points, points[1:])):
                        self.selected_edge = edge
                        break
        if self.drag and self.drag[0] == 'node':
            self.CaptureMouse()
        self.Refresh()

    def motion(self, event):
        self.cursor = self.point(event)
        if self.drag and not self.running:
            if self.drag[0] == 'node':
                _, node, offset = self.drag
                graph = CeciliaLib.session
                x, y = self.cursor[0]-offset[0], self.cursor[1]-offset[1]
                if node in graph.source_ids:
                    if x <= self.SOURCE_DIVIDER_X:
                        return
                    module = next(m for m in graph.modules if m.id == node)
                    if not self.can_move_source(module):
                        return
                    graph.set_source(module, False)
                    graph.positions[node] = [max(220, x), max(16, y)]
                    CeciliaLib.getVar('audioServer').cleanup_module()
                    from . import ChainUI
                    ChainUI.refresh(self.frame)
                else:
                    graph.positions[node] = [max(220, x), max(16, y)]
                    self.rebuild()
            else:
                self.Refresh()

    def release(self, event):
        # Cables remain attached to the cursor until the next click.
        if self.drag and self.drag[0] == 'cable':
            return
        self.drag = None
        if self.HasCapture():
            self.ReleaseMouse()
        self.rebuild()

    def capture_lost(self, event):
        self.drag = None
        self.Refresh()

    def open_editor(self, module):
        from . import ChainUI
        ChainUI.select(self.frame, module)

    def edit(self, event):
        node = self.hit_node(self.point(event))
        if node:
            self.open_editor(next(m for m in CeciliaLib.session.modules if m.id == node))

    def can_move_source(self, module):
        return module.primary_input is not None and len(CeciliaLib.session.source_ids) > 1

    def can_remove(self, node):
        graph = CeciliaLib.session
        return node not in graph.source_ids or len(graph.source_ids) > 1 or len(graph.modules) == 1

    def change_source(self, module, enabled):
        if self.running:
            return
        try:
            CeciliaLib.session.set_source(module, enabled)
            CeciliaLib.getVar('audioServer').cleanup_module()
            from . import ChainUI
            ChainUI.refresh(self.frame)
        except ValueError as error:
            CeciliaLib.showErrorDialog('Cannot change source', str(error))

    def menu(self, event):
        if self.drag and self.drag[0] == 'cable':
            self.drag = None
            self.Refresh()
            return
        point = self.point(event)
        node = self.hit_node(point)
        if node is None:
            if not self.running and not any(rect.Contains(point) for rect in self.rects.values()):
                position = self.frame.ScreenToClient(self.ClientToScreen(event.GetPosition()))
                self.frame.menubar.showModuleMenu(event, position)
            return
        module = next(m for m in CeciliaLib.session.modules if m.id == node)
        menu = wx.Menu()
        edit = menu.Append(wx.ID_ANY, 'Edit')
        remove = menu.Append(wx.ID_ANY, 'Remove')
        remove.Enable(not self.running and self.can_remove(node))
        is_source = node in CeciliaLib.session.source_ids
        role = menu.Append(wx.ID_ANY, 'Use as processor' if is_source else 'Use as source')
        role.Enable(not self.running and (self.can_move_source(module) if is_source else
                    not any(b == node for a, b in CeciliaLib.session.connections)))
        menu.Bind(wx.EVT_MENU, lambda event: self.change_source(module, not is_source), role)
        menu.Bind(wx.EVT_MENU, lambda event: self.open_editor(module), edit)
        menu.Bind(wx.EVT_MENU, lambda event: CeciliaLib.removeChainModule(module), remove)
        try:
            popup_menu(self, menu)
        finally:
            menu.Destroy()

    def key(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE and self.drag and self.drag[0] == 'cable':
            self.drag = None
            self.Refresh()
            return
        if event.GetKeyCode() in (wx.WXK_DELETE, wx.WXK_BACK) and self.selected_edge and not self.running:
            CeciliaLib.session.disconnect(*self.selected_edge)
            self.selected_edge = None
            CeciliaLib.getVar('audioServer').cleanup_module()
            self.rebuild()
        else:
            event.Skip()
