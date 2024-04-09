# Cricket_Stat_App
Web app which can be used to record the cricket stats of your team. This uses mysql database and html/css to display the computed data. The ETL process is performed using python.
Check out for sample input > <input>/<inputfile>
Install required libraries using req_lib.txt
The overall process will be input_file<excel> - mysql<db> - json - frontend
Each steps can be scheduled as jobs using the scripts so that it ll be triggered on specific intervals and the application can be reloaded periodically.
Load Data to db Automated.py (script) - used to load data from excel, Web_app_reload.py - used to reload the web app using API, Flask_main.py - flask application
