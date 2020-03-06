import plotly.express as px
import pandas as pd
with open("times.txt", "r") as File:
    data = File.read()
wide_df = pd.DataFrame(dict(Data = data))
fig = px.box(wide_df, y="Data")
fig.show()
