# speed_testing

Simple speed testing server setup that stores results of 5 speed test every iteration in a sqlite DB.

DB name is hard coded in models.py, so that needs updated before running.

DB can be created by running models module with "create" argument:

    'python3 models.py create'
    
 

Flask server can be started with:
    
    'python3 app.py'
    
I recommend scheduling check_speed.py with cron
