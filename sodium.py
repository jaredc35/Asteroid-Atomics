'''
Material Properties for Sodium
'''
import math

class sodium:

    def __init__(self, T):
        self.h = self.enthalpy(T)
        self.hg = self.enthalpygas(T)
        self.rhog = self.liquiddensity(T)
        self.rhov = self.vapordensity(T)
        self.vp = self.vaporpressure(T)


    def enthalpy(self, T):
        #Enthalpy of Liquid sodium
        #Good between 371K to 2000 K
        ent = -365.77 + 1.6582*T - 4.2395e-4*T**2 + 1.4847e-7*T**3 + 2992.6/T #[KJ/kg]
        return ent/1000. #[J/kg]

    def enthalpygas(self, T):
        """
        Doesn't work, check page 25
        """
        Tc = 2503.7
        Havg = 2128.4 + 0.86496*T
        enthvap = 393.37*(1-(T/Tc)) + 4398.6*(1-T/Tc)**0.29302
        return enthvap/1000. + self.enthalpy(T) #J/Kg

    def liquiddensity(self, T):
        rhoC = 219.
        f = 275.32
        Tc = 2503.7
        g = 511.58
        h = 0.5
        return rhoC + f*(1-T/Tc)+g*(1-T/Tc)**h

    def vapordensity(self, T):
        P = math.exp(7.827 - 11275/T - 4.6192e5/T**2)
        a = -85.768
        b = 24951
        c = 1.2406e-1
        d = -8.3368e-5
        e = 2.6214e-8
        f = -3.0733e-12

        return P*(a/T + b + c*T + d*T**2 + e*T**3 + f*T**4)

    def vaporpressure(self, T):
        return math.e**(11.9463-12633.73/T-0.4672*math.log(T))/10e6


# print (sodium(2000).h)
# print (sodium(2000).hg)
print (sodium(2000).rhog)
print (sodium(2000).rhov)
# print (sodium(2000).vp)
