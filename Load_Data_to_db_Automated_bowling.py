import pymysql
import pandas
import Read_dat_from_excel_auto_bowling
import xlrd3 as xl
def connect_db():
    print("connect db fnct intiated")
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
    try:
        Read_dat_from_excel_auto_bowling.Read_data(Names_in_db,executor)
        #executor.execute(insert_query,player_details)
        db.commit()
    except Exception as arg:
        print("Got the below error")
        print(arg)
    executor.close()
    db.close()
if __name__ == '__main__':
    connect_db()