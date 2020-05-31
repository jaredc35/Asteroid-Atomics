import matplotlib.pyplot as plt
import numpy as np
import math
import AAShort

pi = math.pi
"""
Program that evaluates the heat system
for the reactor
"""

Qdot = 500e3 #500 KW
T_h = 1200 #K
APPF = 1.25
RPPF = 1.35
# N = 387 #Number of pins
# L = 42 #cm/pin
N= 91 #Number of heat pipes
L = 42 #cm,
qprimemax = APPF*RPPF*(Qdot/(N*L))
print (qprimemax)



"""
Heat Pipe Parameters
Material: Nb-1%Zr Tube

"""
wallthick = 0.2 #cm
kHP =  0.523#W/cmK
rHPo =  1#cm,  wall thickness is 0.2 cm
rHPi = rHPo-wallthick
RHP = (1/(2*pi*kHP))*math.log(rHPo/rHPi)

"""
Properties of Fuel
Material: Uranium Nitride
"""
kF = 0.3 #W/cmK
rF = [rHPo+x*0.1 for x in range(10, 101)]
tF = [x-rHPo for x in rF]
# print (rF)
def Rf(rF):
    return (1/(2*pi*kF))*math.log(rF/rHPo)

def Tfmax(rF):
    return T_h+qprimemax*(Rf(rF)+RHP)

# print ("Short's design applied to our operating needs: ")
# print (AAShort.AAShortapprox)
# print ('')
print ("Block design applied to our operating needs: ")
print ('Fuel Radius of 1.5 cm and a max temp of: ',Tfmax(2.5))

plt.plot(tF, [Tfmax(r) for r in rF], 'ro', label=' Max Temperature at given Thickness')
plt.xlabel('Thickness of Fuel [cm]')
plt.ylabel('Max Fuel Temperature [K]')
# plt.plot(Trange, [cp(T) for T in Trange], 'k', label='Specific Heat [J/kgK]')
plt.legend()
plt.show()
