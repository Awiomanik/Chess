"""
This module provides data structures and functions used in UI module.

Classes:
    - InputEvent: Represents an individual input event (e.g., key press or mouse click).
    - InputStack: Manages a stack of InputEvent objects, allowing for easy handling of input events.

Author: WK-K
"""

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
        """
        Clear all events from the stack.
        """
        self.stack.clear()

    def __repr__(self) -> str:
        """
        Returns a string representation of the InputStack instance, 
        which includes all the input events currently in the stack numbered.

        Returns:
        - (str) A string that represents the InputStack object.
        """
        representation = "InputStack:"
        num = 1
        for event in self.stack:
            representation += f"\n{num}. {event}"
            num += 1
        return representation








