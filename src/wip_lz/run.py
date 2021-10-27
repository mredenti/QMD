#import terminalplot as tp

def run_simple(time, space, solver, wave, fname):

    f = open(fname, 'w')
    header = 'itr \t mass \t mean_x \t mean_p \n'
    f.write(header)
    
    for itr in range(1, time.max_itr + 1):
        
        solver.do_step(wave, space, itr, time.max_itr)
        
        data = np.array([itr, 
                wave.get_massx(space), 
                wave.get_meanx(space),
                wave.get_meanp(space)])
        
        np.savetxt(f, data.reshape(1,-1))
        
        if itr in time.snap:
            print('%.2f %%' % (itr/(time.max_itr) * 100), end='\r')
            print("------------ Observables -------------") # do not repeat
            print("      Mass x={:.12f}  ".format(data[0]))
            print("      Mean x={:.12f}  ".format(data[1]))
            print("      Mass p={:.12f}  ".format(wave.get_massp(space)))
            print("      Mean p={:.12f}  ".format(data[2]))
            # have the wave class automatically call these statistics
            
            #tp.plot(list(space.xgrid), list(abs(wave.psi)**2))
        
    f.close()

    return wave

def run_stop(time, space, solver, wave, fname):
    
    itr = range(1, time.max_itr + 100)
    count = 0
    while wave.get_meanx(space) > 0: 
        solver.do_step(wave, space, itr[count], time.max_itr)
        if itr[count] in time.snap:
            print('%.2f %%' % (itr[count]/(time.max_itr) * 100), end='\r')
            print("------------ Observables -------------") # do not repeat
            print("      Mass x={:.12f}  ".format(wave.get_massx(space)))
            print("      Mean x={:.12f}  ".format(wave.get_meanx(space)))
            print("      Mass p={:.12f}  ".format(wave.get_massp(space)))
            print("      Mean p={:.12f}  ".format(wave.get_meanp(space)))
            
            #tp.plot(list(space.xgrid), list(abs(wave.psi)**2))
        count += 1
    return wave

def run_coupled(time, space, solver, wave, potential, fname):
    
    f = open(fname, 'w')
    header = 'itr \t mean_x_up \t mean_x_down \t mean_p_up \t mean_p_down \
            \t ke_up \t ke_down \t e_up \t e_down \t mass_up \t mass_down \n'
    f.write(header)

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
            
    f.close()
    
    return wave


if __name__ == '__main__':
    """ Sample Wigner distribution --> evolve particles --> detect crossing --> jump """
    import sys 
    sys.path.insert(0, '..')
    from init_cond.gaussian import Gaussian
    from auxiliary.space import Space
    from auxiliary.time import Time
    from auxiliary.efft import ifft, fft
    from auxiliary.data import Data
    from potentials.examples.lz import LZ
    from solvers.pde.strang import Strang
    from transition_formulae import superadiabatic 
    import matplotlib.pyplot as plt 
    import numpy as np
    #import logging 

    # ----------------- PRINT OUPUT TO A FILE
    sys.stdout = open("info_run.txt", "w")
    
    #  ---------------- PARAMETERS FOR INITIAL WIGNER DISTRIBUTION 
    EPS, q, p = 0.05, -10, 4 
    #  ---------------- PARAMETERS FOR UNIFORM GRID
    XL, XR, N = -20, 20,  2**16
    #  ---------------- PARAMETERS FOR TIME
    T, TSTEP, TDIR= 20/p, 1/100/p, 1 
    #  ---------------- PARAMETERS FOR POTENTIAL 
    DELTA, ALPHA = 0.5, 0.5 # delta 0.1# CHANGE PARAMETERS
    NEQS = 2
    #  ---------------- CHECK FOR COMMAND LINE ARGUMENTS
    if len(sys.argv) > 1:
        DELTA = float(sys.argv[1]) # change parameters
        # add a check for the parameters fed 
    # ----------------- SAVE DATA TO FOLLOWING FILE 
    FNAME = './data/wavepacketdelta%.4falpha%.4feps%.4fp%d.txt' \
            %(DELTA, ALPHA, EPS, p) # TO CHANGE
    FNAME_OBS = './data/observablesdelta%.4falpha%.4feps%.4fp%d.txt' \
            %(DELTA, ALPHA, EPS, p) # TO CHANGE
    
    print("############ Simulation parameters ##############")
    print("-----> Potential is Landau Zener") 
    # makes sense to have this potential class
    print("-----> delta={:.4f}, alpha={:.4f}".format(DELTA, ALPHA))
    print("------------ Simulation parameters ---------------")
    print("------------ Simulation parameters ---------------")

    # --------------- INITIALISE SPACE-TIME-POTENTIAL BACKWARD
    space = Space(N, XL, EPS, XR)
    potential = LZ(ALPHA, DELTA, 'up')
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


