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

## Create Database SQL
	CREATE DATABASE library;
	CREATE USER 'library'@'localhost' IDENTIFIED BY 'udaysingh';
	USE library;
	GRANT ALL PRIVILEGES ON *.* TO 'library'@'localhost';

## Load Fixtures
	python manage.py loaddata initial_data.json
