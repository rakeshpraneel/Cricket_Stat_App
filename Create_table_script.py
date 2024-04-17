import pymysql

def sql_connection():
    db = pymysql.connect(host="",user="", password="", database="")
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
    user_input = input("Want to create table(c) or drop table(d): ")
    if user_input.lower() == 'c':
        try:
            user_input = input("Want to create fielding table(f) or bowling table(bo): ")
            if user_input.lower() == 'f':
                Create_Table_fielding(Names_in_db,executor)
            elif user_input.lower() == 'bo':
                Create_Table_bowling(Names_in_db,executor)
        except Exception as arg:
            print("Facing below error while try to create new tables")
            print(arg)
    elif user_input.lower() == 'd':
        try:
            user_input = input("Want to drop fielding table(f) or bowling table(bo): ")
            if user_input.lower() == 'f':
                Drop_Table_fielding(Names_in_db,executor)
            elif user_input.lower() == 'bo':
                Drop_Table_bowling(Names_in_db,executor)
        except Exception as arg:
            print("Facing below error while try to droppping tables")
            print(arg)

def Create_Table_bowling(Names_in_db,exec):
    for player_name in Names_in_db:
        player_name = player_name + "_bowling"
        bowling_tb_query = f"Create table {player_name} (Innings int, Runs_Conceded int, Overs int, Wicket int, Fours int, Sixes int, Extras int, Opponent varchar(255), Player_id int);"
        exec.execute(bowling_tb_query)
        print(f"Table {player_name} created")

def Create_Table_fielding(Names_in_db, exec):
    for player_name in Names_in_db:
        player_name = player_name + "_fielding"
        bowling_tb_query = f"Create table {player_name} (Catches int, Run_Outs int, Overs int, Wicket int, Fours int, Sixes int, Extras int, Opponent varchar(255), Player_id int);"
        exec.execute(bowling_tb_query)
        print(f"Table {player_name} created")

def Drop_Table_fielding(Names_in_db, exec):
    for player_name in Names_in_db:
        player_name = player_name + "_fielding"
        bowling_tb_query = f"drop table {player_name};"
        exec.execute(bowling_tb_query)
        print(f"Dropped Table {player_name}")

def Drop_Table_bowling(Names_in_db, exec):
    for player_name in Names_in_db:
        player_name = player_name + "_bowling"
        bowling_tb_query = f"drop table {player_name};"
        exec.execute(bowling_tb_query)
        print(f"Dropped Table {player_name}")

sql_connection()
