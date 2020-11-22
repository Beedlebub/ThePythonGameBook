#generic menu for pygame

import pygame
import pygame.colordict
import random


class Item:

    def __init__(self, name="dummy", choices=[], cindex=0, rect=None):
        """
        Menu Item. For use inside Menu.items list.
        """
        self.name = name
        self.choices = choices
        self.cindex = cindex
        self.rect = rect


class Menu:

    def __init__(self, name="root", items=[], rect=None):
        """
        Menu , a list of Menu Items.
        Every Submenu (except the 'root' main menu) get's automatically added an Item('back')
        """
        self.name = name
        self.items = items
        self.rect = rect
        self.add_back_item() # autoexec: add 'back' as first item if necessary

    def add_back_item(self):
        if self.name != "root":
            if "back" not in [i.name for i in self.items]:
                self.items.insert(0, Item("back"))

class Viewer:
    """pygame Viewer, handles uses class variables instead of global variables"""
    width: int
    height: int
    screenrect: pygame.Rect
    screen = None
    background = None
    font = None
    menu = None

    def __init__(self, width=800, height=600):
        # ---- pygame init
        pygame.init()
        Viewer.width = width
        Viewer.height = height
        self.setup_screen(width, height)
        # -------- autoexec ------
        self.create_menu()
        self.run()

    def setup_screen(self, width, height, backgroundcolor=(255,255,255)):
        Viewer.screenrect = pygame.Rect(0, 0, width, height)
        Viewer.screen = pygame.display.set_mode(
            (width, height), pygame.DOUBLEBUF
        )
        Viewer.background = pygame.Surface((width, height))
        Viewer.background.fill(backgroundcolor)


    def create_menu(self):
        # ----------- create menu ----------------------
        # ---- audio (submenu of settings)----
        audiomenu = Menu(name="audio", items=[
            Item("sound effects", choices=["on", "off"], cindex=0),
            Item("music", choices=["on", "off"], cindex=0),
        ])
        # ---- video (submenu of settings) ----
        # ----list of possible video resolutions without double entries -> set ----
        reslist = list(set(pygame.display.list_modes(flags=pygame.FULLSCREEN)))
        reslist.sort()  # sort the list from smalles resolution to biggest
        # concert list of tuples( int,int) into list of strings
        # print("reslist", reslist)
        reslist = ["x".join((str(x), str(y))) for (x, y) in reslist]
        # print("reslist", reslist)
        videomenu = Menu(name="video", items=[
            Item("fullscreen", choices=["on", "off"], cindex=0),
            Item("screen resolution", choices=reslist, cindex=4)
        ])
        # --- color (sub-menu of settings)----
        # --- prepare lists for acceptable values -----
        # --- list of some colors (only colornames without numbers in it ----
        #colors = colornames(5)  # max. lenght of colorname is 8
        colors = [str(hex(a))[-2:]+str(hex(b))[-2:]+str(hex(c))[-2:] for a in range(16,256,80) for b in range(16,256,80) for c in range(16,256,80)]
        colormenu = Menu(name="colors", items=[
            Item("color_background", choices=colors, cindex=-2),
            Item("color_small_font1", choices=colors, cindex=3),
            Item("color_small_font2", choices=colors, cindex=7),
            Item("color_big_font", choices=colors, cindex=4),
        ])
        # ------ fontsize (submenu of settings)  ------
        # --- prepare list for acceptable values ---
        fontsizes = range(8, 50, 2)
        # convert into string
        fontsizes = [str(x) for x in fontsizes]
        fontsizemenu = Menu(name="fontsizes", items=[
            Item("fontsize_small", choices=fontsizes, cindex=3),
            Item("fontsize_big", choices=fontsizes, cindex=8),
        ])
        # ---- settings submenu ---
        settingsmenu = Menu(name="settings", items=[
            audiomenu,
            videomenu,
            fontsizemenu,
            colormenu
        ])
        # ---- merge all submenus into root menu ------
        rootmenu = Menu(name="root", items=[Item("play"), Item("credits"), settingsmenu, Item("quit")])
        # ---- create a PygameMenu and store it into the class variable Viewer.menu1 ----
        Viewer.menu1 = PygameMenu(rootmenu)

    def run(self):
        # ---- main loop ----
        running = True
        while running:
            # get a command from the menu. All code must be handled here inside your game loop.
            # the menu save is persistant as
            menuvalues_old = {}
            for k, v in Viewer.menu1.make_choices_dict(Viewer.menu1.rootmenu).items():
                menuvalues_old[k] = v
            print("old:", menuvalues_old)
            command = Viewer.menu1.run()

            menuvalues_new = Viewer.menu1.make_choices_dict(Viewer.menu1.rootmenu)

            print("menu command is:", command)

            print("new:", menuvalues_new)

            # ---- excecute commands ----
            if command == "play":
                ## start game code here
                print("playing a game...")
            # execute a bunch of commands if one of the menusettings points was accepted with ENTER

            elif command == "screen resolution":
                pass
                # change screen resolution
                # if command in res:
                # change the screen resolution
                # x, y = int(command.split("x")[0]), int(command.split("x")[1])
                # pygame.display.set_mode((x, y))
                # self.setup_screen(x, y)
                ## m1.screen = self.screen
                # m1.background = self.background

            elif command == "quit":
                running = False
                # break
            # --------------update all game settings they have been changed  ------------

            for k, v in menuvalues_new.items():
                print("comparing:", k,v, menuvalues_old[k])
                if menuvalues_old[k] != v:
                    print("change in ", k, v)
                    # value has changed. update:
                    if k == "color_background":
                        print("background has changed")
                        # color is hex value change back into decimal
                        Viewer.menu1.background.fill(pygame.Color(int(v[0:2],16), int(v[2:4], 16), int(v[4:6],16)))
                    if k == "color_small_font1":
                        Viewer.menu1.helptextcolor1 = pygame.Color(int(v[0:2],16), int(v[2:4], 16), int(v[4:6],16))
                    if k == "color_small_font2":
                        Viewer.menu1.helptextcolor2 = pygame.Color(int(v[0:2],16), int(v[2:4], 16), int(v[4:6],16))
                    if k == "color_big_font":
                        Viewer.menu1.textcolor = pygame.Color(int(v[0:2],16), int(v[2:4], 16), int(v[4:6],16))
                    if k == "fontsize_small":
                        Viewer.menu1.helptextfontsize = int(v)
                    if k == "fontsize_big":
                        Viewer.menu1.fontsize = int(v)
                    if k == "screen resolution":
                        # resolution is string like '800x600' -> create integer values for x,y:
                        x, y = int(v.split("x")[0]), int(v.split("x")[1])
                        pygame.display.set_mode((x, y))
                        self.setup_screen(x, y)
                        Viewer.menu1.screen = self.screen
                        Viewer.menu1.background = self.background

            # -----
        # -------------------------
        print("end of mainloop")
        pygame.quit()


class PygameMenu:

    def __init__(self,
                 rootmenu,
                 cursortext="-->",
                 startIndex = 0,
                 cycle_up_down=False,
                 menuname="root",
                 cursorTextList = ["→  ", "-→ ", "--→"],
                 cursorAnimTime = 550,
                 cursorSprite=None,
                 menutime=0,
                 textcolor=(0,0,225),
                 background=None,
                 screen=None,
                 fontsize=24,
                 fontname="mono",
                 yspacing=10,
                 helptextheight = 100,
                 helptextcolor1 = (0,0,0),
                 helptextcolor2=(0, 200, 200),
                 helptextfontsize = 15,

                 ) :

        # --- start--------

        self.rootmenu = rootmenu
        self.cursortext = cursortext
        self.cycle_up_down = cycle_up_down
        self.i = startIndex
        self.menu = rootmenu
        self.history = [] # traceback, must be empty list at start
        #---- pygame variables
        self.cursorSprite = cursorSprite
        self.cursorTextList = cursorTextList
        self.cursorAnimTime = cursorAnimTime
        self.menutime = menutime # age of menu in seconds
        if background is None:
            self.background = Viewer.background # pygame surface to blit
        else:
            self.background = background
        if screen is None:
            self.screen = Viewer.screen
        else:
            self.screen = screen
        self.screenrect = self.screen.get_rect()
        self.textcolor = textcolor # black
        self.clock = pygame.time.Clock()
        self.fps = 400
        self.fontsize = fontsize
        self.fontname = fontname
        #self.font = pygame.font.SysFont(name=fontname, size=fontsize, bold=True, italic=False)
        self.yspacing = yspacing # pixel vertically between text lines
        self.helptextheight = helptextheight # pixel distance to top border of window, to display helptext
        self.helptextcolor1 = helptextcolor1
        self.helptextcolor2 = helptextcolor2
        self.helptextfontsize = helptextfontsize
        #self.helptextfont = pygame.font.SysFont(name=fontname, size=helptextfontsize, bold=True)
        # ------
        self.anim = 0

    @property
    def font(self):
        """read only attribute, influened by fontname and fontsize"""
        return pygame.font.SysFont(name=self.fontname, size=self.fontsize, bold=True, italic= False)

    @property
    def smallfont(self):
        """read only attribute, influened by fontname and helptextfontsize"""
        return pygame.font.SysFont(name=self.fontname, size=self.helptextfontsize, bold=True, italic=False)

    def cursor_up(self, menupoints):
        # move cursor up to previous menupoint
        self.i -= 1
        if self.i < 0:
            if self.cycle_up_down:
                self.i = len(menupoints) - 1
            else:
                self.i = 0

    def cursor_down(self, menupoints):
        # move cursor down to next menupoint
        self.i += 1
        if self.i >= len(menupoints):
            if self.cycle_up_down:
                self.i = 0
            else:
                self.i = len(menupoints) - 1

    def cursor_back(self):
        # go back in history  to previous menu

        #if len(self.history) == 0:
        #    return # already
        if len(self.history) == 0:
            self.menu = self.rootmenu
            print("you are already at root menu... going back is not possible from here")
            return
        self.history.pop()  # delete last entry in history list
        # start from root until the desired menu is found
        self.menu = self.rootmenu
        self.i = 0
        if len(self.history) == 0:
            return # already back at root
        #self.cursor_goto_menu(self.history[-1])
        # iterate over all history until the history[-1]
        for name in self.history:
            for item in self.menu.items:
                if item.name == name and type(item) == Menu:
                    self.menu = item
                    break
            else:
                raise ValueError(f"could not find history item {name} in menuitems {self.menu.items}")
        return # should be now in menu with name of last entry in history

    def cursor_goto_menu(self, targetname, menu):
        # recursive serach over ALL menus to go to targetname
        for item in menu.items:
            print("searching", targetname , " checking item:", item, "in menu:", menu.name)
            if type(item) == Menu:
                if item.name == targetname:
                    self.menu = item
                    self.i = 0
                    return True
                if self.cursor_goto_menu(targetname, item):
                    return True
        return False


    def cursor_goto_submenu(self, name):
        """change menu into 'name', witch must be on of the current Menu Items """
        if name not in [item.name for item in self.menu.items if type(item) == Menu]:
            raise ValueError(f"no submenu named {name} in current Menuitems: {self.menu.items}")

        for item in self.menu.items:
            if item.name == name and type(item) == Menu:
                self.menu = item
                self.history.append(name)
                self.i = 0
                return
        raise ValueError("no matching menu found...")


        #print("history is now:", self.history)
        #print("items:", self.menu.items)
        self.menu = self.rootmenu
        #print("menu is now:", self.menu.name, "items:", self.menu.items)

    def next_choice(self):
        activeitem = self.menu.items[self.i]
        if type(activeitem) != Item:
            return # it's not an Item
        if len(activeitem.choices) <= 1:
            return # nothing to change here
        activeitem.cindex += 1
        if activeitem.cindex >= len(activeitem.choices):
            activeitem.cindex = 0

    def previous_choice(self):
        activeitem = self.menu.items[self.i]
        if type(activeitem) != Item:
            return  # it's not an Item
        if len(activeitem.choices) <= 1:
            return  # nothing to change here
        activeitem.cindex -= 1
        if activeitem.cindex < 0:
            activeitem.cindex = len(activeitem.choices) - 1 # go to last item

    def make_choices_dict(self, menu, result={}):
        """recursive crawl over all items and return a dict with all choices and their currently ativce values
        asserts that all Items have unique names"""
        for item in menu.items:
            if type(item) == Item:
                if len(item.choices) > 0:
                    result[item.name] = item.choices[item.cindex]
            else:
                result = self.make_choices_dict(menu=item, result=result)
        return result


    def run(self):
        # calcualte best position for menu (to not recalculate each sub-menu)
        #width, height, entries = self.calculate_all_dimensions()
        #if width > self.screenrect.width:
        #    print("warning: fontsize too big or menuentries too long or screen width too small:" )
        #if height > self.screenrect.height - self.helptextheight:
        #    print("warning: fontsize / helptext too big or too many menuentries or screen height too small" )
        #dy = height / entries

        #    srcolling = True
        # else:
        #    scrolling = False
        # x =  s
        # center menu on screen, calculate topleft position for menu
        #cx = self.screenrect.width // 2 - width // 2
        #cy = self.helptextheight + (self.screenrect.height-self.helptextheight) // 2 - height // 2
        cx = 100 # topleft point for menu (cursor is LEFT of this!)
        cy = 100
        hy = 10 # history y
        hx = 10 # history x
        dy = 25
        choicedistance_x = 500 # from cx to begin of choices
        choicedistance_y = 5 # between each line
        running = True
        #counter = 0
        while running:
            #print("counter:", counter)
            #counter += 1
            # clock
            milliseconds = self.clock.tick(self.fps)  #
            seconds = milliseconds / 1000
            self.menutime += seconds
            # ---------- clear all --------------
            self.screen.blit(self.background, (0, 0))
            # pygame.display.set_icon(self.icon)
            # ----- get current menupoints and selection ------
            #print("menu in loop", self.menu)
            menupoints = [p for p in self.menu.items]
            selection = self.menu.items[self.i] # self.menudict[self.menuname][self.i]

            # ------- cursor animation --------
            # bounce coursor from left to right:
            maxcursordistance = 20
            ## first value is animation time (lower is slower), second value is travel distance of Curosr
            #cursordistance = (self.menutime * 20) % 50
            anim = int((self.menutime * 1.5 ) % len(self.cursorTextList))
            cursortext = self.cursorTextList[anim]
            cursordistance = 0
            # cursor color:
            #r,g,b = self.textcolor
            #r += random.randint(-140,140)
            #g += random.randint(-140,140)
            #b += random.randint(-140,140)
            #r = max(0, min(255,r))
            #g = max(0, min(255,g))
            #b = max(0, min(255,b))
            #cursorcolor = (r,g,b)
            cursorcolor = self.textcolor


            # ----------- writing history on screen ----------
            if len(self.history) == 0:
                historytext = "You are here: root"
            else:
                historytext = "You are here: root>{}".format(">".join(self.history))
            #historytext = "you are here: root{} ".format(">".join(*self.history) if len(self.history)>1 else self.history[0] if )
            hw, hh = write(self.screen, historytext, hx, hy, self.textcolor, self.smallfont, origin="topleft" )
            # ------- write cursor and entry --------
            maxwidth = 0
            for i, entry in enumerate(menupoints):
                if i == self.i:
                    # ----write cursor ---
                    write(self.screen, cursortext, cx - maxcursordistance + cursordistance, cy + dy * i ,
                               cursorcolor, self.font, origin="topright")
                # ----------- write entry ---
                w,h = write(self.screen, entry.name, cx, cy + dy * i, self.textcolor, self.font, origin="topleft")
                entry.rect = pygame.Rect(cx, cy + dy*i, w, h) # update rect information
                #pygame.draw.rect(self.screen, (50,50,50), entry.rect, 1)
                # ----write indicator to the right if entry is a submenu ----
                maxwidth = max(maxwidth, w)
                if type(entry) == Menu:
                    w2, h2 = write(self.screen, " >", cx + w, cy+dy*i, self.textcolor, self.font, origin="topleft")
                    maxwidth = max(maxwidth, w+w2)
                elif type(entry) == Item and len(entry.choices) > 0:
                    # ----- write currently selected choice if entry is an Item --------
                    w2, h2 = write(self.screen, ": "+ entry.choices[entry.cindex], cx+w, cy+dy*i, self.textcolor, self.font, origin="topleft")
                    maxwidth = max(maxwidth, w+w2)
            # --- maxwitdth is now calculated for all items in this menu ---
            # ---- write list of choices for active Item ----
            activeitem = self.menu.items[self.i]
            if type(activeitem) == Item and len(activeitem.choices) > 1:
                w,h = write(self.screen, "cycle through choices with ← →, Accept with ENTER, Cancel with ESC", hx, hy + hh, self.helptextcolor1, self.smallfont, origin="topleft")
                hh += h
                # topleft startpoint for choices:
                ox, oy = cx + max(maxwidth+10, choicedistance_x), hy + hh
                choicerects = []
                for ctext in activeitem.choices:
                    w,h = write(self.screen, ctext, ox, oy, self.textcolor, self.smallfont, origin="topleft" )
                    choicerects.append(pygame.Rect(ox, oy, w, h))
                    oy += choicedistance_y + h

                # ---- paint line from active item to currently active choice -----
                x1 = cx + maxwidth + 5
                x3 = cx + max(maxwidth+10, choicedistance_x) - 5
                x2 = x1 + (x3-x1)//2
                y1 = self.menu.items[self.i].rect.y + self.menu.items[self.i].rect.height //2
                y2 = choicerects[activeitem.cindex].y + choicerects[activeitem.cindex].height //2
                pygame.draw.line(self.screen, self.textcolor, (x1, y1), (x2,y1), 1)
                pygame.draw.line(self.screen, self.textcolor, (x2, y1), (x2, y2), 1)
                pygame.draw.line(self.screen, self.textcolor, (x2, y2), (x3, y2), 1)



            # -------- events ------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                # ------- pressed and released key ------
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                            return "quit"
                    if event.key == pygame.K_UP or event.key == pygame.K_KP8:
                        self.cursor_up(menupoints)
                    if event.key == pygame.K_DOWN or event.key == pygame.K_KP2:
                        self.cursor_down(menupoints)

                    if event.key == pygame.K_BACKSPACE:
                       self.cursor_back()
                    if event.key in (pygame.K_SPACE, pygame.K_RIGHT, pygame.K_PLUS, pygame.K_KP_PLUS):
                        self.next_choice()
                    if event.key in (pygame.K_LEFT, pygame.K_MINUS, pygame.K_KP_MINUS):
                        self.previous_choice()
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        if selection.name == "back":
                            self.cursor_back() # go back to previous menu
                        elif type(selection) == Menu:
                            self.cursor_goto_submenu(selection.name) # jump into submenu
                        else:
                            return selection.name

            # ---------- end of event handler -----
            # --- special sprites ---
            # self.menusprites.update(seconds)
            # self.menusprites.draw(self.screen)
            #-------- update screen -------------
            #pygame.display.set_caption(f"mouse xy: {pygame.mouse.get_pos()}")
            pygame.display.flip()


#def colornames(max_lenght_of_name = 6):
#    """return a list of short colornames without numbers in the name"""
#    colornames = []
#    for colorname in pygame.colordict.THECOLORS:
#        if len(colorname) > max_lenght_of_name:
#            continue
#        # test if any number 0-9 is in the colorname
#        result = [str(x) in colorname for x in range(10)]
#        if any(result):
#            continue
#        colornames.append(colorname)
#    return colornames


def write(
        background,
        text,
        x=50,
        y=150,
        color=(0, 0, 0),
        font= None,
        origin="topleft",
):
    """blit text on a given pygame surface (given as 'background')
    the origin is the alignment of the text surface
    origin can be 'center', 'centercenter', 'topleft', 'topcenter', 'topright', 'centerleft', 'centerright',
    'bottomleft', 'bottomcenter', 'bottomright'
    -> width, height
    """
    #if font_size is None:
    #    font_size = 24
    #font = pygame.font.SysFont(font_name, font_size, bold)
    if font is None:
        font=pygame.font.SysFont("mono", 24, True),
    width, height = font.size(text)
    surface = font.render(text, True, color)

    if origin == "center" or origin == "centercenter":
        background.blit(surface, (x - width // 2, y - height // 2))
    elif origin == "topleft":
        background.blit(surface, (x, y))
    elif origin == "topcenter":
        background.blit(surface, (x - width // 2, y))
    elif origin == "topright":
        background.blit(surface, (x - width, y))
    elif origin == "centerleft":
        background.blit(surface, (x, y - height // 2))
    elif origin == "centerright":
        background.blit(surface, (x - width, y - height // 2))
    elif origin == "bottomleft":
        background.blit(surface, (x, y - height))
    elif origin == "bottomcenter":
        background.blit(surface, (x - width // 2, y))
    elif origin == "bottomright":
        background.blit(surface, (x - width, y - height))
    return width, height



if __name__ == "__main__":
    Viewer(800,640)  # initialize
