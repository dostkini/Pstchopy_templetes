# Pstchopy_templetes
It is template for my hackathon which will be soon. But u also can use my classe for youe projects to make you exiting expirements easier
# Как пользоваться stimuls.py на хакатоне

## 1. Базовые принципы
- Все стимулы наследуются от `BaseStim`
- Управление через методы: `.show()`, `.hide()`, `.set_pos()`, `.set_color()`, `.set_size()`, `.set_opacity()`
- По умолчанию `auto_draw=False` → нужно явно вызвать `.show()`

## Эксперимент 1 — Два круга, меняющие цвет по клавишам

```python
from psychopy import visual, event, core
from stimuls import ShapeStim

win = visual.Window([800, 600], color='black', units='height')

left_circle  = ShapeStim(win, pos=(-0.3, 0), radius=0.15, color='white')
right_circle = ShapeStim(win, pos=( 0.3, 0), radius=0.15, color='white')

left_circle.show()
right_circle.show()

while True:
    keys = event.getKeys()
    if 'escape' in keys:
        break
    if 'left' in keys:
        left_circle.set_color('blue')
    if 'right' in keys:
        right_circle.set_color('red')
    if 'r' in keys:  # сброс
        left_circle.set_color('white')
        right_circle.set_color('white')

    win.flip()
win.close()
core.quit()
