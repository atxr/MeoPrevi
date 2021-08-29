# MeoPrevi
Python script that displays the **timeline** of excepted satellites above **Calern** in a browser.


The timeline is generated for a week, and zooms in automatically at startup at UTC current time, for 2 hours.
You can change the time span, and select which satellites to display in the timeline in the right column.
You can also visualize the trajectory of each satellite in the sky.

## Installation

To install this script, use the github repo with
```bash
git -C ~/.local/bin clone https://github.com/atxr/MeoPrevi; sudo ~/.local/bin/MeoPrevi/INSTALL.sh
```

Otherwise, if you have the archive, extract it with the command
```bash
unzip path/to/the/archive -d ~/.local/bin; sudo ~/.local/bin/MeoPrevi/INSTALL.sh
```

## Usage

After a successful installation, the server can be started by executing 
```bash
previ
```

You can add this command at the boot in the background of your system. For example, on Debian based distro, you can add it to rc.local:
```bash
sudo echo 'previ' >> /etc/rc.local
```
If you got trouble with this script, check dependency section at the end.

Once the server is running, **browse http://127.0.0.1:8050**.

## Add satellites

The script provide a tool for adding a satellite directly with its Spacetrack catalog number. Visit the [following website](https://heavens-above.com/Satellites.aspx) to find Spacetrack catalog numbers of the satellite you want to add.

## List of satellites
Different lists of satellites can be found in the data directory. 
The one used by default is data/ILRS\_Satellites.data. 
List of available database:
- data/ILRS\_Satellites.data: most important satellites, according with the [ILRS priority list](https://ilrs.gsfc.nasa.gov/missions/mission_operations/priorities/index.html)
- data/All\_Satellites.data: most of the observable satellites from Calern. Warning, because of the length of this database, the display may be bad.
- data/Galileo.data: all Galileo GNSS European satellites

If you want to change the database, select the new one in the 'Dataset' Dropdown.
You can manage your dataset by adding and removing Satellites with the dedicated buttons. Once you have modify your dataset, you can save it to a new file under the 'Dataset' Dropdown, just by selecting the name of the new dataset.

## Dependencies

Firefox
Geckodriver for selenium. The INSTALL.sh script install this dependency for Linux-64. 

Python3 and the following modules:
- pandas
- plotly (and its own dependencies like numpy)
- dash
- selenium
- pyautogui

These modules can be installed with **pip** for python3.
```bash
pip3 install numpy plotly pandas dash selenium pyautogui
```

#TODO 
- Select time range for previ
- Nicer interface
- Display when downloading
- More than 3 points for polar
- Install script bug

