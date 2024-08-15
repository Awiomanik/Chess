"""
This module provides data structures and functions used in UI module.

Classes:
    - InputEvent: Represents an individual input event (e.g., key press or mouse click).
    - InputStack: Manages a stack of InputEvent objects, allowing for easy handling of input events.

Functions:
    - render_multiline_text(text: str, font: pygame.font.Font,
                            color: tuple[int, int, int] | tuple[int, int, int, int],
                            spacing_factor: float=1, tabulator_width: int=8) -> pygame.Surface:
        Renders a multiline text onto the surface.

Author: WK-K
"""

import pygame

# Data Type for stacking events
class InputEvent:
    """
    A class to represent an input event in the game.

    Attributes:
    - event_type: str - The type of event (e.g., "key", "mouse").
    - data: tuple(int, int)|str - Additional data related to the event (tuple of mouse coordinates or pressed key str).

    Methods:
    - __repr__(): Returns a string representation of the InputEvent instance for easy debugging.

    Special keys:
    - Arrow keys: "UP", "DOWN", "LEFT", "RIGHT"
    - Return key: "ENTER"
    """
    def __init__(self, event_type: str, data: tuple[int, int]|str=None):
        """
        Initialize an input event.

        Parameters:
        - event_type: str - The type of event (e.g., "key", "mouse").
        - data: tuple(int, int)|str - Additional data related to the event (tuple of mouse coordinates or pressed key str).
        """
        self.event_type: str = event_type
        self.data: tuple[int, int]|str = data
    
    def __repr__(self):
        """Returns stiring representation of the InputEvent (one line)"""
        return f"InputEvent({self.event_type}, {self.data})"

class InputStack:
    """
    A class to manage a stack of input events, allowing for efficient handling of user input in a game.

    Attributes:
    - stack: list of InputEvent - A list that holds all input events in a stack (LIFO) structure.

    Methods:
    - push(event_type: str, data: tuple[int, int]|str=None) -> None: Adds a new InputEvent to the stack.
    - pop() -> InputEvent|None: Removes and returns the last InputEvent from the stack.
    - peek() -> InputEvent|None: Returns the last InputEvent from the stack without removing it.
    - clear() -> None: Clears all events from the stack.
    - __repr__() -> str: Returns a string representation of the InputStack instance for easy debugging.
    """
    def __init__(self) -> None:
        """
        Initialize the stack to hold input events.
        """
        self.stack = []

    def push(self, event_type: str, data: tuple[int, int]|str=None) -> None:
        """
        Push a new event onto the stack.

        Parameters:
        - event_type: str - The type of event (e.g., "key", "mouse").
        - data: tuple(int, int)|str - Additional data related to the event (tuple of mouse coordinates or pressed key str).
        """
        self.stack.append(InputEvent(event_type, data))

    def pop(self) -> InputEvent|None:
        """
        Pop the last event from the stack.

        Returns:
        - The last input event if available, otherwise None.
        """
        if self.stack:
            return self.stack.pop()
        return None

    def peek(self) -> InputEvent|None:
        """
        Peek at the last event on the stack without removing it.

        Returns:
        - The last input event if available, otherwise None.
        """
        if self.stack:
            return self.stack[-1]
        return None

    def clear(self) -> None:
        """Clear all events from the stack."""
        self.stack.clear()

    def __repr__(self) -> str:
        """
        Returns a string representation of the InputStack instance, 
        which includes all the input events currently in the stack numbered.
        Representation is a multiple line string.

        Returns:
        - (str) A string that represents the InputStack object.
        """
        representation = "InputStack:"
        num = 1
        for event in self.stack:
            representation += f"\n{num}. {event}"
            num += 1
        return representation

def render_multiline_text(text: str, font: pygame.font.Font,
                            color: tuple[int, int, int] | tuple[int, int, int, int],
                            spacing_factor: float=1, tabulator_width: int=8) -> pygame.Surface:
    """
    Renders a multiline text onto the surface.
    Swaps tabulators for corresponding number of spaces based on tabulator_width parameter.

    Returns:
    - pygame.Surface: Semi transparent surface with text rendered on it.
    
    Parameters:
    - text (str): The multiline text to render.
    - font (pygame.Font): The font object used to render the text.
    - color (tuple[int, int, int]): The color of the text.
    - spacing_factor (float): Factor by which spacing between lines (defaults to hight of text) is devided.
    - tabulator_width (int): Maximum width of the tabulator to be swapped with spaces
    """
    # Split the text into lines
    lines: list[str] = text.splitlines()

    # Process each line to calculate the size of the final surface
    rendered_lines: list[pygame.Surface] = []
    max_width: int = 0
    total_height: int = 0

    for line in lines:
        # Convert tabs to spaces based on the tabulator width
        line_splitted = line.split('\t')
        if len(line_splitted) > 1:
            temp_line = ''
            for part in line_splitted:
                temp_line += part
                temp_line += ' ' * (tabulator_width - (len(temp_line) % tabulator_width))
            line = temp_line
        
        # Render the line to get its surface
        line_surface = font.render(line, True, color)
        rendered_lines.append(line_surface)
        
        # Calculate width and height
        max_width = max(max_width, line_surface.get_width())
        total_height += line_surface.get_height() // spacing_factor

    # Create a new surface to hold the entire multiline text
    text_surface = pygame.Surface((max_width, total_height), pygame.SRCALPHA)
    text_surface = text_surface.convert_alpha()  # Support transparency

    # Blit each line onto the text surface
    y = 0
    for line_surface in rendered_lines:
        text_surface.blit(line_surface, (0, y))
        y += line_surface.get_height() // spacing_factor

    return text_surface


