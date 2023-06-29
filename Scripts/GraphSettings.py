import pyglet
import Constants
from Constants import Colors
from Displays import LimitDisplay

class GraphSettingsPanel():

    lowerX = ["-", 1, 0]
    upperX = [1, 0]
    lowerY = ["-", 1, 0]
    upperY = [1, 0]

    instance = None

    def __init__(self):
        self.panelBackground = pyglet.shapes.Rectangle(530, 0, 750, Constants.graphBottom, Colors.DARK_2)
        self.title = self.title = pyglet.text.Label(text = 'Graph Settings', font_name = Constants.FONT, font_size = 20,
                          x = 540, y = 100, anchor_x='left', anchor_y='center', color = Colors.LIGHT_4, bold=True)

        yPos = 50

        self.lowerXBound = LimitDisplay(640, yPos, 100, 40, GraphSettingsPanel.lowerX, besideText='X: ')
        self.upperXBound = LimitDisplay(830, yPos, 100, 40, GraphSettingsPanel.upperX, besideText='< x <')
        self.lowerYBound = LimitDisplay(1020, yPos, 100, 40, GraphSettingsPanel.lowerY, besideText='Y: ')
        self.upperYBound = LimitDisplay(1210, yPos, 100, 40, GraphSettingsPanel.upperY, besideText='< y <')

        self.displays = []
        self.displays.append(self.lowerXBound)
        self.displays.append(self.upperXBound)
        self.displays.append(self.lowerYBound)
        self.displays.append(self.upperYBound)
        for display in self.displays:
            self.fixDisplay(display)

        GraphSettingsPanel.instance = self


    def draw(self):
        self.panelBackground.draw()
        self.title.draw()
        for display in self.displays:
            display.draw()

    def writeBounds(self, lowerX, upperX, lowerY, upperY):
        
        self.write(GraphSettingsPanel.lowerX, lowerX)
        self.write(GraphSettingsPanel.upperX, upperX)
        self.write(GraphSettingsPanel.lowerY, lowerY)
        self.write(GraphSettingsPanel.upperY, upperY)

    def write(self, array, number):
        array.clear()

        for o in str(number):
            if o == "." or o == "-":
                array.append(o)
            else:
                array.append(int(o))

    def fixDisplay(self, display):
        display.text.x -= 15