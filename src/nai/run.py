def run_coupled(time, space, solver, wave, potential, fname):
    
    f = open(fname, 'w')
    header = 'itr \t mean_x_up \t mean_x_down \t mean_p_up \t mean_p_down \
            \t ke_up \t ke_down \t e_up \t e_down \t mass_up \t mass_down \n'
    f.write(header)

    count = 0 
    for itr in range(time.max_itr):
        
        solver.do_step(wave, space, itr, time.max_itr)
        
        if itr in time.snap:
            mean_x_up = wave.get_meanx(space)[0]
            mean_x_down = wave.get_meanx(space)[1]
            mean_p_up = wave.get_meanp(space)[0]
            mean_p_down = wave.get_meanp(space)[1]
            ke_up = wave.get_ke(space)[0]
            ke_down = wave.get_ke(space)[1]
            e_up = wave.get_e(space, potential)[0]
            e_down = wave.get_e(space, potential)[1]
            
            data = np.array([itr, 
                    mean_x_up, mean_x_down,
                    mean_p_up, mean_p_down,
                    ke_up, ke_down, 
                    e_up, e_down,
                    wave.get_massx(space)[0], 
                    wave.get_massx(space)[1]])
            
            np.savetxt(f, data.reshape(1,-1))
            print('%.2f %%' % (itr/(time.max_itr) * 100), end='\r')
            print("------------ Observables -------------") # do not repeat
            print("      Mass x={:.12f}  ".format(wave.get_massx(space)[0]))
            print("      Mean x={:.12f}  ".format(wave.get_meanx(space)[0]))
            print("      Mass p={:.12f}  ".format(wave.get_massp(space)[0]))
            print("      Mean p={:.12f}  ".format(wave.get_meanp(space)[0]))
            
            #tp.plot(list(space.xgrid), list(abs(wave.psi[0,:])**2))
            """
            fig, axs = plt.subplots(2, 2)
            axs[0, 0].plot(space.xgrid, abs(wave.psi[0,:]), label = r'$|\phi^+|$')
            axs[0, 0].plot(space.xgrid, abs(wave.psi[1,:]), label = r'$|\phi^-|$')
            axs[0, 0].set_xlim(mean_x_up - 2, mean_x_up + 2)
            axs[0, 0].set_title('Axis [0, 0]')
            axs[0, 0].set(xlabel = 'x')
            axs[0, 1].plot(space.pgrid, abs(wave.psihat[0,:]), label = r'$|\hat{\phi}^+|$')
            axs[0, 1].plot(space.pgrid, abs(wave.psihat[1,:]), label = r'$|\hat{\phi}^-|$')
            axs[0, 1].set_xlim(mean_p_up - 2, mean_p_up + 2)
            axs[1, 0].plot(space.xgrid, potential.rho(space.xgrid) + potential.d(space.xgrid))
            axs[1, 0].plot(space.xgrid, - potential.rho(space.xgrid) + potential.d(space.xgrid))
            axs[1, 0].set_xlim(mean_x_up - 2, mean_x_up + 2)
            axs[1, 1].plot(space.xgrid, potential.rho(space.xgrid) + potential.d(space.xgrid))
            axs[1, 1].plot(space.xgrid, - potential.rho(space.xgrid) + potential.d(space.xgrid))

            # Hide x labels and tick labels for top plots and y ticks for right plots.
            for ax in axs.flat:
                ax.legend()
            plt.savefig('animation/wave-{}.pdf'.format(count))
            plt.cla()
            count += 1
            #plt.pause(0.001) #is necessary for the plot to update for some reason
            #plt.cla()
            """

    plt.close('all')
    f.close()
    
    return wave


if __name__ == '__main__':
    import sys 
    sys.path.insert(0, '..')
    from init_cond.gaussian import Gaussian
    from auxiliary.units import Units
    from auxiliary.space import Space
    from auxiliary.time import Time
    from auxiliary.efft import ifft, fft
    from auxiliary.data import Data
    from potentials.examples.nai import NaI
    from solvers.pde.strang import Strang
    from transition_formulae import superadiabatic 
    import matplotlib.pyplot as plt 
    import numpy as np
    #import logging 

    # ----------------- PRINT OUPUT TO A FILE
    sys.stdout = open("info_run.txt", "w")
    
    #  ---------------- PARAMETERS FOR INITIAL WIGNER DISTRIBUTION 
    EPS, q, p = 0.014654629670711006, 5, 0 
    #  ---------------- PARAMETERS FOR UNIFORM GRID
    XL, XR, N = 2 * Units.Atob, 16 * Units.Atob,  2**16
    #  ---------------- PARAMETERS FOR TIME
    T, TSTEP, TDIR= 80, 1/800, 1 
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
    FNAME = './data/wavepacketdt800.txt' 
    FNAME_OBS = './data/observablesdt800.txt'
    
    print("-----> Case study: NaI  -----------------") 
    print("-----> Change of units is done at runtime for the potential") 

    ################### TO CHECK/CHANGE ###################
    # --------------- INITIALISE SPACE-TIME-POTENTIAL BACKWARD
    space = Space(N, XL, EPS, XR) 
    potential = NaI(A1, BETA1, R0,
            A2, B2, RO, LAMBDAP, LAMBDAM, C2, DELTAE,
            A12, BETA12, RX)
    
    wave = Gaussian(EPS, q, p, 'exact', 2, space) # init psi and psi hat
    time_forward = Time(T, TSTEP, 1)
    solver_coupled = Strang(EPS, space, time_forward, potential, 2)
    run_coupled(time_forward, space, solver_coupled, wave, potential, FNAME_OBS)
    
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
    sys.stdout.close()

