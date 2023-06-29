# Represents 
class Function:

    functionArray = ["x"]

    lowerLimit = [0]

    upperLimit = [1, 0]

    activeArray = functionArray

    @classmethod
    # Parses array into string
    def parseArray(cls, array):
        stringFunction = ''
        for o in array:
            if isinstance(o, str):
                stringFunction += o
            if isinstance(o, int):
                stringFunction += str(o)
        return stringFunction

    
