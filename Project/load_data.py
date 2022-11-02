import pandas as pd

def loadData():
    df1 = pd.read_json("../MyData/StreamingHistory0.json")
    df2 = pd.read_json("../MyData/StreamingHistory1.json")
    df3 = pd.read_json("../MyData/StreamingHistory2.json")
    df4 = pd.read_json("../MyData/StreamingHistory3.json")
    
    # Concatinating them into one dataframe
    return pd.concat([df1,df2,df3,df4],ignore_index=True) #SH as in Streaming History