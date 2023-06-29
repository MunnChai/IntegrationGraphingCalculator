import pyglet
import Constants
import math
from MathFunction import Function
from Constants import Colors
from NumericalIntegration import simpsonsRuleCalc
from Parsing import Parser
from Displays import *
from pyglet.gl import *

class ResultPanel:

    singleton = None

    def __init__(self):
        self.panelBackground = pyglet.shapes.Rectangle(0, 0, 530, 260, Colors.DARK_3)

        self.title = pyglet.text.Label(text = 'Integrate', font_name = Constants.FONT, font_size = 30,
                          x = 30, y = 240, anchor_x='left', anchor_y='center', color = Colors.LIGHT_4, bold=True)
        
        ResultPanel.singleton = self

        self.displays = []
        
        self.upperLimit = LimitDisplay(280, 170, 70, 50, Function.upperLimit, 'to ')
        self.lowerLimit = LimitDisplay(150, 170, 70, 50, Function.lowerLimit, 'From ')

        self.displays.append(self.upperLimit)
        self.displays.append(self.lowerLimit)

        self.integralSymbol = pyglet.resource.image('integralSymbol.png')
        self.pic = pyglet.sprite.Sprite(img = self.integralSymbol)
        self.pic.position = (40, 80, 0)
        self.pic.scale = 0.05

        self.function = self.result = pyglet.text.Label(text = '', font_name = Constants.FONT, font_size = 20,
                          x = 60, y = 105, anchor_x='left', anchor_y='center', color = Colors.LIGHT_2)
        

    # Drawing components of panel
    def draw(self):
        self.panelBackground.draw()
        self.title.draw()

        for display in self.displays:
            display.draw()

        self.drawIntegralResult()
        

    # Draws integration symbol, function, and result
    def drawIntegralResult(self):
        glEnable(GL_BLEND)

        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.pic.draw()

        self.updateFunction()
        
    # Updates current function
    def updateFunction(self):
        
        function = Parser.parseFunction(Parser.instance, Function.functionArray)

        self.function.text = "(" + Function.parseArray(Function.functionArray) + ")dx \u2248 " + str(self.evalSimpsons(function))
        self.function.draw()

    # Returns evaluated function as a double, rounded to 5 decimal places
    def evalFunction(self, stringFunction):
        if stringFunction == '':
            return ''
        elif 'x' in stringFunction:
            return 'Contains x'
        else:
            decimalRounding = 5
            try:
                return round(eval(stringFunction), decimalRounding)
            except ZeroDivisionError:
                return "Error: division by zero" 
            except ValueError:
                return "Error: value too large"
            except SyntaxError:
                return "Error: equation syntax"
    
    # Returns simposon's rule approximation of integral
    def evalSimpsons(self, stringFunction):

        upperLimit = self.evalFunction(Parser.parseFunction(Parser.instance, Function.upperLimit))
        lowerLimit = self.evalFunction(Parser.parseFunction(Parser.instance, Function.lowerLimit))

        if stringFunction == '' or lowerLimit == '' or upperLimit == '':
            return ''
        elif isinstance(upperLimit, str):
            return 'Err: up lim'
        elif isinstance(lowerLimit, str): 
            return 'Err: low lim'
        else:
            try:
                decimalRounding = 5
                return str(round(simpsonsRuleCalc(upperLimit, lowerLimit, stringFunction), decimalRounding)) 
            except ZeroDivisionError:
                return "Err: division by 0"
            except ValueError:
                return "Err: cannot compute"
            except SyntaxError:
                return "Err: function syntax"
    
