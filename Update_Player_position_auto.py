def Update_player_post():
    query = f"UPDATE {table_name} SET Playing_Order= CASE WHEN position>=1 AND position<=3 THEN 'Top Order'" \
            f"WHEN position>=4 AND position<=6 THEN 'Middle Order'" \
            f"WHEN position>=7 AND position<=9 THEN 'Lower Middle Order'" \
            f"WHEN position>9 THEN 'Lower Order'" \
            f" END" \
            f" WHERE position>0"