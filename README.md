# MeoPrevi
Python script that displays the **timeline** of excepted satellites above **Calern** in a browser.


The timeline is generated for a week, and zooms in automatically at startup at UTC current time, for 2 hours.
You can change the time span, and select which satellites to display in the timeline in the right column.

## Installation

To install this script, use the github repo with
```bash
sudo git -C /opt clone https://github.com/atxr/MeoPrevi; sudo /opt/MeoPrevi/INSTALL.sh
```

Otherwise, if you have the archive, extract it with the command
```bash
sudo unzip path/to/the/archive -d /opt; sudo /opt/MeoPrevi/INSTALL.sh
```

## Usage

Before using the script, geckodriver, a dependency of selenium must be placed in the PATH.
The release of geckodriver can be [downloaded here](https://github.com/mozilla/geckodriver/releases)

If you use Linux x64, you can simply use this command to download and add geckodriver to your path
```bash
wget 'https://github.com/mozilla/geckodriver/releases/download/v0.29.1/geckodriver-v0.29.1-linux64.tar.gz'; sudo tar -xf geckodriver-v0.29.1-linux64.tar.gz -C /usr/bin
```

Then, to launch the script, execute 
```bash
/opt/MeoPrevi/previ.py
```
It should automatically open a new tab in the default browser.
If not, browse directly the link the terminal will print, usually http://127.0.0.1:8050
If you got trouble with the script, check the dependencies section at the end.

## Add satellites

The script provide a tool for adding a satelitte directly with its Spacetrack catalog number. Visit the [following website](https://heavens-above.com/Satellites.aspx) to find Spacetrack catalog numbers of the satellite you want to add.

## List of satellites
Different lists of satellites can be found in the data directory. 
The one used by default is data/maj\_sats.data. 
List of available database:
- data/maj\_sats.data: most important satellites, according with the [ILRS priority list](https://ilrs.gsfc.nasa.gov/missions/mission_operations/priorities/index.html)
- data/sats.data: most of the observable satellites from Calern. Warning, because of the length of this database, the display may be bad.
- data/galileo.data: all Galileo GNSS European satellites

If you want to change the database, modify at the beginning of previ.py the line 
```python
import maj_sats.py
```
with the name of the correct database.


## Dependencies

Firefox
Geckodriver for selenium. CF installation section.

Python3 and the following modules:
- pandas
- plotly (and its own dependencies like numpy)
- dash
- selenium

These modules can be installed with pip for python3.

#TODO 
- Better deletion of sats
- Visualize trajectory of the sat in the sky
- Select time range for previ
- Nicer interface
- Display when downloading

