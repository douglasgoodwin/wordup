#wordup

A Vocabulary Builder


## Quickstart


### make directories
mkdir /var/www/envs/wordup

### create the virtualenv
cd /var/www/envs/wordup
virtualenv .
. bin/activate

### clone the code repository
git clone git@github.com:douglasgoodwin/wordup.git

### install the site requirements
cd wordup/
pip install -r requirements.txt 

### try it out!
uwsgi --ini uwsgi-dev.ini 

### in your browser:
http://127.0.0.1:5000