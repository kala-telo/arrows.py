# Credits: @howthefuuu on Discord
#          @kala-telo on GitHub

import arrows

m = arrows.Map()
m.version = 5  # Key arrows always carry data in arrows.py -> v0 cannot store them (v4+ required)


def _1b_adder(x, y, toggle_buttons: bool = True, output: bool = True):
    m.get(x, y).type = arrows.ArrowType.Blue_I_Splitter
    m.get(x+1, y).type = arrows.ArrowType.And_gate
    m.get(x+2, y).type = arrows.ArrowType.XOR_gate
    m.get(x+1, y+1).type = arrows.ArrowType.Diagonal_Splitter
    m.get(x+2, y+1).type = arrows.ArrowType.Diagonal_Splitter

    m.get(x, y).direction = arrows.Direction.West
    m.get(x+1, y).direction = arrows.Direction.West
    m.get(x+2, y+1).flipped = True

    if toggle_buttons:
        m.get(x+1, y+2).type = arrows.ArrowType.T_flip_flop
        m.get(x+2, y+2).type = arrows.ArrowType.T_flip_flop
        m.get(x+1, y+3).type = arrows.ArrowType.Key
        m.get(x+2, y+3).type = arrows.ArrowType.Key

    if output:
        m.get(x+2, y-1).type = arrows.ArrowType.Blue_arrow


def adder(bits: int = 8,
          toggle_buttons: bool = True,
          output: bool = True):

    for i in range(bits):
        _1b_adder(i*3, 0, toggle_buttons, output)


adder()
print(m.export())
