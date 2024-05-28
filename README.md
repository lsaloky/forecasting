## Initial setup of an environment

1. Install VS Code
If you haven't already installed Visual Studio Code, you can download it from [here](https://code.visualstudio.com/Download).

2. Install Python
Make sure you have Python installed on your machine. You can download it from [here](https://www.python.org/downloads/).

3. Install the Python Extension for VS Code
To enhance your Python development experience, you should install the Python extension for VS Code:
   - Open VS Code.
   - Go to the Extensions view by clicking on the Extensions icon in the Activity Bar on the side of the window or by pressing Ctrl+Shift+X.
   - In the search box, type "Python" and install the extension published by Microsoft.

4. Open This Project Directory in VS Code
   - Open VS Code.
   - Click on File > Open Folder....
   - Navigate to the directory which contains this file and select it.

5. Set Up a Virtual Environment (Optional but Recommended)
Setting up a virtual environment helps to manage dependencies for your project. Here’s how to create and activate a virtual environment:
   - Open the terminal in VS Code by selecting Terminal > New Terminal or pressing `Ctrl+``.
   - Navigate to your project directory in the terminal.
   - Run the following command to create a virtual environment: python -m venv venv
   - If the previous command fails due to PowerShell execution policy (Windows only):
   - run PowerShell as an administrator,
   - type a command (Windows only): Set-ExecutionPolicy Unrestricted
   - Activate the virtual environment (Windows only): .\venv\Scripts\activate
   - Alternative for macOS / Linux: source venv/bin/activate

6. Configure the Python Interpreter
   - Open the command palette by pressing Ctrl+Shift+P.
   - Type and select Python: Select Interpreter.
   - Choose the interpreter from your virtual environment (it should be something like .\venv\Scripts\python.exe or ./venv/bin/python).

7. Installing Packages
   - To install packages listed in your requirements.txt, run the following command in the terminal: pip install -r requirements.txt

8. Run Your Python Code
You can run your code directly in VS Code:
   - Open linear.py.
   - Press F5 to start debugging and run your code, or right-click inside the file and select Run Python File in Terminal.

## Run an application

For time series forecasting, run time_series.py. You need to specify what to predict and periods. You can choose from a predefined list of predicitions configured in config.json.

Example: predict 'BTC' with 30 periods will predict BTC price for 30 days in advance.

## Configure a new data source

Datasource must be in CSV format, with header row specifying column names.

In config.json, add a new JSON key with attributes:

   - x_column_name: column name for x axis, must contain date values
   - y_column_name: column name for y axis
   - frequency: B = business day, D = calendar day, W = weekly, M = monthly, Q = quarterly, Y = yearly, h = hourly
   - seasonality_mode: use `additive` for data which are not dependent on seasonality, otherwise `multiplicative`
   - timespan_days: optional, must be supported by data source. Historical data for days specified will be downloaded. Data source must accept Unix tiestamp values.

Example:

```
"MyNewDataDource": {
    "file": "https://mydatasource.com?from={}&to={}",
    "x_column_name": "Date",
    "y_column_name": "MyValue",
    "frequency": "D",
    "seasonality_mode": "additive",
    "timespan_days": "365"
}
```
