# a musical piece is made up of sections
# a section is an array of chords, with some additional metadata
# a chord is a collection of notes
# a guitar note is a string index (0 based) and fret (0 based)

import json
from pathlib import Path

def create_empty_piece() -> list:
    return [
        {
            'description': 'section 1',
            'chords': [[[0,0]], [[1,0]], [[2,0]], [[3,0]], [[4,0]], [[5,0]]]
        },
        {
            'description': 'section 2',
            'chords': [[[5,0]], [[4,0]], [[3,0]], [[2,0]], [[1,0]], [[0,0]]]
        }
    ]

class State:
    def __init__(self) -> None:
        self.piece: list = create_empty_piece()
        self.file_path: Path | None = None

    def insert_empty_chord(self, current_section: int, chord_index: int) -> None:
        self.piece[current_section]['chords'].insert(chord_index, [])

    def get_chord(self, current_section: int, chord_index: int) -> list | None:
        chords = self.piece[current_section]['chords']
        if len(chords) <= chord_index:
            return None
        return chords[chord_index]

    def new_file(self, file_path: Path) -> None:
        self.file_path = file_path
        self.piece = create_empty_piece()

    def load_file(self, file_path: Path) -> None:
        self.file_path = file_path

        with open(self.file_path, 'r') as f:
            self.piece = json.load(f)

    def save_file(self) -> None:
        if self.file_path is None: return
        with open(self.file_path, 'w') as f:
            json.dump(self.piece, f)

    def reload_file(self) -> None:
        if self.file_path is None: return
        with open(self.file_path, 'r') as f:
            self.piece = json.load(f)

_state: State | None = None

def get() -> State:
    global _state

    if _state is None:
        _state = State()

    return _state