import reactor as react
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# from matplotlib import cm
# from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
import time
plt.style.use('dark_background')
plt.rcParams['figure.facecolor'] = (0., 0., 30/255)

# plt.rcParams['axes.labelsize'] = 16
# plt.rcParams['axes.labelweight', 'axes.titleweight', 'axes.tickweight'] = 'bold'
class system:
    '''
    Build full systems to anaylze
    '''
    def __init__(self, ident, reactor, hp, fuel, emissurf, L_c): #The reactor components
        self.id = ident
        self.reactor = reactor
        self.stirling = self.reactor.stirling
        self.hp = hp
        self.throughput = hp.maxthroughput
        self.fuel = fuel
        self.radiator = react.radiator(self.reactor, self.stirling)

        ###Fuel and HP Properties
        self.numpipes = self.fuel.number
        self.HPmass = self.numpipes*self.hp.mass
        self.layers = self.fuel.layers
        self.hpload = self.fuel.hpload
        self.hpcost = self.hp.cost * self.numpipes #Cost of the heat pipes
        self.fuelcost = self.fuel.fuelcost
        self.fuelmass = self.fuel.mass
        self.maxfueltemp =  self.fuel.maxtemp()
        self.transientTemp = self.fuel.transientTemp()

        ###Radiator Props to Append
        self.radHP = react.heatPipe(False, .0125, self.stirling, L_c = L_c) #2.5 cm diameter
        self.radiativelength = L_c
        self.radiativefin = react.radiativefins(self.radHP, self.reactor, tapered=True, emisssurf=emissurf)
        self.radiativematerial = emissurf
        self.fins = self.radiativefin.finsRequired
        self.radiativearea = self.radiativefin.totalSurfaceArea
        # self.outerraddia = self.radiativefin.outconedia
        # self.innerraddia = self.radiativefin.inconedia
        self.width = self.radiativefin.w
        self.D = self.radiativefin.D
        self.radmaxtemp = self.radiativefin.transienttemp
        self.radiativemass = self.radiativefin.totalMass
        self.radiativecost = self.radiativefin.totalcost
        self.radiativespmass = float(self.radiativefin.alpha)

        ###Reflector Props to Append
        # self.reflector = self.reactor.ref
        self.maxtemp = 0
        self.reflectormass = reactor.refmass
        self.structuralmass = reactor.strmass
        self.bothmass = self.reflectormass + self.structuralmass
        self.reflectorcost = reactor.reftotalcost

        ###Reactor Props to append
        self.power = self.reactor.power
        self.electricaloutput = self.reactor.electricaloutput
        self.numengines = self.reactor.numengines
        self.enginecost = self.reactor.enginecost
        self.enginemass = self.stirling.specificmass * self.electricaloutput

        self.totalcost = self.enginecost + self.hpcost + self.fuelcost + self.reflectorcost + self.radiativecost
        self.totalmass = self.enginemass + self.fuelmass + self.HPmass + self.bothmass + self.radiativemass
        self.specificmass = self.totalmass/self.electricaloutput


def is_valid(sys):

    fuel = sys.fuel
    fuelMP = fuel.MP
    HPMP = sys.hp.MP
    reflMP = min([sys.reactor.strucMP, sys.reactor.MP])

    if sys.transientTemp > fuelMP*0.8 or sys.transientTemp > HPMP*0.8 or sys.radmaxtemp > HPMP*0.8:
        return False

    if sys.maxfueltemp > fuelMP*0.8 or sys.maxfueltemp*0.5 > reflMP:
        # print ('here')
        return False


    if fuel.fuelwidth < 0.02:
        # print ('2')
        return False

    if sys.totalmass > 8000: #Falcon Heavy Payload
        # print ('3')
        return False

    if sys.numengines > 42: #Don't have more stirlings
        # print ('4')
        return False
    # if sys.area >

    return True

def coreanalyzer():
    """
    This is where we build all of the possible core configurations
    As of 11/12/18, no variables to feed in as it builds all every single
    time but maybe in the future, add some variablility to which get tested.
    Returns: List of all VALID system configurations
    """

    core_radii = [x/100 for x in range(17, 18)] #Range should be size in cm as it gets divided by 100
    core_powers = [x*10**5 for x in range(4,5)] #Core thermal power ranges
    maxthroughputs =  [20e3]#[1e3, 2e3, 5e3, 10e3, 20e3, 25e3, 100.e3/3, 50e3, 100e3]#Throughputs of the various heatpipes
    # stirlings = [react.stirling(T_c=x) for x in range(500, 550)] #Cold end temp of the stirling engine
    stirlings = [react.stirling(), #Default reactor
                  # react.stirling(maxpower=6e3, T_h=830, T_c=415, eta=0.25, specificmass=.005, enginecost=1e1), #2010 Reactor
                 ]

    ### Uncomment line below for list of all reactors to consider
    # print (len(core_radii)*len(core_powers)*len(maxthroughputs)*len(stirlings))

    reactors = []
    for radius in core_radii:
        for reactorpower in core_powers:
            for stirling in stirlings:
                for strmaterial in react.structdict.keys():
                    for refmaterial in react.reflectdict.keys():
                        for emisssurf in react.radiativeSurfProps.keys():
                            reactors.append(react.reactor(radius, stirling, power=reactorpower, refmat=refmaterial, strmat=strmaterial))

    validreactors =[]
    L_cs = [x/100 for x in range(200, 410, 10)]
    print ('Num of Reactors: ',len(reactors)*len(L_cs))
    counter = 0 #This is used to track the ID number of the reactor
    for reactor in reactors[:]:
        for throughput in maxthroughputs[:]:
            for emisssurf in react.radiativeSurfProps.keys():
                for L_c in L_cs:
                    stirling = reactor.stirling
                    hp = react.heatPipe(True, .01, stirling, throughput=throughput)
                    fuel = react.fuel(hp, reactor)
                    sys = system(counter, reactor, hp, fuel,'C-C', L_c)

                    if is_valid(sys):
                        validreactors.append(sys) #Reactor Properties [12]
                        counter += 1

    print ('Num of Valid Reactors: ',len(validreactors))
    return validreactors

def radiatorcamparison(reactors):
    core_radii = .34
    maxthrough = 20e3
    corepower = 400e3
    L_cs = []
    costs = []
    specificmasses = []
    num = []



    for sys in reactors:
        L_cs.append(sys.radiativelength)
        costs.append(sys.radiativecost)
        specificmasses.append(sys.radiativespmass)
        num.append(sys.fins)
#        print (sys.radiativematerial)

    fig = plt.figure()
    ax = fig.add_subplot(111, )

    maxLc = max(L_cs)
    maxcost = max(costs)
    maxalpha = max(specificmasses)

    x = [x/1 for x in L_cs]
    y = [x/1 for x in costs]
    z = [x/1 for x in specificmasses]
    a = [x/1 for x in num]

    xval = 0
    yval = 0
    for i in range(len(x)):
        if x[i] != 3.:
            plt.plot(a[i], x[i], 'co')
        else:
            xval = a[i]
            yval = x[i]
            plt.plot(a[i], x[i], 'ro')
    plt.vlines(xval, 2.1, yval, 'r')
    plt.hlines(yval, 52, xval, 'r')
    plt.tick_params(labelsize=15)
    # plt.plot(a, x, 'o')

    plt.xlabel('Number of Radiative Fins Required', fontsize=15, weight='bold')
    plt.ylabel('Length of Condensing Section [m]', fontsize=15, weight='bold')
    plt.title('Length of Radiating Section versus Number of Fins', fontsize=15, weight='bold')
    # ax.tick_params(grid_linewidth=4)

    ax.set_facecolor((0/255, 0/255, 30/255))

    plt.show()


def topreactors(reactors, toreturn):
    """
    This function is what weights the configurations based on a variety
    of parameters
    reactors: list - of all the reactors to compare (recommend only comparing valid reactors)
    toreturn: int - # of reactors to return in a list type form
    Returns: List of best reactors
    """
    validreactors = reactors
    # print (validreactors)
    ###Method below is faster than building a bunch of lists from one for loop
    ### and sorting all of them
    absolutemaxtemp = max([sys.maxfueltemp for sys in validreactors])
    # absolutemaxarea = max([sys.area for sys in validreactors])
    absolutemaxcost = max([sys.totalcost for sys in validreactors])
    absolutemaxpower = max([sys.electricaloutput for sys in validreactors])
    maxspecficmass = max([sys.specificmass for sys in validreactors])


    print ('Most expensive core config cost: $',absolutemaxcost)


    bestrigs = []
    ### The for loop below normalized all variables of interest
    for sys in validreactors:
        normtemp = sys.maxfueltemp/absolutemaxtemp
        normarea = 1#sys.area/absolutemaxarea
        normcost = sys.totalcost/absolutemaxcost
        normpower = 1 - sys.electricaloutput/absolutemaxpower # We want more power so do 1 - norm
        normspmass = sys.specificmass/maxspecficmass


        ### A higher score is a lower quality reactor

        # points = normtemp + normarea + normcost + normpower + normspmass
        points = normspmass
        bestrigs.append((points, sys, normtemp, normarea, normcost, normpower, normspmass))

        # points = normspmass
        # bestrigs.append((points, sys, normcost, normspmass))

    ###Sorts all reactors based on the points, lower points is better
    bestrigs.sort(key=lambda x: x[0])

    ### Returns the number set by a user in a list form
    return bestrigs[:toreturn]

def pprint(reactors):
    """
    This function prints all of the reactors in reactors
    in a more user-readable fashion.
    """

    # for value, sys, cost, spmass in reactors:
    for value, sys, temp, area, cost, power,spmass in reactors:
        print ('')
        print ('This reactor had a score of: ',value)
        print ('Reactor Thermal Output: ', sys.power/1000, 'KW with a diameter of: ',sys.reactor.dia*100,'cm')
        print ('Electrical Output is: ', sys.electricaloutput/1000, 'KWe with ', sys.numengines, 'engines.')
        print ('--------------------------------------------------------------')
        print ('Reflector Material: ',sys.reactor.refmaterial, ', Structural Material:', sys.reactor.strmaterial)
        print ('The Reflector system mass is: ', sys.reflectormass,'and cost: $', "{0:.2f}".format(sys.reflectorcost))
        print ('HP Throughput was: ',sys.throughput/1000,'KW. This led to:', sys.layers,'layers, with ', sys.numpipes, ' heatpipes.')
        print ('The max space between heat pipes was: ',sys.fuel.fuelwidth*100, 'cm')
        print ('The max fuel temp was: ', int(sys.maxfueltemp), 'K')
        print ('The weight of fuel was: ', int(sys.fuelmass), "Kg, which cost: $", int(sys.fuelcost))
        print ('--------------------------------------------------------------')
        print ('There is a total of : ',sys.fins, 'radiative fins. This led to a surface area of: ',int(sys.radiativearea),'m^2')
        print ('The fins are made of: ',sys.radiativematerial)
        print ('The radiative length is: ', sys.radiativelength, 'm.')
        print ('The radiative width is: ',sys.width)
        print ('The radiative depth is: ', sys.D/2)
        # print ('The outer radiative cone diameter is: ', "{0:.2f}".format(sys.outerraddia), 'm. The inner cone diameter is: '"{0:.2f}".format(sys.innerraddia), 'm.')
        print ('The mass of the radiative system is: ', int(sys.radiativemass),'kg.  It costs: $', int(sys.radiativecost))
        print ('--------------------------------------------------------------')
        print ('Total System Mass is: ', int(sys.totalmass), "Kg, and costs: $", int(sys.totalcost))  #Doesn't include radiator mass or HPs
        print ('Transient Temp: ',int (sys.transientTemp))
        print ('Specific Mass is: ', "{0:.2f}".format(sys.specificmass*1000),'kg/KWe')
        print ('====================================================')


if __name__=='__main__':
    # throughputvscoresize()

    # radiatorcamparison(coreanalyzer())
    pprint(topreactors(coreanalyzer(), 3))
    # best = topreactors(coreanalyzer(), 1)[0][1]
    # print (best)
    # print (best.fuel.longestdist)
    # print (topreactors(coreanalyzer(), 1))
#     radiatoranalyzer()
