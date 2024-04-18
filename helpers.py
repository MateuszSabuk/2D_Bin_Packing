import random
import copy
import re

# Exceptions
class ValidationError(Exception):
    '''
    Error thrown when attempting to solve the problem
    ### Values
    - `.message` - message of the error
    - `.val` - is a specific error code string
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
    def __init__(self,size: tuple):
        if any(x <= 0 for x in size):
            raise ValidationError("Box dimensions must be bigger than zero", "box_size")
        self.w, self.h = size
        self.x, self.y = None, None

    def __repr__(self):
        return f"Box(Pos({self.x}, {self.y}), Size{self.w, self.h})\n"

class BoxStackingSolver:
    '''Main problem solving class'''
    def __init__(self):
        self.boxes = []
        self.bin_size = None

    def generate_boxes(self, min_w: int, max_w: int, min_h: int, max_h: int, num_boxes: int) -> None:
        '''
        Initializes the self.boxes list
        ### Arguments
        - `min_w` - min width of the boxes
        - `max_w` - max width of the boxes
        - `min_h` - min height of the boxes
        - `max_h` - max height of the boxes
        - `num_boxes` - number of the boxes
        '''
        if min_w > max_w or min_h > max_h or min_w <= 0 or min_h <= 0:
            raise ValidationError("Wrong generation dimensions", "gen_dim")

        self.boxes = [] # Empty the array
        for _ in range(num_boxes):
            self.boxes.append(Box((random.randint(min_w, min(max_w, self.bin_size[0])),
                                    random.randint(min_h, min(max_h, self.bin_size[1])))))

    def solve(self, algorithm) -> list[Box]:
        '''
        Run the solver using selected algorithm
        ### Arguments
        - `algorithm` - reference to a method of Algorithms Class
        '''
        # Validate state of the variables
        if self.bin_size == None:
            raise ValidationError("Bin size not initialized", "bin_size")
        if not self.boxes:
            raise ValidationError("List of boxes not initialized", "boxes")
        if not callable(algorithm):
            raise ValidationError("Wrong algorithm", "algorithm")

        # Run selected algorithm on the chosen data
        return algorithm(self.bin_size, copy.deepcopy(self.boxes))
    
    def get_boxes_text(self) -> str:
        '''Returns the string with box dimensions'''
        arr = [f"{box.w}x{box.h}" for box in self.boxes]
        return "\n".join(arr)
    
    def update_boxes_from_txt(self, text: str) -> None:
        '''Updates the state of solver boxes list'''
        new_boxes = []
        for i, line in enumerate(text.splitlines()):
            match = re.match(r'^(\d+)x(\d+)$', line)
            if match:
                width, height = map(int, match.groups())
                if width > self.bin_size[0] or height > self.bin_size[1]:
                    raise ValidationError( f"To big box at line {i+1}: {line}", f"box_size:{i}")
                try:
                    new_boxes.append(Box((width, height)))
                except ValidationError as e:
                    if e.val == "box_size":
                        raise ValidationError(f"{e} at line {i+1}: {line}", f"{e.val}:{i}")
            else:
                raise ValidationError( f"Error while parsing boxes input at line {i+1}: {line}", f"bad_line:{i}")
        self.boxes = new_boxes

    def update_bin_size(self, text: str) -> None:
        match = re.match(r'^([1-9]\d*)x([1-9]\d*)$', text)
        if match:
            w, h = map(int, match.groups())
            self.bin_size = (w, h)
        else:
            raise ValidationError( f"Error while parsing bin size", f"bin_size_parsing")
        