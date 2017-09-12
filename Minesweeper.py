####################################
##
##Jerry Aska
##
##Grid Click
##
####################################
import pygame, pygame.gfxdraw, sys, random, math
from pygame.locals import *

pygame.init()

# colours        R    G    B

WHITE          = (255, 255, 255)
GREY           = (125, 125, 125)
BLACK          = (  0,   0,   0)
RED            = (255,   0,   0)
ORANGE         = (255, 125,   0)
YELLOW         = (255, 255,   0)
GREEN          = (  0, 255,   0)
BLUE           = (  0,   0, 255)
PURPLE         = (255,   0, 255)

list_of_colors         = [RED, ORANGE, YELLOW, GREEN, PURPLE, BLACK, WHITE]
list_of_colors_names   = ["RED", "ORANGE", "YELLOW", "GREEN", "PURPLE", "BLACK", "WHITE"]
scr_height             = 600
scr_width              = 600
DISPLAYSURF            = pygame.display.set_mode((scr_width, scr_height),pygame.RESIZABLE)


FPS = 60
fpsClock = pygame.time.Clock()

SCREEN_COLOR     = GREEN
SCREEN_COLUMNS   = 10
SCREEN_ROWS      = 10
SCREEN_RATIO     = SCREEN_COLUMNS/SCREEN_ROWS
GRID_FACTOR      = SCREEN_ROWS


TEXT_COLOR                 = WHITE

FONT_STYLE                 = "calibri"
FONT_SIZE_PERCENT          = 1/(SCREEN_ROWS/100)

bomb_concentration = 10

 
###########################################################################################################################
##                                                  Classes Definition
###########################################################################################################################

class nothing:
    """
    Place Holder Object

    This object is simply to be used as a default for relational operators for when there is no object to relate to.
    It contains all the attributes necessary for relational operators in this program set to 0 indicating to other objects
    that there is nothing there.
    """
    def __init__(self, pos_x = 0, pos_y = 0, height = 0, width = 0, space_above = 0, space_to_the_left = 0, columns = 0, rows = 0, grid_size = 0, is_nothing = True):
        self.pos_x              = pos_x
        self.pos_y              = pos_y
        self.height             = height
        self.width              = width
        self.space_above        = space_above
        self.space_to_the_left  = space_to_the_left
        self.columns            = columns
        self.rows               = rows
        self.grid_size          = grid_size
        self.is_nothing         = is_nothing

###########################################################################################################################

class screen:
    """
    Screen Object

    This object contains attributes to allow for a miniature screen within the display surface. This object can be given a
    specific ratio and will maintain this ratio even when the display surface is resized. It can also be given items to
    share the display surface with and can be resized to allow space for those objects while still maintaining the ratio.
    """
    def __init__(self, width = scr_width, height = scr_height, item_above = nothing(), item_to_the_left = nothing(), space_to_the_left = 0, space_above = 0, color = SCREEN_COLOR, ratio = SCREEN_RATIO, grid_factor = GRID_FACTOR, screen_columns = SCREEN_COLUMNS, screen_rows = SCREEN_ROWS):
        self.pos_x              = item_to_the_left.pos_x + item_to_the_left.width + item_to_the_left.space_to_the_left
        self.pos_y              = item_above.pos_y + item_above.height + item_above.space_above
        self.space_to_the_left  = space_to_the_left
        self.space_above        = space_above
        self.width              = width - item_to_the_left.width
        self.height             = height - item_above.height
        self.item_to_the_left   = item_to_the_left
        self.item_above         = item_above
        self.color              = color
        self.ratio              = ratio
        self.is_nothing         = False
        self.grid_size          = self.height / grid_factor
        self.grid_factor        = grid_factor
        self.columns            = screen_columns
        self.rows               = screen_rows


    def display(self):
        DISPLAYSURF.fill(self.color, ((self.pos_x + self.space_to_the_left, self.pos_y + self.space_above), (self.width, self.height)))


    def resize(self, new_width, new_height, item_above = nothing(), item_to_the_left = nothing()):
        if not item_to_the_left.is_nothing:
            self.item_to_the_left = item_to_the_left
        if not item_above.is_nothing:
            self.item_above = item_above
        new_width = new_width - (self.item_to_the_left.pos_x + self.item_to_the_left.width)
        new_height = new_height - (self.item_above.pos_y + self.item_above.height)
        ratio = new_width / new_height
        if ratio == self.ratio:
            self.width = new_width
            self.height = new_height
            self.space_above = 0
            self.space_to_the_left = 0
        if ratio > self.ratio:
            self.width = int(new_height * self.ratio)
            self.height = new_height
            self.space_to_the_left = (new_width - self.width) // 2
            self.space_above = 0
        if ratio < self.ratio:
            self.width = new_width
            self.height = int(new_width / self.ratio)
            self.space_to_the_left = 0
            self.space_above = (new_height - self.height) // 2
        self.grid_size          = self.height / self.grid_factor

###########################################################################################################################

class sector:
    """
    
    """
    def __init__(self, sector_pos, screen, color = WHITE, Type = "None", text_color = TEXT_COLOR, font_style = FONT_STYLE, font_size_percent = FONT_SIZE_PERCENT):
        self.sector_pos  = sector_pos
        self.pos_x       = (sector_pos % screen.columns) * screen.grid_size + screen.space_to_the_left + screen.pos_x
        self.pos_y       = (sector_pos // screen.columns) * screen.grid_size + screen.space_above + screen.pos_y
        self.width       = screen.width // screen.columns
        self.height      = screen.height // screen.rows
        self.mid_x       = self.pos_x + self.width // 2
        self.mid_y       = self.pos_y + self.height // 2
        self.radius      = min(self.width,self.height) // 2
        self.state       = False
        self.color       = color
        self.points      = 0
        self.screen      = screen
        self.type        = Type
        self.is_nothing  = False
        self.highlight   = False
        self.displayed   = False
        self.setable     = True
        self.bomb_count  = 0
        self.text_color  = text_color
        self.style       = font_style
        self.size        = font_size_percent / 100
        self.font        = pygame.font.SysFont(self.style, int(screen.height * self.size))
        self.adjacents   = []

    
    def hide(self):
        self.highlight  = False
        if not self.state:
            self.displayed  = False
            
            
    def reset(self, color = WHITE, Type = "None"): 
        self.state       = False
        self.type        = Type
        self.color       = color
        self.highlight   = False
        self.displayed   = False
        self.setable     = True
        self.bomb_count  = 0

        
    def resize(self, screen = nothing()):  
        if not screen.is_nothing:
            self.screen = screen
        self.pos_x   = (self.sector_pos % self.screen.columns) * self.screen.grid_size + self.screen.space_to_the_left + self.screen.pos_x
        self.pos_y   = (self.sector_pos // self.screen.columns) * self.screen.grid_size + self.screen.space_above + self.screen.pos_y
        self.width   = self.screen.width // self.screen.columns
        self.height  = self.screen.height // self.screen.rows
        self.mid_x   = self.pos_x + self.width // 2
        self.mid_y   = self.pos_y + self.height // 2
        self.radius  = min(self.width, self.height) // 2
        self.font   = pygame.font.SysFont(self.style, int(self.screen.height * self.size))

        
    def set_state(self, sector_list):
        if self.type == "Bomb":
            game_over("Lose:(")
        elif self.setable and not self.state:
            self.state      = True
            self.displayed  = True
            if self.bomb_count == 0:
                for x in list(self.adjacents):
                    sector_list.list[x].set_state(sector_list)

            
    def is_clicked(self, mouse_pos_x, mouse_pos_y):
        if mouse_pos_x > self.pos_x and mouse_pos_x < self.pos_x + self.width:
            if mouse_pos_y > self.pos_y and mouse_pos_y < self.pos_y + self.height:
                return True
        return False


    def is_highlighted(self, mouse_pos_x, mouse_pos_y):
        if not self.state:
            if mouse_pos_x > self.pos_x and mouse_pos_x < self.pos_x + self.width:
                if mouse_pos_y > self.pos_y and mouse_pos_y < self.pos_y + self.height:
                    self.highlight = True
                else:
                    self.highlight = False
            else:
                self.highlight = False


    def recolor(self, new_color):
        self.color = new_color

    
    def count(self, sector_list):
        if not self.type == "Bomb":
            check1 = self.sector_pos - self.screen.rows
            check2 = self.sector_pos
            check3 = self.sector_pos + self.screen.rows
            check = [check1 - 1, check1, check1 + 1, check2 - 1, check2 + 1, check3 - 1, check3, check3 + 1]
            a = [check1 - 1, check2 - 1, check3 - 1]
            b = [check1 + 1, check2 + 1, check3 + 1]
            c = [check1 - 1, check1, check1 + 1]
            d = [check3 - 1, check3, check3 + 1]
            if self.sector_pos % self.screen.rows == 0:
                for x in a:
                    if x in check:
                        check.remove(x)
            if (self.sector_pos + 1) % self.screen.rows == 0:
                for x in b:
                    if x in check:
                        check.remove(x)
            if (self.sector_pos) // self.screen.rows == 0:
                for x in c:
                    if x in check:
                        check.remove(x)
            if (self.sector_pos) // self.screen.rows == self.screen.columns - 1:
                for x in d:
                    if x in check:
                        check.remove(x)
            self.adjacents = check
            for x in check:
                if sector_list.list[x].type == "Bomb":
                    self.bomb_count += 1
                
        
    def do_function(self, sector_list, player):
        pass


    def display(self):
        if self.highlight or self.displayed:
            if not self.type == "Bomb":
                TEXT = pygame.font.Font.render(self.font, str(self.bomb_count), True, self.text_color)
                DISPLAYSURF.blit(TEXT, (self.pos_x + int(3/12*self.width), self.pos_y))
            else:                
                pygame.draw.rect(DISPLAYSURF, self.color, (self.pos_x, self.pos_y, self.width, self.height))
        elif not self.setable:
            pygame.draw.rect(DISPLAYSURF, PURPLE, (self.pos_x, self.pos_y, self.width, self.height))

###########################################################################################################################

class object_list:
    """
    
    """
    def __init__(self):
        self.list       = []
        self.is_nothing = False

        
    def append(self, item):
        self.list.append(item)


    def are_active(self):
        active = True
        for x in range(len(self.list)):
            if self.list[x].state or self.list[x].type == "Bomb":
                continue
            else:
                active = False
                break
        return active

        
    def resize(self, item_to_follow = nothing()):
        for y in range(len(self.list)):
            self.list[y].resize(item_to_follow)

            
    def reset(self, color = WHITE):
        for x in range(len(self.list)):
            self.list[x].reset(color = color)

    def hide(self):
        for x in range(len(self.list)):
            self.list[x].hide()

    def recolor(self, color = WHITE):
        for x in range(len(self.list)):
            if not self.list[x].state:
                if str(color) == "Random":
                    self.list[x].reset(color = list_of_colors[random.randrange(0,len(list_of_colors))])
                else:
                    self.list[x].reset(color = color)


    def check_if_highlighted(self, mouse_pos_x, mouse_pos_y):
        for x in range(len(self.list)):
            self.list[x].is_highlighted(mouse_pos_x, mouse_pos_y)

    def count(self):
        for x in range(len(self.list)):
            self.list[x].count(self)

    
    def check_if_clicked(self, mouse_pos_x, mouse_pos_y, button):
        for x in range(len(self.list)):
            if self.list[x].is_clicked(mouse_pos_x, mouse_pos_y):
                if button == 1:
                    self.list[x].set_state(self)
                if button == 3:
                    if not self.list[x].state:
                        self.list[x].setable = not self.list[x].setable
                if button == 4:
                    if self.list[x].state:
                        for y in list(self.list[x].adjacents):
                            self.list[y].set_state(self)
                        

    
    def display(self):
        for y in range (len(self.list)):
            self.list[y].display()
            
    def make_displayed(self):
        for y in range(len(self.list)):
            self.list[y].displayed = True

###########################################################################################################################
 
def draw_grid(game_screen):
    for x in range(round(game_screen.width/game_screen.grid_size) + 1):
        pygame.draw.line(DISPLAYSURF,WHITE,(x * game_screen.grid_size + game_screen.space_to_the_left + game_screen.pos_x, game_screen.space_above + game_screen.pos_y),(x * game_screen.grid_size + game_screen.space_to_the_left + game_screen.pos_x, game_screen.space_above + game_screen.height + game_screen.pos_y))
    for y in range(round(game_screen.height/game_screen.grid_size) + 1):
        pygame.draw.line(DISPLAYSURF,WHITE,(game_screen.space_to_the_left + game_screen.pos_x, y * game_screen.grid_size + game_screen.space_above + game_screen.pos_y), (game_screen.space_to_the_left + game_screen.width + game_screen.pos_x, y * game_screen.grid_size + game_screen.space_above + game_screen.pos_y))

###########################################################################################################################

def game_over(text):
    sectors.make_displayed()
    game_screen.display()
    sectors.display()
    draw_grid(game_screen)
    pygame.display.update()
    bombs.clear()

    
    font   = pygame.font.SysFont(FONT_STYLE, int(game_screen.height / 5))
        
    TEXT = pygame.font.Font.render(font, "You " + str(text), True, TEXT_COLOR)
    pygame.time.delay(1000)
    DISPLAYSURF.fill(game_screen.color)
    DISPLAYSURF.blit(TEXT, (game_screen.pos_x + game_screen.width // 12, game_screen.pos_y + game_screen.height // 3))
    pygame.display.update()
    for x in range(int((game_screen.rows * game_screen.columns)/100 * bomb_concentration)):
        while True:
            z = random.randrange(0, game_screen.rows * game_screen.columns)
            if not z in bombs:
                bombs.append(z)
                break
    l = True
    
    s_time = pygame.time.get_ticks()
    
    while l:
        c_time = pygame.time.get_ticks()
        if c_time - s_time > 2000:
            break
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_c:
                    key_i = pygame.key.get_pressed()
                    if key_i[K_LCTRL] or key_i[K_RCTRL]:
                        pygame.quit()
                        sys.exit()
            if event.type == MOUSEBUTTONDOWN or event.type == KEYDOWN:
                l = False
                
    for y in range(game_screen.rows * game_screen.columns):
        if not y in bombs:
            sectors.list[y].reset(GREEN, "Safe")
        else:
            sectors.list[y].reset(RED, "Bomb")

    sectors.count()

    pygame.event.clear()
    game_screen.display()
    sectors.display()
    draw_grid(game_screen)
    pygame.display.update()
    
                              
game_screen = screen(color = BLACK)
bombs = []
for x in range(int((game_screen.rows * game_screen.columns)/100 * bomb_concentration)):
    while True:
        z = random.randrange(0, game_screen.rows * game_screen.columns)
        if not z in bombs:
            bombs.append(z)
            break

sectors     = object_list()
for y in range(game_screen.rows * game_screen.columns):
    if not y in bombs:
        sectors.append(sector(y, game_screen, color = GREEN, Type = "Safe"))
    else:
        sectors.append(sector(y, game_screen, color = RED, Type = "Bomb"))

sectors.count()                   

###########################################################################################################################
##                                                  Main Game Loop
###########################################################################################################################
s_time = pygame.time.get_ticks()
while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_c:
                key_i = pygame.key.get_pressed()
                if key_i[K_LCTRL] or key_i[K_RCTRL]:
                    pygame.quit()
                    sys.exit()
            if event.key == K_m:
                pass            
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1 or event.button == 3:# or event.button == 4:
                mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
                sectors.check_if_clicked(mouse_pos_x, mouse_pos_y, event.button)
##            if event.button == 4:
##                sectors.make_displayed()
##            if event.button == 5:
##                sectors.hide()
        if event.type == VIDEORESIZE:
            DISPLAYSURF = pygame.display.set_mode((event.w, event.h),pygame.RESIZABLE)            
            game_screen.resize(event.w, event.h)
            sectors.resize()
            pass
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    if sectors.are_active():
        game_over("Win!!!")
        pygame.event.clear()
    DISPLAYSURF.fill(GREY)
    game_screen.display()
    sectors.display()
    draw_grid(game_screen)
    pygame.display.update()
    fpsClock.tick(FPS)
