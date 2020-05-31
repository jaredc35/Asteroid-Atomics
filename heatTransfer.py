import matplotlib.pyplot as plt
import numpy as np
"""
Program that evaluates the heat system
for the reactor
"""
Qdot = 100e3 #100 KW
Pdot = 25e3 #25 KW of power
T_h = 1200 #K
T_c = 850 #K

"""
Let's look at varying ranges of power throughput for the
heat pipes, say 10, 20, 25, 33.3, 50, 100 KWt
"""
hpThroughput = [10, 20, 25, 100./3, 50, 100] #in KWt
HPs = [x*10**3 for x in hpThroughput] #in Wt
print (HPs)


"""
Properties of Fuel
"""
Trange = range(100, 1300)

k = lambda T: 3.26631e-6*T**2+2.24774e-2*T+9.62036 #From paper "thermalCondU10Zr" in 22.033 Dropbox folder
cp = lambda T: 1.9364931e-7*T**3-2.1177933e-4*T**2+1.5615193e-1*T+93.07013 #From same paper as above

# print (k(600))
plt.plot(Trange, [k(T) for T in Trange], 'r-', label='Thermal Conductivity [W/mk]')
plt.plot(Trange, [cp(T) for T in Trange], 'k', label='Specific Heat [J/kgK]')
plt.legend()
plt.show()
