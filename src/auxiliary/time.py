import numpy as np

class Time:

    def __init__(self, t, tstep, tdir):

        # have print statements in each class
        self.t          = t # adjust by momentum p0 
        self.dt         = tstep 
        self.dir        = tdir
        self.max_itr    = int(t/tstep)
        self.snap       = np.arange(0,self.max_itr, int(t/tstep/40))    #       
        print('Time: T=%d, dt=%.3f, dir=%d, max_itr=%d \n' 
             %(t, tstep, tdir, self.max_itr))
