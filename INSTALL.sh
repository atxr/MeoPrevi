#/bin/sh

pip3 install numpy plotly selenium pyautogui dash
wget --output-document /tmp/geckodriver-v0.29.1-linux64.tar.gz \
  'https://github.com/mozilla/geckodriver/releases/download/v0.29.1/geckodriver-v0.29.1-linux64.tar.gz' 
tar -xf /tmp/geckodriver-v0.29.1-linux64.tar.gz -C ~/.local/bin/MeoPrevi
ln -s ~/.local/bin/previ ~/.local/bin/MeoPrevi/previ.py
ln -s ~/.local/bin/geckodriver ~/.local/bin/MeoPrevi/geckodriver
