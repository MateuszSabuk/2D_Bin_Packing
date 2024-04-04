import random
from enum import Enum

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
    


class Algorithms(Enum):
    '''
    Algorithms for the problem solving\\
    Provides an enum of the functions
    '''
    @staticmethod
    def __FFDH(boxes: list[Box], bin_widht) -> list[list[Box]]:
        boxes.sort(key=lambda box: box.h, reverse=True)  # Sort boxes by height in decreasing order

        strips: list[list[Box]] = []

        for box in boxes:
            placed = False
            for strip in strips:
                if placed:
                    break
                available_strip_space = bin_widht
                for placed_box in strip:
                    available_strip_space -= placed_box.w
                if available_strip_space > box.w: # Check if the box fits into the strip
                    strip.append(box)
                    placed = True
            if not placed: # Create new strip
                strips.append([box])

        return strips


    @staticmethod
    def __FFD(strips: list[list[Box]], bin_height):
        bins: list[list[list[Box]]] = []

        for strip in strips:
            placed = False
            for bin in bins:
                if placed:
                    break
                available_bin_space = bin_height
                for placed_strip in bin:
                    available_bin_space -= placed_strip[0].h
                if available_bin_space > strip[0].h:
                    bin.append(strip)
                    placed = True
            if not placed: # Create new bin
                bins.append([strip])    

        return bins
    
    @staticmethod
    def __unstrip_bins(bins_with_strips: list[list[list[Box]]]):
        '''Sets the positions of the boxes in each bin'''
        bins: list[list[Box]] = [[] for _ in bins_with_strips]

        for src_bin, dst_bin in zip(bins_with_strips, bins):
            y = 0
            for strip in src_bin:
                x = 0
                for bin in strip:
                    bin.x = x
                    bin.y = y
                    dst_bin.append(bin)
                    x += bin.w
                y += strip[0].h
        
        return bins

    
    @staticmethod
    def HFF(bin_size: tuple, boxes: list[Box]):
        # First phase: FFDH algorithm to create a strip packing
        strips = Algorithms.__FFDH(boxes, bin_widht=bin_size[0])
        # Second phase: FFD algorithm to create finite bin packing solutions
        bins_with_strips = Algorithms.__FFD(strips, bin_height=bin_size[1])
        return Algorithms.__unstrip_bins(bins_with_strips)

    @staticmethod
    def HNF(bin_size: tuple, boxes: list[Box]):
        '''Hybrid Next-Fit'''
        pass

    @staticmethod
    def HBF(bin_size: tuple, boxes: list[Box]):
        '''Hybrid Best-Fit'''
        pass

    @staticmethod
    def FC(bin_size: tuple, boxes: list[Box]):
        '''Floor-Ceiling'''
        pass

    @staticmethod
    def FNF(bin_size: tuple, boxes: list[Box]):
        '''Finite Next-Fit'''
        pass

    @staticmethod
    def FFF(bin_size: tuple, boxes: list[Box]):
        '''Finite First-Fit'''
        pass

    @staticmethod
    def FBL(bin_size: tuple, boxes: list[Box]):
        '''Finite Bottom-left'''
        pass

    @staticmethod
    def NBL(bin_size: tuple, boxes: list[Box]):
        '''Next Bottom-left'''
        pass
    
    @staticmethod
    def AD(bin_size: tuple, boxes: list[Box]):
        '''Alternate Directions'''
        pass

class BoxStackingProblem:
    '''Main problem solving class'''
    def __init__(self):
        self.boxes = []
        self.bin_size = None

    def generate_boxes(self, min_dim: int, max_dim: int, num_boxes: int):
        '''
        Initializes the self.boxes list
        ### Arguments
        - `min_dim` - min length of the boxes
        - `max_dim` - max length of the boxes
        - `num_boxes` - number of the boxes
        '''
        self.boxes = [] # Empty the array
        for _ in range(num_boxes):
            self.boxes.append(Box(tuple(random.randint(min_dim, max_dim) for _ in range(2))))

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
        print(algorithm(self.bin_size, self.boxes))


def main():
    bsp = BoxStackingProblem() # Create the main solver
    bsp.bin_size = (10, 10) # Set the size for the containers
    bsp.generate_boxes(1, 10, 5)  # Generate boxes (5 boxes with dimensions ranging from 1 to 10)
    
    # Try solving the problem
    try:
        bsp.solve(Algorithms.HFF)
    except ValidationError as err:
        print(f"Exception: {err}")


if __name__ == "__main__":
    main()