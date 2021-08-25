#/bin/sh

wget --output-document /tmp/geckodriver-v0.29.1-linux64.tar.gz \
  'https://github.com/mozilla/geckodriver/releases/download/v0.29.1/geckodriver-v0.29.1-linux64.tar.gz' 
sudo tar -xf /tmp/geckodriver-v0.29.1-linux64.tar.gz -C /opt/MeoPrevi
sudo ln -s /opt/MeoPrevi/geckodriver /usr/bin/geckodriver
sudo ln -s /opt/MeoPrevi/previ.py /usr/bin/previ

