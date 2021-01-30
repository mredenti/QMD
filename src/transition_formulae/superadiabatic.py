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
        value = eps/alpha/qc * (p + alpha) + (p - alpha)/alpha * eps/2/qc + \
                (p + alpha)**2/2/alpha * \
                (np.exp(-2*qc/eps*(p - alpha)) * sc.expi(2*qc/eps*(p-alpha)) - \
                 np.exp(2*qc/eps*(p - alpha)) * sc.expi(-2*qc/eps*(p-alpha)))
        print(value)

        return value

    pgrid = space.pgrid
    num1 = - (np.sin(np.pi*gamma/2))**2 * (pgrid + np.sqrt(pgrid**2 + 4 * delta))**2
    den1 = 2 * pgrid * np.sqrt(pgrid**2 + 4*delta)
    num2 = 1j * (np.sin(np.pi * gamma/2))**2 
    den2 = np.pi * pgrid

    psi_hat_corr = np.zeros(len(pgrid), dtype='complex_')
    integral = np.zeros(len(pgrid), dtype='complex_')
    for ix, p in enumerate(pgrid):
        if p > 0 and p < P0 + 6: # possibly need to restric this to +- mean momentum
            nu = np.sqrt(p**2 + 4*delta)
            a1 = nu
            a2 = -nu
            qc = tau
            integral[ix] = 1/2/nu * (get_integral(eps, a1, qc, p) + \
                                     get_integral(eps, a2, qc, p))
            psi_hat_corr[ix] = (num1[ix]/den1[ix]*np.exp(-2*tau/eps*np.abs(p - nu))) * \
                    psi_hat[ix] + (num2/den2[ix]*integral[ix]) * psi_hat[ix]
    
    return psi_hat_corr
