import pygame as pg
import guitar.const as cst
import guitar.serialization as ser

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

def start_editor(chosen: str) -> None:    
    pg.init()

    font = pg.font.SysFont("Arial", 15)
    screen = pg.display.set_mode((w,h))
    clock = pg.time.Clock()

    desc = None
    m_part_num = 0
    cursor = 0
    lmb, rmb = False, False
    clear = False
    mousepos = []
    tab = {}
    for string in range(6):
        for note_pos in range(TAB_LEN):
            tab[string, note_pos] = ser.TabCell(
                cw, ch, cox, coy,
                string, note_pos)

    piano_keys = []
    if True:
        kb_x = 30
        kb_y = 6*ch+6*coy + 20
        k_w, k_h = 25, 80
        k_o = 3
        for octave in range(4):
            g_x = kb_x + octave * (7 * (k_w + k_o) + 6)
            for key in range(7):
                piano_keys.append(ser.PianoKey(
                    g_x + key * (k_w + k_o), kb_y, 
                    k_w, k_h, octave, key, False))
                    
            for key in range(2):
                piano_keys.append(ser.PianoKey(
                    g_x
                    + k_w * 0.7
                    + key * (k_w + k_o) * 1.1, kb_y,
                    k_w * 0.75, k_h * 0.5,
                    octave, key + 7, True))  

            for key in range(3):
                piano_keys.append(ser.PianoKey(
                    g_x 
                    + 3 * (k_w + k_o)
                    + k_w * 0.7
                    + key * (k_w + k_o) * 1.05, kb_y,
                    k_w * 0.75, k_h * 0.5,
                    octave, key + 7 + 2, True))

    def load(data: dict):
        notes = data['notes']
        if notes == None: return

        nonlocal tab
        for c in tab.values():
            c.val = None
        for n in notes:
            tab[n[0],n[1]].val = n[2]

        window_title = f"guitar tabber pro - {chosen}"

        nonlocal desc
        D = 'description'
        if D in data: 
            desc = data[D]
            window_title += f' - {desc}'

        pg.display.set_caption(window_title)

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
                target.val = res
                cursor += 1 
                return

        for c in tab.values():
            if c.button.check_hover(mousepos):
                if c.val == 1:
                    c.val = num + 10
                else:
                    c.val = num
                return

    def update_cur():
        nonlocal cursor
        for c in tab.values():
            if c.button.check_hover(mousepos):
                cursor = c.note
                return

    def clear_cell():
        nonlocal mousepos
        for c in tab.values():
            if c.button.check_hover(mousepos):
                c.val = None
                return

    def mark_cell():
        nonlocal mousepos
        for c in tab.values():
            if c.button.check_hover(mousepos):
                c.marked = True
                return

    def get_piano_key_state(octave: int, note: int) -> int:
        nonlocal cursor
        nonlocal tab

        for string in range(6):
            c = tab[string, cursor]
            if c.val == None: continue
            if c.val >= len(cst.STRINGS[0]): continue
            tab_key = cst.STRINGS[string][c.val]
            
            if tab_key[0] == octave and tab_key[1] == note:
                return 1 # ACTIVE

        for c in tab.values():
            if not c.marked or c.val == None or c.val >= len(cst.STRINGS[0]): continue
            # all cells marked and valid
            tab_key = cst.STRINGS[c.string][c.val]
            
            if tab_key[0] == octave and tab_key[1] == note:
                return 2 # MARKED

        return 0 # NONE

    def get_tab_cell_state(cell: ser.TabCell) -> int:
        if cell.note != cursor: return None
        # cells under cursor

        choices = []

        for pk in piano_keys:
            if not pk.hover: continue
            # single hovered key
            
            for s, string in enumerate(cst.STRINGS):
                for n, note in enumerate(string):
                    if note[0] == pk.octave and note[1] == pk.note:
                        choices.append((s, n))
                        break

        for c in choices:
            if c[0] == cell.string:
                return c[1]
        
        return None
    
    def move_note(up: bool) -> None:
        nonlocal mousepos
        for c in tab.values():
            if not (c.button.check_hover(mousepos) and c.val != None): continue
            if up:
                if c.string < 1: return
                move = -4 if c.string == 2 else -5
                temp = c.val + move
                if temp < 0: return
                tab[c.string - 1, c.note].val = temp
                c.val = None

            else:
                if c.string > 4: return
                move = 4 if c.string == 1 else 5
                temp = c.val + move
                tab[c.string + 1, c.note].val = temp
                c.val = None

    def transpose(by: int):
        for c in tab.values():
            if c.val != None:
                c.val += by

    def insert_empty(position: int):
        nonlocal tab

        for string in range(6):
            pos = TAB_LEN - 1

            while pos > position:
                tab[string, pos].val = tab[string, pos - 1].val

                pos -= 1 

    load(ser.import_from_file(chosen, 0))

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
                elif event.key == pg.K_e: ser.export_to_file(chosen, { 
                    'section_num': m_part_num, 
                    'cells': tab.values(),
                    'description': desc })
                elif event.key == pg.K_r: load(ser.import_from_file(chosen, m_part_num))
                elif event.key == pg.K_t: transpose(int(input('transpose by>')))
                elif event.key == pg.K_i: insert_empty(cursor)

                elif event.key == pg.K_LEFT and cursor > 0: cursor -= 1
                elif event.key == pg.K_RIGHT: cursor += 1 
                elif event.key == pg.K_UP:
                    m_part_num += 1
                    load(ser.import_from_file(chosen, m_part_num))
                elif event.key == pg.K_DOWN and m_part_num > 0:
                    m_part_num -= 1
                    load(ser.import_from_file(chosen, m_part_num))

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
            res = get_tab_cell_state(c)
            pg.draw.rect(screen, LIGHTBLUE if c.marked else WHITE, c.button.rect)
            if c.val != None or res != None:
                screen.blit(
                    font.render(
                        ' {}'.format(c.val if res == None else res), 
                        True, 
                        BLACK if res == None else MAGENTA), 
                    c.button.rect)

        cursor_x = cursor * (cw + cox) + cw * 0.5
        pg.draw.line(screen, GREY, (cursor_x, 0), (cursor_x, 6*ch+6*coy))

        for pk in piano_keys:
            res = get_piano_key_state(pk.octave, pk.note)
            pg.draw.rect(screen, 
                RED if res == 1 
                else BLUE if res == 2 
                else MAGENTA if pk.hover 
                else BLACK if pk.sharp 
                else LIGHTGREY, pk.button.rect)

        pg.display.update()
        clock.tick(33)