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
    
    return None

def get_correction(psi_hat, space, eps, tau, delta, gamma, P0):
    """
    Returns adjusted wavepacket post avoided crossing
    See [paper reference]
    """
    import scipy.special as sc
    
    def get_integral(beta, ypsilon, c, gamma):
        value = 2*(1/beta**2 - ypsilon/beta) + \
                4*c/beta * (np.exp(-beta*ypsilon1) + 1) + \
                c**2*(- np.exp(beta*ypsilon) * sc.expi(-beta*ypsilon) + \
                       np.exp(-beta*ypsilon)*(sc.expi(beta*gamma)))
        # copy integral from below
        return value

    pgrid = space.pgrid
    num1 = - (np.sin(np.pi*gamma/2))**2 * (pgrid + np.sqrt(pgrid**2 + 4 * delta))**2
    den1 = 2 * pgrid * np.sqrt(pgrid**2 + 4*delta)
    num2 = - 1j * (np.sin(np.pi * gamma/2))**2 
    den2 = np.pi * pgrid

    psi_hat_corr = np.zeros(len(pgrid), dtype='complex_')
    integral = np.zeros(len(pgrid), dtype='complex_')
    for ix, p in enumerate(pgrid):
        if p > 0 and p < P0 + 3: # possibly need to restric this to +- mean momentum
            nu = np.sqrt(p**2 + 4*delta)
            beta = 2*tau/eps
            ypsilon1 = p + nu # i will most likely need both terms of the integral...?
            c1 = p - nu
            ypsilon2 = nu - p
            c2 = - p - nu
            integral[ix] = 1/2/nu * (get_integral(beta,ypsilon1, c1, gamma) + \
                                     get_integral(beta, ypsilon2, c2, gamma))
            psi_hat_corr[ix] = (num1[ix]/den1[ix]*np.exp(-2*tau/eps*np.abs(p - nu))) * psi_hat[ix] \
                    + (num2/den2[ix] * integral[ix]) * psi_hat[ix]
    
    # do not know how they are evaluating the exponential integral at this stage
    # seems they do an analytic continuation - something we were not able to do 
    #sc.exp1(x)
    # python exponential integral 
    return psi_hat_corr
