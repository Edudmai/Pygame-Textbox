"""
A module to implement an editable text entry box for Pygame applications.
Requires use of the *pygame* module.
*pygame.KEYDOWN*, *pygame.KEYUP*, and *pygame.MOUSEBUTTONUP* events must be enabled.

Classes:

TextBox - Creates a user-editable text box using Pygame.

"""

from .textbox import (default_antialias, default_background_color, default_font,
                      default_inactive_color, default_margin, default_placeholder,
                      default_placeholder_color, default_text_color, TextBox)

__all__ = ['default_antialias', 'default_background_color', 'default_font',
           'default_inactive_color', 'default_margin', 'default_placeholder',
           'default_placeholder_color', 'default_text_color', 'TextBox']