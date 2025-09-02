import os, sys, json
from pathlib import Path
import guitar.state as s
import guitar.editor as ge
import guitar.utils as u

if __name__ == '__main__':    
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

    name_choices = set()
    for file in os.listdir('gtp'):
        if file.endswith(".gtp"):
            name_choices.add('gtp' / Path(file))

    if len(name_choices) == 0:
        print('no .gtp files found')
        
        new_file_name = input('enter new music file name:')

        s.get().new_file(('gtp' / Path(new_file_name)).with_suffix('.gtp'))
        ge.start_editor()

    else:
        name_choices = list(sorted(name_choices))

        print("choose file:")
        for i, choice in enumerate(name_choices):
            print(i, ":", choice)
            with open(Path(choice), 'r') as f:
                u.print_piece(json.load(f), 20)

        inp = input('>')

        if inp.startswith('new'):
            parts = inp.strip().split(' ')
            s.get().new_file(('gtp' / Path(parts[1])).with_suffix('.gtp'))

        else:
            choice = int(inp)
            if choice < 0 or choice > len(name_choices) - 1: sys.exit(1) 
            chosen = name_choices[choice]
            print('choice:', chosen)
            s.get().load_file(chosen)

        ge.start_editor()