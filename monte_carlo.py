import json
import numpy
import pandas
import time

import matplotlib.pyplot as plt

SIMULATIONS_COUNT = 1000

config = json.load(open('config.json', 'r'))
prediction = input(f'Choose prediction ({', '.join(config.keys())}): ')
periods = input('Periods to predict: ')

# Load data from CSV, allowing to specify timespan in URL, if configured (timespan_days)
if 'timespan_days' in config[prediction].keys():
    filename = config[prediction]['file'].format(int(time.time()) - int(config[prediction].get('timespan_days', 0)) * 24 * 3600, int(time.time()))
else:
    filename = config[prediction]['file']
    
# Filter the data, if configured (filter_by and filter_value)
if 'filter_by' in config[prediction].keys() and 'filter_value' in config[prediction].keys():
    unfiltered_data = pandas.read_csv(filename)
    data = unfiltered_data[unfiltered_data[config[prediction]['filter_by']] == config[prediction]['filter_value']]
else:
    data = pandas.read_csv(filename)

xcolumn = config[prediction]['x_column_name']
ycolumn = config[prediction]['y_column_name']

# Simulation - for every day, add a random daily diff from the observed values
simulation = [[0 for i in range(SIMULATIONS_COUNT)] for j in range(int(periods))]
for simulation_index in range(SIMULATIONS_COUNT):
    for day_index in range(int(periods)):
        # Use the last known observed value to start simulation. 
        previous = simulation[day_index - 1][simulation_index] if day_index > 0 else data[ycolumn].values[-1]
        index = numpy.random.randint(0, data[ycolumn].size - 1)
        simulation[day_index][simulation_index] = previous + data[ycolumn].values[index + 1] - data[ycolumn].values[index]

# For each simulation, get 25th percentile, median and 75th percentile for every day
lower_bound = []
median = []
upper_bound = []
for day_index in range(int(periods)):
    lower_bound.append(numpy.percentile(simulation[day_index], 25))
    median.append(numpy.percentile(simulation[day_index], 50))
    upper_bound.append(numpy.percentile(simulation[day_index], 75))

# Prepare future values in a new DataFrame
forecast = pandas.DataFrame({
    xcolumn: pandas.date_range(start=data[xcolumn].iloc[-1], periods=int(periods), freq=config[prediction]['frequency']),
    'lower': lower_bound,
    ycolumn: median,
    'upper': upper_bound
})
forecast[xcolumn] = [str(i.date()) for i in pandas.to_datetime(forecast[xcolumn])]

# Plot forecast
plt.plot(data[xcolumn], data[ycolumn], label='Observed')
plt.plot(forecast[xcolumn], median, label='Forecast')
plt.fill_between(forecast[xcolumn], forecast['lower'], forecast['upper'], color='gray', alpha=0.2)
plt.show()
