import pymysql
import json


# Function to Calculate bowling leaderboard
def Calculate_leaderboard_batting(Leaderboard_dict):
    Leaderboard_dict = dict(reversed(sorted(Leaderboard_dict.items(), key=lambda x: x[1]['Wickets'])))
    #print(Leaderboard_dict)
    Leaderboard_dict = {k: Leaderboard_dict[k] for k in list(Leaderboard_dict)[:6]}
    return Leaderboard_dict

#Function to Calculate the individual stats
def Calculate_data(runs,overs,wicket,fours,sixes,extra):
    Total_innings = len(runs)
    Total_runs = sum(runs)
    Total_overs = sum(overs)
    Total_wicket = sum(wicket)
    fs_c = sum(fours)+sum(sixes)
    Total_extra = sum(extra)
    # wicket taken interval
    Strike_rate = int(round(Total_overs*6/Total_wicket,0)) if Total_wicket != 0 else '0 wickets taken'
    if Total_runs != 0:
        Economy = round(Total_runs/Total_overs,1) if Total_overs != 0 else '0 overs bowled'
    else:
        Economy = 0
    #print("Calculate boundary interval")
    #print("Total no of boundaries")
    # boundaries conceded intervals
    Bounday_interval = int(round((Total_overs*6)/fs_c,0)) if fs_c != 0 else '0 boundaries conceded'
    # extras conceded intervals
    Extra_interval = int(round(Total_overs*6/Total_extra,0)) if Total_extra != 0 else '0 extras conceded'
    Individual_player_dict = {}
    # Packaging the data
    Individual_player_dict["Innings"] = Total_innings
    Individual_player_dict["Total_Runs"] = Total_runs
    Individual_player_dict["Overs"] = Total_overs
    Individual_player_dict["Wickets"] = Total_wicket
    Individual_player_dict["Economy"] = Economy
    Individual_player_dict["Wickets taken interval"] = Strike_rate
    Individual_player_dict["Boundaries given interval"] = Bounday_interval
    Individual_player_dict["Extras bowled interval"] = Extra_interval
    return Individual_player_dict

def Read_data_from_db():
    db = pymysql.connect(host="", user="",
                         password="", database="")
    executor = db.cursor()
    select_query = "Select * from player_details;"
    executor.execute(select_query)
    result = executor.fetchall()
    print(result)
    Player_dict={}
    Indivi_dict={}
    #Leaderboard_dict
    Leaderboard_dict={}
    for r in result:
        player_name = r[1].strip()
        tb_name = player_name+'_bowling'
        try:
            select_stat_query = f"Select * from {tb_name};"
            executor.execute(select_stat_query)
            result_2 = executor.fetchall()
            player_name_crted=player_name.replace("_"," ")
            Player_runs=[]
            Player_overs=[]
            Player_wicket=[]
            Player_Fours=[]
            Player_sixes=[]
            Player_extra=[]
            All_Innings_dict={}
            Indivi_dict={}
            for r2 in result_2:
                #Player_dict.update({player_name:{r2[0]:{}}})
                Innings_dict = {"Runs Conceded":r2[1],"Overs":r2[2],"Wicket":r2[3],"Fours":r2[4],"Sixes":r2[5],
                                           "Extras":r2[6],"Opponent":r2[7]}
                All_Innings_dict.update({r2[0]:Innings_dict})
                # Collect the stats
                Player_runs.append(int(r2[1]))
                Player_overs.append(int(r2[2]))
                Player_wicket.append(int(r2[3]))
                Player_Fours.append(int(r2[4]))
                Player_sixes.append(int(r2[5]))
                Player_extra.append(int(r2[6]))
            # Calculating Individual stat
            if Player_runs:
                try:
                    #print(Player_runs,Player_overs,Player_wicket,Player_Fours,Player_sixes,Player_extra)
                    Indivi_dict = Calculate_data(Player_runs,Player_overs,Player_wicket,Player_Fours,Player_sixes,Player_extra)
                except Exception as arg:
                    print("Faced below error while trying to calculate the individual stat")
                    print(arg)
            All_Innings_dict.update(Indivi_dict)
            Leaderboard_dict[player_name_crted] = Indivi_dict
            # this condition will vomit player with no records
            if All_Innings_dict:
                Player_dict[player_name_crted] = All_Innings_dict
            #Player_dict[player_name] = Indivi_dict
        except Exception as arg:
            print("faced below error while trying to read data from db")
            print(arg)
    #Player_dict["Players"]=Innings_dict
    print(Player_dict)
    with open("Data/bowling.json","w") as jsonfile:
        json.dump(Player_dict,jsonfile)
    #Calculate Leaderboard data
    try:
        #print(Leaderboard_dict)
        #cleaning the empty dictionaries
        Leaderboard_dict={x:y for x,y in Leaderboard_dict.items() if y}
        Leaderboard_dict = Calculate_leaderboard_batting(Leaderboard_dict)
        print("Calculated bowling LeaderBoard")
        print(Leaderboard_dict)
        # load the data to json
        with open("Data/bowling_leaderboard.json","w") as jsonfile_1:
            json.dump(Leaderboard_dict,jsonfile_1)
    except Exception as arg:
        print("Faced below error while trying to calculate bowling leaderboard")
        print(arg)


Read_data_from_db()
