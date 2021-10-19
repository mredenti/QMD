
def SA(p, tau, delta, eps):

    k = np.sqrt(p**2 + 4 * delta)

    return np.exp(- tau / delta / eps * np.abs(k - p))


def SA1(p, alpha, delta, eps): # check this implementation against PDF
    
    tau = np.pi * delta**2 / 2 / alpha 

    return SA(p, tau, delta, eps)


def SA2(p, tau, delta, eps):

    return np.exp(- tau / delta / eps * np.abs(2*delta / p))

def SA12(p, alpha, delta, eps):

    tau = np.pi * delta**2 / 2 / alpha 
    
    return SA2(p, tau, delta, eps) # check this as I am not sure

def LZa(p, delta, eps, pot, x_c):

    k = np.sqrt(p**2 * (pot.Zd(x_c)**2 + pot.v12d(x_c)**2)) 
            #+ \
    k = p**2 * (pot.Z(x_c) * pot.Zdd(x_c) + pot.v12(x_c)*pot.v12dd(x_c))

    print("Belayev rate k = %.17g \n" % k)

    return np.exp(- np.pi / eps * delta**2 / k)

# when verifying the mass transfer (rate of chemical reactions)
# we are assuming that alpha, delta, tau have been computed 
# accurately and reliably
if __name__ == '__main__':

    import sys
    sys.path.insert(0, '../..')
    from potentials.potential import Potential
    from potentials.examples.nai import NaI
    from auxiliary.units import Units
    import numpy as np
    

    A1 = 0.813 * Units.eVtoH 
    BETA1 = 4.08 / Units.Atob  
    R0 = 2.67  * Units.Atob
    A2 = 2760 * Units.eVtoH
    B2 = 2.398 * Units.eVtoH**(1/8) * Units.Atob
    C2 = 11.3 * Units.eVtoH * Units.Atob**(6)
    LAMBDAP = 0.408 * Units.Atob**3
    LAMBDAM = 6.431 * Units.Atob**3 
    RO = 0.3489 * Units.Atob
    DELTAE = 2.075 * Units.eVtoH
    A12 = 0.055 * Units.eVtoH
    BETA12 = 0.6931 / Units.Atob**(2)
    RX = 6.93 * Units.Atob
    pot = NaI(A1, BETA1, R0, A2, B2, RO, LAMBDAP, LAMBDAM, C2, DELTAE, A12, BETA12, RX, 'up')

    tau = 0.0023923147 
    alpha = 0.002669794983146837
    delta = 0.002010562925688143
    p = 0.24843052119644576
    eps = 0.0019227199721312948 # check! different from Ben's code
    x_c = 13.27801894097567 
    
    print("Mass transfer for mean momentun particle")
    print("SA =", SA(p, tau, delta, eps), "\n")
    print("SA1 =", SA1(p, alpha, delta, eps), "\n")
    print("SA2 =", SA2(p, tau, delta, eps), "\n")
    print("SA12 =", SA12(p, alpha, delta, eps), "\n")
    print("LZa =", LZa(p, delta, eps, pot, x_c), "\n")

