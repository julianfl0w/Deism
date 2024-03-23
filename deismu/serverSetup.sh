sudo apt update
sudo apt install chromium-browser chromium-chromedriver
sudo apt install python3 python3-pip gunicorn
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
pip install -r requirements.txt
sudo apt --fix-broken install