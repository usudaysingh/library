# Set Up

## Install Pip
	sudo apt-get install python-pip

## SetUp VirtualEnv

	pip install virtualenv
	mkdir ~/.virtualenvs
	pip install virtualenvwrapper
	export Projects=~/.virtualenvs
	
	Add this line to the end of ~/.bashrc so that the virtualenvwrapper commands are loaded.
	. /usr/local/bin/virtualenvwrapper.sh

## Activate VirtualEnv
	mkvirtualenv Library
	workon Library

## Clone library repository
	git clone git@github.com:usudaysingh/library.git

## Install Requirements
	pip install -r requirements.txt

## Set Up MySQL
	sudo apt-get install libmysqlclient-dev
	sudo apt-get install mysql-server
	mysql -u root -p --execute "create database library; grant all on library.* to library@localhost identified by 'udaysingh';"

## Load Fixtures
	python manage.py loaddata initial_data.json

## Run Server
	python manage.py runserver
	open localhost:8000 in your browser
