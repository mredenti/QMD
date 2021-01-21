import setup
import numpy as np
# perhaps should have all of the above in a script
# and then call it from the different tests
# ----------------- RUN -----------------------
for itr in range(1, setup.time.max_itr + 1):
    setup.solver.do_step(setup.wave_boa, setup.space, itr, setup.time.max_itr)
    print('%.2f %%' % (itr/(setup.time.max_itr) * 100), end='\r')

import matplotlib.pyplot as plt
plt.plot(setup.space.xgrid, abs(setup.wave_boa.psi)**2)
plt.show()
plt.close()

np.savetxt('wave_boa_pos.txt', setup.wave_boa.psi)

