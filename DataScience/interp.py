import numpy as np
import unittest

class LinearInterpolator:
    def __init__(self,x,y):
        
        if any(x1 - x0 < 0 for x0, x1 in zip(x, x[1:])):
            print("Input series non ascending, sorting for you...")
            x = np.sort(x)
        self.x_in = x
        self.y_in = y
        # Zip object of with each index
        # containing x interval with corresponding
        # y values. Create by zipping z, y, and
        # shifted versions of themselves.
        # intervals has len(x)-1 indices with 4 values
        # in each corresponding to
        # x_n, x_n-1, y_n, y_n-1
        intervals = zip(x, x[1:], y, y[1:])
        self.slopes = [(y2-y1)/(x2-x1) for x1, x2, y1, y2 in intervals]
        
    def __call__(self,x):
        
        if (not(self.x_in[0] <= x <= self.x_in[-1])):
            print("Input out of interpolation range, returned NaN.")
            return np.nan
        if x == self.x_in[-1]:
            return self.y_in[-1]
        # Get closest leftward x_in index in reference to value x.
        # (this is equivalent to bisect.bisect_right)
        r,l = 0, len(self.x_in)-1
        while r < l:
            if (self.x_in[l] < x):
                i = l 
            elif (self.x_in[r] > x):
                i = r - 1
            r += 1
            l -= 1

        return self.y_in[i] + self.slopes[i] * (x - self.x_in[i])

    
