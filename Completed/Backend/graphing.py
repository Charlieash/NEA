import plotly.express as px
import pandas as pd
import os 
data = []
cur_path = os.path.dirname(__file__)
new_path = cur_path + "\\Data_Transfer\\times.txt"
with open(new_path, "r") as File:
    for row in File:
        data.append(int(row))
wide_df = pd.DataFrame(dict(Time = data))
fig = px.box(wide_df, y="Time", labels={'Time':'Time of routes in minutes'})
fig.show()
