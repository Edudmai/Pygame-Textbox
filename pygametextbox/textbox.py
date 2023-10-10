"""textbox File Description

Intended for internal use only. Features may be imported to pygametextbox.__init__ to be made public.

Contains all functionality for the pygametextbox package.
"""









# Imports

from __future__ import annotations
import pygame, typing
from pyperclip import copy, paste









# Initialization

#if not pygame.get_init(): pygame.init()
if not pygame.font.get_init(): pygame.font.init()









# Variables

default_antialias: bool = True
"""textbox.default_antialias"""

default_background_color: pygame.Color = pygame.Color('gray97')
"""textbox.default_antialias"""

default_font: pygame.font.Font = pygame.font.Font()
"""textbox.default_background_color"""

default_inactive_color: pygame.Color = pygame.Color('gray90')
"""textbox.default_inactive_color"""

default_margin: int = 2
"""textbox.default_margin"""

default_placeholder: str | None = None
"""textbox.default_placeholder"""

default_placeholder_color: pygame.Color = pygame.Color('gray50')
"""textbox.default_placeholder_color"""

default_text_color: pygame.Color = pygame.Color('gray3')
"""textbox.default_text_color"""









# Classes

class TextBox:
    """pygametextbox.TextBox Class Description"""
    








    def __init__(self, pos:tuple[int,int], width:int, lines:int,
                 placeholder:str|None=default_placeholder, font=default_font,
                 colors:list[pygame.Color|tuple[int,int,int]]=None):
        """pygametextbox.TextBox.__init__ Description"""

        height: int = default_margin + lines * font.get_linesize() + default_margin

        # Internal property defaults
        self._action: typing.Callable[[TextBox], None] | None = None
        self._antialias: bool = default_antialias
        self._cursor_position: int = 0
        self._is_selected: bool = False
        self._letters: list[pygame.Surface] = []
        self._margin: int = default_margin
        self._placeholder_render: pygame.Surface | None = None
        self._prev_text: str = ""
        self._surface: pygame.Surface = pygame.Surface((width, height))
        self._text: str = ""

        # Internal property values from arguments
        self._font: pygame.font.Font = font
        self._placeholder: str | None = placeholder
        self._rect: pygame.Rect = pygame.Rect(pos, (width, height))

        # Colors
        self._text_color: pygame.Color = colors[0] if colors and len(colors) >= 1 else default_text_color
        self._bg_color: pygame.Color = colors[1] if colors and len(colors) >= 2 else default_background_color
        self._inactive_color: pygame.Color = colors[2] if colors and len(colors) >= 3 else default_inactive_color
        self._placeholder_color: pygame.Color = colors[3] if colors and len(colors) >= 4 else default_placeholder_color

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
    def placeholder(self) -> str | None:
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

        self._placeholder_render = self.font.render(self.placeholder, self.antialias, self._placeholder_color)
        self._is_dirty = True
    




    def drawTo(self, window:pygame.Surface):
        """pygametextbox.TextBox.draw Method Description"""

        window.blit(self.get_surface(), self.rect)
    




    def rerender(self):
        """pygametextbox.TextBox.rerender Method Description"""

        # Rerender letters if needed FIXME - Skip unnecesary rerenders
        if self.text != self._prev_text: self._letters = _renderLetters(self.font, self.text, self.antialias, self._text_color)
        self._prev_text = self.text
        
        bg_color = self._bg_color if self.is_selected else self._inactive_color
        self._surface.fill(bg_color)

        # Blit letters to surface
        x = 0
        for letter in self._letters:
            self._surface.blit(letter, (self.margin+x, self.margin))
            x += letter.get_width()
            if x >= self._surface.get_width(): break
        
        if self.placeholder and not self.text: self._surface.blit(self._placeholder_render, (self.margin, self.margin))

        # Draw cursor
        if self.is_selected: #TODO - Make readable
            pygame.draw.rect(self._surface, self._text_color, (self.margin+sum(letter.get_width() for letter in self._letters[:self.cursor_position]), self.margin, 2, self.font.get_height()))
    




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
        
        # Command key (Mac) TODO - Make universal
        if mod == 1024 or mod == 2048: self._control_handler(key)
        
        # Left/right arrow keys
        elif key == pygame.K_LEFT:
            if self.cursor_position > 0: self.cursor_position-=1

        elif key == pygame.K_RIGHT:
            if self.cursor_position < len(self.text): self.cursor_position+=1
        
        # Enter/return key
        elif key == pygame.K_RETURN:
            if self._action: self._action(self.text)

        # Delete/backspace key
        elif key == pygame.K_DELETE or key == pygame.K_BACKSPACE:
            if self.text[:self.cursor_position]:
                self.cursor_position-=1
                self.text = self.text[:self.cursor_position] + self.text[self.cursor_position+1:]
        
        # Typing key
        elif unicode and key != pygame.K_TAB:
            self.text = self.text[:self.cursor_position] + unicode + self.text[self.cursor_position:]
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
            copy(self.text)
            self.text = ""
            self.cursor_position = 0



    def _mousebuttonup_handler(self, pos):

        # Check for click on TextBox
        if self.rect.collidepoint(pos): self.is_selected = True
        else: self.is_selected = False

        # Set cursor position
        if self.is_selected:
            cursor_position = 0
            x = pos[0] - self.rect.left - self.margin
            prev_possible_cursor_position = 0
            for possible_cursor_position in [sum(letter_surface.get_width() for letter_surface in self._letters[:i])
                                             for i in range(1, len(self._letters)+1)]:
                if abs(x-possible_cursor_position) > abs(x-prev_possible_cursor_position): break
                prev_possible_cursor_position = possible_cursor_position
                cursor_position+=1
            self.cursor_position = cursor_position









# Functions

def _renderLetters(font:pygame.font.Font, text:str|bytes|None, antialias:bool,
               color:pygame.Color|tuple[int,int,int],
               background:pygame.Color|tuple[int,int,int]|None=None) -> list[pygame.Surface]:
    """pygametextbox._renderLetters Function Description"""
    letters: list[pygame.Surface] = []
    for letter in text: letters.append(font.render(letter, antialias, color, background))
    return letters









# Example

if __name__ == "__main__":

    # Enter action
    def enterAction(textbox:TextBox):
        print(textbox.text)
        textbox.text = ""

    # Finals - Settings for the project
    BG_COLOR: pygame.font.Font = pygame.Color('tan')
    FONT: pygame.font.Font = pygame.font.SysFont('Menlo', 24)
    FPS: int = 30
    TEXTBOX_HEIGHT: int = FONT.get_ascent() + -FONT.get_descent() + 4 # Extra 4 added to account for 2 px. margin on top & bottom
    TEXTBOX_POSITION: tuple[int, int] = 10, 10
    TEXTBOX_WIDTH: int = 280
    WIN: pygame.Surface = pygame.display.set_mode((300, TEXTBOX_HEIGHT+80))

    # Variables
    textbox: TextBox = TextBox(TEXTBOX_POSITION, 280, 2, "Placeholder!", FONT)
    clock: pygame.time.Clock = pygame.time.Clock()
    running: bool = True

    # Set up
    pygame.display.set_caption("pygametextbox Demo")
    pygame.event.set_blocked(None)
    pygame.event.set_allowed((pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONUP))
    pygame.key.set_repeat(300, 100)
    textbox.set_action(enterAction)

    # Game loop
    while running:

        # Event handling
        events: list[pygame.event.Event] = pygame.event.get()
        for event in events:
            match event.type:
              case pygame.QUIT: running = False

        textbox.update(events) # Pass events to the textbox.update method every frame
        
        # Draw to the window
        WIN.fill(BG_COLOR)
        # It is recommended to use the TextBox.drawTo method instead of blitting directly
        # If it is blitted directly, it must be at the coordinates passed when initializing the TextBox
        textbox.drawTo(WIN)
        pygame.display.flip()
    
        clock.tick(FPS)