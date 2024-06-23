import math
from helpers import Box

class Algorithms:
    '''
    Algorithms for the problem solving\\
    Provides multiple functions:
    - get_implemented_names()

    - Two-phase algorithms
        - HFF - Hybrid First-Fit
        - HNF - Hybrid Next-Fit
        - HBF - Hybrid Best-Fit
        - FC - Floor-Ceiling
    - One-phase algorithms
        - FNF - Finite Next-Fit
        - FFF - Finite First-Fit
        - FBL - Finite Bottom-left
        - NBL - Next Bottom-left
        - AD - Alternate Directions
    '''
    @staticmethod
    def get_implemented_names():
        return ["HFF", "HNF", "HBF", "FBL", "NBL", "AD"]
    
    @staticmethod
    def HFF(bin_size: tuple, boxes: list[Box]) -> list[list[Box]]:
        '''Hybrid First-Fit'''
        # First phase: FFDH algorithm to create a strip packing
        strips = Algorithms.__FFDH(boxes, bin_width=bin_size[0])
        # Second phase: FFD algorithm to create finite bin packing solutions
        bins_with_strips = Algorithms.__FFD(strips, bin_height=bin_size[1])
        return Algorithms.__unstrip_bins(bins_with_strips)

    @staticmethod
    def HNF(bin_size: tuple, boxes: list[Box]) -> list[list[Box]]:
        '''Hybrid Next-Fit'''
        # First phase: NFDH algorithm to create a strip packing
        strips = Algorithms.__NFDH(boxes, bin_width=bin_size[0])
        # Second phase: NFD algorithm to create finite bin packing solutions
        bins_with_strips = Algorithms.__NFD(strips, bin_height=bin_size[1])
        return Algorithms.__unstrip_bins(bins_with_strips)

    @staticmethod
    def HBF(bin_size: tuple, boxes: list[Box]) -> list[list[Box]]:
        '''Hybrid Best-Fit'''
        # First phase: BFDH algorithm to create a strip packing
        strips = Algorithms.__BFDH(boxes, bin_width=bin_size[0])
        # Second phase: BFD algorithm to create finite bin packing solutions
        bins_with_strips = Algorithms.__BFD(strips, bin_height=bin_size[1])
        return Algorithms.__unstrip_bins(bins_with_strips)

    @staticmethod
    def FC(bin_size: tuple, boxes: list[Box]):
        '''Floor-Ceiling'''
        pass

    @staticmethod
    def FBL(bin_size: tuple, boxes: list[Box]) -> list[list[Box]]:
        '''Finite Bottom-left'''
        boxes.sort(key=lambda box: box.w, reverse=True)  # Sort boxes by width in decreasing order
            
        bins = []

        def fits_in_bin(bin, box):
            for b in bin:
                if not (b.x + b.w <= box.x or b.x >= box.x + box.w or b.y + b.h <= box.y or b.y >= box.y + box.h):
                    return False
            return True

        def find_position(bin, box):
            max_x, max_y = bin_size
            for y in range(max_y):
                for x in range(max_x):
                    box.x, box.y = x, y
                    if x + box.w <= max_x and y + box.h <= max_y and fits_in_bin(bin, box):
                        return True
            return False

        for box in boxes:
            placed = False
            for bin in bins:
                if find_position(bin, box):
                    bin.append(box)
                    placed = True
                    break
            if not placed:
                new_bin = []
                if find_position(new_bin, box):
                    new_bin.append(box)
                    bins.append(new_bin)
        bins = [bin for bin in bins if bin]
        return bins



    @staticmethod
    def NBL(bin_size: tuple, boxes: list[Box]) -> list[list[Box]]:
        '''Next Bottom-left'''
        boxes.sort(key=lambda box: box.w, reverse=True)  # Sort boxes by width in decreasing order

        bins = []

        def fits_in_bin(bin, box):
            for b in bin:
                if not (b.x + b.w <= box.x or b.x >= box.x + box.w or b.y + b.h <= box.y or b.y >= box.y + box.h):
                    return False
            return True

        def find_position(bin, box):
            max_x, max_y = bin_size
            for y in range(max_y):
                for x in range(max_x):
                    box.x, box.y = x, y
                    if x + box.w <= max_x and y + box.h <= max_y and fits_in_bin(bin, box):
                        return True
            return False

        current_bin = []

        for box in boxes:
            if not find_position(current_bin, box):
                bins.append(current_bin)
                current_bin = []
                find_position(current_bin, box)
            current_bin.append(box)

        if current_bin:
            bins.append(current_bin)
        bins = [bin for bin in bins if bin]
        return bins
    
    @staticmethod
    def AD(bin_size: tuple, boxes: list[Box]):
        '''Alternate Directions'''
        total_area = sum(box.w * box.h for box in boxes)
        bin_area = bin_size[0] * bin_size[1]
        L = math.ceil(total_area / bin_area)
        bins = [[] for _ in range(L)]

        def fits_in_bin(bin, box):
            for b in bin:
                if not (b.x + b.w <= box.x or b.x >= box.x + box.w or b.y + b.h <= box.y or b.y >= box.y + box.h):
                    return False
            return True

        def find_position(bin, box, direction='bottom'):
            max_x, max_y = bin_size
            if direction == 'bottom':
                for y in range(max_y):
                    for x in range(max_x):
                        box.x, box.y = x, y
                        if x + box.w <= max_x and y + box.h <= max_y and fits_in_bin(bin, box):
                            return True
            elif direction == 'left_to_right':
                for x in range(max_x):
                    for y in range(max_y):
                        box.x, box.y = x, y
                        if x + box.w <= max_x and y + box.h <= max_y and fits_in_bin(bin, box):
                            return True
            elif direction == 'right_to_left':
                for x in range(max_x - 1, -1, -1):
                    for y in range(max_y):
                        box.x, box.y = x, y
                        if x + box.w <= max_x and y + box.h <= max_y and fits_in_bin(bin, box):
                            return True
            return False

        # Sort boxes by decreasing height
        boxes.sort(key=lambda box: box.h, reverse=True)

        # Pack first L bins using BFD
        packed = []
        for box in boxes:
            placed = False
            for bin in bins:
                if find_position(bin, box, direction='bottom'):
                    bin.append(box)
                    packed.append(box)
                    placed = True
                    break
            if not placed:
                break

        remaining_boxes = [box for box in boxes if box not in packed]

        # Pack remaining items in alternate directions
        direction = 'left_to_right'
        current_bin_index = 0
        while remaining_boxes:
            current_box = remaining_boxes.pop(0)
            placed = False
            while current_bin_index < len(bins):
                if find_position(bins[current_bin_index], current_box, direction=direction):
                    bins[current_bin_index].append(current_box)
                    placed = True
                    break
                current_bin_index += 1

            if not placed:
                current_bin_index = len(bins)
                new_bin = []
                bins.append(new_bin)
                find_position(new_bin, current_box, direction=direction)
                new_bin.append(current_box)

            direction = 'right_to_left' if direction == 'left_to_right' else 'left_to_right'

        return bins


    # ######################################################
    # ############# PRIVATE HELPER FUNCTIONS ###############
    # ######################################################
    @staticmethod
    def __FFDH(boxes: list[Box], bin_width) -> list[list[Box]]:
        boxes.sort(key=lambda box: box.h, reverse=True)  # Sort boxes by height in decreasing order

        strips: list[list[Box]] = []

        for box in boxes:
            placed = False
            for strip in strips:
                if placed:
                    break
                available_strip_space = bin_width
                for placed_box in strip:
                    available_strip_space -= placed_box.w
                if available_strip_space >= box.w: # Check if the box fits into the strip
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
                if available_bin_space >= strip[0].h:
                    bin.append(strip)
                    placed = True
            if not placed: # Create new bin
                bins.append([strip])
        bins = [bin for bin in bins if bin]
        return bins


    @staticmethod
    def __NFDH(boxes: list[Box], bin_width) -> list[list[Box]]:
        boxes.sort(key=lambda box: box.h, reverse=True)  # Sort boxes by height in decreasing order

        strips: list[list[Box]] = [[]]

        i = 0
        for box in boxes:
            available_strip_space = bin_width
            for placed_box in strips[i]:
                available_strip_space -= placed_box.w
            if available_strip_space >= box.w: # Check if the box fits into the strip
                strips[i].append(box)
            else: # Create new strip
                strips.append([box])
                i += 1

        return strips

    @staticmethod
    def __NFD(strips: list[list[Box]], bin_height):
        bins: list[list[list[Box]]] = [[]]

        i = 0
        for strip in strips:
            available_bin_space = bin_height
            for placed_strip in bins[i]:
                available_bin_space -= placed_strip[0].h
            if available_bin_space >= strip[0].h:
                bins[i].append(strip)
            else:
                bins.append([strip])
                i += 1
        bins = [bin for bin in bins if bin]
        return bins
    

    @staticmethod
    def __BFDH(boxes: list[Box], bin_width) -> list[list[Box]]:
        # Sort boxes by height in decreasing order
        boxes.sort(key=lambda box: box.h, reverse=True)

        strips: list[list[Box]] = []
        strip_left_space = []

        for box in boxes:
            best_strip_index = None
            min_space_left = float('inf')

            for i, space in enumerate(strip_left_space):
                # Check if this bin has the least space left that can ffit the strip
                if space >= box.w and space < min_space_left:
                    min_space_left = space
                    best_strip_index = i

            if best_strip_index is not None:
                # Place the strip in the bin with the smallest space left
                strips[best_strip_index].append(box)
                strip_left_space[best_strip_index] -= box.w
            else:
                # Create a new strip
                new_strip = [box]
                strips.append(new_strip)
                strip_left_space.append(bin_width - box.w)

        return strips

    @staticmethod
    def __BFD(strips: list[list[Box]], bin_height):
        bins: list[list[list[Box]]] = [[]]

        bin_left_space = [bin_height]

        for strip in strips:
            best_bin_index = None
            min_space_left = float('inf')

            for i, space in enumerate(bin_left_space):
                # Check if this bin has the least space left that can ffit the strip
                if space >= strip[0].h and space < min_space_left:
                    min_space_left = space
                    best_bin_index = i

            if best_bin_index is not None:
                # Place the strip in the bin with the smallest space left
                bins[best_bin_index].append(strip)
                bin_left_space[best_bin_index] -= strip[0].h
            else:
                # Create a new bin
                new_bin = [strip]
                bins.append(new_bin)
                bin_left_space.append(bin_height - strip[0].h)

        # Remove empty bins
        bins = [bin for bin in bins if bin]

        return bins

    @staticmethod
    def __unstrip_bins(bins_with_strips: list[list[list[Box]]]) -> list[list[Box]]:
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