import xlsxwriter
import run
import pandas as pd
import reactor as react
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# systems = run.coreanalyzer()
# analyzed = run.topreactors(systems,1000)

columns = ['ID', 'Points', 'Normalized Temp', 'Normalized Area', 'Normalized Electrical Power',
            'HP Throughput [W]', '# HPs', '# Layers', 'Fuel Cost', 'Fuel Mass [Kg]', 'Max Fuel Temp [K]',
            'Radiator Surf Temp [K]', 'Radiator SA [m^2]',
            'Thermal Power [W]', 'Electrical Power [W]', '# Engines', 'Engine Mass [Kg]',
            'Total Cost [$]', 'Total Mass [Kg]']
id, points, normtemps, normareas, normcosts, normpowers = [], [], [], [], [], [] #Compares
throughput, numpipes, layers, fuelcost, fuelmass, maxfueltemp = [], [], [], [], [], [] #Fuel and HP Props
surftemp, area = [], [] #Radiator Props
thermpower, elecpower, numengines, enginemass = [], [], [], [] #Reactor/Engine Props
totalcost, totalmass = [], []



#for point, sys, normtemp, normarea, normcost, normpower in analyzed:
#    id.append(sys.id)
#    points.append(point)
#    normtemps.append(normtemp)
#    normareas.append(normarea)
#    normcosts.append(normcost)
#    normpowers.append(normpower)
#
#    throughput.append(sys.throughput)
#    numpipes.append(sys.numpipes)
#    layers.append(sys.layers)
#    fuelcost.append(sys.fuelcost)
#    fuelmass.append(sys.fuelmass)
#    maxfueltemp.append(sys.maxfueltemp)
#
#    surftemp.append(sys.surftemp)
#    area.append(sys.area)
#
#    thermpower.append(sys.power)
#    elecpower.append(sys.electricaloutput)
#    numengines.append(sys.numengines)
#    enginemass.append(sys.enginemass)
#
#    totalcost.append(sys.totalcost)
#    totalmass.append(sys.totalmass)

#holddict = {'ID':id, 'Points':points, 'Normalized Temp':normtemps, 'Normalized Area':normareas, 'Normalized Cost': normcosts, 'Normalized Electrical Power':normpowers,
#            'HP Throughput [W]':throughput, '# HPs':numpipes, '# Layers':layers, 'Fuel Cost':fuelcost, 'Fuel Mass [Kg]':fuelmass, 'Max Fuel Temp [K]':maxfueltemp,
#            'Radiator Surf Temp [K]':surftemp, 'Radiator SA [m^2]':area,
#            'Thermal Power [W]':thermpower, 'Electrical Power [W]':elecpower, '# Engines':numengines, 'Engine Mass [Kg]':enginemass,
#            'Total Cost [$]':totalcost, 'Total Mass [Kg]':totalmass}
#
#df = pd.DataFrame(holddict)
#
#writer = pd.ExcelWriter('Evaluated_Systems.xlsx', engine='xlsxwriter')
#
#df.to_excel(writer, sheet_name='Sheet1')
#
#workbook = writer.book
#worksheet = writer.sheets['Sheet1']
#
#def get_col_widths(dataframe):
#    # First we find the maximum length of the index column
#    idx_max = max([len(str(s)) for s in dataframe.index.values] + [len(str(dataframe.index.name))])
#    # Then, we concatenate this to the max of the lengths of column name and its values for each column, left to right
#    return [idx_max] + [max([len(str(s)) for s in dataframe[col].values] + [len(col)]) for col in dataframe.columns]
#
#for i, width in enumerate(get_col_widths(df)):
#    worksheet.set_column(i, i, width)
#
#worksheet.conditional_format('L2:L1000', {'type': '3_color_scale', #Fuel Mass
#                                         'min_color': "green",
#                                         'mid_color': "white",
#                                         'max_color': "red"})
#worksheet.conditional_format('M2:M1000', {'type': '3_color_scale', #Fuel Temp
#                                         'min_color': "green",
#                                         'mid_color': "white",
#                                         'max_color': "red"})
#worksheet.conditional_format('T2:T1000', {'type': '3_color_scale', #Total Cost
#                                         'min_color': "green",
#                                         'mid_color': "white",
#                                         'max_color': "red"})
#worksheet.conditional_format('U2:U1000', {'type': '3_color_scale', #Total Mass
#                                      'min_color': "green",
#                                      'mid_color': "white",
#                                      'max_color': "red"})
#
#
#writer.save()


# workbook = xlsxwriter.Workbook('Evaluated_Systems.xlsx')
# worksheet = workbook.add_worksheet()
#
# #Adds bold format
# bold = workbook.add_format({'bold': True})
#
# worksheet.write('A1', 'System ID', bold)
# worksheet.write('B1', 'Evaluated Points', bold)
# worksheet.write('C1', 'Normalized Fuel Temp', bold)
# worksheet.write('D1', 'Normalized Radiator Area', bold)
# worksheet.write('E1', 'Normalized Total Cost', bold)
# worksheet.write('H1', 'Normalized Power', bold)
#
# #Start at the first cell below the headers
# row = 1
# col = 0
#
# for points, sys, temp, area, cost, power in analyzed:
#     worksheet.write(row,col,sys.id)
#     worksheet.write(row,col+1,points)
#     worksheet.write(row,col+2,temp)
#     worksheet.write(row,col+3,area)
#     worksheet.write(row,col+4,cost)
#     worksheet.write(row, col+5,power)
#     row += 1
#
# workbook.close()

# def throughputvscoresize():
#     radii = range(1, 101) #Radius of the core in cms
#
#     maxthroughputs = [1e3, 2e3, 5e3, 10e3, 20e3, 25e3, 100.e3/3, 50e3, 100e3]
#     # maxthroughputs = [x*10**3 for x in range(1, 101)]
#
#
#     fig = plt.figure()
#     ax = fig.add_subplot(111,projection='3d')
#
#     x,y,z = [], [], []
#     holderlist = []
#     for radius in radii:
#         for maxthroughput in maxthroughputs:
#             hp = react.heatPipe(True, .01, maxthroughput)
#             reac = react.reactor(radius/100)
#             if react.fuel(hp, reac).valid:
#                 maxtemp = react.fuel(hp, reac).maxtemp()
#                 x.append(maxthroughput)
#                 y.append(radius)
#                 z.append(maxtemp)
#                 holderlist.append([hp.maxthroughput, reac.radius, maxtemp])
#
#     x = np.array(x)
#     y = np.array(y)
#     z = np.array(z)
#
#
#     scat = ax.scatter(x, y, z, c=z, marker='o', cmap = 'jet')
#
#     plt.colorbar(scat)
#     # plt.clim(vmin=0, vmax=2000)
#     ax.set_zlim3d(0,2000)
#     ax.set_xlabel('HeatPipe Throughput [W]')
#     ax.set_ylabel('Core Radius [cm]')
#     ax.set_zlabel('Max Fuel Temperature [K]')
#
#     plt.show()

def radiatoranalyzer():

     stirlings = [react.stirling(T_c=x) for x in range(300, 601)]
     reactors = [react.reactor(42, stirlings[x], power=x*10**5) for x in range(1,20)]

     fig = plt.figure()
     ax = fig.add_subplot(111,projection='3d')

     x = []
     y = []
     z = []
     for stirling in stirlings:
         for reactor in reactors:
             x.append(stirling.T_c) #Append Surface Temp
             y.append(reactor.power) #Append Power
             z.append(react.radiator(reactor, stirling).area()) #Append area

     print (len(x), len(y), len(z))
     scat = ax.scatter(x, y, z, c=z, marker='o', cmap = 'jet')

     plt.colorbar(scat)
     # plt.clim(vmin=0, vmax=2000)
     # ax.set_zlim3d(2000)
     ax.set_xlabel('Surface Temperature [K]')
     ax.set_ylabel('Core Power Output [W]')
     ax.set_zlabel('Area of Radiators [m^2]')

     plt.show()
     
radiatoranalyzer() 
