import pymysql
import json

def Calculate_data(runs,balls,status,fours,sixes,orders):
    Total_innings = len(runs)
    Total_runs = sum(runs)
    Total_balls = sum(balls)
    Total_out = status.count('Out')
    Total_fours = sum(fours)
    Total_sixes = sum(sixes)
    Average_strike_rate = round((Total_runs/Total_balls)*100, 2)
    Average = round(Total_runs/Total_out,1)
    Individual_player_dict = {}
    # finding frequently played position
    max_c = Total_innings
    Freq_played_order = []
    Freq_played_order_string = ''
    for post in orders:
        count = orders.count(post)
        count_percentage = (count/max_c)*100
        if count_percentage > 30 and Freq_played_order.count(post) == 0 and not post is None:
            print(f"{post} played percentage is {count_percentage}")
            Freq_played_order.append(post)
    print(f"Frequently played order list: {Freq_played_order}")
    if Freq_played_order:
        for string in Freq_played_order:
            Freq_played_order_string = Freq_played_order_string + " / " + str(string) if Freq_played_order_string else str(string)
    else:
        Freq_played_order_string = "Unknown"
    # Packaging the data
    Individual_player_dict["Innings"] = Total_innings
    Individual_player_dict["Total Runs"] = Total_runs
    Individual_player_dict["Strike Rate"] = Average_strike_rate
    Individual_player_dict["Average"] = Average
    Individual_player_dict["Total 4s"] = Total_fours
    Individual_player_dict["Total 6s"] = Total_sixes
    Individual_player_dict["Position"] = Freq_played_order_string
    return Individual_player_dict

def Read_data_from_db():
    db = pymysql.connect(host="StumpsManiac.mysql.pythonanywhere-services.com", user="StumpsManiac",
                         password="StumpsDatabase", database="StumpsManiac$players")
    executor = db.cursor()
    select_query = "Select * from player_details;"
    executor.execute(select_query)
    result = executor.fetchall()
    print(result)
    Player_dict={}
    Indivi_dict={}
    for r in result:
        player_name = r[1].strip()
        try:
            select_stat_query = f"Select * from {player_name};"
            executor.execute(select_stat_query)
            result_2 = executor.fetchall()
            player_name_crted=player_name.replace("_"," ")
            Player_runs=[]
            Player_balls=[]
            Player_status=[]
            Player_Fours=[]
            Player_sixes=[]
            Player_order=[]
            All_Innings_dict={}
            Indivi_dict={}
            for r2 in result_2:
                #Player_dict.update({player_name:{r2[0]:{}}})
                Innings_dict = {"Runs":r2[1],"Balls":r2[2],"Status":r2[3],"Fours":r2[4],"Sixes":r2[5],
                                           "Position":r2[6],"Order":r2[7],"Opponent":r2[8]}
                All_Innings_dict.update({r2[0]:Innings_dict})
                # Collect the stats
                Player_runs.append(int(r2[1]))
                Player_balls.append(int(r2[2]))
                Player_status.append(r2[3])
                Player_Fours.append(int(r2[4]))
                Player_sixes.append(int(r2[5]))
                Player_order.append(r2[7])
            # Calculating Individual stat
            if Player_runs:
                try:
                    Indivi_dict = Calculate_data(Player_runs,Player_balls,Player_status,Player_Fours,Player_sixes,Player_order)
                except Exception as arg:
                    print("Faced below error while trying to calculate the individual stat")
                    print(arg)
            All_Innings_dict.update(Indivi_dict)
            Player_dict[player_name_crted] = All_Innings_dict
            #Player_dict[player_name] = Indivi_dict
        except Exception as arg:
            print("faced below error while trying to read data from db")
            print(arg)
    #Player_dict["Players"]=Innings_dict
    print(Player_dict)
    with open("/home/StumpsManiac/content/player_details.json","w") as jsonfile:
        json.dump(Player_dict,jsonfile)


Read_data_from_db()