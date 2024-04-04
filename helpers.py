# Exceptions
class ValidationError(Exception):
    '''
    Error thrown when attempting to solve the problem
    ### Values
    - `.message` - message of the error
    - `.val` - is one of the strings:
        - "bin_size"
        - "boxes"
        - "algorithm"
    '''
    def __init__(self, message, val):
        super().__init__(message)
        self.val = val

class Box:
    '''
    Single box Class
    ### Values
    - `.w and .h` - size of the box
    - `.x and .y` - position of the box\\
    if equal to None then the box is not positioned
    '''
    def __init__(self,size):
        self.w, self.h = size
        self.x, self.y = None, None

    def __repr__(self):
        return f"Box(Pos({self.x}, {self.y}), Size{self.w, self.h})\n"
