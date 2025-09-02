import guitar.state as s

class Button:
    def __init__(self, x: int, y: int, w: int, h: int) -> None:
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.rect = (x, y, w, h)

    def check_hover(self, pos):
        return (
            self.x < pos[0] and
            self.x + self.w > pos[0] and
            self.y < pos[1] and
            self.y + self.h > pos[1])

    def check_hover_lower(self, pos):
        return (
            self.x < pos[0] and
            self.x + self.w > pos[0] and
            self.y + self.h * 0.5 < pos[1] and
            self.y + self.h > pos[1])

class TabCell:
    def __init__(self, cw: int, ch: int, cox: int, coy: int, string: int, chord_index: int) -> None:
        self.button = Button(
            (cw + cox) * chord_index,
            (ch + coy) * string,
            cw, ch)

        self.string = string
        self.chord_index = chord_index
        
        self.marked = False

    def get_fret(self, current_section: int) -> int | None:
        chords = s.get().piece[current_section]['chords']

        if len(chords) <= self.chord_index:
            return None
        
        for note in chords[self.chord_index]:
            if note[0] == self.string:
                return note[1]

        return None
    
    def set_fret(self, current_section: int, to: int) -> None:
        chords = s.get().piece[current_section]['chords']

        while len(chords) <= self.chord_index:
            chords.append([])

        chord = chords[self.chord_index]

        i = 0
        while i < len(chord):
            if chord[i][0] == self.string:
                chord.pop(i)
            else:
                i += 1
            
        chords[self.chord_index].append([self.string, to])

    def clear_fret(self, current_section: int) -> None:
        chords = s.get().piece[current_section]['chords']

        if len(chords) <= self.chord_index:
            return
        
        chord = chords[self.chord_index]

        i = 0
        while i < len(chord):
            if chord[i][0] == self.string:
                chord.pop(i)
            else:
                i += 1

class PianoKey:
    def __init__(self, x, y, w, h, note: int, sharp: bool) -> None:
        self.button = Button(x, y, w, h)

        self.sharp = sharp

        self.note = note

        self.hover = False


