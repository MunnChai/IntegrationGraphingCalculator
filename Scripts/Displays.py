import pyglet
from Constants import Colors
import Constants
from MathFunction import Function

# Represents a display on the calculator which displays user input
class Display:

    def __init__(self, x, y, width, height, color, fontsize, array):

        # Display Rectangle
        self.displayRectangle = pyglet.shapes.Rectangle(x, y, width, height, color)
        self.displayRectangle.anchor_position = (self.displayRectangle.width/2, self.displayRectangle.height/2)

        # Setting display locations
        self.originalX = x
        self.originalY = y
        self.originalWidth = width
        self.originalHeight = height
        self.originalFontSize = fontsize

        # Display's display array
        self.array = array

        # Whether display is selected to type in
        self.active = False

        # Display Text
        self.text = pyglet.text.Label(text = '', font_name = Constants.FONT, font_size = fontsize,
                          x = x - self.displayRectangle.width / 2 + 20, y = y + 5, anchor_x='left', 
                          anchor_y='center', color = Colors.LIGHT_4)
        
    # Draw display
    def draw(self):

        if Function.activeArray is self.array:
            self.displayRectangle.color = Colors.LIGHT_2
        else:
            self.displayRectangle.color = Colors.DARK_1

        self.updateDisplay()
        self.displayRectangle.draw()
        self.text.draw()

    # Checking if mouse is over display
    # Checks if mouse position is on button
    def checkMouseClick(self, x, y):
        rect = self.displayRectangle
        return (x >= rect.x - rect.width/2 and x <= rect.x + rect.width/2 
                and y >= rect.y - rect.height/2 and y <= rect.y + rect.height/2)

    # Switches active display to this display when mouse clicked
    def buttonPressDown(self):

        Function.activeArray = self.array

    

        



# Represents display panel for formula
class CalculatorDisplay(Display):

    def __init__(self):
        super().__init__(265, 350 + 260, 480, 50, Colors.DARK_1, 30, Function.functionArray)

    # Draw display
    def draw(self):
        super().draw()

    # Update display
    def updateDisplay(self):
        self.text.text = "f(x) = " + Function.parseArray(self.array)

    
    


# Represents calculator display of upper and lower limits
class LimitDisplay(Display):

    def __init__(self, x, y, width, height, array, besideText):
        super().__init__(x, y, width, height, Colors.DARK_1, 20, array)
        self.text.x = x - 25
        self.text.y = y + 2.5

        self.besideText = pyglet.text.Label(text = besideText, font_name = Constants.FONT, font_size = 20,
                          x = x - self.displayRectangle.width / 2 - 10, y = y + 2.5, anchor_x='right', 
                          anchor_y='center', color = Colors.LIGHT_4)

    # Draw display
    def draw(self):
        super().draw()
        self.besideText.draw()

    # Update display
    def updateDisplay(self):
        self.text.text = Function.parseArray(self.array)
