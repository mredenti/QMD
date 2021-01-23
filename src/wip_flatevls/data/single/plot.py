import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd

def angle(z1, z2, y1, y2):
    "angle of the difference would be wrong - consider the case of two \
            vectors with the same phase and of different lenghts"
    diff = abs(np.arctan2(z2, z1) - np.arctan2(y2, y1))
    #return np.min(diff, 2*np.pi - diff)
    return diff

EPS, Q0, P0 = 1/10, 0, 5 # momentums 2 and 5 in the paper 
DELTA, C, ALPHA = 0.5, -3.14, 3.14
FNAME = './center/flatdelta%.3fc%.3falpha%.3feps%.3fp%d.txt' %(DELTA, C, ALPHA, EPS, P0)
#FNAME = './right/flatdelta%.3fc%.3falpha%.3feps%.3fp%d.txt' %(DELTA, C, ALPHA, EPS, P0)

#df = pd.read_csv(FNAME, delimiter='\t')
#print(df.head(5))
data = np.loadtxt(FNAME, skiprows=5)

#plt.plot(data[:,1], data[:,4]**2 + data[:,5]**2, label = 'boa up hat') # BOA + hat
#plt.plot(data[:,1], data[:,8]**2 + data[:,9]**2, label = 'exact up hat') # EXACT up hat
#plt.plot(data[:,1], data[:,16]**2 + data[:,17]**2, label = 'formula up hat') # formula up hat 

# PLOT PHASE DIFFERENCE
#plt.plot(data[:,1], angle(data[:,8], data[:,9], data[:,4], data[:,5]))

# PLOT IMAGINARY PART OF EXACT SOLUTION
plt.plot(data[:,1], data[:,9], label = 'Imag(exact up hat)') # EXACT up hat
plt.plot(data[:,1], data[:,4]**2 + data[:,5]**2, label = 'boa up hat - abs^2') # BOA + hat

#plt.plot(data[:,1], data[:,12]**2 + data[:,13]**2, label = 'exact down hat') # EXACT DOWN HAT
#plt.plot(data[:,1], data[:,20]**2 + data[:,21]**2) # formula down hat


plt.xlabel('momentum')
#plt.ylabel('abs^2')
plt.xlim(P0 - 2, P0 + 2)
plt.legend()
plt.show()
plt.close('all')

print('boa mass', np.sum(data[:,4]**2 + data[:,5]**2)*(data[2,1] - data[1,1]))
print('exact up hat mass', np.sum(data[:,8]**2 + data[:,9]**2)*(data[2,1] - data[1,1]))
print(np.sum(data[:,8]**2 + data[:,9]**2)*(data[2,1] - data[1,1]) + \
        np.sum(data[:,12]**2 + data[:,13]**2)*(data[2,1] - data[1,1]))
print('formula down hat mass', np.sum(data[:,20]**2 + data[:,21]**2)*(data[2,1] - data[1,1]))
print('exact down hat mass', np.sum(data[:,12]**2 + data[:,13]**2)*(data[2,1] - data[1,1]))
print('formula up hat mass', np.sum(data[:,16]**2 + data[:,17]**2)*(data[2,1] - data[1,1]))

