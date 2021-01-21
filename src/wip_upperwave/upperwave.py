import sys 
sys.path.insert(0, '..')
from init_cond.gaussian import Gaussian
from auxiliary.space import Space
from auxiliary.time import Time
from auxiliary.error import norm2, relerror2
from auxiliary.efft import ifft
from potentials.examples.simple import Simple
from solvers.pde.strang import Strang
import matplotlib.pyplot as plt 
import numpy as np



# ----------------- RUN -----------------------
def save_data(f, wave, itr):
    data = (wave.get_meanx(space)[0], wave.get_meanx(space)[1],
            wave.get_meanp(space)[0], wave.get_meanp(space)[1],
            wave.get_massx(space)[0], itr)
    f.write('\t'.join(map(str, data)) + '\n')




def run(time, solver, wave, space ,save = False):
    
    snap = [i for i in range(0,time.max_itr,int(time.max_itr/100))]
    
    if save:
        f = open('./data/delta%.3feps%.3fp%d.txt' %(DELTA, EPS, P0), 'w')
        f1 = open('./data/wavedelta%.3feps%.3fp%d.txt' %(DELTA, EPS, P0), 'w')
        f.write("x+ \t x- \t p+ \t p- \t mass_x+ \t itr \n")
        save_data(f, wave, 0)

    for itr in range(1, time.max_itr):
        """ 
        if itr in snap:
            psi = solver.to_adiab(wave.psi)
            plt.plot(space.xgrid, abs(psi[0,:]))
            plt.plot(space.xgrid, abs(psi[1,:]))
            plt.pause0.005)
            plt.cla()
        """
        solver.do_step(wave, space, itr, time.max_itr)
        print('%.2f %%' % (itr/(time.max_itr - 1) * 100), end='\r')
        #psi = solver.to_adiab(wave.psi)
        if save:
            save_data(f, wave, itr)
    
    if save:
        f1.write("xgrid \t psiboa+_real \t psiboa+_imag \t \
                 psi+_real \t psi+_imag \t \
                 psi-_real \t psi-_imag \t \
                 pgrid \t psihatboa+_real \t psiboa+_imag \t \
                 psihat+_real \t psihat+_imag \t \
                 psihat-_real \t psihat-_imag\n")
    
        np.savetxt(f1, np.c_[space.xgrid,
                             boadiff.psihat.real, boadiff.psihat.imag,
                            wave.psi[0,:].real, wave.psi[0,:].imag,
                            wave.psi[1,:].real, wave.psi[1,:].imag,
                            space.pgrid, 
                            boa.psihat.real, boa.psihat.imag,
                            wave.psihat[0,:].real, wave.psihat[0,:].imag,
                            wave.psihat[1,:].real, wave.psihat[1,:].imag,
                             psiguess.real, psiguess.imag,
                            shift.real, shift.imag],
                            delimiter = '\t')
        f.close()

if __name__ == '__main__':
    # ------------------- PARAMETERS ----------------
    # init wave params
    EPS, Q0, P0 = 1/10, 0, 5 
    # space    
    XL, XR = -30, 30
    N = 2**14
    # time
    T, TSTEP, TDIR= 20/P0, 1/100/P0, 1
    #potential params
    ALPHA, DELTA = 0.5, 0.5 
    LEVEL = 'up'
    NEQS = 2
    # ---------------- INIT -------------------------
    space = Space(N, XL, EPS, XR)
    time = Time(T, TSTEP, TDIR)
    boa = Gaussian.init(EPS, Q0, P0, 1, space) # init psi and psi hat
    boa_temp = Gaussian.init(EPS, Q0, P0, 1, space) # init psi and psi hat
    potential = Simple(ALPHA, DELTA, LEVEL)
    #------------- EVOLVE BACK --------------------- 
    time.dir = -1
    time.t /= 2
    solverboa = Strang(boa_temp, space, time, potential, 1)
    run(time, solverboa, boa_temp, space)
    # ------------ EVOLVE FORWARD ------------------
    time.dir = 1
    time.t *= 2
    wave = Gaussian(EPS, Q0, P0) # init psi and psi hat
    wave.psi = np.stack((boa_temp.psi, 
                         np.zeros(space.n, dtype='complex_'))) 
    wave.psihat = np.stack((boa_temp.psihat, 
                            np.zeros(len(boa_temp.psihat), dtype='complex_'))) 
    solver = Strang(wave, space, time, potential, 2)
    run(time, solver, wave, space)
    # ------------ EVOLVE BACKWARDS LOWER LEVEL -----------
    potential.level = 'down'
    time.dir = -1
    time.t /= 2
    EXACT_UP = wave.psihat[0,:].copy()
    wave.psi = wave.psi[1,:]
    wave.psihat = wave.psihat[1,:]
    solver = Strang(wave, space, time, potential, 1)
    run(time, solver, wave, space)
    
    from scipy import interpolate
    coeffs_real = interpolate.splrep(space.pgrid, wave.psihat.real)
    coeffs_imag = interpolate.splrep(space.pgrid, wave.psihat.imag)
    shift = np.zeros(len(boa.psihat), dtype='complex_')
    shift = interpolate.splev(np.sqrt(space.pgrid**2 + 4*DELTA) ,coeffs_real) \
        +1j*interpolate.splev(np.sqrt(space.pgrid**2 + 4*DELTA),coeffs_imag)  
    
    # --------------- final forward -----------------
    wave.psihat = boa.psihat - shift 
    wave.psi = ifft(wave, space)
    potential.level = 'up'
    time.dir = 1
    solver = Strang(wave, space, time, potential, 1)
    run(time, solver, wave, space)

    f = open('./data/guessdelta%.3feps%.3fp%d.txt' %(DELTA, EPS, P0), 'w')
    f.write("pgrid \t psihatexact+_real \t psihatexact+_imag \t \
             psihatguess+_real \t psihatguess+_imag \n")
    np.savetxt(f, np.c_[space.pgrid, 
                        EXACT_UP.real, EXACT_UP.imag,
                        wave.psihat.real, wave.psihat.imag],
                        delimiter = '\t')
    f.close()

