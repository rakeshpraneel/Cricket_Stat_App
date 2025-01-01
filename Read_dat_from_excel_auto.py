import xlrd3 as xl
from datetime import date

# Function to read excel
def Read_data(Names_in_db,executor):
    #Obtaining file and sheet name
    #file_path = input("Enter the file path: ")
    #sheet_name = input("Enter the sheet name: ")
    file_path = "Sample/Sample_bowling.xlsx"
    #Reading the data
    excel_sheet = xl.open_workbook(file_path)
    print(f"Total sheets present in the excel: {excel_sheet.nsheets}")
    Names_in_sheet = excel_sheet.sheet_names()
    print(f"Sheet names found in the file {Names_in_sheet}")
    for Name in Names_in_sheet:
        tb_exist_flag = 1
        if not Name in Names_in_db:
            tb_exist_flag = 0
            print(f"Name is not found in the DB: {Name}")
            new_player_id_query = "select count(*) from player_details;"
            executor.execute(new_player_id_query)
            new_player_id = executor.fetchone()[0]
            print(new_player_id)
            new_player_id = int(new_player_id)+1
            new_table_confirmation = input(f"Confirm whether new table can be created ?(y/n) "
                                           f"the player id will be {new_player_id}")
            try:
                if new_table_confirmation == "Y" or new_table_confirmation == 'y':
                    # Inserting the entry into player details table
                    insert_query_player_details_tb = "insert player_details (player_id, Name) values (%s,%s)"
                    playerDetails_tb_values = (new_player_id,Name)
                    executor.execute(insert_query_player_details_tb,playerDetails_tb_values)
                    # Create new Table
                    create_tb = f"Create table {Name} (Innings int, Runs int, Balls int, Status varchar(255), Fours int, Sixes int, Position int, Playing_Order varchar(255), Opponent varchar(255), Player_id int);"
                    executor.execute(create_tb)
                    print(f"Table {Name} has been created")
                    tb_exist_flag = 1
            except Exception as arg:
                print(f"Faced below error, While trying to Create new table {Name}")
                print(arg)
        if tb_exist_flag:
            try:
                sheet = excel_sheet.sheet_by_name(Name)
                print(sheet)
                select_count_query = f"Select count(*) from {Name};"
                insert_query = f"Insert {Name} (Player_id, Innings, Runs, Balls, Status, Fours, Sixes, Position, Opponent, Playing_Order) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
                executor.execute(select_count_query)
                select_count = executor.fetchone()[0]
                print(f"count of {Name} table is: {select_count} ")
                print(f"Total rows in the sheet is: {sheet.nrows}")
                if sheet.nrows > select_count+1:
                    try:
                        # Create Backup
                        Name_bkp = Name + "_bkp_" + str(date.today())
                        Name_bkp = Name_bkp.replace("-","_")
                        backup_tb = f"Create table {Name_bkp} as select * from {Name};"
                        executor.execute(backup_tb)
                        print(f"Table {Name_bkp} backup has been created")
                    except Exception as arg:
                        print(f"Faced below error while taking backup - {backup_tb}")
                        print(arg)
                    for r in range(select_count+1, sheet.nrows):
                        Player_id = int(sheet.cell(r, 0).value)
                        Innings = int(sheet.cell(r, 1).value)
                        Runs = int(sheet.cell(r, 2).value)
                        Balls = int(sheet.cell(r, 3).value)
                        Status = sheet.cell(r, 4).value
                        Fours = int(sheet.cell(r, 5).value)
                        Sixes = int(sheet.cell(r, 6).value)
                        Position = int(sheet.cell(r, 7).value)
                        Opponent = sheet.cell(r, 9).value
                        if Position>=1 and Position<=3:
                            Playing_Order = "Top Order"
                        elif Position>=4 and Position<=6:
                            Playing_Order = "Middle Order"
                        elif Position>=7 and Position<=9:
                            Playing_Order = "Lower Middle Order"
                        elif Position>=10:
                            Playing_Order = "Lower"
                        else:
                            Playing_Order = None
                        player_details = (Player_id, Innings, Runs, Balls, Status, Fours, Sixes, Position, Opponent, Playing_Order)
                        executor.execute(insert_query, player_details)
                else:
                    print(f"No new records found in the sheet. Hence skipping records of {Name}")
            except Exception as arg:
                print(f"Faced below error while trying to insert new data into {Name}")
                print(arg)



