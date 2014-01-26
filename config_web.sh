sudo apt-get update
sudo apt-get install git

sudo apt-get install python-virtualenv 
sudo apt-get install python-dev
sudo apt-get install build-essential
  
sudo pip install virtualenv 

virtualenv --no-site-packages --distribute bdenv
. bdenv/bin/activate
pip install -f http://tg.gy/230 TurboGears2 
pip install jinja2
