import sys
sys.path.insert(0, '../..')
import numpy as np
from potentials.potential import Potential
from auxiliary.units import Units
# ------------- DIABATIC POTENTIALS ------------------
class NaI(Potential):

    def __init__(self, a1, beta1, r0,
                        a2, b2, ro, lambdap, lambdam, c2, deltae,
                        a12, beta12, rx, level=None):
        super().__init__(level)
        
        # ADD REFERENCE TO PAPER
        self.a1 = a1
        self.beta1 = beta1
        self.r0 = r0
        self.a2 = a2
        self.b2 = b2
        self.ro = ro
        self.lambdap = lambdap
        self.lambdam = lambdam
        self.c2 = c2
        self.deltae = deltae
        self.a12 = a12
        self.beta12 = beta12
        self.rx = rx
        self.name = 'NaI'

    # ----------------- DIABATIC POTENTIAL --------------

    def v11(self, x):

        return self.a1 * np.exp(- self.beta1 * (x - self.r0))
    
    def v11d(self, x):

        return - self.beta1 * self.v11(x)

    def v11dd(self, x):

        return self.beta1**2 * self.v11(x)
    
    def v22(self, x):
        # not convinced this will make sense
        return ( self.a2 + ( self.b2 / x )**8 ) * np.exp( - x / self.ro ) + \
                - Units.e / x - Units.e * (self.lambdap + self.lambdam) / (2*x**4) + \
                - self.c2 / x**6 - 2 * Units.e * self.lambdap * self.lambdam / x**7 + self.deltae   

    def v22d(self, x):
        # not convinced this will make sense
        return - 8 * self.b2**8 / x**9 * np.exp(- x / self.ro ) \
                - 1 / self.ro * ( self.a2 + ( self.b2 / x )**8 ) * np.exp( - x / self.ro ) + \
                + Units.e / x**2 + 2 * Units.e * (self.lambdap + self.lambdam) / x**5 + \
                + 6 * self.c2 / x**7 + 14 * Units.e * self.lambdap * self.lambdam / x**8   
    
    def v22dd(self, x):
        # not convinced this will make sense
        return 72 * self.b2**8 / x**10 * np.exp( - x / self.ro ) \
                + 1 / self.ro**2 * ( self.a2 + ( self.b2 / x )**8 ) * np.exp( - x / self.ro ) + \
                + 16 * self.b2**8 / self.ro / x**9 * np.exp( - x / self.ro ) + \
                - 2 * Units.e / x**3 - 10 * Units.e * (self.lambdap + self.lambdam) / x**6 + \
                - 42 * self.c2 / x**8 - 112 * Units.e * self.lambdap * self.lambdam / x**9  
    
    def v12(self, x):

        return self.a12 * np.exp(- self.beta12 * (x - self.rx)**2)  

    def v12d(self, x):

        return - 2 * self.beta12 * (x - self.rx) * self.v12(x) 
    
    def v12dd(self, x):

        return (-2 * self.beta12 + 4 * self.beta12**2 * (x - self.rx)**2 ) * self.v12(x)
    
    def v21(self, x):

        return self.v12(x)  

    # FROM HERE ON IS WRONG AND NEEDS TO BE FIXED #

    def get_tau(self, x):
        """Check numerically
        rather than x you probably want to specify 
        a tolerance"""
        """
        import pylab
        pylab.imshow(np.abs(self.rho_complex_arg(X,Y)), extent = [13 - 2, 13 + 2, -2, 2])
        pylab.colorbar()
        pylab.xlabel('Re')
        pylab.ylabel('Im')
        pylab.title(r'$|\rho(z)|$')
        pylab.show()
        """
        # find complex conjugate roots 
        from scipy.optimize import fsolve 
        root = fsolve(self.rho_complex_arg, [13.25, 0.71]) # secant method by default?
        # location of avoided crossing
        x_c = x[np.argmin(self.rho(x))] # location avoided crossing - 1d -real 
        dx =  10**(-6) # want to evaluate rho along a straight line - alternatively what if I pick the Manhattan route?
        dy = root[1] / abs(root[0] - x_c)  * dx
        dz = dx + 1j * dy
        x = np.arange(x_c, root[0], - dx)
        y = np.arange(0, root[1], dy)
        print(self.rho_complex_arg2(root[0], root[1]))
        sum_ = 0
        for i in range(len(x)):
            sum_ += self.rho_complex_arg2(x[i], y[i])
        print('tau_c = %.10f + i %.10f' % (2 * (sum_ * dz).real, 2 * (sum_ * dz).imag))
        return 2 * sum_ * dz 

    def get_xc(self, x):
        
        ixx_c = np.argmin(self.rho(x))

        return x[ixx_c]

    def get_alpha(self, x):
        
        rhodd = (self.Zd(x)**2 + self.Z(x)*self.Zdd(x) + self.v12d(x)**2 + self.v12(x) * self.v12dd(x)) / self.rho(x) - \
                (self.Z(x) * self.Zd(x) + self.v12(x) * self.v12d(x))**2 / self.rho(x)**3
        ixx_c = np.argmin(self.rho(x))
        print("x_c = %.4f" % x[ixx_c])
        delta = self.rho(x[ixx_c])
        print("delta = %.4f" % delta)
        alpha = np.sqrt(delta * rhodd[ixx_c])
        print("alpha = %.17g" % alpha)
        return alpha
        
# ------------- ADIABATIC POTENTIALS ------------------

    def V1(self, x): 
        """Check gradient"""    
        sign = 1 if self.level == 'up' else -1
        s = np.tanh(x)
            
        return sign * self.alpha**2 * s *(1 - s**2)/self.rho(x)
    
    def V2(self, x): 
        
        a = self.alpha
        s = np.tanh(x)
        sign = 1 if self.level == 'up' else -1
            
        return sign *( (-2) * a**2 * s**2 * (1 - s**2)/self.rho(x) \
                      + a**2 * (1 - s**2)**2/self.rho(x) \
                      - a**4 * s**2 * (1 - s**2)**2/self.rho(x)**3)
    

if __name__ == "__main__":
    # note I am already converting to 
    # atomic units
    #A1, BETA1, R0 = 0.813, 4.08, 2.67  
    A1 = 0.813 * Units.eVtoH 
    BETA1 = 4.08 / Units.Atob # ???????? 
    R0 = 2.67  * Units.Atob
    #A2, B2, C2, LAMBDAP, LAMBDAM, RO, DELTAE = 2760, 2.398, 11.3, 0.408, 6.431, 0.3489, 2.075
    A2 = 2760 * Units.eVtoH
    B2 = 2.398 * Units.eVtoH**(1/8) * Units.Atob
    C2 = 11.3 * Units.eVtoH * Units.Atob**(6)
    LAMBDAP = 0.408 * Units.Atob**3
    LAMBDAM = 6.431 * Units.Atob**3 
    RO = 0.3489 * Units.Atob
    DELTAE = 2.075 * Units.eVtoH
    #A12, BETA12, RX = 0.055, 0.6931, 6.93
    A12 = 0.055 * Units.eVtoH
    BETA12 = 0.6931 / Units.Atob**(2)
    RX = 6.93 * Units.Atob
    pot = NaI(A1, BETA1, R0, A2, B2, RO, LAMBDAP, LAMBDAM, C2, DELTAE, A12, BETA12, RX, 'up')
    x = np.linspace(2,16,2**14) * Units.Atob 
    pot.get_tau(x)
    print(pot.get_alpha(x))
    mean_p = np.sqrt(2 * (pot.V(5) - pot.V(pot.get_xc(x))))
    print("The mean momentum at the crossing is ", mean_p, "\n")
    b = 5
    print("v_z ", pot.Z(b), "\n")
    print("v_zd ", pot.Zd(b), "\n")
    print("v_zdd ", pot.Zdd(b), "\n")
    print("v_v12 ", pot.v12(b), "\n")
    print("v_v12d ", pot.v12d(b), "\n")
    print("v_v12dd ", pot.v12dd(b), "\n")
    print("v_trace ", (pot.v11(b) + pot.v22(b))/2, "\n")
    #print(x[np.argmin(pot.rho(x))]) # delta - half the gap?
    #print(pot.rho(x)[np.argmin(pot.rho(x))]) # delta - half the gap?
    """
    print(A1, BETA1, R0, "\n")
    print(A2, B2, C2, LAMBDAP, LAMBDAM, RO, DELTAE, "\n")
    print(A12, BETA12, RX)
    print("\n", Units.e)
    """
    """
    import matplotlib.pyplot as plt 
    #plt.plot(x, (pot.rho(x) + pot.d(x)) / Units.eVtoH )
    #plt.plot(x, (- pot.rho(x) + pot.d(x)) / Units.eVtoH )
    plt.plot(x, pot.rho(x) + pot.d(x))
    plt.plot(x, - pot.rho(x) + pot.d(x))
    plt.show()
    plt.close('all')
    """
    
    #print(np.min(pot.rho(x)))
    #print(x[np.argmin(pot.rho(x))])

    """
    plt.title('Adiabatic surfaces (a.u.)')
    plt.plot(space.xgrid, 
            (potential.rho(space.xgrid) + potential.d(space.xgrid)) )
    plt.plot(space.xgrid , 
            (- potential.rho(space.xgrid) + potential.d(space.xgrid)) )
    plt.ylabel(r'$Potential$')
    plt.xlabel(r'$x$')
    #plt.ylabel(r'$Potential [eV]$')
    #plt.xlabel(r'$x [\mathring{A}]$')
    plt.grid()
    plt.savefig('nai_adiabatic_surfaces_atomic_units.pdf')
    """

