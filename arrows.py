from enum import IntEnum
import base64

class Direction(IntEnum):
    North = 0
    East  = 1
    South = 2
    West  = 3

class ArrowType(IntEnum):
    Empty                  = 0
    Arrow                  = 1
    Source                 = 2
    Blocker                = 3
    Delay                  = 4
    Detector               = 5
    SplitterUpDown         = 6
    SplitterUpRight        = 7
    SplitterUpRightLeft    = 8
    Pulse                  = 9
    BlueArrow              = 10
    Diagonal               = 11
    BlueSplitterUpUp       = 12
    BlueSplitterRightUp    = 13
    BlueSplitterUpDiagonal = 14
    Not                    = 15
    And                    = 16
    Xor                    = 17
    Latch                  = 18
    Flipflop               = 19
    Random                 = 20
    Button                 = 21
    LevelSource            = 22
    LevelTarget            = 23
    DirectoinalButton      = 24
    Unknown                = 25


class Arrow:
    def __init__(self, type: ArrowType = ArrowType.Empty, direction: Direction = Direction.North, flipped = False):
        self.type = type
        self.direction = direction
        self.flipped = flipped

    direction: Direction = Direction.North
    flipped: bool = False
    type: ArrowType = ArrowType.Empty

class Chunk:
    arrows: list[Arrow]
    def __init__(self):
        self.arrows = ([Arrow()] * 256).copy()

    def get(self, x: int, y: int) -> Arrow:
        return self.arrows[y*16+x]
    def set(self, x: int, y: int, arrow: Arrow):
        self.arrows[y*16+x] = arrow

class Map:
    version: int = 0
    chunks: dict[tuple[int, int], Chunk]

    def __init__(self, string: None|str = None):
        self.chunks = {}
        if string is not None:
            self.import_(string)

    def get(self, x: int, y: int) -> Arrow:
        chunk_x = x//16
        chunk_y = y//16
        arrow_x = x % 16
        arrow_y = y % 16
        if (chunk_x, chunk_y) not in self.chunks:
            self.chunks[(chunk_x, chunk_y)] = Chunk()
        return self.chunks[(chunk_x, chunk_y)].get(arrow_x, arrow_y)

    def set(self, x: int, y: int, arrow: Arrow):
        chunk_x = x//16
        chunk_y = y//16
        arrow_x = x % 16
        arrow_y = y % 16
        if (chunk_x, chunk_y) not in self.chunks:
            self.chunks[(chunk_x, chunk_y)] = Chunk()

        self.chunks[(chunk_x, chunk_y)].set(arrow_x, arrow_y, arrow)

    def import_(self, string: str):
        raw_data = base64.b64decode(string)
        def pop8() -> int:
            nonlocal raw_data
            val = raw_data[:1]
            raw_data = raw_data[1:]
            return int.from_bytes(val, byteorder='little')
        def pop16() -> int:
            nonlocal raw_data
            val = raw_data[:2]
            raw_data = raw_data[2:]
            return int.from_bytes(val, byteorder='little', signed=True)

        self.version = pop16()
        chunks_count = pop16()
        for _ in range(chunks_count):
            chunk_x = pop16()
            chunk_y = pop16()
            arrow_types = pop8()+1
            for _ in range(arrow_types):
                type = pop8()
                type_count = pop8()+1
                for _ in range(type_count):
                    position = pop8()
                    x = position & 0x0F
                    y = (position & 0xF0) >> 4
                    direction_and_flipped = pop8()
                    direction = direction_and_flipped & 0b011
                    flipped = direction_and_flipped & 0b100 != 0
                    arrow = Arrow()
                    arrow.flipped = flipped
                    arrow.type = ArrowType(type)
                    arrow.direction = Direction(direction)
                    self.set(chunk_x*16 + x, chunk_y*16 + y, arrow)

    def export(self) -> str:
        raw_data = bytearray([])
        def push8(val: int):
            nonlocal raw_data
            raw_data.extend(val.to_bytes(byteorder='little', length=1))
        def push16(val: int):
            nonlocal raw_data
            raw_data.extend(val.to_bytes(byteorder='little', length=2, signed=True))


        push16(self.version)
        push16(len(self.chunks))
        for cords, chunk in self.chunks.items():
            types: list[ArrowType] = []
            for arrow in chunk.arrows:
                if arrow.type != ArrowType.Empty and arrow.type not in types:
                    types.append(arrow.type)
            if types == []: continue
            push16(cords[0])
            push16(cords[1])
            push8(len(types)-1)
            for type in types:
                push8(type)
                push8(0)
                types_count_index = len(raw_data)-1
                types_count = 0
                for x in range(16):
                    for y in range(16):
                        arrow = chunk.get(x, y)
                        if arrow.type != type: continue
                        position = x | (y<<4)
                        rotation = arrow.direction | (arrow.flipped << 2)
                        push8(position)
                        push8(rotation)
                        types_count += 1
                raw_data[types_count_index] = types_count-1
        return base64.b64encode(raw_data).decode('utf-8')
