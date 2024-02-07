import streamlit as st
import plotly.express as px
import pandas as pd

try:
    data = pd.read_csv('vehicles_us.csv')
except:
    data = pd.read_csv('https://raw.githubusercontent.com/vekim91/webdev_proj/main/vehicles_us.csv')

data[['make','model']] = data['model'].str.split(' ',n=1,expand=True)
data = data[['price', 'model_year', 'make', 'model', 'condition', 'cylinders', 'fuel', 'odometer', 'transmission', 'type', 'paint_color', 'is_4wd', 'date_posted', 'days_listed']]

st.header('Introduction')
st.write('We\'re starting this project by doing some EDA on the `vehicles_us.csv` file. The goal of the EDA is to generate some figures that would help us appreciate and digest the data easier. We do this by looking at our data in EDA, and see how we generate meaningful and interactive figures that we can export to Render using `Streamlit`.\n\n Let\'s load our data and see what would be interesting visuals to help us understand it better!')

# Get the list of unique brands in the data
brand_list = sorted(data['make'].unique())

# Initiate filter list
filter_list = []

num_columns = 4

# Create columns for aesthetics
cb_columns = st.columns(num_columns)

# Iterate the unique list to generate checkboxes
for i, brand in enumerate(brand_list):
    checkbox_value = cb_columns[i % num_columns].checkbox(label=brand)

    if checkbox_value:
        filter_list.append(brand)
    else:
        try:
            filter_list.remove(brand)
        except:
            pass

scatter_fig = px.scatter(data_frame=data[data['make'].isin(filter_list)],
                        x='model_year',
                        y='price',
                        color='make',
                        hover_data='model',
                        title="Scatterplot of Price vs Model Year")
st.plotly_chart(scatter_fig)

histo_fig = px.histogram(data_frame=data[data['make'].isin(filter_list)],
                        x='model_year',
                        title='Distribution of Cars per Year')
st.plotly_chart(histo_fig)