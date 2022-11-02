from functions import *
from process_data import processData
import streamlit as st
import matplotlib.pyplot as plt 
import seaborn as sns
import numpy as np
import pandas as pd
from wordcloud import WordCloud
from PIL import Image
from load_data import loadData
from pwc import plotly_wordcloud

# st.write("Hello, Worlds!")
st.sidebar.title('Data Vizualisation of Spotify History')
st.sidebar.header('By Asma GRAIESS.')
image = Image.open('images/person.jpg')
st.sidebar.image(image,width=300)
# st.sidebar.image('/Users/asma/Dropbox/My Mac (Asma’s MacBook Pro)/Downloads/qrcode_www.linkedin.com.png',width=150)
agree = st.radio('Would you like to vizualise my Spotify data or yours ?', ('Mine', 'Yours'))

unprocessed=pd.DataFrame()
SH=pd.DataFrame()

person="I"
if agree=='Yours':
    person="You"
    st.header('I will be analysing and visualizing your Spotify streaming history data. Hope you enjoy it !')
    st.subheader('We are going to concatinate your files into one dataframe to do the vizualisations. Choose how many files you are going to use :')
    uploaded_files = st.file_uploader("Upload JSON", type=["JSON"], accept_multiple_files=True) # '+person+' think that Spotify only lets you upload you Streaming History as a JSON file
    if uploaded_files:
        for file in uploaded_files:
            file.seek(0) # '+person+' saw this line that solved the issue in Streamlit discussions
        uploaded_data_read = [pd.read_json(file) for file in uploaded_files]
        unprocessed = pd.DataFrame(pd.concat(uploaded_data_read,ignore_index=True))
        SH=processData(unprocessed.copy())
if agree=='Mine':
    person="I"
    unprocessed=loadData()
    SH=processData(unprocessed.copy())

if len(SH)!=0:
    st.header('Analysis of Dataset')
    if st.checkbox('Show Original Dataset'):
        st.header("Row Dataset")
        number = st.number_input('Insert the number of random rows you want to display',value=5,step=1,key='3')
        st.write(unprocessed.sample(number))
        if st.checkbox('Column Names'):
            st.write(unprocessed.columns.transpose())

    # Sample of the transformed data
    if st.checkbox('Show Processed Dataset'):
        st.header("Processed Dataset")
        number = st.number_input('Insert the number of random rows you want to display',value=5,step=1,key='4')
        st.write(SH.sample(number))
        if st.checkbox('Column Names',key="col2"):
            st.write(SH.columns.transpose())

    # Top 5 most streamed artists
    st.header("Analysis By Artists")
    number=5
    if st.checkbox('Top most streamed artists'):
        number = st.number_input('Write N for Top(N) analysis',value=5,step=1,key='04')
        st.plotly_chart(TopArtists(SH,int(number)))
    if st.checkbox('Top Fav Artists (Pie Chart)'):
        numberpieartist = st.number_input('Write N for Top(N) analysis',value=5,step=1,key='44')
        st.plotly_chart(TopArtistsPieChart(SH,int(numberpieartist)))
    if st.checkbox('Top Artists Occurance (WordCloud)'):
        st.plotly_chart(plotly_wordcloud(' '.join(list(SH.artistName))))

    st.header("Analysis By Tracks")
    if st.checkbox('Analysis of Unique Songs'):
        st.header("Do "+person+" prefer to discover new songs or do "+person+" just listen to the same songs over and over again?")
        st.plotly_chart(uniqueSongs2(SH))
        st.write('This demonstrates that '+person+' would rather hear the same music over and over than seek out new ones.')

    if st.checkbox('Top Most Played Tracks'):
        tracknumber = st.number_input('Write N for Top(N) analysis',value=5,step=1,key='5')
        st.plotly_chart(TopTracks(SH,int(tracknumber)))
    
    if st.checkbox('Top Fav Tracks (Pie Chart)'):
        numberpieartist = st.number_input('Write N for Top(N) analysis',value=5,step=1,key='55')
        st.plotly_chart(TopTracksPieChart(SH,int(numberpieartist)))

    if st.checkbox('Top Tracks Occurance (WordCloud)'):
        st.plotly_chart(plotly_wordcloud(' '.join(list(SH.trackName))))


    st.header("Analysis By Usage")
    if st.checkbox('Days on which '+person+' listen to Spotify the most '):
        genre=st.radio('Choose how you want to plot it',('Bar Chart','Pie Chart'))
        st.plotly_chart(daywiseUsage(SH,genre))

# When do '+person+' listen to Spotify the most ?
    if st.checkbox('Average Usage of Spotify'):
        genre=st.radio('Choose the Feature',('Daily', 'Weekly', 'Yearly'))
        st.plotly_chart(usageByTime(SH,genre))


    # How many hours did '+person+' spent on Spotify Streaming since the day '+person+' signed up for it?
    date_df = SH["end-Time"]
    days_spotify=(date_df.iloc[33900] - date_df.iloc[0]) / np.timedelta64(1,"D")
    time_spent_hours = SH["Duration(Hours)"].sum()
    Nb_days=SH['end-Time'][33900]-SH['end-Time'][0]
    if st.checkbox('Total time spent on Spotify'):
        st.write('Since the day '+person+' signed up for Spotify, '+person+' have streamed for exactly',round(time_spent_hours), 'hours of in a year.')
        time_spent_days=time_spent_hours/24
        time_spent_weeks=time_spent_days/7
        st.write('Which is equal to',round(time_spent_days), 'days. Or also to',round(time_spent_weeks),'weeks worth of listeneing to spotify non stop.')
        st.write('Which means out of the', 52 ,'weeks in the year, '+person+' have spent',round(time_spent_weeks),'of them listening to music on Spotify.')
        col1, col2, col3 = st.columns(3)
        col1.metric("Hours",round(time_spent_hours))
        col2.metric("Days", round(time_spent_days))
        col3.metric("Weeks", round(time_spent_weeks))
        if st.checkbox('Pie chart'):
            fig = px.pie(values=[time_spent_weeks,days_spotify/7], names=["On Spotify","Other Activities"],color_discrete_sequence=px.colors.sequential.Blues)
            fig.update_layout(title="<b>Yearly Activity Analysis</b>")
            st.plotly_chart(fig)
    
        # What are the top 5 days '+person+' played maximum number of songs ?
    SH["date"] = SH["end-Time"].dt.date
    most_songs = SH.groupby(["date"])[["Count"]].sum().sort_values(by="Count", ascending=False)
    if st.checkbox(person+ ' played maximum number of songs'):
        days=SH['end-Time'].dt.date
        days=days.value_counts()
        fig=px.scatter(days,color=days.keys())
        trace = next(fig.select_traces())
        n = len(trace.x)
        k = 0
        color = [trace.marker.color] * n
        color[k] = "red"
        size = [8] * n
        size[k] = 15
        symbol = [trace.marker.symbol] * n
        symbol[k] = "circle"
        trace.marker.color = color
        trace.marker.size = size
        trace.marker.symbol = symbol
        st.plotly_chart(fig)
        st.subheader('The days when '+person+' listened to Spotify the most: ')
        st.table(most_songs.head(5))

    # What is the average numbers of songs '+person+' played ?
    if st.checkbox('Average numbers of songs played '):
        total_songs = SH["trackName"].count()
        average_songs_played_daily = (total_songs / days_spotify).round()
        average_songs_played_weekly= (total_songs / days_spotify*7 ).round()
        col1, col2 = st.columns(2)
        col1.metric("Daily",int(average_songs_played_daily))
        col2.metric("Weekly",int(average_songs_played_weekly))

    st.header("Thank You 😊")
    if st.checkbox('The End'):
        st.title('Thank you for your attention !!')
        st.balloons()
