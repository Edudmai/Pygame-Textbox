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
import pygame
import typing
from pyperclip import copy, paste


# Initialization
if not pygame.font.get_init(): pygame.font.init()


# Classes
class TextBox:
    """pygametextbox.TextBox Class Description"""
    
    def __init__(self, rect:pygame.Rect, placeholder:str="Enter Text Here...", font=pygame.font.Font(),
                 colors:list[pygame.Color|tuple[int,int,int]]=None):
        """pygametextbox.TextBox.__init__ Description"""

        # Internal property defaults
        self._action: typing.Callable[[TextBox], None] = None
        self._antialias: bool = True
        self._cursor_position: int = 0
        self._is_selected: bool = False
        self._margin: int = 2
        self._text: str = ""

        # Internal property values from arguments
        self._font: pygame.font.Font = font
        self._placeholder: str = placeholder
        self._rect: pygame.Rect = rect

        # Colors
        self._bg_color: pygame.Color = pygame.Color('gray97')
        self._inactive_color: pygame.Color = pygame.Color('gray90')
        self._placeholder_color: pygame.Color = pygame.Color('gray50')
        self._text_color: pygame.Color = pygame.Color('gray3')

        self._letter_surfaces: list[pygame.Surface] = []
        self._prev_text = ""
        self._surface = pygame.Surface(rect.size)

        # Initialization
        self._rerender_placeholder()
        self.rerender()









    # Attributes/Properties

    @property
    def antialias(self) -> bool:
        """pygametextbox.TextBox.antialias Attribute Description"""
        return self._antialias

    @antialias.setter
    def antialias(self, value:bool):
        self._antialias = value
        self._is_dirty = True
        self._rerender_placeholder()
    




    @property
    def bg_color(self) -> pygame.Color:
        """pygametextbox.TextBox.bg_color Attribute Description"""
        return self._bg_color

    @bg_color.setter
    def bg_color(self, value:pygame.Color|tuple[int,int,int]|str):
        if not isinstance(value, pygame.Color): value = pygame.Color(value)
        self._bg_color = value
        self._is_dirty = True
    




    @property
    def cursor_position(self) -> int:
        """pygametextbox.TextBox.cursor_position Attribute Description"""
        return self._cursor_position

    @cursor_position.setter
    def cursor_position(self, value:int):
        self._cursor_position = value
        self._is_dirty = True
    




    @property
    def font(self) -> pygame.font.Font:
        """pygametextbox.TextBox.font Attribute Description"""
        return self._font

    @font.setter
    def font(self, value:pygame.font.Font):
        self._font = value
        self._is_dirty = True
    




    @property
    def inactive_color(self) -> pygame.Color:
        """pygametextbox.TextBox.inactive_color Attribute Description"""
        return self._inactive_color
    
    @inactive_color.setter
    def inactive_color(self, value:pygame.Color|tuple[int,int,int]|str):
        if not isinstance(value, pygame.Color): value = pygame.Color(value)
        self._inactive_color = value
        self._is_dirty = True
    




    @property
    def is_selected(self) -> bool:
        """pygametextbox.TextBox.is_selected Attribute Description"""
        return self._is_selected

    @is_selected.setter
    def is_selected(self, value:bool):
        self._is_selected = value
        self._is_dirty = True
    




    @property
    def margin(self) -> int:
        """pygametextbox.TextBox.margin Attribute Description"""
        return self._margin

    @margin.setter
    def margin(self, value:int):
        self._margin = value
        self._is_dirty = True
    




    @property
    def placeholder(self) -> str:
        """pygametextbox.TextBox.placeholder Attribute Description"""
        return self._placeholder

    @placeholder.setter
    def placeholder(self, value:str|None):
        self._placeholder = value
        self._is_dirty = True
        self._rerender_placeholder()
    




    @property
    def placeholder_color(self) -> pygame.Color:
        """pygametextbox.TextBox.placeholder_color Attribute Description"""
        return self._placeholder_color

    @placeholder_color.setter
    def placeholder_color(self, value:pygame.Color|tuple[int,int,int]|str):
        if not isinstance(value, pygame.Color): value = pygame.Color(value)
        self._placeholder_color = value
        self._is_dirty = True
        self._rerender_placeholder()
    




    @property
    def rect(self) -> pygame.Rect:
        """pygametextbox.TextBox.rect Attribute Description"""
        return self._rect
    
    @rect.setter
    def rect(self, value:pygame.Rect|tuple[int,int,int,int]):
        if not isinstance(value, pygame.Rect): value = pygame.Rect(value)
        self._rect = value
        self._is_dirty = True
    




    @property
    def text(self) -> str:
        """pygametextbox.TextBox.text Attribute Description"""
        return self._text
    
    @text.setter
    def text(self, value:str):
        self._text = value
        self._is_dirty = True





    @property
    def text_color(self) -> pygame.Color:
        """pygametextbox.TextBox.text_color Attribute Description"""
        return self._text_color
    
    @text_color.setter
    def text_color(self, value:pygame.Color|tuple[int,int,int]|str):
        if not isinstance(value, pygame.Color): value = pygame.Color(value)
        self._text_color = value
        self._is_dirty = True
    








    # Special getters/setters

    def get_surface(self) -> pygame.Surface:
        """pygametextbox.TextBox.get_surface Method Description"""
        if self._is_dirty: self.rerender()
        return self._surface # Possible BUG if Surface is too mutable
    




    def set_action(self, action:typing.Callable[[TextBox],None]):
        """pygametextbox.TextBox.set_action Method Description"""
        self._action = action
    








    # Methods

    def _rerender_placeholder(self):

        self._placeholder_render = self._font.render(self._placeholder, self._antialias, self._placeholder_color)
        self._is_dirty = True
    




    def drawTo(self, window:pygame.Surface):
        """pygametextbox.TextBox.draw Method Description"""

        window.blit(self.get_surface(), self._rect)
    




    def rerender(self):
        """pygametextbox.TextBox.rerender Method Description"""

        # Rerender letters if needed FIXME - Skip unnecesary rerenders
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
            pygame.draw.rect(self._surface, self._text_color, (self._margin+sum(letter.get_width() for letter in self._letter_surfaces[:self._cursor_position]), self._margin, 2, self._font.get_height()))
    




    def update(self, events: list[pygame.event.Event]):
        """pygametextbox.TextBox.update Method Description"""

        # Event Handling
        for event in events:
            match event.type:
              # Keyboard Handling
              case pygame.KEYDOWN:
                if self.is_selected: self._keydown_handler(event.key, event.mod, event.unicode)
              # Mouse handling
              case pygame.MOUSEBUTTONUP:
                if event.button == 1: self._mousebuttonup_handler(event.pos)



    def _keydown_handler(self, key, mod, unicode):
        
        # Command key (Mac)
        if mod == 1024 or mod == 2048: self._control_handler(key)
        
        # Left/right arrow keys
        elif key == pygame.K_LEFT:
            if self._cursor_position > 0: self.cursor_position-=1

        elif key == pygame.K_RIGHT:
            if self._cursor_position < len(self._text): self.cursor_position+=1
        
        # Enter/return key
        elif key == pygame.K_RETURN:
            if self._action: self._action(self.text)

        # Delete/backspace key
        elif key == pygame.K_DELETE or key == pygame.K_BACKSPACE:
            if self._text[:self._cursor_position]:
                self.cursor_position-=1
                self.text = self._text[:self._cursor_position] + self._text[self._cursor_position+1:]
        
        # Typing key
        elif unicode and key != pygame.K_TAB:
            self.text = self._text[:self._cursor_position] + unicode + self._text[self._cursor_position:]
            self.cursor_position+=1



    def _control_handler(self, key):

        # Copy
        if key == pygame.K_c: copy(self.text)

        # Paste
        elif key == pygame.K_v:
            self.text = paste()
            self.cursor_position = len(self.text)
            
        # Cut
        elif key == pygame.K_x:
            copy(self._text)
            self.text = ""
            self.cursor_position = 0



    def _mousebuttonup_handler(self, pos):

        # Check for click on TextBox
        if self._rect.collidepoint(pos): self.is_selected = True
        else: self.is_selected = False

        # Set cursor position
        if self._is_selected:
            cursor_position = 0
            x = pos[0] - self._rect.left - self._margin
            prev_possible_cursor_position = 0
            for possible_cursor_position in [sum(letter_surface.get_width() for letter_surface in self._letter_surfaces[:i])
                                             for i in range(1, len(self._letter_surfaces)+1)]:
                if abs(x-possible_cursor_position) > abs(x-prev_possible_cursor_position): break
                prev_possible_cursor_position = possible_cursor_position
                cursor_position+=1
            self.cursor_position = cursor_position


# Functions
def renderLetters(font:pygame.font.Font,
               text:str|bytes|None, antialias:bool,
               color:pygame.Color|tuple[int,int,int], background:pygame.Color|tuple[int,int,int]|None=None) -> list[pygame.Surface]:
    letters: list[pygame.Surface] = []
    for letter in text: letters.append(font.render(letter, antialias, color, background))
    return letters


# Example
if __name__ == "__main__":

    # Finals - Settings for the project
    BG_COLOR = pygame.Color('tan')
    FONT = pygame.font.SysFont('Comic Sans MS', 24)
    FPS = 30
    HEIGHT = FONT.get_linesize()-FONT.get_descent()
    WIN = pygame.display.set_mode((300, HEIGHT+80))

    # Variables
    textbox = TextBox(pygame.Rect(10, 10, 280, HEIGHT), font=FONT)
    clock = pygame.time.Clock()
    running = True

    # Set up
    pygame.display.set_caption("pygametextbox Demo")
    pygame.event.set_blocked(None)
    pygame.event.set_allowed( (pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONUP) )
    pygame.key.set_repeat(300, 100)

    # Game loop
    while running:

        # Event handling
        events = pygame.event.get()
        for event in events:
            match event.type:
              case pygame.QUIT: running = False

        textbox.update(events) # Pass events to the textbox.update method every frame
        
        # Draw to the window
        WIN.fill(BG_COLOR)
        textbox.drawTo(WIN)
        pygame.display.flip()
    
        clock.tick(FPS)

    pygame.quit()
    exit()