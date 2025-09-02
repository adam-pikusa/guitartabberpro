import pygame as pg
import guitar.const as cst
import guitar.models as models
import guitar.state as state
import guitar.utils as utils

BLACK = [0,0,0]
RED = [240,0,0]
GREEN = [0,255,0]
BLUE = [0,0,255]
WHITE = [255,255,255]
LIGHTGREY = [240,240,240]
LIGHTBLUE = [200,200,255]
GREY = [100,100,100]
MAGENTA = [255,0,255]

w, h = 1366, 400
cw, ch = 20, 20
cox, coy = 3, 3
TAB_LEN = 60

def create_tab_cells() -> dict:
    tab = {}
    for string in range(6):
        for chord_index in range(TAB_LEN):
            tab[string, chord_index] = models.TabCell(
                cw, ch, cox, coy,
                string, chord_index)
    return tab

def create_piano_keys() -> list:
    piano_keys = []
    kb_x = 30
    kb_y = 6*ch+6*coy + 20
    k_w, k_h = 25, 80
    k_o = 3
    for octave in range(4):
        g_x = kb_x + octave * (7 * (k_w + k_o) + 6)

        for i, key in enumerate((0, 2, 4, 5, 7, 9, 11)):
            piano_keys.append(models.PianoKey(
                g_x + i * (k_w + k_o), kb_y, 
                k_w, k_h, 
                (octave - 2) * 12 + key, False))
                
        for i, key in enumerate((1, 3)):
            piano_keys.append(models.PianoKey(
                g_x + k_w * 0.7 + i * (k_w + k_o) * 1.1, kb_y,
                k_w * 0.75, k_h * 0.5,
                (octave - 2) * 12 + key, True))  

        for i, key in enumerate((6, 8, 10)):
            piano_keys.append(models.PianoKey(
                g_x + 3 * (k_w + k_o) + k_w * 0.7 + i * (k_w + k_o) * 1.05, kb_y,
                k_w * 0.75, k_h * 0.5,
                (octave - 2) * 12 + key, True))
            
    return piano_keys

def update_caption(current_section: int) -> None:
    pg.display.set_caption(f"guitar tabber pro - {state.get().file_path} - {state.get().piece[current_section]['description']}")

def start_editor() -> None:    
    pg.init()

    font = pg.font.SysFont("Arial", 15)
    screen = pg.display.set_mode((w,h))
    clock = pg.time.Clock()

    current_section = 0
    cursor = 0
    lmb, rmb = False, False
    clear = False
    mousepos = []
    tab = create_tab_cells()
    piano_keys = create_piano_keys()

    def kp_click(num: int):
        nonlocal cursor
        nonlocal tab
        for pk in piano_keys:
            if not pk.hover: continue
            if 0 >= num > 6: break
            num -= 1

            target = tab[num, cursor]
            res = get_tab_cell_state(target)
            if res != None:
                target.set_fret(current_section, res)
                cursor += 1 
                return

        for c in tab.values():
            if c.button.check_hover(mousepos):
                if c.get_fret(current_section) == 1:
                    c.set_fret(current_section, num + 10)
                else:
                    c.set_fret(current_section, num)
                return

    def update_cur():
        nonlocal cursor
        for c in tab.values():
            if c.button.check_hover(mousepos):
                cursor = c.chord_index
                return

    def clear_cell():
        nonlocal mousepos
        for c in tab.values():
            if c.button.check_hover(mousepos):
                c.clear_fret(current_section)
                return

    def mark_cell():
        nonlocal mousepos
        for c in tab.values():
            if c.button.check_hover(mousepos):
                c.marked = True
                return

    def get_piano_key_state(pk: models.PianoKey) -> int:
        nonlocal cursor
        nonlocal tab

        for string in range(6):
            c = tab[string, cursor]
            fret = c.get_fret(current_section)
            if fret == None: continue
            if fret >= len(cst.STRINGS[0]): continue
            tab_key = cst.STRINGS[string][fret]
            
            if tab_key == pk.note:
                return 1 # ACTIVE

        for c in tab.values():
            fret = c.get_fret(current_section)
            if not c.marked or fret == None or fret >= len(cst.STRINGS[0]): continue
            # all cells marked and valid
            tab_key = cst.STRINGS[c.string][fret]
            
            if tab_key == pk.note:
                return 2 # MARKED

        return 0 # NONE

    def get_tab_cell_state(cell: models.TabCell) -> int | None:
        if cell.chord_index != cursor: return None
        # cells under cursor

        choices = []

        for pk in piano_keys:
            if not pk.hover: continue
            # single hovered key
            
            for string, frets in enumerate(cst.STRINGS):
                for fret, note in enumerate(frets):
                    if note == pk.note:
                        choices.append((string, fret))
                        break

        for c in choices:
            if c[0] == cell.string:
                return c[1]
        
        return None
    
    def move_note(up: bool) -> None:
        nonlocal mousepos
        for c in tab.values():
            fret = c.get_fret(current_section)
            if not (c.button.check_hover(mousepos) and fret != None): continue
            if up:
                if c.string < 1: return
                move = -4 if c.string == 2 else -5
                temp = fret + move
                if temp < 0: return
                tab[c.string - 1, c.chord_index].set_fret(current_section, temp)
                c.clear_fret(current_section)

            else:
                if c.string > 4: return
                move = 4 if c.string == 1 else 5
                temp = fret + move
                tab[c.string + 1, c.chord_index].set_fret(current_section, temp)
                c.clear_fret(current_section)

    def transpose(by: int):
        for c in tab.values():
            fret = c.get_fret(current_section)
            if fret != None:
                c.set_fret(current_section, fret + by)

    update_caption(current_section)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: pg.quit()

            elif event.type == pg.MOUSEMOTION:
                mousepos = event.pos

                for pk in piano_keys:
                    pk.hover = pk.button.check_hover(mousepos) if pk.sharp else pk.button.check_hover_lower(mousepos)
    
                if lmb: update_cur()
                elif rmb: mark_cell()
                elif clear: clear_cell()

            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mousepos = event.pos
                    lmb = True
                    update_cur()

                elif event.button == 2:
                    for c in tab.values():
                        c.marked = False
                elif event.button == 3: 
                    rmb = True

            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1: lmb = False
                elif event.button == 3: rmb = False

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()

                elif event.key == pg.K_c: clear = True
                elif event.key == pg.K_e: state.get().save_file()
                elif event.key == pg.K_r: state.get().reload_file()
                elif event.key == pg.K_t: transpose(int(input('transpose by>')))
                elif event.key == pg.K_i: state.get().insert_empty_chord(current_section, cursor)

                elif event.key == pg.K_LEFT and cursor > 0: cursor -= 1
                elif event.key == pg.K_RIGHT: cursor += 1 
                elif event.key == pg.K_UP and current_section < len(state.get().piece) - 1:
                    current_section += 1
                    update_caption(current_section)
                elif event.key == pg.K_DOWN and current_section > 0:
                    current_section -= 1
                    update_caption(current_section)

                elif event.key == pg.K_g: move_note(True)
                elif event.key == pg.K_b: move_note(False)


                elif event.key == pg.K_KP0: kp_click(0)
                elif event.key == pg.K_KP1: kp_click(1)
                elif event.key == pg.K_KP2: kp_click(2)
                elif event.key == pg.K_KP3: kp_click(3)
                elif event.key == pg.K_KP4: kp_click(4)
                elif event.key == pg.K_KP5: kp_click(5)
                elif event.key == pg.K_KP6: kp_click(6)
                elif event.key == pg.K_KP7: kp_click(7)
                elif event.key == pg.K_KP8: kp_click(8)
                elif event.key == pg.K_KP9: kp_click(9)

            elif event.type == pg.KEYUP:
                if event.key == pg.K_c: clear = False

        screen.fill(GREY)

        for c in tab.values():
            fret = c.get_fret(current_section)
            res = get_tab_cell_state(c)
            pg.draw.rect(screen, LIGHTBLUE if c.marked else WHITE, c.button.rect)
            if fret != None or res != None:
                screen.blit(
                    font.render(
                        ' {}'.format(fret if res == None else res), 
                        True, 
                        BLACK if res == None else MAGENTA), 
                    c.button.rect)

        cursor_x = cursor * (cw + cox) + cw * 0.5
        pg.draw.line(screen, GREY, (cursor_x, 0), (cursor_x, 6*ch+6*coy))

        for pk in piano_keys:
            res = get_piano_key_state(pk)
            pg.draw.rect(screen, 
                RED if res == 1 
                else BLUE if res == 2 
                else MAGENTA if pk.hover 
                else BLACK if pk.sharp 
                else LIGHTGREY, pk.button.rect)

        pg.display.update()
        clock.tick(33)