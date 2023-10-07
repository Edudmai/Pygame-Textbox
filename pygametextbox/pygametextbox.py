"""pygametextbox Module Description
A module to implement an editable text entry box for the pygame module.
Requires use of the pygame module.
pygame.MOUSEBUTTONUP and pygame.KEYDOWN events must be enabled.
"""

# if __name__ == "__main__":
#     print("The pygametextbox module is not designed to be run on its own.")
#     exit()


# Imports
from __future__ import annotations
import pygame as pg
import typing
from pyperclip import copy, paste


# Initialization
if not pg.font.get_init(): pg.font.init()


# Finals
ACCEPTED_CHARS = ("abcdefghijklmnopqrstuvwxyz" +
                  "ABCDEFGHIJKLMNOPQRSTUVWXYZ" +
                  "0123456789 _-~")
DEFAULT_FONT = pg.font.Font()
GRAY = pg.Color('gray')#127, 127, 127)
LIGHT_BLUE = pg.Color('light blue')#191, 191, 255)
LIGHT_GRAY = pg.Color('light gray')#191, 191, 191)
SOFT_BLACK = pg.Color('gray1')#15, 15, 15)
SOFT_WHITE = pg.Color('gray15')#239, 239, 239)


# Classes
class TextBox:
    """pygametextbox.TextBox Class Description"""
    
    def __init__(self, rect:pg.Rect, placeholder:str="…", font=DEFAULT_FONT,
                 colors:list[pg.Color|tuple[int,int,int]]=None):
        """pygametextbox.TextBox.__init__ Description"""

        # Internal property defaults
        self._action = None
        self._antialias = True
        self._cursor_position = 0
        self._is_selected = False
        self._margin = 2
        self._text = ""

        # Internal property values from arguments
        self._font = font
        self._placeholder = placeholder

        # Colors
        self._bg_color = SOFT_WHITE
        self._inactive_color = LIGHT_GRAY
        self._placeholder_color = GRAY
        self._text_color = SOFT_BLACK

        self.rect = rect
        self._placeholder_render = font.render(self._placeholder, self._antialias, self._placeholder_color)
        self._is_dirty = True
        self._letter_surfaces: list[pg.Surface] = []
        self._prev_text = ""
        self._surface = pg.Surface(rect.size)




    # Attributes/Properties
    @property
    def antialias(self) -> bool:
        """pygametextbox.TextBox.antialias Attribute Description"""
        return self._antialias

    @antialias.setter
    def antialias(self, value:bool):
        self._is_dirty = True
        self._antialias = value
    


    @property
    def bg_color(self) -> pg.Color:
        """pygametextbox.TextBox.bg_color Attribute Description"""
        return pg.Color(self._bg_color)

    @bg_color.setter
    def bg_color(self, value:pg.Color|tuple[int,int,int]|str):
        self._is_dirty = True
        self._bg_color = pg.Color(value)
    


    @property
    def cursor_position(self) -> int:
        """pygametextbox.TextBox.cursor_position Attribute Description"""
        return self._cursor_position

    @cursor_position.setter
    def cursor_position(self, value:int):
        self._is_dirty = True
        self._cursor_position = value
    


    @property
    def font(self) -> pg.font.Font:
        """pygametextbox.TextBox.font Attribute Description"""
        return self._font #BUG - mutable object - no mudbath

    @font.setter
    def font(self, value:pg.font.Font):
        self._is_dirty = True
        self._font = value #BUG - mutable object - no mudbath
    


    @property
    def inactive_color(self) -> pg.Color:
        """pygametextbox.TextBox.inactive_color Attribute Description"""
        return pg.Color(self._inactive_color)
    
    @inactive_color.setter
    def inactive_color(self, value:pg.Color|tuple[int,int,int]|str):
        self._is_dirty = True
        self._inactive_color = pg.Color(value)
    


    @property
    def is_selected(self) -> bool:
        """pygametextbox.TextBox.is_selected Attribute Description"""
        return self._is_selected

    @is_selected.setter
    def is_selected(self, value:bool):
        self._is_dirty = True
        self._is_selected = value
    


    @property
    def margin(self) -> int:
        """pygametextbox.TextBox.margin Attribute Description"""
        return self._margin

    @margin.setter
    def margin(self, value:int):
        self._is_dirty = True
        self._margin = value
    


    @property
    def placeholder(self) -> str:
        """pygametextbox.TextBox.placeholder Attribute Description"""
        return self._placeholder

    @placeholder.setter
    def placeholder(self, value:str|None):
        self._is_dirty = True
        self._placeholder = value
    


    @property
    def placeholder_color(self) -> pg.Color:
        """pygametextbox.TextBox.placeholder_color Attribute Description"""
        return pg.Color(self._placeholder_color)

    @placeholder_color.setter
    def placeholder_color(self, value:pg.Color|tuple[int,int,int]|str):
        self._is_dirty = True
        self._placeholder_color = pg.Color(value)
    


    @property
    def text(self) -> str:
        """pygametextbox.TextBox.text Attribute Description"""
        return self._text
    
    @text.setter
    def text(self, value:str):
        self._is_dirty = True
        self._text = value



    @property
    def text_color(self) -> pg.Color:
        """pygametextbox.TextBox.text_color Attribute Description"""
        return pg.Color(self._text_color)
    
    @text_color.setter
    def text_color(self, value:pg.Color|tuple[int,int,int]|str):
        self._is_dirty = True
        self._text_color = pg.Color(value)
    



    # Special getters/setters
    def get_surface(self) -> pg.Surface:
        """pygametextbox.TextBox.get_surface Method Description"""
        if self._is_dirty: self.rerender()
        return self._surface
    


    def set_action(self, action:typing.Callable[[TextBox],None]):
        """pygametextbox.TextBox.set_action Method Description"""
        self._action = action
    



    # Methods
    def rerender(self):
        """pygametextbox.TextBox.rerender Method Description"""

        # Rerender letters if needed
        if self._text != self._prev_text: self._letter_surfaces = renderLetters(self._font, self._text, self._antialias, self._text_color)
        self._prev_text = self._text
        
        bg_color = self._bg_color if self._is_selected else self._inactive_color
        self._surface.fill(bg_color)

        # Blit letters to surface
        x = 0
        for letter in self._letter_surfaces:
            self._surface.blit(letter, (self._margin+x, self._margin))
            x += letter.get_width()
            if x >= self._surface.get_width(): break
        
        if self._placeholder and not self._text: self._surface.blit(self._placeholder_render, (self._margin, self._margin))

        # Draw cursor
        if self._is_selected: #TODO - Make readable
            pg.draw.rect(self._surface, self._text_color, (self._margin+sum(letter.get_width() for letter in self._letter_surfaces[:self._cursor_position]), self._margin, 2, self._font.get_height()))
    


    def update(self, events: list[pg.event.Event]):
        """pygametextbox.TextBox.update Method Description"""

        # Event Handling
        for event in events:
            match event.type:
              # Keyboard Handling
              case pg.KEYDOWN:
                if self.is_selected:
                    # Command key (Mac)
                    if event.mod == 1024 or event.mod == 2048:
                        # Copy
                        if event.key == pg.K_c: copy(self.text)

                        # Paste
                        elif event.key == pg.K_v:
                            self.text = paste()
                            self.cursor_position = len(self.text)
                        
                        # Cut
                        elif event.key == pg.K_x:
                            copy(self._text)
                            self.text = ""
                            self.cursor_position = 0

                    # Typing key
                    elif event.unicode and event.unicode in ACCEPTED_CHARS:
                        self.text = self._text[:self._cursor_position] + event.unicode + self._text[self._cursor_position:]
                        self.cursor_position+=1
                    
                    # Delete/backspace key
                    elif event.key == pg.K_DELETE or event.key == pg.K_BACKSPACE:
                        if self._text[:self._cursor_position]:
                            self.cursor_position-=1
                            self.text = self._text[:self._cursor_position] + self._text[self._cursor_position+1:]
                    
                    # Left/right arrow keys
                    elif event.key == pg.K_LEFT:
                        if self._cursor_position > 0: self.cursor_position-=1

                    elif event.key == pg.K_RIGHT:
                        if self._cursor_position < len(self._text): self.cursor_position+=1
                    
                    # Enter/return key
                    elif event.key == pg.K_RETURN and self._action: self._action(self.text)

              # Mouse handling
              case pg.MOUSEBUTTONUP:
                if event.button == 1:
                    #prev_is_selected = self.is_selected TODO
                    # Check for click on TextBox
                    if self._rect.collidepoint(event.pos): self.is_selected = True
                    else: self.is_selected = False
                    #if prev_is_selected != self.is_selected: self._is_dirty = True

                    # Set cursor position
                    if self._is_selected:
                        cursor_position = 0
                        x = event.pos[0] - self.rect.left - self.margin
                        prev_possible_cursor_position = 0
                        for possible_cursor_position in [sum(letter_surface.get_width() for letter_surface in self._letter_surfaces[:i])
                                                         for i in range(1, len(self._letter_surfaces)+1)]:
                            if abs(x-possible_cursor_position) > abs(x-prev_possible_cursor_position): break
                            prev_possible_cursor_position = possible_cursor_position
                            cursor_position+=1
                        if self.cursor_position != cursor_position: self._is_dirty = True
                        self.cursor_position = cursor_position


# Functions
def renderLetters(font:pg.font.Font,
               text:str|bytes|None, antialias:bool,
               color:pg.Color|tuple[int,int,int], background:pg.Color|tuple[int,int,int]|None=None) -> list[pg.Surface]:
    letters: list[pg.Surface] = []
    for letter in text: letters.append(font.render(letter, antialias, color, background))
    return letters


# Example
if __name__ == "__main__":

    # Finals - Settings for the project
    BG_COLOR = pg.Color('tan')
    FONT = pg.font.SysFont('Comic Sans MS', 24)
    FPS = 30
    HEIGHT = FONT.get_linesize()-FONT.get_descent()
    WIN = pg.display.set_mode((300, HEIGHT+20))

    # Variables
    textbox = TextBox(pg.Rect(10, 10, 280, HEIGHT), font=FONT)
    clock = pg.time.Clock()
    running = True

    # Set up
    pg.display.set_caption("pygametextbox Demo")
    pg.event.set_blocked(None)
    pg.event.set_allowed( (pg.QUIT, pg.KEYDOWN, pg.KEYUP, pg.MOUSEBUTTONUP) )
    pg.key.set_repeat(300, 100)

    # Game loop
    while running:

        # Event handling
        events = pg.event.get()
        for event in events:
            match event.type:
              case pg.QUIT: running = False

        textbox.update(events) # Pass events to the textbox.update method every frame
        
        # Draw to the window
        WIN.fill(BG_COLOR)
        WIN.blit(textbox.surface, textbox.rect)
        pg.display.flip()
    
        clock.tick(FPS)

    pg.quit()
    exit()