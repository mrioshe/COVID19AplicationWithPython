from ipywidgets import widgets,interact,Layout  
from plotly.subplots import make_subplots

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