import Constants
import math

class Parser:

    instance = None

    def __init__(self):
        Parser.instance = self

    # Evaluates given string function
    def evalFunction(self, array):
        return eval(self.parseFunction(array))

    # Parses array of inputs into a string expression with proper python syntax
    def parseFunction(self, array):
        parsed = ''

        currentPos = 0
        for object in array:
            if object in Constants.NUMBERS:
                parsed += self.parseNumber(object, currentPos, array)
            elif object in Constants.MATH_OPS:
                parsed += self.parseMathOperation(object, currentPos, array)
            elif object in Constants.PARENTHESES:
                parsed += self.parseParenthesis(object, currentPos, array)
            elif object in Constants.MATH_CONSTANTS:
                parsed += self.parseConstant(object, currentPos, array)
            elif object in Constants.SPECIAL_FUNCTIONS:
                parsed += self.parseSpecOp(object, currentPos, array)

            currentPos += 1

        return parsed
        
    # Returns a parsed number
    def parseNumber(self, number, currentPos, array):
        
        functionLength = len(array)
        if functionLength == 0 or currentPos == 0:
            return str(number)
        elif array[currentPos - 1] in Constants.MATH_CONSTANTS or array[currentPos - 1] == ')':
            return "*" + str(number)
        else:
            return str(number)
        
    # Returns a parsed math operation 
    def parseMathOperation(self, operation, currentPos, array):
        if operation == '^':
            return '**' # NOTE: this may be a point of error
        return operation
    
    # Returns a parsed parenthesis
    def parseParenthesis(self, parenthesis, currentPos, array):

        functionLength = len(array)
        if functionLength == 0 or currentPos == 0:
            return parenthesis
        elif (array[currentPos - 1] == ")" or array[currentPos - 1] in Constants.NUMBERS 
              or array[currentPos - 1] in Constants.MATH_CONSTANTS) and parenthesis == '(':
            return "*" + parenthesis
        elif array[currentPos - 1] in Constants.NUMBERS and parenthesis == '(':
            return "*" + parenthesis
        else:
            return parenthesis
        
    # Returns a parsed mathematical constant 
    def parseConstant(self, constant, currentPos, array):

        functionLength = len(array)
        if constant == 'e':
            if functionLength == 0 or currentPos == 0:
                return str(math.e)
            elif array[currentPos - 1] in Constants.NUMBERS or array[currentPos - 1] in Constants.MATH_CONSTANTS or array[currentPos - 1] == ')':
                return "*" + str(math.e)
            else:
                return str(math.e)
        elif constant == 'π':
            if functionLength == 0 or currentPos == 0:
                return str(math.pi)
            elif array[currentPos - 1] in Constants.NUMBERS or array[currentPos - 1] in Constants.MATH_CONSTANTS or array[currentPos - 1] == ')':
                return "*" + str(math.pi)
            else:
                return str(math.pi)
        elif constant == 'x':
            if functionLength == 0 or currentPos == 0:
                return 'x'
            elif array[currentPos - 1] in Constants.NUMBERS or array[currentPos - 1] in Constants.MATH_CONSTANTS or array[currentPos - 1] == ')':
                return '*x'
            else:
                return 'x'
            
    # Returns a special function parsed
    def parseSpecOp(self, specialOperation, currentPos, array):

        functionLength = len(array)
        
        if specialOperation == 'ln(':
            if functionLength == 0 or currentPos == 0:
                return 'math.log('
            elif array[currentPos - 1] in Constants.NUMBERS or array[currentPos - 1] in Constants.MATH_CONSTANTS or array[currentPos - 1] == ')':
                return '*math.log('
            else:
                return 'math.log('
        else:
            if functionLength == 0 or currentPos == 0:
                return 'math.' + specialOperation
            elif array[currentPos - 1] in Constants.NUMBERS or array[currentPos - 1] in Constants.MATH_CONSTANTS or array[currentPos - 1] == ')':
                return '*math.' + specialOperation
            else:
                return 'math.' + specialOperation