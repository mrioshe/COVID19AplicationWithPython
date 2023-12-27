from ipywidgets import widgets,interact,Layout  
from plotly.subplots import make_subplots
import plotly.graph_objects as go
with open("GetCOVID19DataAndCleaning.py") as f:
    exec(f.read())

#Header: An image will be read y from it a widget object will be create

file= open("images/logo_corona.png","rb")
image =file.read()
HeaderImage=widgets.Image(
    value=image,
    format='png',
    width=1000,
    height=200,
)

#Table: aplicative resume table 

tableFig=go.FigureWidget(go.Table(
    header=dict(
        values=["Country<br> name", "Cases", "Deaths"], font=dict(size=12), align="left"),
        cells=dict(values=[df_summaryCOVID19descendent])




))