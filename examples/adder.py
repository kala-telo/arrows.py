# Credits: @howthefuuu on Discord

import arrows

m = arrows.Map()


def _1b_adder(x, y, toggle_buttons: bool = True, output: bool = True):
    m.get(x, y).type = arrows.ArrowType.BlueSplitterUpUp
    m.get(x+1, y).type = arrows.ArrowType.And
    m.get(x+2, y).type = arrows.ArrowType.Xor
    m.get(x+1, y+1).type = arrows.ArrowType.BlueSplitterUpDiagonal
    m.get(x+2, y+1).type = arrows.ArrowType.BlueSplitterUpDiagonal

    m.get(x, y).direction = arrows.Direction.West
    m.get(x+1, y).direction = arrows.Direction.West
    m.get(x+2, y+1).flipped = True

    if toggle_buttons:
        m.get(x+1, y+2).type = arrows.ArrowType.Flipflop
        m.get(x+2, y+2).type = arrows.ArrowType.Flipflop
        m.get(x+1, y+3).type = arrows.ArrowType.Button
        m.get(x+2, y+3).type = arrows.ArrowType.Button

    if output:
        m.get(x+2, y-1).type = arrows.ArrowType.BlueArrow


def adder(bits: int = 8,
          toggle_buttons: bool = True,
          output: bool = True):

    for i in range(bits):
        _1b_adder(i*3, 0, toggle_buttons, output)


adder()
print(m.export())
