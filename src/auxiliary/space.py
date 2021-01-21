import numpy as np

class Space:
    """
    ddf
    """
    def __init__(self, n, xleft, eps, xright = None):
       
        # make methods private
        self.n = n # number intervals
        self.xleft = xleft
        self.xright = xright if xright != None else xleft

        self.xgrid, self.dx = np.linspace(
                xleft, xright, n, retstep=True)
        self.dp = 2*np.pi*eps/(n*self.dx)
        self.pgrid = ((np.arange(0, n, 1) - n/2)*self.dp)
        
        print('Grid points=%d, xl = %d, xr = %d' %(n, xleft, xright))
