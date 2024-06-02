import json
import matplotlib
import pandas
import prophet
import time

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

# Ensure the data has the correct columns needed by Prophet library: ds and y, with correct data type
data.rename(columns={config[prediction]['x_column_name']: 'ds', config[prediction]['y_column_name']: 'y'}, inplace=True)
data['ds'] = pandas.to_datetime(data['ds'])

# Create and fit the model, with uncertainty interval 25% to 75%
model = prophet.Prophet(interval_width = 0.5, seasonality_mode=config[prediction]['seasonality_mode'])
model.fit(data)

# Forecast future values
future = model.make_future_dataframe(periods=int(periods), freq=config[prediction]['frequency'])
forecast = model.predict(future)
forecast['ds'] = pandas.to_datetime(forecast['ds'])

# Plot forecast
matplotlib.pyplot.plot(data['ds'], data['y'], label='Observed')
matplotlib.pyplot.plot(forecast['ds'], forecast['yhat'], label='Forecast')
matplotlib.pyplot.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], color='gray', alpha=0.2)
matplotlib.pyplot.show()
