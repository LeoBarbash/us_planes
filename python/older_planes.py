def box_plot_decade_planes():
    
    import sqlite3
    import sql_query
    import pandas as pd
    import numpy as np
    import seaborn as sns
    import matplotlib.pyplot as plt
    
    dep_old_planes_delay = sql_query.execute_sql_query('''
    SELECT planes.year AS year, DepDelay as DepDelay
    FROM planes JOIN ontime USING(tailnum)
    WHERE ontime.Cancelled = 0 AND ontime.Diverted = 0 AND ontime.DepDelay > 0 AND planes.year != '0000' AND planes.year IS NOT NULL AND planes.year != 'None'
    ''')

    for i in range(1950, 2001, 10):
        decade = str(i) + 's'
        dep_old_planes_delay.loc[(dep_old_planes_delay[0].astype(int) < i + 10) & (dep_old_planes_delay[0].astype(int) >= i), 'Decade'] = decade
    dep_old_planes_delay = dep_old_planes_delay.rename(columns={0: 'Year',1:'Delay'})
    
    sns.set(rc={'figure.figsize':(11.7,8.27)})
    sns.boxplot(data=dep_old_planes_delay, x='Decade', y='Delay', showfliers = False, order=dep_old_planes_delay['Decade'].value_counts().sort_index().index)
