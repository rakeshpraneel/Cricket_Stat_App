import pymysql
from datetime import date

def sql_connection():
    db = pymysql.connect(host="StumpsManiac.mysql.pythonanywhere-services.com",user="StumpsManiac", password="StumpsDatabase", database="StumpsManiac$players")
    executor = db.cursor()
    query_id="Select * from player_details;"
    executor.execute(query_id)
    result=executor.fetchall()
    print(f"Please find the below player names and their ids \n {result}")
    # Check for player names in input file
    Names_in_db = []
    for names in result:
        Names_in_db.append(names[1].strip())
    print(Names_in_db)
    # get all available tables
    query_id="Show Tables;"
    executor.execute(query_id)
    result=executor.fetchall()
    print(result)
    table_created_before_7_days = "select table_schema as database_name,table_name,create_time from information_schema.tables where create_time < adddate(current_date,INTERVAL -7 DAY) and table_schema not in('information_schema', 'mysql'," \
                                  "'performance_schema','sys') and table_type ='BASE TABLE' -- and table_schema = 'your database name' order by create_time desc, table_schema;"
    executor.execute(table_created_before_7_days)
    result_before_7_days = executor.fetchall()
    print(result_before_7_days)
    user_input = input("Find backup tables (y/n): ")
    if user_input.lower() == 'y':
        try:
            Find_backup_tables(result)
        except Exception as arg:
            print(arg)
    user_input = input("Delete the backup tables that are 15 days older (y/n): ")
    if user_input.lower() == 'y':
        try:
            Delete_Older_bkp_tb(result_before_7_days)
        except Exception as arg:
            print(arg)

# Finding the total backup tables available
def Find_backup_tables(show_table_re):
    backup_table = []
    for table_name in show_table_re:
        if table_name[0].__contains__('_bkp_'):
            backup_table.append(table_name[0])
    print(backup_table)

# Deleting older backup tables
def Delete_Older_bkp_tb(older_tables):
    older_backup_table = []
    for table_name in older_tables:
        if table_name[1].__contains__('_bkp_'):
           older_backup_table.append(table_name[1])
    print(older_backup_table)

sql_connection()