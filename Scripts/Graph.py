import pyglet
import math
import Constants
from Constants import Colors
from NumericalIntegration import evalFunction
from Parsing import Parser
from MathFunction import Function
from GraphSettings import GraphSettingsPanel

class GraphPanel:
    instance = None

    def __init__(self):
        self.panelBackground = pyglet.shapes.Rectangle(Constants.graphLeft, Constants.graphBottom, 
                                                        Constants.graphRight - Constants.graphLeft, 
                                                        Constants.graphTop - Constants.graphBottom, Colors.DARK_4)

        self.curvePoints = []
        self.curveLines = []
        self.integrationFillLines = []
        self.axisLines = []
        self.axisLabels = []
        self.mouseDown = False
        
        GraphPanel.instance = self

    # Draws graph panel
    def draw(self):
        self.updateGraph()
        self.drawBackground()
        try:
            self.drawPoints()
        except IndexError:
            pass # TODO Print errors more clearly

        for line in self.integrationFillLines:
            line.draw()

        for line in self.axisLines:
            line.draw()

        for label in self.axisLabels:
            label.draw()

        for line in self.curveLines:
            line.draw()

    def updateGraph(self):
        try: 
            lowerX = Parser.evalFunction(Parser.instance, GraphSettingsPanel.lowerX)
            upperX = Parser.evalFunction(Parser.instance, GraphSettingsPanel.upperX)
            lowerY = Parser.evalFunction(Parser.instance, GraphSettingsPanel.lowerY)
            upperY = Parser.evalFunction(Parser.instance, GraphSettingsPanel.upperY)

            function = Parser.parseFunction(Parser.instance, Function.functionArray)
        except Exception:
            pass # TODO Deal with errors better

        try:
            self.drawIntegrationFill(function, lowerX, upperX, lowerY, upperY)
        except Exception:
            pass # TODO Deal with errors better

        try:
            self.drawGraph(function, lowerX, upperX, lowerY, upperY)
        except Exception:
            pass # TODO Deal with errors better

    # Draws panel background and graph axes
    def drawBackground(self):
        self.panelBackground.draw()

    # Draws graph of given function
    def drawGraph(self, function, lowerX, upperX, lowerY, upperY):

        self.plotPoints(function, lowerX, upperX, lowerY, upperY)
        self.plotAxes(lowerX, upperX, lowerY, upperY)


    # Returns list of tuples representing (x, y) coordinates 
    def plotPoints(self, function, lowerX, upperX, lowerY, upperY):
    
        self.curvePoints.clear()
        # Number of points
        n = Constants.GRAPHING_INTERVALS
        deltaX = ((upperX - lowerX) / n)

        points = []
        currentX = lowerX
        for i in range(n + 1):
            try:
                x = currentX
                y = evalFunction(currentX, function)
                point = (x, y)
                points.append(point)
            except Exception:
                pass
            currentX += deltaX

        self.curvePoints = self.convertPoints(points, lowerX, upperX, lowerY, upperY)

    # Draws points on graph
    def drawPoints(self):

        self.curveLines.clear()
        
        points = self.curvePoints
        firstPoint = points[0]

        previousX = firstPoint[0]
        previousY = firstPoint[1]
        for point in points:
            currentX = point[0]
            currentY = point[1]

            line = pyglet.shapes.Line(previousX, previousY, currentX, currentY, 5, Colors.LIGHT_2)
            self.curveLines.append(line)

            previousX = currentX
            previousY = currentY

    # Converts mathematical x, y points into true coordinates of points on the application window
    def convertPoints(self, points, lowerX, upperX, lowerY, upperY):

        newPoints = []
        for point in points:
            try:
                newPoint = self.convertPoint(point, lowerX, upperX, lowerY, upperY)
                newPoints.append(newPoint)
            except ZeroDivisionError:
                return newPoints 

        return newPoints
    
    # Converts a coordinate point to its actual position on the display
    def convertPoint(self, point, lowerX, upperX, lowerY, upperY):
        oldX = point[0]
        oldY = point[1]

        percentVertical = (oldY - lowerY) / (upperY - lowerY)
        newY = (Constants.graphTop - Constants.graphBottom) * percentVertical + Constants.graphBottom
        percentHorizontal = (oldX - lowerX) / (upperX - lowerX)
        newX = (Constants.graphRight - Constants.graphLeft) * percentHorizontal + Constants.graphLeft
        newPoint = (newX, newY)
        return newPoint
    
    # Draws x and y axes onto graph
    def plotAxes(self, lowerX, upperX, lowerY, upperY):

        xAxisRight = self.convertPoint((upperX, 0), lowerX, upperX, lowerY, upperY)
        xAxisLeft = self.convertPoint((lowerX, 0), lowerX, upperX, lowerY, upperY)

        yAxisUpper = self.convertPoint((0, lowerY), lowerX, upperX, lowerY, upperY)
        yAxisLower = self.convertPoint((0, upperY), lowerX, upperX, lowerY, upperY)
        
        self.axisLines.clear()
        self.axisLabels.clear()
        if lowerX <= 0 and 0 <= upperX:
            self.drawYAxis(yAxisLower, yAxisUpper)
        if lowerY <= 0 and 0 <= upperY:
            self.drawXAxis(xAxisLeft, xAxisRight)
        self.drawXAxisLabels(xAxisLeft, xAxisRight, lowerX, upperX)
        self.drawYAxisLabels(yAxisLower, yAxisUpper, lowerY, upperY)
            
        
    # Draws x axis
    def drawXAxis(self, xAxisLeft, xAxisRight):
        
        xAxis = pyglet.shapes.Line(xAxisRight[0], xAxisRight[1], 
                                   xAxisLeft[0], xAxisLeft[1], 3, Colors.LIGHT_4)
        
        self.axisLines.append(xAxis)

    # Draws y axis
    def drawYAxis(self, yAxisLower, yAxisUpper):

        yAxis = pyglet.shapes.Line(yAxisUpper[0], yAxisUpper[1], 
                                   yAxisLower[0], yAxisLower[1], 3, Colors.LIGHT_4)
        self.axisLines.append(yAxis)

    # Draws X axis labels
    def drawXAxisLabels(self, xAxisLeft, xAxisRight, lowerX, upperX):
        topLimit = Constants.graphTop - 40
        if xAxisRight[1] >= topLimit:
            xAxisRight = (xAxisRight[0], topLimit)
            xAxisLeft = (xAxisLeft[0], topLimit)
        bottomLimit = Constants.graphBottom + 20
        if xAxisRight[1] <= bottomLimit:
            xAxisRight = (xAxisRight[0], bottomLimit)
            xAxisLeft = (xAxisLeft[0], bottomLimit)

        xAxisRightLabel = pyglet.text.Label(text = str(upperX), font_name = Constants.FONT, font_size = 15,
                          x = xAxisRight[0] - 5, y = xAxisRight[1] + 10, anchor_x='right', anchor_y='center', color = Colors.LIGHT_4)
        xAxisLeftLabel = pyglet.text.Label(text = str(lowerX), font_name = Constants.FONT, font_size = 15,
                          x = xAxisLeft[0] + 5, y = xAxisLeft[1] + 10, anchor_x='left', anchor_y='center', color = Colors.LIGHT_4)
        
        self.axisLabels.append(xAxisRightLabel)
        self.axisLabels.append(xAxisLeftLabel)

    # Draws y axis labels
    def drawYAxisLabels(self, yAxisLower, yAxisUpper, lowerY, upperY):
        leftLimit = Constants.graphLeft - 5
        if yAxisLower[0] <= leftLimit:
            yAxisLower = (leftLimit, yAxisLower[1])
            yAxisUpper = (leftLimit, yAxisUpper[1])
        rightLimit = Constants.graphRight - 55
        if yAxisLower[0] >= rightLimit:
            yAxisLower = (rightLimit, yAxisLower[1])
            yAxisUpper = (rightLimit, yAxisUpper[1])

        yAxisLowerLabel = pyglet.text.Label(text = str(upperY), font_name = Constants.FONT, font_size = 15,
                          x = yAxisLower[0] + 30, y = yAxisLower[1] - 10, anchor_x='center', anchor_y='center', color = Colors.LIGHT_4)
        yAxisUpperLabel = pyglet.text.Label(text = str(lowerY), font_name = Constants.FONT, font_size = 15,
                          x = yAxisUpper[0] + 30, y = yAxisUpper[1] + 10, anchor_x='center', anchor_y='center', color = Colors.LIGHT_4)
        
        self.axisLabels.append(yAxisLowerLabel)
        self.axisLabels.append(yAxisUpperLabel)

    # Fills in area from function to x axis within given integral bounds
    def drawIntegrationFill(self, function, lowerX, upperX, lowerY, upperY):

        self.integrationFillLines.clear()
        
        lowerLimit = eval(Parser.parseFunction(Parser.instance, Function.lowerLimit))
        upperLimit = eval(Parser.parseFunction(Parser.instance, Function.upperLimit))

        n = 25

        if (upperLimit > upperX):
            upperLimit = upperX
        if (lowerLimit < lowerX):
            lowerLimit = lowerX

        currentX = lowerLimit
        deltaX = (upperLimit - lowerLimit) / n
        for i in range(n + 1):
            x = currentX
            y = evalFunction(currentX, function)
            axisPoint = self.convertPoint((x, 0), lowerX, upperX, lowerY, upperY)
            functionPoint = self.convertPoint((x, y), lowerX, upperX, lowerY, upperY)
            line = pyglet.shapes.Line(axisPoint[0], axisPoint[1], 
                                      functionPoint[0], functionPoint[1], 8, Colors.DARK_1)
            self.integrationFillLines.append(line)
            currentX += deltaX

    # Checking if mouse is within graph
    def checkMouseClick(self, x, y):
        rect = self.panelBackground
        return (x >= rect.x and x <= rect.x + rect.width
                and y >= rect.y and y <= rect.y + rect.height)

    # Mouse drag
    def buttonPressDown(self):
        self.mouseDown = True

    # Mouse release
    def buttonRelease(self):
        self.mouseDown = False

    # Changes graph bounds based on mouse movement
    def dragGraph(self, dx, dy):
        lowerX = Parser.evalFunction(Parser.instance, GraphSettingsPanel.lowerX)
        upperX = Parser.evalFunction(Parser.instance, GraphSettingsPanel.upperX)
        lowerY = Parser.evalFunction(Parser.instance, GraphSettingsPanel.lowerY)
        upperY = Parser.evalFunction(Parser.instance, GraphSettingsPanel.upperY)

        xDragRatio = upperX - lowerX
        yDragRatio = upperY - lowerY

        yAdjustmentRatio = 1.4

        lowerX -= dx * xDragRatio * Constants.graphDragSpeed
        upperX -= dx * xDragRatio * Constants.graphDragSpeed
        lowerY -= dy * yDragRatio * Constants.graphDragSpeed * yAdjustmentRatio
        upperY -= dy * yDragRatio * Constants.graphDragSpeed * yAdjustmentRatio

        lowerX = round(lowerX, Constants.graphBoundDecimals)
        upperX = round(upperX, Constants.graphBoundDecimals)
        lowerY = round(lowerY, Constants.graphBoundDecimals)
        upperY = round(upperY, Constants.graphBoundDecimals)

        GraphSettingsPanel.writeBounds(GraphSettingsPanel.instance, lowerX, upperX, lowerY, upperY)

    # Zooms in the graph where the mouse cursor currently is 
    def zoomIn(self, x, y, scrollAmount):
        lowerX = Parser.evalFunction(Parser.instance, GraphSettingsPanel.lowerX)
        upperX = Parser.evalFunction(Parser.instance, GraphSettingsPanel.upperX)
        lowerY = Parser.evalFunction(Parser.instance, GraphSettingsPanel.lowerY)
        upperY = Parser.evalFunction(Parser.instance, GraphSettingsPanel.upperY)

        lowerX += self.calculateZoomAmount(abs(Constants.graphLeft - x), lowerX, upperX, scrollAmount, 'x')
        upperX -= self.calculateZoomAmount(abs(Constants.graphRight - x), lowerX, upperX, scrollAmount, 'x')
        lowerY += self.calculateZoomAmount(abs(Constants.graphBottom - y), lowerY, upperY, scrollAmount, 'y')
        upperY -= self.calculateZoomAmount(abs(Constants.graphTop - y), lowerY, upperY, scrollAmount, 'y')

        lowerX = round(lowerX, Constants.graphBoundDecimals)
        upperX = round(upperX, Constants.graphBoundDecimals)
        lowerY = round(lowerY, Constants.graphBoundDecimals)
        upperY = round(upperY, Constants.graphBoundDecimals)

        GraphSettingsPanel.writeBounds(GraphSettingsPanel.instance, lowerX, upperX, lowerY, upperY)

    # Zooms out of the graph
    def zoomOut(self, x, y, scrollAmount):
        lowerX = Parser.evalFunction(Parser.instance, GraphSettingsPanel.lowerX)
        upperX = Parser.evalFunction(Parser.instance, GraphSettingsPanel.upperX)
        lowerY = Parser.evalFunction(Parser.instance, GraphSettingsPanel.lowerY)
        upperY = Parser.evalFunction(Parser.instance, GraphSettingsPanel.upperY)

        lowerX -= self.calculateZoomAmount(abs(Constants.graphLeft - x), lowerX, upperX, scrollAmount, 'x')
        upperX += self.calculateZoomAmount(abs(Constants.graphRight - x), lowerX, upperX, scrollAmount, 'x')
        lowerY -= self.calculateZoomAmount(abs(Constants.graphBottom - y), lowerY, upperY, scrollAmount, 'y')
        upperY += self.calculateZoomAmount(abs(Constants.graphTop - y), lowerY, upperY, scrollAmount, 'y')

        lowerX = round(lowerX, Constants.graphBoundDecimals)
        upperX = round(upperX, Constants.graphBoundDecimals)
        lowerY = round(lowerY, Constants.graphBoundDecimals)
        upperY = round(upperY, Constants.graphBoundDecimals)

        GraphSettingsPanel.writeBounds(GraphSettingsPanel.instance, lowerX, upperX, lowerY, upperY)
        
    def calculateZoomAmount(self, distance, lower, upper, scrollAmount, axis):

        if axis == 'x':
            graphSize = (Constants.graphRight - Constants.graphLeft)
        elif axis == 'y':
            graphSize = (Constants.graphTop - Constants.graphBottom) 
        else:
            print('check your syntax fool')

        zoomRatio = distance / graphSize * (upper - lower) 
        multiplier = Constants.graphZoomSpeed * scrollAmount

        return zoomRatio * multiplier


        

    
