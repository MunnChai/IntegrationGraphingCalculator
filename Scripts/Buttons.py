import pyglet
import Constants
from Constants import Colors
from MathFunction import Function

from Result import ResultPanel
from Graph import GraphPanel # Functionality may be removed - see EnterButton.buttonPressDown()

# Represents a button on the calculator
class Button:

    def __init__(self, xPos, yPos, width, height, text, fontsize, buttonColor, textColor):

        # Creating shapes and text
        self.rectangle = pyglet.shapes.Rectangle(xPos, yPos, width, height, buttonColor)
        self.rectangle.anchor_position = (width/2, height/2)
        self.text = pyglet.text.Label(text = text, font_name = Constants.FONT, font_size = fontsize,
                          x = xPos, y = yPos + 5, anchor_x='center', anchor_y='center', color = textColor)
        
        # Setting button locations
        self.originalX = xPos
        self.originalY = yPos
        self.originalWidth = width
        self.originalHeight = height
        self.originalFontSize = fontsize

    # Draws all components of button
    def draw(self):
        self.rectangle.draw()
        self.text.draw()


    # Checks if mouse position is on button
    def checkMouseClick(self, x, y):
        rect = self.rectangle
        return (x >= rect.x - rect.width/2 and x <= rect.x + rect.width/2 
                and y >= rect.y - rect.height/2 and y <= rect.y + rect.height/2)
    
    # Scales button down when mouse clicked on button
    def buttonPressDown(self):
        rect = self.rectangle
        
        rect.x += rect.width * 0.05
        rect.y += rect.height * 0.05
        rect.width = rect.width * 0.9
        rect.height = rect.height * 0.9
        self.text.font_size = self.text.font_size * 0.9
    
    # Scales button back to default size when mouse released
    def buttonRelease(self):
        rect = self.rectangle

        rect.x = self.originalX
        rect.y = self.originalY
        rect.width = self.originalWidth
        rect.height = self.originalHeight
        self.text.font_size = self.originalFontSize



# Represents a button on the calculator to input numbers (eg. 1, 2, 5)
class NumpadButton(Button):

    BUTTON_WIDTH = 50
    BUTTON_HEIGHT = 50
    FONT_SIZE = 30

    def __init__(self, xPos, yPos, text, displayText):
        super().__init__(xPos, yPos, NumpadButton.BUTTON_WIDTH, NumpadButton.BUTTON_HEIGHT, text, 
                         NumpadButton.FONT_SIZE, Colors.DARK_1, Colors.LIGHT_4)

        # Text to be displayed on calculator display panel
        self.displayText = displayText

    # Performs button press action
    def buttonPressDown(self):
        super().buttonPressDown()
        Function.activeArray.append(self.displayText)



# Represents buttons on the calculator for clearing the function (eg. clear and delete)
class DeleteButton(Button):

    BUTTON_WIDTH = 85
    BUTTON_HEIGHT = 50
    FONT_SIZE = 20

    def __init__(self, xPos, yPos, text):
        super().__init__(xPos, yPos, DeleteButton.BUTTON_WIDTH, DeleteButton.BUTTON_HEIGHT, text, 
                         DeleteButton.FONT_SIZE, Colors.LIGHT_1, Colors.LIGHT_4)

        # Type of delete button (clear or delete)
        self.type = text

    # Performs button press action
    def buttonPressDown(self):
        super().buttonPressDown()

        array = Function.activeArray
        length = len(array)

        if self.type == "Clear":
            array.clear()
            ParenthesisButton.openParentheses = 0
        elif self.type == "Delete" and len(array) > 0:
            if array[length - 1] == '(':
                ParenthesisButton.openParentheses -= 1
            elif array[length - 1] == ')':
                ParenthesisButton.openParentheses += 1
            array.pop(length - 1)



# Represents a button on the calculator to input simple mathematical operations (eg. +, -, *)
class MathOpButton(Button):

    BUTTON_WIDTH = 50
    BUTTON_HEIGHT = 50
    FONT_SIZE = 30

    def __init__(self, xPos, yPos, text, displayText):
        super().__init__(xPos, yPos, MathOpButton.BUTTON_WIDTH, MathOpButton.BUTTON_HEIGHT, text, 
                         MathOpButton.FONT_SIZE, Colors.DARK_2, Colors.LIGHT_4)

        # Text to be displayed on calculator display panel
        self.displayText = displayText

    # Performs button press action
    def buttonPressDown(self):
        super().buttonPressDown()

        array = Function.activeArray
        # Checks if display is empty, or if previous input was a math operation
        length = len(array)

        if self.displayText == "-":
            array.append(self.displayText)
        elif length > 0 and not self.notViable(array[length - 1]):
            array.append(self.displayText)
    
    # Checks if given string is a math operation
    def notViable(self, string):
        return string in Constants.MATH_OPS or string in Constants.SPECIAL_FUNCTIONS or string == "("



# Represents buttons to input mathetmatical constants (eg. pi, euler's number)
class ConstantButton(Button):

    BUTTON_WIDTH = 50
    BUTTON_HEIGHT = 50
    FONT_SIZE = 30

    def __init__(self, xPos, yPos, text, displayText):
        super().__init__(xPos, yPos, ConstantButton.BUTTON_WIDTH, ConstantButton.BUTTON_HEIGHT, text, 
                         ConstantButton.FONT_SIZE, Colors.DARK_2, Colors.LIGHT_4)

        # Text to be displayed on calculator display panel
        self.displayText = displayText

    # Performs button press action
    def buttonPressDown(self):
        super().buttonPressDown()
        Function.activeArray.append(self.displayText)



# Represents buttons for parentheses
class ParenthesisButton(Button):

    BUTTON_WIDTH = 50
    BUTTON_HEIGHT = 50
    FONT_SIZE = 30

    # Counting open parentheses for closing parentheses
    openParentheses = 0

    def __init__(self, xPos, yPos, text, displayText):
        super().__init__(xPos, yPos, ParenthesisButton.BUTTON_WIDTH, ParenthesisButton.BUTTON_HEIGHT, text, 
                         ParenthesisButton.FONT_SIZE, Colors.DARK_2, Colors.LIGHT_4)

        # Text to be displayed on calculator display panel
        self.displayText = displayText

    # Performs button press action
    def buttonPressDown(self):
        super().buttonPressDown()

        array = Function.activeArray

        length = len(array)

        if length == 0 and self.displayText == ')': # Checks if display is empty
            pass

        elif self.displayText == '(':
            array.append(self.displayText)
            ParenthesisButton.openParentheses += 1

        elif self.notViable(array[length - 1]): # Checks if previous input was a math operation
            pass

        elif self.displayText == ')':

            # Checks if there are any open parentheses
            if ParenthesisButton.openParentheses > 0:
                array.append(self.displayText)
                ParenthesisButton.openParentheses -= 1
                
        
    
    # Checks if given string is a math operation
    def notViable(self, string):
        return string in Constants.MATH_OPS or string in Constants.SPECIAL_FUNCTIONS or string == "("
    


# Represents a button for special operations (eg. sin, cos, ln)
class SpecialOperationButton(Button):

    BUTTON_WIDTH = 85
    BUTTON_HEIGHT = 50
    FONT_SIZE = 20

    def __init__(self, xPos, yPos, text, displayText):
        super().__init__(xPos, yPos, SpecialOperationButton.BUTTON_WIDTH, SpecialOperationButton.BUTTON_HEIGHT, text, 
                         SpecialOperationButton.FONT_SIZE, Colors.DARK_2, Colors.LIGHT_4)

        # Type of delete button (clear or delete)
        self.displayText = displayText

    # Performs button press action
    def buttonPressDown(self):
        super().buttonPressDown()

        Function.activeArray.append(self.displayText)
        ParenthesisButton.openParentheses += 1
