# Cricket_Stat_App
Web app which can be used to record the cricket stats of your team. This uses mysql database and html/css to display the computed data. The ETL process is performed using python.
Check out for sample input > <input>/<inputfile>
Install required libraries using req_lib.txt
The overall process will be input_file<excel> - mysql<db> - json - frontend
Each steps can be scheduled as jobs using the scripts so that it ll be triggered on specific intervals and the application can be reloaded periodically.
Load Data to db Automated.py (script) - used to load data from excel, Web_app_reload.py - used to reload the web app using API, Flask_main.py - flask application

Pre-Requisites
Use the sample xlsx sheets present in Sample directory to create individual player data for batting and bowling.

How to Install and Run the Project
Install the required packages using requirements.txt file. There are seperate scripts to generate JSON and populate data into Database. Host a mysql db and you can provide the credentials in the data load related python scripts. If in case you are using different input file then modify the same in the respective data read scripts.

Docker Setup
Cricket_stat docker file can be used to build the docker image for the flask application and make sure the json files generated are placed in data/ folder since the docker will check for it while lanuching the container. I do have a builded image for this application, available in docker hub: https://hub.docker.com/repository/docker/rocky03/cricketstatapp/general
[ as of now i've kept as private, let me know if required will provide ]

you can use below command to build image and run it
> docker build Cricket_stat
> docker run <imageid>
