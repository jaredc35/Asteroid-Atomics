import numpy as np
import matplotlib.pyplot as plt

surfacetemps = range(300,1201, 10)
powerout = 4e5 #400,000 W 
emiss = 0.9 #Anodized Aluminum
SB = 5.67e-8
T_sp = 3 # 3 K

area = [powerout/(emiss*SB*(T_s**4-T_sp**4)) for T_s in surfacetemps]

plt.plot(surfacetemps, area)
plt.title('Radiative Surface Area vs Skin Temperature')
plt.xlabel('Skin Temperature (K)')
plt.ylabel('Surface Area (m^2)')
plt.show()
