import numpy as np

class Time:

    def __init__(self, t, tstep, tdir):

        # have print statements in each class
        self.t          = t # adjust by momentum p0 
        self.dt         = tstep 
        self.dir        = tdir
        self.max_itr    = int(t/tstep)
        self.snap       = np.arange(1,self.max_itr + 6, int(self.max_itr/200))         
        print('Time: T=%d, dt=%.3f, dir=%d, max_itr=%d \n' 
             %(t, tstep, tdir, self.max_itr))
