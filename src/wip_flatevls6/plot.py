import numpy as np
import matplotlib.pyplot as plt 
SMALL_SIZE = 12
MEDIUM_SIZE = 14
BIGGER_SIZE = 16

plt.rc('font', size=MEDIUM_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=MEDIUM_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=10)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

def angle(z1, z2, y1, y2):
    "angle of the difference would be wrong - consider the case of two \
            vectors with the same phase and of different lenghts"
    diff = (np.arctan2(z2, z1) - np.arctan2(y2, y1))
    #return np.min(diff, 2*np.pi - diff)
    return np.minimum(np.abs(diff), np.abs(diff - 2*np.pi))


def l2norm(re,im,dx):

    return np.sum(re**2 + im**2)*dx

def l2relerror(re1, im1, re2, im2, dx):
    
    # can definitely define it in other ways
    return l2norm(re1 - re2, im1 - im2, dx)/l2norm(re2, im2, dx)


EPS, Q0, P0 = 1/10, 0, 5 # momentums 2 and 5 in the paper 
DELTA, C, ALPHA = 0.5, -np.pi, np.pi
FNAME = './data/delta%.3fc%.3falpha%.3feps%.3fp%d.txt' %(DELTA, C, ALPHA, EPS, P0)
#FNAME = './right/flatdelta%.3fc%.3falpha%.3feps%.3fp%d.txt' %(DELTA, C, ALPHA, EPS, P0)

data = np.loadtxt(FNAME, skiprows=7)

boa_up_real = data[:,4]
boa_up_imag = data[:,5]

exact_up_real = data[:,8]
exact_up_imag = data[:,9]

exact_down_real = data[:,12]
exact_down_imag = data[:,13]

formula_up_real = data[:,16]
formula_up_imag = data[:,17]

formula_down_real = -data[:,20]
formula_down_imag = -data[:,21]

upper_mass_real = data[:,24]
upper_mass_imag = data[:,25]

upper_minus_real = data[:,28]
upper_minus_imag = data[:,29]

dp = data[2,1] - data[1,1]

plt.plot(data[:,1], boa_up_real**2 + boa_up_imag**2, label = 'boa up hat') # BOA + hat
plt.plot(data[:,1], exact_up_real**2 + exact_up_imag**2, label = 'exact up hat') # EXACT up hat
plt.plot(data[:,1], formula_up_real**2 + formula_up_imag**2, label = 'formula up hat') #formula up hat 
plt.plot(data[:,1], upper_mass_real**2 + upper_mass_imag**2, label = 'sqrt(1 - mass)') # EXACT up hat
plt.plot(data[:,1], upper_minus_real**2 + upper_minus_imag**2, label = 'boa - formula-') #formula up hat 
#plt.plot(data[:,1], exact_down_real**2 + exact_down_imag**2, label = 'exact down hat') # EXACT DOWN HAT
#plt.plot(data[:,1], formula_down_real**2 + formula_down_imag**2, label = 'formula down hat') # formula down hat
plt.xlabel('momentum')
plt.ylabel('abs^2')
plt.xlim(P0 - 2, P0 + 2)
plt.legend()
plt.show()
plt.close('all')

# -------------------------
p0_ix = int((P0 - data[0,1])/dp) 
phase_shift_improvement = (angle(exact_up_real[p0_ix], exact_up_imag[p0_ix], 
                                 boa_up_real[p0_ix], boa_up_imag[p0_ix]) - \
                            angle(exact_up_real[p0_ix], exact_up_imag[p0_ix],
                                  formula_up_real[p0_ix], formula_up_imag[p0_ix])) \
        /angle(exact_up_real[p0_ix], exact_up_imag[p0_ix], boa_up_real[p0_ix], boa_up_imag[p0_ix])
print(phase_shift_improvement)
#---------------------------

plt.plot(data[:,1], angle(exact_up_real, exact_up_imag, formula_up_real, formula_up_imag), label = 'phase-diff formula') 
plt.plot(data[:,1], angle(exact_up_real, exact_up_imag, boa_up_real, boa_up_imag), label = 'phase-diff boa') 
plt.xlim(P0 - 2, P0 + 2)
plt.ylim(0, np.pi/2)
plt.xlabel('momentum')
plt.ylabel('phase')
plt.legend()
plt.show()
plt.close('all')
#------------------------------------------
plt.plot(data[:,1], angle(exact_down_real, exact_down_imag, formula_down_real, formula_down_imag), label = 'phase-diff formula down') 
plt.xlim(P0 - 2, P0 + 2)
plt.xlabel('momentum')
plt.ylabel('phase')
plt.legend()
plt.show()
plt.close('all')

#------------------------------------------
plt.plot(data[:,1], abs(np.arctan2(formula_up_imag, formula_up_real)), label = 'phase formula') 
plt.plot(data[:,1], abs(np.arctan2(exact_up_imag, exact_up_real)), label = 'phase exact') 
plt.plot(data[:,1], abs(np.arctan2(boa_up_imag, boa_up_real)), label = 'phase boa') 
plt.xlabel('momentum')
plt.xlim(P0 - 0.5, P0 + 0.5)
plt.legend()
plt.show()
plt.close('all')

#--------------------------
plt.plot(data[:,1], abs(np.arctan2(formula_down_imag, formula_down_real)), label = 'phase formula down') 
plt.plot(data[:,1], abs(np.arctan2(exact_down_imag, exact_down_real)), label = 'phase exact down') 
plt.xlabel('momentum')
plt.xlim(P0 - 2, P0 + 2)
plt.legend()
plt.show()
plt.close('all')

#---------------------------
plt.plot(data[:,1], (exact_down_real - formula_down_real)**2 + \
                        (exact_up_imag - formula_up_imag)**2, label = 'phase formula') 
plt.xlabel('momentum')
plt.xlim(P0 - 0.5, P0 + 0.5)
plt.legend()
plt.show()
plt.close('all')
print('-----------------MASS------------------')
print('Boa up %.4f' % l2norm(boa_up_real, boa_up_imag, dp))
print('Exact up %.4f' % l2norm(exact_up_real, exact_up_imag, dp))
print('Formula up %.4f' % l2norm(formula_up_real, formula_up_imag, dp))
#print(np.sum(data[:,8]**2 + data[:,9]**2)*(dp) + \
#        np.sum(data[:,12]**2 + data[:,13]**2)*(dp))
print('Exact down %.4f' % l2norm(exact_down_real, exact_down_imag, dp))
print('Formula down %.4f' % l2norm(formula_down_real, formula_down_imag, dp))

print('-----------------L2 REL ERROR------------------')
print('Boa up %.4f' % l2relerror(boa_up_real, boa_up_imag, exact_up_real, exact_up_imag, dp))
print('Formula up %.4f' % l2relerror(formula_up_real, formula_up_imag, exact_up_real, exact_up_imag, dp))
print('Formula down %.4f' % 
      l2relerror(formula_down_real, formula_down_imag, exact_down_real, exact_down_imag, dp))

