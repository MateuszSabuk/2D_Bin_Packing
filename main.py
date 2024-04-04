import random
from helpers import *
from algorithms import Algorithms

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