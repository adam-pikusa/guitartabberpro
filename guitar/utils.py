import guitar.const as cst

def print_piece(piece: list, column_limit: int) -> None:
    header = ''
    lines = [''] * 6
    offset = 0

    for section in piece:
        header += section['description'] + '  '

        for i, chord in enumerate(section['chords']):
            for note in chord:
                num = str(note[1])
                if len(num) == 1:
                    lines[note[0]] += '-'
                lines[note[0]] += num
                lines[note[0]] += ' '
            
            for l in range(6):
                if len(lines[l]) - offset <= i * 3:
                    lines[l] += '-- '

        for l in range(6):
            lines[l] += '  '

        section_header_len = len(header) - offset
        section_lines_len = len(lines[0]) - offset

        if section_header_len < section_lines_len:
            d = section_lines_len - section_header_len
            header += ' ' * d
            offset += section_lines_len
        elif section_lines_len < section_header_len:
            d = section_header_len - section_lines_len
            for l in range(6):
                lines[l] += ' ' * d
            offset += section_header_len
        else:
            offset += section_header_len

        if offset > column_limit:
            print(header)
            for line in lines:
                print(line)
            header = ''
            lines = [''] * 6
            offset = 0

    if header != '':
        print(header)
        for line in lines:
            print(line)


def detect_chord(notes: list) -> str | None:
    for chord_name, chord_notes in cst.CHORD_NOTES.items():
        mod_notes = [cst.STRINGS[note[0]][note[1]] % 12 for note in notes]
        if len(set(mod_notes)) > 2 and all((mod_note in chord_notes) for mod_note in mod_notes):
            return chord_name
        
    return None
                