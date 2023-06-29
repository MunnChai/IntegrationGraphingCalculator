# Font
FONT = 'CMU Serif'

# Function Inputs
PARENTHESES = ['(', ')']
NUMBERS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
MATH_OPS = ["+", "-", "*", "/", ".", "^"]
MATH_CONSTANTS = ['x', 'e', 'π'] # NOTE: x is not a constant, but it behaves like one when parsing user input
SPECIAL_FUNCTIONS = ["sin(", "cos(", "tan(", "ln("]

# Intervals for graphing and calculating simpson's rule approximation
SIMPSONS_INTERVALS = 50
GRAPHING_INTERVALS = 100

# Palette of colors used in app
class Colors:

    DARK_4 = (13, 43, 69, 255) # Darkest
    DARK_3 = (32, 60, 86, 255)
    DARK_2 = (84, 78, 104, 255)
    DARK_1 = (141, 105, 122, 255)
    LIGHT_1 = (208, 129, 89, 255)
    LIGHT_2 = (255, 170, 94, 255)
    LIGHT_3 = (255, 212, 163, 255)
    LIGHT_4 = (255, 236, 214, 255)

graphTop = 720
graphBottom = 140
graphLeft = 530
graphRight = 1280

graphDragSpeed = 0.00135
graphZoomSpeed = 0.05

graphBoundDecimals = 3