import matplotlib.pyplot as plt
import numpy as np
import math

pi = math.pi
"""
Program that evaluates the heat system
for the reactor
"""
Qdot = 1.2e6 #1.2 MW
T_h = 1800 #K
APPF = 1.25

RPPF = 1.35
N = 387 #Number of pins
L = 42 #cm/pin
qprimemax = APPF*RPPF*(Qdot/(N*L))
print (qprimemax)

"""
Properties of Fuel
Material: Uranium Nitride
"""
kF = 0.3 #W/cmK
RF = 1/(4*pi*kF)

'''
Properties of Gap
Fill Liquid: Unknown
'''
rg = 0.875 # cm
hg = 0.6 #W/cm^2K From reference 42 in his paper
Rg = 1/(2*pi*rg*hg)

"""
Clad Parameters
Material: Rhenium
"""
rco = 1.0 #cm
rci = 0.9 #cm
Kc = 0.711 #W/cmK
Rc = (1/(pi*2*Kc))*math.log(rco/rci)

"""
Tricusp Parameters
Material: Rhenium
"""
rT = 1.5 #cm, this value could be a range of things
rTrange = [rT + x*.1 for x in range(-3, 6)]
thickness = [0.5+x*.1 for x in range(-3, 6)]
kT = 0.711 #W/cmK
def RT(radius):
    return (1/(2*pi*kT))*math.log((radius)/rco)

"""
Heat Pipe Parameters
Material: Nb-1%Zr
Thickness: 2mm
"""
kHP = 0.523 #W/cmK
rHP = 1.7 #cm,  wall thickness is 0.2 cm
RHP = (1/(2*pi*kHP))*math.log(rHP/rT)



# Tfmax = T_h+qprimemax*(RF+Rg+Rc+RT(0.5)+RHP)
def Tfmax(thickness):
    return T_h+qprimemax*(RF+Rg+Rc+RT(thickness)+RHP)





plt.plot(thickness, [Tfmax(T) for T in rTrange], 'ro', label='Temperature at given Thickness')
plt.xlabel('Thickness of Tricusp [cm]')
plt.ylabel('Temperature [K]')
# plt.plot(Trange, [cp(T) for T in Trange], 'k', label='Specific Heat [J/kgK]')
plt.legend()
plt.show()
