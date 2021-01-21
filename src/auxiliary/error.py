import numpy as np


def l2norm(f,dx):

    return np.sqrt(np.sum(abs(f)**2)*dx)

def l2relerror(f,g,dx):
    
    # can definitely define it in other ways
    return l2norm(f - g, dx)/l2norm(g, dx)
