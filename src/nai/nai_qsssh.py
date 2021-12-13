def run_qsssh(time, space, solver_up, wave, potential, solver_down, rate, fname):
    
    f = open(fname, 'w')
    header = 'itr \t mean_x_up \t mean_x_down \t mean_p_up \t mean_p_down \
            \t ke_up \t ke_down \t e_up \t e_down \t mass_up \t mass_down \n'
    f.write(header)

    # probably here you'd want to initialise the gap values
    ####
    wave.rho_new = potential.rho(wave.get_meanx(space))
    wave.rho_curr =  wave.rho_new
    wave.rho_old = wave.rho_curr
    ####
    spawned = False
    for itr in range(time.max_itr):
        
        solver_up.do_step(wave, space, itr, time.max_itr)
        # update gap status
        wave.rho_old = wave.rho_curr
        wave.rho_curr = wave.rho_new
        wave.rho_new = potential.rho(wave.get_meanx(space))
        
        if (wave.rho_old - wave.rho_curr) * (wave.rho_new - wave.rho_curr) > 0:
            # spawn a wavepacket onto the lower level 
            wave_spawned = get_spawned_wavepacket(wave, potential, space, rate)
            spawned = True
            # evolved the spawned wavepacket until the last itr 
        if spawned:
            solver_down.do_step(wave_spawned, space, itr, time.max_itr)
            print("Mass_up x={:.17g}  ".format(wave.get_massx(space)))
            print("Mass_down x={:.17g} \n ".format(wave_spawned.get_massx(space)))
            if itr in time.snap:
                mean_x_up = wave.get_meanx(space)
                mean_x_down = wave_spawned.get_meanx(space)
                mean_p_up = wave.get_meanp(space)
                mean_p_down = wave_spawned.get_meanp(space)
                ke_up = wave.get_ke(space)
                ke_down = wave_spawned.get_ke(space)
                e_up = wave.get_e(space, potential)
                e_down = wave_spawned.get_e(space, potential)
                
                data = np.array([itr, 
                        mean_x_up, mean_x_down,
                        mean_p_up, mean_p_down,
                        ke_up, ke_down, 
                        e_up, e_down,
                        wave.get_massx(space), 
                        wave_spawned.get_massx(space)])
                
                np.savetxt(f, data.reshape(1,-1))
                print('%.2f %%' % (itr/(time.max_itr) * 100), end='\r')
                print("------------ Observables -------------") # do not repeat
                print("      Mass x={:.12f}  ".format(wave.get_massx(space)))
                print("      Mean x={:.12f}  ".format(wave.get_meanx(space)))
                print("      Mass p={:.12f}  ".format(wave.get_massp(space)))
                print("      Mean p={:.12f}  ".format(wave.get_meanp(space)))
            

    plt.close('all')
    f.close()
    
    return (wave, wave_spawned)


if __name__ == '__main__':
    import sys 
    sys.path.insert(0, '..')
    from init_cond.gaussian import Gaussian
    from auxiliary.units import Units
    from auxiliary.space import Space
    from auxiliary.time import Time
    from auxiliary.efft import ifft, fft
    from auxiliary.data import Data
    from auxiliary.error import l2norm, l2relerror
    from potentials.examples.nai import NaI
    from solvers.pde.strang import Strang
    from transition_formulae.superadiabatic import get_spawned_wavepacket 
    import matplotlib.pyplot as plt 
    import numpy as np
    #import logging 

    # YOU WANT TO SET THE PARAMETERS IN A COMMON FILE 
    # SO THAT THERE IS NO RISK IN OTHER SCRIPTS USING 
    # DIFFERENT VALUES
    RATE = 'SA'
    # ----------------- PRINT OUPUT TO A FILE
    sys.stdout = open("info_runSA.txt", "w")
    
    #  ---------------- PARAMETERS FOR INITIAL WIGNER DISTRIBUTION 
    EPS, q, p = 0.014654629670711006, 5, 0 
    #  ---------------- PARAMETERS FOR UNIFORM GRID
    XL, XR, N = 2 * Units.Atob, 16 * Units.Atob,  2**16
    #  ---------------- PARAMETERS FOR TIME
    T, TSTEP, TDIR= 80, 1/400, 1 
    #  ---------------- PARAMETERS FOR POTENTIAL 
    #A1, BETA1, R0 = 0.813, 4.08, 2.67  
    A1 = 0.813 * Units.eVtoH 
    BETA1 = 4.08 / Units.Atob  
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
    NEQS = 2
    # ----------------- SAVE DATA TO FOLLOWING FILE 
    FNAME = './data/qsssh_wavepacket.txt' 
    FNAME_OBS = './data/qsssh_observables.txt'
    
    print("-----> Case study: NaI  -----------------") 
    print("-----> Change of units is done at runtime for the potential") 

    ################### TO CHECK/CHANGE ###################
    # --------------- INITIALISE SPACE-TIME-POTENTIAL BACKWARD
    space = Space(N, XL, EPS, XR) 
    potential_up = NaI(A1, BETA1, R0,
            A2, B2, RO, LAMBDAP, LAMBDAM, C2, DELTAE,
            A12, BETA12, RX, 'up')
    potential_down = NaI(A1, BETA1, R0,
            A2, B2, RO, LAMBDAP, LAMBDAM, C2, DELTAE,
            A12, BETA12, RX, 'down')
    
    wave = Gaussian(EPS, q, p, 'boa', 1, space) # init psi and psi hat
    time_forward = Time(T, TSTEP, 1)
    solver_single_up = Strang(EPS, space, time_forward, potential_up, 1) 
    solver_single_down = Strang(EPS, space, time_forward, potential_down, 1) 
    # run one level dynamics -> detect crossing -> spawn wavepacket 
    wave_boa, wave_spawned = run_qsssh(time_forward, space, solver_single_up, wave, potential_up, solver_single_down, RATE, FNAME_OBS)
    
    print("---------> ERROR ANALYSIS: L2 error (abs, rel) w.r.t. reference solution")
    # reference lower level solution
    data = np.loadtxt('data/wavepacket.txt', skiprows=2)
    psiexact = data[:,6] + 1j*data[:,7]
    # print/compute L2 error (and relative) between exact and qsssh solution
    print("L2 error ", l2norm(psiexact - wave_spawned.psi, space.dx))
    print("L2 relative error ", l2relerror(psiexact, wave_spawned.psi, space.dx))
    sys.stdout.close()

    """
    
    # --------------- SAVE DATA --------------
    wave_up = Gaussian(EPS, q, p, 'exact_up') # init psi and psi hat
    wave_up.psi     = wave.psi[0,:] 
    wave_up.psihat  = wave.psihat[0,:] 
    wave_down = Gaussian(EPS, q, p, 'exact_down') # init psi and psi hat
    wave_down.psi     = wave.psi[1,:] 
    wave_down.psihat  = wave.psihat[1,:] 
    Data.save(FNAME, space, [wave_up, wave_down]) # this will not work

    # ----------------- SAVE DATA
    print("GOOD LUCK -------------------------------------------")
    """
