# MeoPrevi
Python script that display the **timeline** of excepted satellites above **Calern** in a browser.


The timeline is generated for a week, and zooms in automatically at startup at UTC current time, for 2 hours.
One can change the time range, and select what satellites to display in the timeline in the right column.

## Installation

To install this script, use the github repo with
```bash
cd /opt; sudo git clone https://github.com/atxr/MeoPrevi
```

Otherwise, if you own the archive, exctract it with the command 
```bash
sudo unzip path/to/the/archive -d /opt
```
**TODO**: Add installation of geckodriver

## Usage

Then, to launch the script, execute 
```bash
/opt/previ.py
```
. It should automatically open a new tab in the default browser.
If not, browse directly the link the terminal will print, usually http://127.0.0.1:8050
If you got trouble with the script, check the dependencies section at the end.

## List of satellites
Different lists of satellites can be found in the data directory. 
The one used by default is data/maj\_sats.data. 
List of aviable database:
- data/maj\_sats.data: most important satellites, accoreded to the [ILRS priority list](https://ilrs.gsfc.nasa.gov/missions/mission_operations/priorities/index.html)
- data/sats.data: most of the observable satallites from Calern. Warning, because of the length of this database, the display may be bad.
- data/galileo.data: all Galileo GNSS european satellites

If one wants to change the database, modify at the beginning of previ.py the line 
```python
import maj_sats.py
```
with the name of the correct database.

One could add some satellites that aren't in the actual database to the timeline.
To do so, use one of the three database as template. It must contain the **name** and the **Spacetrack catalog number** of each satellites separated by a ~. Spacetrack catalog numbers can be found on the heavens-above satellite database, at https://heavens-above.com/Satellites.aspx

**TODO**: automate the addition of satellites

## Dependencies

Geckodriver, firefox for selenium

Python3 and the following modules:
- pandas
- plotly (and its own dependencies like numpy)
- dash
- selenium

These modules can be installed with pip for python3.

