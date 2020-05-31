import math
from sympy.solvers import solve
from sympy import Symbol, nsolve
from scipy.optimize import fsolve

pi = math.pi
INF = math.inf

reflectdict = {'ZrSi':{'rho': 5880, 'MP':2580, 'cost':320}, #From Short's Paper

                            }
structdict = {#'Al': {'rho':2700, 'MP':933.5, 'cost':1.92},  #From Wikipedia, in $/Kg
             'Ti': {'rho':4506, 'MP':1941., 'cost':17},
            #'Nb': {'rho':8570, 'MP':2750, 'cost':165.35},
            }

radiativeSurfProps = {'Al':{'emiss': 0.85, 'rho':2700, 'k':257, 'mu':.334, 'cost':1.92},
                      'C-C': {'emiss':0.85, 'rho':1218, 'k':1000,'mu':.217, 'cost':10000},
                      #'Be': {'emiss':0.85, 'rho':1800, 'k': 200, 'mu':.263, 'cost':0},
                      }

fuelProps = {'UN': {'k': 25., 'MP': 3000, 'rho': 13500}}

HPmaterialProps = {'Nb-1%Zr': {'k':52.3, 'rho': 8600, 'MP':2683}} 
workingFluids = {'Li': {'P': 3.19e3, 'L':18670, 'sigma':0.212, 'rhov':.2839,
                        'rhol': 380.9, 'muv':1.59e-5, 'mul':1.423e-4, 'K':73.0},
                'Na': {'P': 0, 'L': 0, 'sigma': 0, 'rhov': 0 ,
                        'rhol': 0, 'muv': 0, 'mul': 0, 'k': 0}
                }

class reactor:
    '''
    Initialize our reactor
    '''
    def __init__(self, radius, stirling, height = .42, power=500e3, APPF=1.25, RPPF=1.77,
                    refmat = 'ZrSi', strmat='Al', radmat = 'C-C'):
        '''
        Initialize the key constraints of our reactor.
        We're shooting for 500 KWt
        '''
        self.radius = radius
        self.dia = radius*2
        self.height = height

        self.power = power
        self.APPF = APPF
        self.RPPF = RPPF

        self.stirling = stirling
        self.numengines = math.ceil(self.power/self.stirling.Qdot) #Finds the number of engines
        self.electricaloutput = self.numengines*self.stirling.electricaloutput
        self.enginecost = self.numengines*self.stirling.enginecost

        self.drumradius = self.radius/2

        self.refmaterial = refmat
        self.refmaterialdict = reflectdict[refmat]
        self.rho = self.refmaterialdict['rho']
        self.MP = self.refmaterialdict['MP']
        self.cost = self.refmaterialdict['cost']
        self.refvolume = 6*self.height*pi*self.drumradius**2*(1/3) #Reflector is 1/3 volume of drum, with 6 drums
        self.refmass = self.rho*self.refvolume #Get mass of reflector
        self.refcost = self.cost*self.refmass

        self.strmaterial = strmat
        self.strmaterialdict = structdict[strmat]
        self.strucrho = self.strmaterialdict['rho']
        self.strucMP = self.strmaterialdict['MP']
        self.coststr = self.strmaterialdict['cost']
        self.strvolume = 6*self.height*pi*self.drumradius**2*(2/3) #Str material is 2/3 volume of drum, ""
        self.strmass = self.strvolume*self.strucrho
        self.strcost = self.coststr*self.strmass


        self.reftotalmass = self.refmass + self.strmass
        self.reftotalcost = self.refcost + self.strcost

    def qprimemax(self, numPipes):
        return self.APPF*self.RPPF*(self.power/(numPipes*self.height))

    def qprime(self, numPipes):
        return self.power/(numPipes*self.height)


class stirling:

    def __init__(self, maxpower=25e3, T_h=1050, T_c=525, eta=0.25,
                specificmass=7.07/1000, enginecost=1e6):
        '''
        Initialize the stirling engine.  This is
        one of our main design contraints, so unlikely to change
        much here except possibly an equation for efficiency
        '''
        self.T_h = T_h #Hot end temp
        self.T_c = T_c #Cold end temp
        self.eff = eta #Efficiency
        self.electricaloutput = maxpower #Electrical Output
        self.Qdot = self.electricaloutput/self.eff #Converts to thermal power of stirling engine
        self.specificmass = specificmass #Kg/W
        self.enginecost = enginecost





class heatPipe:

    def __init__(self, HotorCold, radius, stirling, throughput=10e3, material='Nb-1%Zr', thickness=.002,
                        workingfluid = 'Li', cost = 1e4, L_h = .42, L_c = .2):
        '''
        Initialize the heat pipe
        HotorCold: Boolean,     if true, grab hot temp from stirling
                                    otherwise, grab cold temp
        radius: int or float,   pipe outer radius [m]
        '''
        self.engine = stirling
        self.radius = radius
        self.thick = thickness
        self.ri = self.radius-self.thick
        self.length = 1.00 #1 m long heat pipe
        self.L_h = L_h
        self.L_adia = .20
        self.L_c = L_c
        self.annuluswidth = 0.0005 #0.5mm annulus
        self.rv = self.ri-self.annuluswidth
        self.leff = self.L_adia+0.5*self.L_h+0.5*self.L_c
        self.innerarea = pi*self.radius**2

        # print (2*pi*self.radius*self.L_h)


        self.material = material
        self.k = HPmaterialProps[self.material]['k']
        self.HPRho = HPmaterialProps[self.material]['rho']
        self.MP = HPmaterialProps[self.material]['MP']
        self.mass = pi*(self.radius**2-(self.radius-self.thick)**2)*self.length*self.HPRho

        self.workingfluid = workingfluid
        self.P = workingFluids[self.workingfluid]['P'] #Vapor Pressure [Pa]
        self.L = workingFluids[self.workingfluid]['L'] #Latent heat [J/kg]
        self.sigma = workingFluids[self.workingfluid]['sigma'] #surface tension [N/m]
        self.rhov = workingFluids[self.workingfluid]['rhov'] #vapor density [kg/m3]
        self.rhol = workingFluids[self.workingfluid]['rhol'] #liquid density [kg/m3]
        self.muv = workingFluids[self.workingfluid]['muv'] #vapor viscosity [Ns/m2]
        self.mul = workingFluids[self.workingfluid]['mul'] #liquid viscosity [Ns/m2]
        # self.K = workingFluids[self.workingfluid]['K'] #Permeability [W/mk]
        self.K = .302e-10

        if HotorCold: self.operatingtemp = self.engine.T_h + 150
        else:   self.operatingtemp = self.engine.T_c

        self.maxthroughput = throughput #Max at 10 KW

        self.cost = cost

    def resistance(self):
        rHPi = self.radius - self.thick
        rHPo = self.radius

        return (1/(2*pi*self.k))*math.log(rHPo/rHPi)

# print (heatPipe(True, .01).mass)


class fuel:
    def __init__(self, heatpipe, thisreact, fueltype='UN', cost = 17600):
        '''
        Initialize the fuel and the operating temp of
        the heat pipes
        heatpipe: heatPipe object,  to represent the heatpipes
        react: reactor object,      to represent the reactor
        fueltype: str,              to represent type of fuel
        '''
        self.dia = thisreact.dia
        self.reactor = thisreact
        self.HP = heatpipe


        self.number, self.layers = self.findheatpipes()
        self.hpload = self.reactor.power/self.number
        self.fuelwidth = self.dimcore() #The distances between heatpipes
        self.longestdist = self.fuelwidth/2 #Finds the fuel farthest from a heat pipe

        self.fuel = fueltype
        self.k = fuelProps[self.fuel]['k']
        self.density = fuelProps[self.fuel]['rho']
        self.MP = fuelProps[self.fuel]['MP']
        self.enrichcost = cost
        self.mass, self.fuelcost = self.mass_cost()

    def findheatpipes(self):
        '''
        Finds the number of heat pipes based on their max
        thermal capacity
        '''
        maxthrough = self.HP.maxthroughput
        number = 1
        hpload = self.reactor.power/number
        toadd = 6
        counter = 1
        while hpload > maxthrough:
            number = number + toadd
            toadd = toadd + 6
            counter += 1
            hpload = self.reactor.power/number

        return number, counter

    def dimcore(self):
        '''
        Finds the space between the heat pipes
        Returns: int or float,      represents distance between hps
        '''
        hps_across = self.layers*2-1
        numspaces = self.layers*2
        leftoverroom = self.dia-hps_across*self.HP.radius*2
        spacebetweenpipes = leftoverroom/numspaces
        return spacebetweenpipes

    def resistance(self):
        '''
        Calculates thermal resistance of the fuel,
        IMPORTANT: 0 coord is the center of the HP which is
        why the numerator adds the radius of the HP
        '''
        return (1/(2*pi*self.k))*math.log((self.longestdist+self.HP.radius)/self.HP.radius)

    def maxtemp(self):

        resFuel = self.resistance()
        resPipe = self.HP.resistance()
        opTemp = self.HP.operatingtemp
        qprimemax = self.reactor.qprimemax(self.number)

        return opTemp+qprimemax*(resFuel+resPipe)

    def volume(self):
        s = self.dia * math.sin(math.radians(30))
        a = self.dia/2 * math.cos(math.radians(30))
        surfarea = 0.5 * (s*6) * a
        fuelarea = surfarea - self.number*(pi*self.HP.radius**2)
        return fuelarea * self.reactor.height

    def mass_cost(self):
        volume = self.volume()
        mass = volume * self.density #Mass in Kg
        return mass, mass*self.enrichcost

    def transientTemp(self):
        qprimemax = self.reactor.qprimemax(self.number-1)
        #Distance to HPs is doubled
        # print (self.longestdist*2)
        resFuel = (1/(2*pi*self.k))*math.log((self.longestdist*2+self.HP.radius)/self.HP.radius)
        resPipe = self.HP.resistance()
        opTemp = self.HP.operatingtemp

        return opTemp + qprimemax*(resFuel+resPipe)

    def __str__(self):
        first = 'Number of Heat Pipes: '+ str(self.number)
        second = 'Layers: '+str(self.layers)
        third = 'Spacing between pipes: '+str(self.fuelwidth)
        fourth = 'Pipe Throughput: '+str(self.HP.maxthroughput)
        return first+'\n'+second+'\n'+third+'\n'+fourth

class radiativefins:
    def __init__(self, HP, react, tapered=True, emisssurf = 'C-C', numfails = 1):
        self.SB = 5.67e-8
        self.hp = HP
        self.T_o = self.hp.operatingtemp
        self.W = self.hp.radius*2
        self.L = self.hp.L_c
        self.reactor = react
        self.heatToDissipate = self.reactor.power*(1-self.reactor.stirling.eff)
        # print (self.heatToDissipate)
        # print ('L: ', self.L)
        # print ("W: ", self.W)
        # print ("T_o: ", self.T_o)

        self.material = radiativeSurfProps[emisssurf]
        self.emiss = self.material['emiss']
        self.rho = self.material['rho']
        self.cond = self.material['k']
        self.mu = self.material['mu']
        self.matcost = self.material['cost']

        self.R = self.RSolver(tapered)[0]
        if tapered: self.beta = .8825
        else: self.beta = 0.919
        self.w = self.width(tapered)
        self.D = self.depth(tapered)
        self.mass = self.M(tapered)
        self.QM = self.QperM(tapered)
        self.QperFin = self.QM*self.mass
        # print ('R: ', self.R)
        # print ('Width: ',self.w)
        # print ('Depth: ',self.D)
        # print ('Mass: ', self.mass)
        # print ('QperM: ',self.QM)
        # print ('QperFin: ', self.QperFin)
        self.finsRequired = int(self.heatToDissipate/self.QperFin)+1 #Takes Ceiling
        # print ('Number of Fins Required: ', self.finsRequired)
        self.SurfaceAreaperFin = self.SurfaceArea()
        self.MA = self.mass/self.SurfaceAreaperFin
        # print ('M/A: ', self.MA)
        self.totalSurfaceArea = self.finsRequired*self.SurfaceAreaperFin
        # print ('Surface Area per fin: ', self.SurfaceAreaperFin)
        # print ('Total Surface Area: ', self.totalSurfaceArea)
        self.totalMass = self.mass*self.finsRequired
        self.alpha = self.totalMass/self.reactor.electricaloutput
        # print ('Total Mass: ', self.totalMass)
        # print ('Alpha: ', self.alpha)
        self.totalcost = self.finsRequired * (self.hp.cost + self.matcost)
        self.transienttemp = self.maxtemp(numfails)

    def RSolver(self, tapered):

        if tapered:
            bigterm = (self.rho*self.SB*self.emiss*self.T_o**3)/(4*self.mu*self.cond)
            R = Symbol('R')
            return solve((2*R-1+6.188*bigterm**(1/3)*self.W*R**(2/3)), R)
        else:
            bigterm = (self.rho*self.SB*self.emiss*self.T_o**3)/(2*self.mu*self.cond)
            R = Symbol('R')
            return solve((2*R-1+5.609*bigterm**(1/3)*self.W*R**(2/3)),R)

    def QperM(self, tapered):
        first = (2*self.SB*self.emiss*self.T_o**4)/(self.mu*(1+self.R))
        second = (2*self.mu*self.cond*self.R)/(self.rho*self.SB*self.emiss*self.T_o**3)
        if tapered:
            return first*(second**(1/3)*0.6110+self.W)
        else:
            return first*(second**(1/3)*0.5348+self.W)

    def depth(self, tapered):

        first = ((self.mu*self.R)/(2*self.rho*self.beta))**(2/3)
        second = ((2*self.SB*self.emiss*self.T_o**3)/(self.cond))**(1/3)
        return first*second

    def width(self, tapered):
        first = ((self.mu*self.R)/(2*self.rho*self.beta))**(1/3)
        second = ((self.cond)/(2*self.SB*self.emiss*self.T_o**3))**(1/3)
        return self.beta*first*second

    def M(self, tapered):
        return self.L*(self.mu+2*self.rho*self.w*self.D)

    def SurfaceArea(self):
        return self.L*(2*self.w+self.W)
    
    def maxtemp(self, numfails):
        Q = self.heatToDissipate #Thermal power that will always need to be dissipated
        fins = self.finsRequired
        initialtemp = self.T_o
        R = initialtemp/(Q/fins)

        return (Q/(fins-numfails))*R





class radiator:
    def __init__(self, thisreactor, thisstirling, emissivesurf = 'Al', T_amb = 3):
        self.reac = thisreactor
        self.stirl = thisstirling
        self.T_surf = self.stirl.T_c
        self.T_space = T_amb

        self.material = radiativeSurfProps[emissivesurf]
        self.emiss = self.material['emiss']

    def area(self):
        SB = 5.67e-8
        area = self.reac.power/(self.emiss*SB*(self.T_surf**4-self.T_space**4))
        return (area)



if __name__ == '__main__':
    # radii = range(1, 101)
    react = reactor(0.17, stirling(T_c=800), power=400e3)

    # stirl = stirling()
    hp = heatPipe(False, .0125,stirling(T_c=800), L_c=.914)
    # ex = fuel(hp, react)
    # print (radiativefins(hp,emisssurf='C-C').QperM)
    radiativefins(hp, react, emisssurf='C-C', tapered=False)
    # print (ex.maxtemp())
    # print (ex.volume())
