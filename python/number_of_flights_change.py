def networks_popular_flights():
    
    import sqlite3
    import sql_query
    import pandas as pd
    import numpy as np
    import seaborn as sns
    import matplotlib.pyplot as plt
    import networkx as nx
    
    origin_dest = []
    for year in range(2006, 2008):
        temp_sers = sql_query.execute_sql_query('''
        SELECT Origin AS Origin, Dest as Dest
        FROM ontime
        WHERE ontime.Cancelled = 0 AND ontime.Diverted = 0 AND ontime.Year = ''' + str(year) + '''
        ''')
        temp_sers = temp_sers.rename(columns={0:'Origin', 1:'Dest'})
        temp_sers = temp_sers.groupby(['Origin', 'Dest']).size().reset_index().rename(columns={0:'Weight' + str(year)})
        temp_sers = temp_sers.sort_values(by='Weight' + str(year), ascending=False)
        origin_dest.append(temp_sers)
    origin_dest = pd.merge(origin_dest[0].head(100), origin_dest[1], on=['Origin', 'Dest'])
    
    graphs = [nx.Graph(), nx.Graph()]
    min_weight = origin_dest[['Weight2006', 'Weight2007']].min().min()
    max_weight = origin_dest[['Weight2006', 'Weight2007']].max().max()
    plt.subplots(figsize=(25,10))

    for g, year, sbplt in zip(graphs, [2006, 2007], [121, 122]):
        for index, row in origin_dest.iterrows():
            g.add_edge(u_of_edge=row['Origin'], v_of_edge=row['Dest'], weight=row['Weight' + str(year)])
        edges = g.edges()
        weights = [g[u][v]['weight'] for u,v in edges]
        weightsm = list(map(lambda x: (x - min_weight) / (max_weight - min_weight), weights))
        plt.subplot(sbplt)
        pos=nx.circular_layout(g)
        plt.title('100 most popular routes in ' + str(year))
        nx.draw_networkx(g, pos, node_color='blue', edge_color='blue', width=weightsm, node_size=1)
    