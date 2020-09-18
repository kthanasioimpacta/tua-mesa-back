# TUA MESA - BACKEND PROJECT

## REQUIREMENTS 

- python3.7 or superior
- MySql Database

## INSTALL  

- python3 -m venv .venv  
- source .venv/bin/activate  
- pip install -r requirements.txt  


## SETUP  

- Set your non-sensitive configurations in the file ./config.py  
- Create your Mysql database  

Let's assume you choose the following configuration:  

|Name|Value|
|:-|:-|
|Database Name|TUAMESA|
|Username| root|
|Password| password|
|Host| localhost|

- Set your sensitive configurations in the file ./instance/config.py  

For the configuration above, the variable [SQLALCHEMY_DATABASE_URI] in the file [./instance/config.py] must be:

<code>SQLALCHEMY_DATABASE_URI='mysql://root:password@localhost/TUAMESA'</code>


### If you're using a new database (Create your tables as follows)
- flask db stamp base  
- flask db upgrade  

## Starting the Application

- export FLASK_APP=run.py  
- export FLASK_ENV=development  
- flask run  

## Managing Models using Migrations

- Modify / Add / Delete your Model Class (Inside ./app/models/*)  
- If you're adding a new Model, don't forget to import it on the ./app/__init__.py file  
- flask db migrate -m "What's the change"  
- flask db upgrade  

## APIS

- Install POSTMAN application and import this collection:

<code>https://www.getpostman.com/collections/42dba093768b05a82edf</code>