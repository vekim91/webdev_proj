import streamlit as st
import plotly.express as px
import pandas as pd

# Load the data
try:
    data = pd.read_csv('vehicles_us.csv')
except:
    data = pd.read_csv('https://raw.githubusercontent.com/vekim91/webdev_proj/main/vehicles_us.csv')

# Fix the data to separate the make and the model
data[['make','model']] = data['model'].str.split(' ',n=1,expand=True)


# Header copied from the notebook
st.header('Introduction')
st.write('We\'re starting this project by doing some EDA on the `vehicles_us.csv` file. The goal of the EDA is to generate some figures that would help us appreciate and digest the data easier. We do this by looking at our data in EDA, and see how we generate meaningful and interactive figures that we can export to Render using `Streamlit`.\n\n Let\'s load our data and see what would be interesting visuals to help us understand it better!')

# Get the list of unique brands in the data
st.write('***Select the make of the car that you want to see the data for in the figures below:***')
brand_list = sorted(data['make'].unique())

# Create columns for aesthetics of the checkboxes
num_columns = 4
cb_columns = st.columns(num_columns)

# Initiate filter list
filter_list = []

# Iterate the unique list to generate checkboxes and place them in the columns
for i, brand in enumerate(brand_list):
    checkbox_value = cb_columns[i % num_columns].checkbox(label=brand)

    if checkbox_value:
        filter_list.append(brand)
    else:
        try:
            filter_list.remove(brand)
        except:
            pass

# Create the interactive figures for the app
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

st.write(f'**Correlation Matrix for:** {filter_list}')
data_corr_matrix = data[data['make'].isin(filter_list)].drop('is_4wd', axis=1)
corr_matrix = data_corr_matrix.corr(numeric_only=True)
st.dataframe(corr_matrix)

st.write('I hope this project gave you a good impression of what I\'ve learned so far in this bootcamp, and I hope you enjoyed interacting with this simple web app!')
