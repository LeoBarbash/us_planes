def tables_delayed_cascade_delays():
   
    import sqlite3
    import sql_query
    import pandas as pd
    import numpy as np
    
    cascade_delay = sql_query.execute_sql_query('''
        SELECT Year, Month, DayOfMonth, CRSDepTime, DepTime, DepDelay, CRSArrTime, ArrTime, ArrDelay, Origin, Dest, FlightNum
        FROM ontime
        WHERE ontime.Cancelled = 0 AND ontime.Diverted = 0 AND ontime.DepDelay > 0
        ''').rename(columns={0:'Year', 1:'Month', 2:'DayOfMonth', 3:'CRSDepTime', 4:'DepTime', 5:'DepDelay', 
                             6:'CRSArrTime', 7:'ArrTime', 8:'ArrDelay', 9:'Origin', 10:'Dest', 11:'FlightNum'})
    cascade_delay = cascade_delay.sort_values(by=['DepDelay'], ascending=False).reset_index().drop(columns=['index'])
    origin_flight = cascade_delay[cascade_delay['DepDelay'] == cascade_delay.describe().loc['75%', 'DepDelay']].reset_index().drop(columns=['index']).head(1)
    example = origin_flight.loc[0, :]
    delayed_flights = cascade_delay.loc[(cascade_delay['Year'] == example['Year']) & (cascade_delay['Month'] == example['Month']) & (cascade_delay['DayOfMonth'] == example['DayOfMonth']) & (cascade_delay['DepTime'] > example['ArrTime']) & (cascade_delay['CRSDepTime'] < example['ArrTime']) & (cascade_delay['CRSDepTime'] > example['CRSArrTime']) & (cascade_delay['Origin'] == example['Dest']), :].reset_index().drop(columns=['index'])
    
    return origin_flight, delayed_flights    
    