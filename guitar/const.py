# middle C == 0
# half steps == +1
# ... C = 0, C# = 1, D = 2

STRINGS = [
    [  4 + i for i in range(24)],
    [ -1 + i for i in range(24)],
    [ -5 + i for i in range(24)],
    [-10 + i for i in range(24)],
    [-15 + i for i in range(24)],
    [-20 + i for i in range(24)],
]

CHORD_NOTES = {
    'A' : [ 9,  1,  4],
    'a' : [ 9,  0,  4],
    'A#': [10,  2,  5],
    'a#': [10,  1,  5],
    'B' : [11,  3,  6],
    'C' : [ 0,  4,  7], 
    'D' : [ 2,  6,  9], 
    'E' : [ 4,  8, 11], 
    'F' : [ 5,  9,  0],
    'G' : [ 7, 11,  2], 
}