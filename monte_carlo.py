import json
import numpy
import pandas

import matplotlib.pyplot as plt

SIMULATIONS_COUNT = 1000

config = json.load(open('config.json', 'r'))
prediction = 'KP'
periods = '120'

# Load data from space delimited file, ignore first rows(comments)
filename = config[prediction]['file']
data = pandas.read_fwf(filename, skiprows=29)

# Remove data with value Kp of -1
xcolumn = 0
ycolumn = 8
for index in range(len(data) - 1, -1, -1):
    if data.values[index][ycolumn] < 0:
        data.drop(index, inplace = True, axis = 0)

# Simulation - for every day, add a random daily diff from the observed values
simulation = [[0 for i in range(SIMULATIONS_COUNT)] for j in range(int(periods))]
for simulation_index in range(SIMULATIONS_COUNT):
    for day_index in range(int(periods)):
        # Use the last known observed value to start simulation. 
        previous = simulation[day_index - 1][simulation_index] if day_index > 0 else data.values[-1][ycolumn]
        index = numpy.random.randint(0, len(data) - 1)
        simulation[day_index][simulation_index] = previous + data.values[index + 1][ycolumn] - data.values[index][ycolumn]
        if simulation[day_index][simulation_index] < 0:
            simulation[day_index][simulation_index] = 0
        if simulation[day_index][simulation_index] > 9:
            simulation[day_index][simulation_index] = 9

# Interpret the data somehow and create a forecast. Issue: limited data, containing and extraordinary event.
# More data, for multiple years: https://www.spaceweatherlive.com/en/auroral-activity/top-50-geomagnetic-storms/year/2024.html 

# Plot observed data
plt.plot(range(len(data)), data.iloc[:,ycolumn - 1], label='Observed')
plt.show()
