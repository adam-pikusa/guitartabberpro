import json
import os
import guitar.fileio as fio

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
    def __init__(self, cw: int, ch: int, cox: int, coy: int, string: int, index: int) -> None:
        self.button = Button(
            (cw + cox) * index,
            (ch + coy) * string,
            cw, ch)

        self.string = string
        self.index = index
        
        self.val = None
        self.marked = False

class PianoKey:
    def __init__(self, x, y, w, h, octave: int, index: int, sharp: bool) -> None:
        self.button = Button(x, y, w, h)

        self.sharp = sharp

        self.octave = octave
        self.index = index

        self.hover = False

def import_from_file(name: str, m_part_num: int) -> list:
    result = { 'notes': []}
    path = fio.get_path(name, m_part_num)
    if not os.path.exists(path):
        print(path, 'does not exist')
        return None

    with open(path, 'r') as f:
        for l in f:
            if l.startswith('!'):
                parts = l.split(' ')

                if parts[1] == 'DESC':
                    result['description'] = parts[2]
                    continue

                continue

            parts = l.strip().split(';')
            result['notes'].append((
                int(parts[0]), 
                int(parts[1]), 
                int(parts[2])))
    
    return result

def export_to_file(name: str, data: dict):
    section_num = data['section_num']
    cells = data['cells']

    path = fio.get_path(name, section_num)
    
    D = 'description'

    notes = []

    for c in cells:
        if c.val != None:
            notes.append([
                c.string, 
                c.index, 
                c.val
            ])

    section = {
        'name': str(section_num),
        'notes': notes
    }
    payload = {}

    if D in data:
        payload[D] = data[D]

    payload['sections'] = [section]
    
    with open(fr'gtp_files/{name}.gtp', 'w') as f:
        json.dump(payload, f)