import pyglet
from MathFunction import Function
from Constants import Colors
from Buttons import *
from Displays import *

# Represents calculator with interactable buttons
class IntegrationCalculator:

    buttons = {}
    displays = []

    def __init__(self):
        self.panelBackground = pyglet.shapes.Rectangle(0, 260, 530, 460, Colors.DARK_3)

        self.title = self.title = pyglet.text.Label(text = 'Function', font_name = Constants.FONT, font_size = 30,
                          x = 30, y = 680, anchor_x='left', anchor_y='center', color = Colors.LIGHT_4, bold=True)
        self.y = self.panelBackground.y
        self.createDisplays()
        self.createButtons()
        
    # Creates buttons
    def createButtons(self):
        self.createNumpad()
        self.createDeleteButtons()
        self.createMathOperationButtons()
        self.createMathConstantButtons()
        self.createParenthesesButtons()
        self.createSpecOpButtons()
        
    # Creating numpad buttons
    def createNumpad(self):

        buttons = IntegrationCalculator.buttons
        number = 1
        key = pyglet.window.key._1
        y = 230 + self.y
        for i in range(3):
            x = 50
            for j in range(3):
                buttons.update({key: NumpadButton(x, y, str(number), number)})
                x += 60
                number += 1
                key += 1
            y -= 60

        buttons.update({pyglet.window.key._0: NumpadButton(110, 50 + self.y, '0', 0)})

    # Creating backspace and clear buttons
    def createDeleteButtons(self):

        buttons = IntegrationCalculator.buttons
        buttons.update({pyglet.window.key.DELETE: DeleteButton(367.5, 290 + self.y, 'Clear')}) 
        buttons.update({pyglet.window.key.BACKSPACE: DeleteButton(462.5, 290 + self.y, 'Delete')})

    # Creating mathematical operation buttons
    def createMathOperationButtons(self):

        buttons = IntegrationCalculator.buttons
        buttons.update({pyglet.window.key.PLUS: MathOpButton(230, 230 + self.y, '+', '+')})
        buttons.update({pyglet.window.key.MINUS: MathOpButton(290, 230 + self.y, '-', '-')})
        buttons.update({pyglet.window.key.ASTERISK: MathOpButton(230, 170 + self.y, '*', '*')})
        buttons.update({pyglet.window.key.SLASH: MathOpButton(290, 170 + self.y, '÷', '/')})
        buttons.update({pyglet.window.key.GRAVE: MathOpButton(170, 290 + self.y, '^', '^')})
        buttons.update({pyglet.window.key.PERIOD: MathOpButton(50, 50 + self.y, '.', '.')})

    # Creating constant buttons
    def createMathConstantButtons(self):
        
        buttons = IntegrationCalculator.buttons
        buttons.update({pyglet.window.key.X: ConstantButton(170, 50  + self.y, 'x', 'x')})
        buttons.update({pyglet.window.key.P: ConstantButton(230, 110  + self.y, 'π', 'π')})
        buttons.update({pyglet.window.key.E: ConstantButton(290, 110 + self.y, 'e', 'e')})

    # Creating parentheses buttons
    def createParenthesesButtons(self):
        
        buttons = IntegrationCalculator.buttons
        buttons.update({pyglet.window.key.PARENLEFT: ParenthesisButton(50, 290 + self.y, '(', '(')})
        buttons.update({pyglet.window.key.PARENRIGHT: ParenthesisButton(110, 290 + self.y, ')', ')')})

    # Creates buttons for special math operations
    def createSpecOpButtons(self):

        buttons = IntegrationCalculator.buttons
        buttons.update({pyglet.window.key.S: SpecialOperationButton(367.5, 230 + self.y, 'sin()', 'sin(')})
        buttons.update({pyglet.window.key.C: SpecialOperationButton(462.5, 230 + self.y, 'cos()', 'cos(')})
        buttons.update({pyglet.window.key.T: SpecialOperationButton(367.5, 170 + self.y, 'tan()', 'tan(')})
        buttons.update({pyglet.window.key.L: SpecialOperationButton(462.5, 170 + self.y, 'ln()', 'ln(')})
        
    # Creates displays
    def createDisplays(self):

        self.display = CalculatorDisplay()

        IntegrationCalculator.displays.append(self.display)

    # Draw all components of self
    def draw(self):
        self.panelBackground.draw()
        self.title.draw()

        buttons = IntegrationCalculator.buttons.values()

        # Draw buttons
        for button in buttons:
            button.draw()

        # Draw displays
        for display in IntegrationCalculator.displays:
            display.draw()







