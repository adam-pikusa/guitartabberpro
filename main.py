import os, sys
import guitar.editor as ge
import guitar.fileio as fio

if __name__ == '__main__':    
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

    chosen = None

    if len(sys.argv) == 2:
        chosen = sys.argv[1]

    else:
        name_choices = set()
        for file in os.listdir(fio.MUSIC_DIR):
            if file.endswith(".m"):
                res = fio.get_file(file)
                if res[0]:
                    name_choices.add(res[1])

        if len(name_choices) == 0:
            print('no .m files found')
            sys.exit()

        name_choices = list(sorted(name_choices))

        print("choose file:")
        for i, choice in enumerate(name_choices):
            print(i, ":", choice)

        inp = input('>')

        if inp.startswith('new'):
            parts = inp.strip().split(' ')
            chosen = parts[1]
            with open(chosen, 'w') as f: pass

        else:
            choice = int(inp)
            if choice < 0 or choice > len(name_choices) - 1: sys.exit() 
            chosen = name_choices[choice]
            print('choice:', chosen)

    ge.start_editor(chosen)