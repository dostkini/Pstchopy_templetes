from psychopy import visual, core, event
import numpy as np

class BaseStim:
    def __init__(self, win, pos=(0, 0), size=1.0, color='white', opacity=1.0, name=None, auto_draw=False):
        self.win = win
        self.pos = pos
        self.size = size
        self.color = color
        self.opacity = opacity
        self.name = name or self.__class__.__name__
        self.visible = False
        self.auto_draw = auto_draw

        self.stim = None

    def show(self):
        if self.stim is not None:
            self.stim.setAutoDraw(True)
        self.visible = True
        self.auto_draw = True

    def hide(self):
        if self.stim is not None:
            self.stim.setAutoDraw(False)
        self.visible = False
        self.auto_draw = False

    def set_pos(self, pos):
        self.pos = pos
        if self.stim is not None:
            self.stim.pos = pos

    def set_size(self, size):
        self.size = size
        self._update_size()

    def set_opacity(self, opacity):
        self.opacity = opacity
        if self.stim is not None:
            self.stim.opacity = opacity

    def set_color(self, color):
        self.color = color
        if self.stim is not None:
            self.stim.color = color

    def _update_size(self):
        pass


class ShapeStim(BaseStim):
    def __init__(self, win, shape='circle', radius=0.2, edges=32, **kwargs):
        super().__init__(win, **kwargs)
        self.base_radius = radius
        self.edges = 64 if shape == 'circle' else edges

        self.stim = visual.ShapeStim(
            win,
            vertices='circle' if shape == 'circle' else shape,
            size=self.base_radius * 2 * self.size,
            fillColor=self.color,
            lineColor=self.color,
            opacity=self.opacity,
            pos=self.pos,
            edges=self.edges
        )
        if self.auto_draw:
            self.show()

    def _update_size(self):
        if self.stim:
            self.stim.size = self.base_radius * 2 * self.size


class TextStim(BaseStim):
    def __init__(self, win, text="Text", height=0.1, **kwargs):
        super().__init__(win, **kwargs)
        self.base_height = height
        self.text = text

        self.stim = visual.TextStim(
            win, text=text, pos=self.pos, height=self.base_height * self.size,
            color=self.color, opacity=self.opacity, wrapWidth=2
        )
        if self.auto_draw:
            self.show()

    def set_text(self, text):
        self.text = text
        self.stim.text = text

    def _update_size(self):
        if self.stim:
            self.stim.height = self.base_height * self.size


class FixationCross(BaseStim):
    def __init__(self, win, line_length=0.5, line_width=4, **kwargs):
        super().__init__(win, **kwargs)
        self.line_length = line_length
        self.line_width = line_width

        self.horiz = visual.Rect(win,
            width=line_length * self.size, height=line_width,
            fillColor=self.color, lineColor=self.color, pos=self.pos)
        self.vert = visual.Rect(win,
            width=line_width, height=line_length * self.size,
            fillColor=self.color, lineColor=self.color, pos=self.pos)

        # Объединяем в один стимул для удобства
        self.stim = visual.BufferImageStim(win, stim=[self.horiz, self.vert])

        if self.auto_draw:
            self.show()

    def _update_size(self):
        self.horiz.width = self.line_length * self.size
        self.vert.height = self.line_length * self.size

    # Переопределяем show/hide, потому что у нас два отдельных стимула
    def show(self):
        self.horiz.setAutoDraw(True)
        self.vert.setAutoDraw(True)
        self.visible = True

    def hide(self):
        self.horiz.setAutoDraw(False)
        self.vert.setAutoDraw(False)
        self.visible = False


class AnimatedStim:
    def __init__(self, stim, clock=None):
        self.stim = stim
        self.clock = clock or core.Clock()

    def drift(self, speed=0.1, direction=0, duration=None):
        if not hasattr(self.stim.stim, 'phase'):
            return
        start = self.clock.getTime()
        while self.stim.visible and (duration is None or self.clock.getTime() - start < duration):
            phase = (self.clock.getTime() - start) * speed + direction
            self.stim.stim.phase = phase % 1.0
            yield

    def pulse(self, freq=2, min_size=0.8, max_size=1.5, duration=None):
        start = self.clock.getTime()
        while self.stim.visible and (duration is None or self.clock.getTime() - start < duration):
            phase = np.sin(self.clock.getTime() * freq * 2 * np.pi)
            size = min_size + (max_size - min_size) * (phase + 1) / 2
            self.stim.set_size(size)
            yield

    def fade_in(self, duration=0.5):
        start = self.clock.getTime()
        while self.clock.getTime() - start < duration:
            prog = (self.clock.getTime() - start) / duration
            self.stim.set_opacity(prog)
            yield

    def fade_out(self, duration=0.5):
        start = self.clock.getTime()
        while self.clock.getTime() - start < duration:
            prog = 1 - (self.clock.getTime() - start) / duration
            self.stim.set_opacity(prog)
            yield
