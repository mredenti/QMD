import numpy as np

def get_transition(psi_hat, space, eps, tau, delta, gamma):
    """
    Returns transmitted wavepacket
    See [paper reference]
    """
    eta2 = lambda p: p**2 - 4*delta
    p = space.pgrid
    sign_p = np.sign(p)
    
    psihat_crossing = np.zeros(len(p), dtype='complex_')

    for i in range(len(psihat_crossing)):
        if eta2(p[i]) > 0:
            eta = sign_p[i] * np.sqrt(eta2(p[i]))
            psihat_crossing[i] = np.sin(np.pi * gamma/2) * (p[i] + eta)/(abs(eta)) * \
                    np.exp(- tau / eps * np.abs(p[i] - eta)) * \
                    psi_hat[int((eta - p[0]) /space.dp)]
    
    return psihat_crossing
    
def get_correction(psi_hat, space, eps, tau, delta, gamma, P0):
    """
    Returns adjusted wavepacket post avoided crossing
    See [paper reference]
    """
    import scipy.special as sc
    
    def get_integral(eps, alpha, qc, p):
        value = eps/qc * (p - alpha) + (p + alpha) * 2*eps/qc + \
                (p + alpha)**2 * \
                (np.exp(-2*qc/eps*(p - alpha)) * sc.expi(2*qc/eps*(p-alpha)) - \
                 np.exp(2*qc/eps*(p - alpha)) * sc.expi(-2*qc/eps*(p-alpha)))

        return value

    pgrid = space.pgrid
    num1 = - (np.sin(np.pi*gamma/2))**2 * (pgrid + np.sqrt(pgrid**2 + 4 * delta))**2
    den1 = 2 * pgrid * np.sqrt(pgrid**2 + 4*delta)
    num2 = -1j * (np.sin(np.pi * gamma/2))**2 # here for - sign 
    den2 = np.pi * pgrid
    psi_hat_corr = np.zeros(len(pgrid), dtype='complex_')
    integral = np.zeros(len(pgrid), dtype='complex_')
    integral_list = []
    p_list = []
    for ix, p in enumerate(pgrid):
        if p > 0 and p < P0 + 6: # possibly need to restric this to +- mean momentum
            nu = np.sqrt(p**2 + 4*delta)
            a1 = nu
            a2 = -nu
            qc = tau
            # i have taken away 1/2/nu # changed + to -
                                      #- \
                                     #get_integral(eps, a2, qc, p))
            integral[ix] =  -1/2/nu * (get_integral(eps, a1, qc, p) - \
                                      get_integral(eps, a2, qc,p))
            psi_hat_corr[ix] = (num1[ix]/den1[ix]*np.exp(-2*tau/eps*np.abs(p - nu))) * \
                    psi_hat[ix] + (num2/den2[ix]*integral[ix]) * psi_hat[ix]
            
            integral_list.append(integral[ix].real)
            p_list.append(p)
    
    import csv
    with open('integral.csv', 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerows(zip(p_list,integral_list))

    return psi_hat_corr

def get_correction2(psi_hat, space, eps, tau, delta, gamma, P0):
    """
    Returns adjusted wavepacket post avoided crossing
    See [paper reference]
    """
    import scipy.special as sc
    
    def get_integral(eps, alpha, qc, p):
        value = eps/qc * (p - alpha) + (p + alpha) * 2*eps/qc + \
                (p + alpha)**2 * \
                (np.exp(-2*qc/eps*(p - alpha)) * sc.expi(2*qc/eps*(p-alpha)) - \
                 np.exp(2*qc/eps*(p - alpha)) * sc.expi(-2*qc/eps*(p-alpha)))

        return value

    pgrid = space.pgrid
    num1 = - (np.sin(np.pi*gamma/2))**2 * (pgrid + np.sqrt(pgrid**2 + 4 * delta))**2
    den1 = 2 * pgrid * np.sqrt(pgrid**2 + 4*delta)
    num2 = -1j * (np.sin(np.pi * gamma/2))**2 # here for - sign 
    den2 = np.pi * pgrid
    psi_hat_corr = np.zeros(len(pgrid), dtype='complex_')
    integral = np.zeros(len(pgrid), dtype='complex_')
    integral_list = []
    p_list = []
    
    data = np.loadtxt('integral_mathematica_n11.txt', usecols = 1)
    print(data)
    IX = int((P0 - 2 - space.pgrid[0])/space.dp)
    #IXI = int((P0 + 2)/space.dp)
    for ix, value in enumerate(data):
        nu = np.sqrt(space.pgrid[IX + ix]**2 + 4*delta)
        a1 = nu
        a2 = -nu
        qc = tau
        # i have taken away 1/2/nu # changed + to -
                                  #- \
                                 #get_integral(eps, a2, qc, p))
        integral[IX + ix] =  1/2/nu * (value)
        psi_hat_corr[IX + ix] = (num1[IX + ix]/den1[IX + ix]*np.exp(-2*tau/eps*np.abs(space.pgrid[IX + ix] - nu))) * \
                psi_hat[IX + ix] + (num2/den2[IX + ix]*integral[IX + ix]) * psi_hat[IX + ix]
        
        integral_list.append(integral[IX + ix].real)
    

    return psi_hat_corr


def get_upper_mass(psi_hat, mass):
    """
    Returns upper level wavepacket computed using (1 - mass_other)*BOA
    """
    psi = np.zeros(len(psi_hat), dtype='complex_')
    print("\n mass = %.3f \n" % mass)
    psi = np.sqrt(1 - mass)*psi_hat
    return psi

def get_upper_minus(psi_hat, space, eps, tau, delta, gamma):

    eta2 = lambda p: p**2 - 4*delta
    p = space.pgrid
    sign_p = np.sign(p)
    
    psihat_crossing = np.zeros(len(p), dtype='complex_')

    for i in range(len(psihat_crossing)):
        if eta2(p[i]) > 0:
            eta = sign_p[i] * np.sqrt(eta2(p[i]))
            psihat_crossing[i] = np.sin(np.pi * gamma/2) * (p[i] + eta)/(abs(eta)) * \
                    np.exp(- tau / eps * np.abs(p[i] - eta)) * psi_hat[i]

    return psi_hat -  psihat_crossing
