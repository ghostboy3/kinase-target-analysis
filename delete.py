import streamlit as st
import plotly.express as px

# Sample data
data = {'Language': ['Python', 'Java', 'C++', 'JavaScript'],
        'Popularity': [215, 130, 245, 210]}

# Create pie chart
fig = px.pie(names=data['Language'], values=data['Popularity'], title='Programming Language Popularity')

# Display in Streamlit
st.plotly_chart(fig)
