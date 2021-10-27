import matplotlib.pyplot as plt 
import numpy as np

data = np.loadtxt('./flateigenvaluesdelta0.500qc0.500eps0.100p4Hagedorn0.txt', 
        skiprows=1)
x = data[:,1]
y = data[:,4]
plt.plot(x,y)
plt.xlim(0,8)
plt.show()
plt.close()
