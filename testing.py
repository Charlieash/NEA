import plotly.express as px
import pandas as pd
data = []
with open("times.txt", "r") as File:
    for row in File:
        data.append(int(row))
wide_df = pd.DataFrame(dict(Time = data))
fig = px.box(wide_df, y="Time", labels={'Time':'Time of routes in minutes'})
fig.show()
