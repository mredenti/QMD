# ------------ run dynamics
from initialize import space, time, wave, potential, solver
import matplotlib.pyplot as plt
import numpy as np

wave.psi = wave.get_psi(space)
wave.psi = np.stack((wave.psi, np.zeros(space.n, dtype='complex_')))
print(wave.get_massx(space))

for itr in range(1, time.max_itr):
    solver.do_step(itr, wave, time, potential, space)
    print('%.2f %% , q=%.3f' % (itr/(time.max_itr - 1) * 100, wave.q), end='\r')
    wave.psi[0,:] = wave.get_psi(space)
    mass =  wave.get_massx(space)[0]
    print(mass)
    # mass not conserved
plt.plot(space.xgrid, abs(wave.get_psi(space))**2/mass)
plt.show()
plt.close('all')

