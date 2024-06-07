import datetime as dt
import json
import numpy
import pandas
import time
import math

import matplotlib.pyplot as plt

SIMULATIONS_COUNT = 1000

config = json.load(open('config.json', 'r'))
#prediction = input(f'Choose prediction ({', '.join(config.keys())}): ')
prediction = 'BTC-USD'
#periods = input('Periods to predict: ')
# until end of 2026, works only in 2024
periods = str(730 + (dt.date(dt.date.today().year, 12, 31) - dt.date.today()).days)

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
volatility = [[0 for i in range(SIMULATIONS_COUNT)] for j in range(int(periods))]
for simulation_index in range(SIMULATIONS_COUNT):
    for day_index in range(int(periods)):
        # Use the last known observed value to start simulation. 
        previous = simulation[day_index - 1][simulation_index] if day_index > 0 else data[ycolumn].values[-1]
        index = numpy.random.randint(0, data[ycolumn].size - 1)
        simulation[day_index][simulation_index] = previous + data[ycolumn].values[index + 1] - data[ycolumn].values[index]
        # fix issue with data - there might be a nan for a particular day
        while math.isnan(simulation[day_index][simulation_index]):
            index = numpy.random.randint(0, data[ycolumn].size - 1)
            simulation[day_index][simulation_index] = previous + data[ycolumn].values[index + 1] - data[ycolumn].values[index]
        # volatility in 2025 or 2026 only
        if day_index > int(periods) - 730:
            volatility[day_index][simulation_index] = 100 * math.log(data[ycolumn].values[index + 1] / data[ycolumn].values[index])

# Standard deviation per simulation
deviation = [0 for i in range(SIMULATIONS_COUNT)]
for simulation_index in range(SIMULATIONS_COUNT):
    current_volatility = [row[simulation_index] for row in volatility][-729:] # last 729 elements
    deviation[simulation_index] = numpy.std(current_volatility)

# For each simulation, get 25th percentile, median and 75th percentile for every day
lower_bound = []
median = []
upper_bound = []
for day_index in range(int(periods)):
    lower_bound.append(numpy.percentile(simulation[day_index], 25))
    median.append(numpy.percentile(simulation[day_index], 50))
    upper_bound.append(numpy.percentile(simulation[day_index], 75))

print(numpy.percentile(deviation, 25))
print(numpy.percentile(deviation, 50))
print(numpy.percentile(deviation, 75))

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
