from enum import Enum
from helpers import Box

class Algorithms:
    '''
    Algorithms for the problem solving\\
    Provides an enum of the functions
    '''

    # PRIVATE HELPER FUNCTIONS
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

        return bins


    @staticmethod
    def __NFDH(boxes: list[Box], bin_widht) -> list[list[Box]]:
        boxes.sort(key=lambda box: box.h, reverse=True)  # Sort boxes by height in decreasing order

        strips: list[list[Box]] = [[]]

        i = 0
        for box in boxes:
            available_strip_space = bin_widht
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
        '''Hybrid First-Fit'''
        # First phase: FFDH algorithm to create a strip packing
        strips = Algorithms.__FFDH(boxes, bin_widht=bin_size[0])
        # Second phase: FFD algorithm to create finite bin packing solutions
        bins_with_strips = Algorithms.__FFD(strips, bin_height=bin_size[1])
        return Algorithms.__unstrip_bins(bins_with_strips)

    @staticmethod
    def HNF(bin_size: tuple, boxes: list[Box]):
        '''Hybrid Next-Fit'''
        # First phase: NFDH algorithm to create a strip packing
        strips = Algorithms.__NFDH(boxes, bin_widht=bin_size[0])
        # Second phase: NFD algorithm to create finite bin packing solutions
        bins_with_strips = Algorithms.__NFD(strips, bin_height=bin_size[1])
        return Algorithms.__unstrip_bins(bins_with_strips)

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
