def box_plots_best_time():
    
    import sqlite3
    import sql_query
    import pandas as pd
    import numpy as np
    import seaborn as sns
    import matplotlib.pyplot as plt
    
    f, axs = plt.subplots(2, 2, figsize=(12, 8), gridspec_kw=dict(width_ratios=[4, 3]))
    for sql_col, pd_col in zip(['CRSDepTime', 'DayOfWeek', 'DayOfMonth', 'Month'], ['Hours', 'Day of week', 'Day of month', 'Month']):
        temp_delay = sql_query.execute_sql_query('''
        SELECT ''' + sql_col + ''' AS ''' + sql_col + ''', DepDelay as DepDelay
        FROM ontime
        WHERE ontime.Cancelled = 0 AND ontime.Diverted = 0 AND ontime.DepDelay > 0
        ''').rename(columns={0:pd_col, 1:'Delay'})
        temp_delay[pd_col] = temp_delay[pd_col] // (1 + 99 * int(pd_col == 'Hours'))
        temp_axs = axs[int(pd_col == 'Day of month') + int(pd_col == 'Month'), int(pd_col == 'Day of week') + int(pd_col == 'Month')]
        sns.boxplot(data=temp_delay, x=pd_col, y='Delay', showfliers = False, ax=temp_axs)
        temp_axs.set_ylim([0, 160])
    f.tight_layout()