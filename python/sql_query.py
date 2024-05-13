def execute_sql_query(query):
    
    import sqlite3
    import pandas as pd
    import numpy as np
    
    conn = sqlite3.connect('/Users/levbarbash/LSE/LondonProg/Coursework/airline2.db')
    q_planes = conn.execute(query).fetchall()
    conn.close()
    return pd.DataFrame(q_planes)
