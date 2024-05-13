def logreg_classif_plot_coef():
    
    import pandas as pd
    import numpy as np
    import sqlite3
    import sql_query
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score
    
    ml_data = sql_query.execute_sql_query('''
        SELECT Month, DayOfMonth, DayOfWeek, CRSDepTime, 
        DepDelay, CRSArrTime, CRSElapsedTime, Distance,
        planes.year AS year, a1.lat, a1.long, a2.lat, a2.long
        FROM ontime
        JOIN planes USING(tailnum)
        JOIN airports AS a1 ON ontime.Origin = a1.iata
        JOIN airports AS a2 ON ontime.Dest = a2.iata
        WHERE ontime.Cancelled = 0 AND ontime.Diverted = 0 AND planes.year != '0000' AND planes.year IS NOT NULL 
        AND planes.year != 'None'
        ''').rename(columns={0:'Month', 1:'DayOfMonth', 2:'DayOfWeek', 3:'CRSDepTime', 4:'DepDelay', 5:'CRSArrTime', 
                             6:'CRSElapsedTime', 7:'Distance', 8:'PlaneYear', 9:'OrigLat', 10:'OrigLong', 11:'DestLat', 
                             12:'DestLong'})
    ml_data.loc[ml_data['DepDelay'] < 0, 'DepDelay'] = 0
    ml_data['DepDelay'] = ml_data['DepDelay'].astype(bool).astype(int)
    X = ml_data.drop(columns=['DepDelay'])
    y = ml_data['DepDelay']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)
    lr = LogisticRegression(max_iter=1000).fit(X_train, y_train)
    y_pred = lr.predict(X_test)
    draw_plot(lr, ml_data)
    return lr, accuracy_score(y_test, y_pred)
    

def draw_plot(model, X):
    
    import pandas as pd
    import numpy as np
    
    sorted_weights = sorted(zip(model.coef_.ravel(), X.columns), reverse=True)
    weights = [x[0] for x in sorted_weights]
    features = [x[1] for x in sorted_weights]
    df = pd.DataFrame({'features': features, 'weights':weights})
    ax = df.plot.barh(x='features', y='weights', rot=0, )
    
    