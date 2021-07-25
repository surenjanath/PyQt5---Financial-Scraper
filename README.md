# PyQt5 - Financial Scraper! 

This app created to view financial data given a search query of Nasdaq codes:

## Start

- You can clone it and use it at your own discretion
- Please [open an issue](https://github.com/surenjanath/PyQt5_Financial_Scraper/issues/new) if anything is missing or unclear in this
  documentation.

## Installation

In order to use this to it's full potential: Must have pyqt5 and python 3.9.6

Using pyqt5-tools designer in cmd to execute the pyqt5 designer application to edit the UI file

If you're looking at the code then it means that you're good at using python .: edit away.

To execute program just type the following in cmd :
```
python main.py
```
NB : Must have pyqt5 installed 

Alternatively, to run designer just type ` pyqt5-tools designer` in cmd.

To convert ui to py 

```
pyuic5 -x [ui file].ui -o [ui].py
```
## To convert .py to .exe
Install pyinstaller 
```pip install pyinstaller```

Then navigate to [This folder](https://github.com/surenjanath/PyQt5_Financial_Scraper/Convert_to_EXE)
and open cmd .
Run the following code : 

```
pyinstaller --onefile --windowed --icon=app.ico [filename main].py
```

## Troubleshooting & debugging

- If it freezes , check your internet connection
- If lags , give it a few seconds.

## Resources

