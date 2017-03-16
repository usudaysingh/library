#Set Up

Clone library repository
git clone git@github.com:usudaysingh/library.git

pip install -r requirements.txt

#Create Database SQL
CREATE DATABASE library;

#Load Fixtures
python manage.py loaddata initial_data.json
