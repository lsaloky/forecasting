import json
import matplotlib
import pandas
import prophet
import time

config = json.load(open('config.json', 'r'))
prediction = input(f'Choose prediction ({', '.join(config.keys())}): ')
periods = input('Periods to predict: ')

# Load data from CSV
filename = config[prediction]['file'].format(int(time.time()) - int(config[prediction].get('timespan_days', 0)) * 24 * 3600, int(time.time()))
data = pandas.read_csv(filename)

# Ensure the data has the correct columns needed by Prophet library: ds and y, with correct data type
data.rename(columns={config[prediction]['x_column_name']: 'ds', config[prediction]['y_column_name']: 'y'}, inplace=True)
data['ds'] = pandas.to_datetime(data['ds'])

# Create and fit the model, with uncertainty interval 25% to 75%
model = prophet.Prophet(interval_width = 0.5, changepoint_range = 0.9, changepoint_prior_scale = 0.1, seasonality_mode=config[prediction]['seasonality_mode'])
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
