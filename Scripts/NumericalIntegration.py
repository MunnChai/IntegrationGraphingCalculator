import Constants
import math

n = Constants.SIMPSONS_INTERVALS 

def leftRiemannSumCalc(b, a, stringFunction):
    deltaX = ((b - a) / n)
    currentX = a
    previousSum = 0
    for i in range(n):
        currentY = evalFunction(currentX, stringFunction) 
        previousSum += currentY
        currentX += deltaX
    return previousSum * deltaX

def rightRiemannSumCalc(b, a, stringFunction):
    deltaX = ((b - a) / n)
    currentX = a + deltaX
    previousSum = 0

    for i in range(n):
        currentY = evalFunction(currentX, stringFunction) 
        previousSum += currentY
        currentX += deltaX

    return previousSum * deltaX

def simpsonsRuleCalc(b, a, stringFunction):
    
    deltaX = ((b - a) / n)
    currentX = a
    previousSum = 0

    for i in range(n + 1):

        if i == 0:
            currentY = evalFunction(currentX, stringFunction)
            even = 1
        elif i == n:
            currentY = evalFunction(currentX, stringFunction)
        elif even == 1:
            currentY = 4 * evalFunction(currentX, stringFunction)
            even = 0
        else:
            currentY = 2 * evalFunction(currentX, stringFunction)
            even = 1
    
        previousSum += currentY
        currentX += deltaX

    return (previousSum * deltaX) / 3

# Evaluates function
def evalFunction(x, stringFunction):
    try:
        return eval(stringFunction)
    except ZeroDivisionError:
        raise ZeroDivisionError()
    except ValueError:
        raise ValueError()