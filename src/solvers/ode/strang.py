import numpy as np


class Strang:

    def __init__(self):

        print('Solving system of ODEs via Strang Splitting \n')



    def do_step(self, itr, wave, time, pot, space = None):
        """Strang Splitting scheme for Hagedorn Wavepackets
        Reference: ...
        -------- Parameters
        wave: hagedorn wave object (see init_cond/)
        """
        # need not really need to define it at each itr
        dt_p = time.dir * time.dt
        # primitive variable will not be pointers so...
        dt_k = time.dir * time.dt 
        
        if itr != time.max_itr:
            
            if itr == 1:
                dt_k /= 2
            
            # kinetic step 
            wave.q += wave.p * dt_k 
            wave.Q += wave.P * dt_k 
            wave.S += wave.p**2 * dt_k / 2
            #full potential step 
            wave.p -= pot.V1(wave.q) * dt_p  
            wave.P -= pot.V2(wave.q) * wave.Q * dt_p 
            # think there should be a minus for the action
            wave.S -= pot.V(wave.q) * dt_p
            wave.detQ = np.exp(np.log(wave.detQ) + wave.P * 1/wave.Q * dt_p)
            
            """
            rem = pot.V(space.xgrid) - \
                    (pot.V(wave.q) + pot.V1(wave.q) * (space.xgrid - wave.q) +\
                    0.5 * pot.V2(wave.q) * (space.xgrid - wave.q)**2)
            F = np.sum(rem * abs(wave.get_psi(space))**2)*space.dx
            
            wave.c[0] = np.exp(-1j*dt_p/wave.eps * F)*wave.c[0]
            """
        else:
            dt_k /= 2
            # half kinetic step 
            wave.q += wave.p * dt_k 
            wave.Q += wave.P * dt_k 
            wave.S += wave.p**2 * dt_k / 2
