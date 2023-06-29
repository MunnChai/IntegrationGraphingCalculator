import pyglet
from CalculatorPanel import IntegrationCalculator
from Constants import Colors
from Result import ResultPanel
from Graph import GraphPanel
from Parsing import Parser
from GraphSettings import GraphSettingsPanel
import Constants

# Creating the window
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
WINDOW = pyglet.window.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Integration Calculator")
WINDOW_BACKGROUND = pyglet.shapes.Rectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, color = Colors.DARK_4)

# Loading font
pyglet.resource.add_font('cmunbx.ttf')
pyglet.resource.add_font('cmunrm.ttf')
uni_sans_heavy_caps = pyglet.font.load(Constants.FONT)

# Instantiating components
calculator = IntegrationCalculator()
results = ResultPanel()
graph = GraphPanel()
parser = Parser()
graphSettings = GraphSettingsPanel()
fps_display = pyglet.window.FPSDisplay(window=WINDOW)

# Drawing the Window
@WINDOW.event
def on_draw():
    WINDOW.clear()
    graph.draw()
    calculator.draw()
    results.draw()
    graphSettings.draw()
    fps_display.draw()

# Mouse Events
@WINDOW.event
def on_mouse_press(x, y, mouseButton, modifiers):
    if pyglet.window.mouse.LEFT:
        for button in calculator.buttons.values():
            if button.checkMouseClick(x, y):
                button.buttonPressDown()
        for display in calculator.displays:
            if display.checkMouseClick(x, y):
                display.buttonPressDown()
        for display in results.displays:
            if display.checkMouseClick(x, y):
                display.buttonPressDown()
        for display in graphSettings.displays:
            if display.checkMouseClick(x, y):
                display.buttonPressDown()
        if graph.checkMouseClick(x, y):
            graph.buttonPressDown()
            
@WINDOW.event
def on_mouse_release(x, y, mouseButton, modifiers):
    for button in calculator.buttons.values():
        button.buttonRelease()
    graph.buttonRelease()

@WINDOW.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if (buttons == pyglet.window.mouse.LEFT) and graph.mouseDown: 
        graph.dragGraph(dx, dy)

@WINDOW.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    if scroll_y > 0:
        graph.zoomIn(x, y, scroll_y)
    elif scroll_y < 0:
        graph.zoomOut(x, y, abs(scroll_y))


# Key Events
@WINDOW.event
def on_key_press(symbol, modifiers):
    if modifiers == pyglet.window.key.MOD_SHIFT:
        if symbol == pyglet.window.key.BACKSPACE:
            calculator.buttons.get(pyglet.window.key.BACKSPACE).buttonPressDown()
        elif symbol == pyglet.window.key._6:
            calculator.buttons.get(pyglet.window.key.GRAVE).buttonPressDown()
        elif symbol == pyglet.window.key._8:
            calculator.buttons.get(pyglet.window.key.ASTERISK).buttonPressDown()
        elif symbol == pyglet.window.key.EQUAL:
            calculator.buttons.get(pyglet.window.key.PLUS).buttonPressDown()
        elif symbol == pyglet.window.key._9:
            calculator.buttons.get(pyglet.window.key.PARENLEFT).buttonPressDown()
        elif symbol == pyglet.window.key._0:
            calculator.buttons.get(pyglet.window.key.PARENRIGHT).buttonPressDown()
    else:
        if symbol == pyglet.window.key.TAB:
            currentDisplayIndex = IntegrationCalculator.displays.index(IntegrationCalculator.activeDisplay)
            if currentDisplayIndex >= len(IntegrationCalculator.displays) - 1:
                nextDisplay = IntegrationCalculator.displays[0]
            else:
                nextDisplay = IntegrationCalculator.displays[currentDisplayIndex + 1]
            IntegrationCalculator.activeDisplay = nextDisplay
        if symbol in calculator.buttons.keys():
            calculator.buttons.get(symbol).buttonPressDown()

@WINDOW.event
def on_key_release(symbol, modifiers):
    if modifiers == pyglet.window.key.MOD_SHIFT:
        if symbol == pyglet.window.key.BACKSPACE:
            calculator.buttons.get(pyglet.window.key.BACKSPACE).buttonRelease()
        elif symbol == pyglet.window.key._6:
            calculator.buttons.get(pyglet.window.key.GRAVE).buttonRelease()
        elif symbol == pyglet.window.key._8:
            calculator.buttons.get(pyglet.window.key.ASTERISK).buttonRelease()
        elif symbol == pyglet.window.key.EQUAL:
            calculator.buttons.get(pyglet.window.key.PLUS).buttonRelease()
        elif symbol == pyglet.window.key._9:
            calculator.buttons.get(pyglet.window.key.PARENLEFT).buttonRelease()
        elif symbol == pyglet.window.key._0:
            calculator.buttons.get(pyglet.window.key.PARENRIGHT).buttonRelease()
    else:   
        if symbol in calculator.buttons.keys():
            calculator.buttons.get(symbol).buttonRelease()

# Run application
pyglet.app.run()
