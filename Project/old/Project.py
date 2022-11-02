import streamlit as st
import matplotlib.pyplot as plt 
import seaborn as sns
import numpy as np
import pandas as pd
from wordcloud import WordCloud
from PIL import Image
import time

st.sidebar.title('Hello !!!')
# Show Spotify's Logo
# image = Image.open('/Users/asma/Desktop/S7/DataVisualisation/Spotify-Logo1.jpeg')
# st.sidebar.image(image,width=300)
st.sidebar.header('I am Asma GRAIESS. This is my data vizualisation project. Hope you enjoy it !')
# st.sidebar.image('/Users/asma/Dropbox/My Mac (Asma’s MacBook Pro)/Downloads/qrcode_www.linkedin.com.png',width=150)

agree = st.radio('Would you like to vizualise my Spotify data or yours ?', ('Mine', 'Yours'))
if agree=='Mine':

    st.header('I will be analysing and visualizing my Spotify streaming history data.')
    # Importing my 4 streaming history JSON files
    df1 = pd.read_json("../MyData/StreamingHistory0.json")
    df2 = pd.read_json("../MyData/StreamingHistory1.json")
    df3 = pd.read_json("../MyData/StreamingHistory2.json")
    df4 = pd.read_json("../MyData/StreamingHistory3.json")

    # Concatinating them into one dataframe
    L=[df1,df2,df3,df4]
    SH=pd.concat(L,ignore_index=True) #SH as in Streaming History

    # Sample of the original data
    if st.checkbox('Show original Dataset'):
        st.header("Here's an insigth of what my data originally looked like :")
        number = st.number_input('Insert the number of random rows you want to display',value=5,step=1,key='3')
        st.write(SH.sample(number))

    # Formatting the 'endTime' and 'msPlayed' columns
    SH["end-Time"]= pd.to_datetime(SH["endTime"])
    SH['year'] = pd.DatetimeIndex(SH["end-Time"]).year
    SH['month'] = pd.DatetimeIndex(SH["end-Time"]).month
    SH['day'] = pd.DatetimeIndex(SH["end-Time"]).day
    SH['weekday'] = pd.DatetimeIndex(SH["end-Time"]).weekday
    SH['time'] = pd.DatetimeIndex(SH["end-Time"]).time
    SH['hours'] = pd.DatetimeIndex(SH["end-Time"]).hour
    SH['day-name'] = SH["end-Time"].apply(lambda x: x.day_name())
    SH['Count'] = 1
    SH["duration (hh-mm-ss)"] = pd.to_timedelta(SH["msPlayed"], unit='ms')
    # This function converts milliseconds to hours
    def hours(x):
        return x.seconds/3600
    # This function converts milliseconds to minutes
    def minutes(x):
        return (x.seconds/60)%60
    SH["Duration(Hours)"] = SH["duration (hh-mm-ss)"].apply(hours).round(2)
    SH["Duration(Minutes)"] = SH["duration (hh-mm-ss)"].apply(minutes).round(2)
    SH.drop(columns=["endTime","duration (hh-mm-ss)","msPlayed"], inplace=True)

    # Sample of the transformed data
    if st.checkbox('Show transformed Dataset'):
        st.header("Now this is what my data lookes like :")
        number = st.number_input('Insert the number of random rows you want to display',value=5,step=1,key='4')
        st.write(SH.sample(number))
        #st.write(SH.sample(15))

    # Percentage of unique songs I streamed
    unique_songs = SH["trackName"].nunique()
    total_songs = SH["trackName"].count()
    unique_songs_percentage = unique_songs/total_songs*100
    unique_songs_list = np.array([unique_songs, total_songs-unique_songs])
    unique_songs_list_labels = [" Unique Songs", "Non Unique Songs"]
    if st.checkbox('Pie chart of my unique tracks'):
        st.header("Do I prefer to discover new songs or do I just listen non stop to unique tracks ?")
        fig, ax1 = plt.subplots(figsize=(12,6))
        ax1.pie(unique_songs_list, labels= unique_songs_list_labels, autopct='%1.1f%%', explode=[0.05,0.05], startangle=180,colors=['#ff9999','#66b3ff']);
        centre_circle = plt.Circle((0,0),0.70,fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        plt.title("Unique Songs Percentage")
        st.pyplot(fig)
        st.subheader('This shows that I prefer to listen on repeat to the same songs rather than discover new ones.')

    # Top 5 most streamed artists
    top_artists_time_df = SH.groupby(["artistName"])[["Duration(Hours)","Duration(Minutes)","Count"]].sum().sort_values(by="Duration(Hours)",ascending=False)
    top_artists_count_df = SH.groupby(["artistName"])[["Duration(Hours)","Duration(Minutes)","Count"]].sum().sort_values(by="Count",ascending=False)
    if st.checkbox('Top 5 most streamed artists'):
        fig, (ax1,ax2) = plt.subplots(1,2,figsize=(15,10))
        #first graph
        ax1.bar(top_artists_time_df.head(5).index,top_artists_time_df["Duration(Hours)"].head(5),color='#99ff99')
        ax1.set(title="My Top 5 Favourite Artists (based on Hours)",xlabel="Artists",ylabel="For how many hours did I stream the artist");
        ax1.tick_params(labelrotation=75);
        #second graph
        ax2.bar(top_artists_count_df.head(5).index,top_artists_count_df["Count"].head(5),color='#ffcc99')
        ax2.set(title="My Top 5 Favourite Artists (based on Counts)",xlabel="Artists",ylabel="How many times did I stream the artist");
        ax2.tick_params(labelrotation=75);
        fig.suptitle('My Top 5 Favourite Artists')
        st.pyplot(fig)

    # Favourite 100 artists
    top_artists_track_df=SH.groupby(["artistName"])
    top_artists_count_df = SH.groupby(["artistName"])[["Duration(Hours)","Duration(Minutes)","Count"]].sum().sort_values(by="Count",ascending=False)
    fav_tracks = SH.groupby(["trackName"])["Count"].count()
    if st.checkbox('Favourite 100 artists'):
        fig, ax = plt.subplots(figsize=(20,15))
        mask = np.array(Image.open("/Users/asma/Desktop/S7/DataVisualisation/pic.jpeg"))
        wordcloud = WordCloud(width=1000,height=600, max_words=100,background_color="white",contour_color='#023075',contour_width=3,colormap='rainbow',relative_scaling=1,normalize_plurals=False,mask=mask).generate_from_frequencies(fav_tracks)
        ax.imshow(wordcloud, interpolation='bilinear')
        plt.axis(False)
        st.pyplot(fig)

    # Top 5 most streamed tracks
    top_tracks_time_df = SH.groupby(["trackName"])[["Duration(Hours)","Duration(Minutes)","Count"]].sum().sort_values(by="Duration(Hours)",ascending=False)
    top_tracks_count_df = SH.groupby(["trackName"])[["Duration(Hours)","Duration(Minutes)","Count"]].sum().sort_values(by="Count",ascending=False)
    if st.checkbox('Top 5 most streamed songs'):
        fig, (ax1,ax2) = plt.subplots(1,2,figsize=(15,10))
        #first graph
        ax1.bar(top_tracks_time_df.head(5).index,top_tracks_time_df["Duration(Hours)"].head(5), color="lightblue")
        ax1.set(title="My Top 5 Favourite tracks (based on Hours)",xlabel="Artists",ylabel="For how many hours did I stream the song");
        ax1.tick_params(labelrotation=75);
        #second graph
        ax2.bar(top_tracks_count_df.head(5).index,top_tracks_count_df["Count"].head(5), color="pink")
        ax2.set(title="My Top 5 Favourite tracks (based on Counts)",xlabel="Artists",ylabel="How many times did I stream the song");
        ax2.tick_params(labelrotation=75);
        fig.suptitle('My Top 5 Favourite tracks')
        st.pyplot(fig)

    # Favourite 100 tracks
    fav_artist = SH.groupby(["artistName"])["Count"].count()
    if st.checkbox('Favourite 100 tracks'):
        fig, ax = plt.subplots(figsize=(20,15))
        mask = np.array(Image.open("/Users/asma/Desktop/S7/DataVisualisation/Guitarehorizontale.png"))
        wordcloud = WordCloud(width=1000,height=600, max_words=100,background_color="white",contour_color='#023075',contour_width=3,colormap='rainbow',relative_scaling=1,normalize_plurals=False,mask=mask).generate_from_frequencies(fav_artist)
        ax.imshow(wordcloud, interpolation='bilinear')
        plt.axis(False)
        st.pyplot(fig)

    # On which day to I listen to Spotify the most ?
    if st.checkbox('Days on which I listen to Spotify the most '):
        genre=st.radio('Choose how you want to plot it',('Box plot','Pie chart'))
        if genre=='Box plot':
            fig, ax = plt.subplots(figsize=(12,8))
            ax = sns.countplot(x=SH["day-name"],ax=ax)
            plt.xticks(rotation=75);
            ax.set(title="Average Spotify Usage over Week",xlabel="Days of the Week",ylabel="Counts of Songs Played")
            st.pyplot(fig)
        if genre=='Pie chart':
            fig, ax = plt.subplots(figsize=(10,8))
            ax.pie(SH["day-name"].value_counts(),labels=SH["day-name"].value_counts().index, autopct='%1.2f%%',startangle=180);
            centre_circle = plt.Circle((0,0),0.70,fc='white')
            fig = plt.gcf()
            fig.gca().add_artist(centre_circle)
            ax.set(title="Day wise % of Spotify Streaming")
            st.pyplot(fig)

    # When do I listen to Spotify the most ?
    if st.checkbox('Average Usage of Spotify'):
        # When do I listen to Spotify the most during a day ?
        genre=st.radio('chooso the frequency',('Daily', 'Weekly', 'Yearly'))
        if genre=='Daily':
            fig, ax = plt.subplots(figsize=(12,8))
            ax.set(title="Average Distribution of Streaming Over Day",xlabel="Hours (in 24 hour format)", ylabel="Songs Played")
            sns.histplot(SH['hours'], bins=24)
            st.pyplot(fig)

        # When do I use Spotify the most in a week ?
        active_usage = SH.groupby(['hours', 'day-name'])['artistName'].size().reset_index()
        active_usage_pivot = active_usage.pivot("hours", 'day-name', 'artistName')
        days = ["Monday", 'Tuesday', "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        if genre=='Weekly':
            fig, ax = plt.subplots(figsize=(10,18))
            ax = sns.heatmap(active_usage_pivot[days].fillna(0), robust=True, cmap="BuPu", ax = ax);
            ax.set(title="Heat Map of Spotify Usage", xlabel="Days of the Week",ylabel="Time (in 24 hrs format)")
            st.pyplot(fig)

        # When do I use Spotify the most in a year ?
        if genre=='Yearly':
            fig, ax = plt.subplots(figsize=(12,6))
            ax = sns.countplot(y=SH["month"], ax=ax)
            ax.set(title="Average Spotify Usage over Years", xlabel="Songs Played in Counts", ylabel="Months (1-12)")
            st.pyplot(fig)

    # How many hours did I spent on Spotify Streaming since the day I signed up for it?
    date_df = SH["end-Time"]
    days_spotify=(date_df.iloc[33900] - date_df.iloc[0]) / np.timedelta64(1,"D")
    time_spent_hours = SH["Duration(Hours)"].sum()
    Nb_days=SH['end-Time'][33900]-SH['end-Time'][0]
    if st.checkbox('Total time spent on Spotify'):
        st.write('Since the day I signed up for Spotify, I have streamed for exactly',round(time_spent_hours), 'hours of in a year.')
        time_spent_days=time_spent_hours/24
        time_spent_weeks=time_spent_days/7
        st.write('Which is equal to',round(time_spent_days), 'days. Or also to',round(time_spent_weeks),'weeks worth of listeneing to spotify non stop.')
        st.write('Which means out of the', 52 ,'weeks in the year, I have spent',round(time_spent_weeks),'of them listening to music on Spotify.')
        col1, col2, col3 = st.columns(3)
        col1.metric("Hours",round(time_spent_hours))
        col2.metric("Days", round(time_spent_days))
        col3.metric("Weeks", round(time_spent_weeks))
        if st.checkbox('Pie chart'):
            fig, ax = plt.subplots(figsize=(10,8))
            ax.pie([time_spent_weeks,days_spotify/7], autopct='%1.2f%%',startangle=180,colors=['#ff9999','#66b3ff'] )
            centre_circle = plt.Circle((0,0),0.70,fc='white')
            fig = plt.gcf()
            fig.gca().add_artist(centre_circle)
            ax.set(title="Year wise % of Spotify Streaming")
            st.pyplot(fig)

    # What are the top 5 days I played maximum number of songs ?
    SH["date"] = SH["end-Time"].dt.date
    most_songs = SH.groupby(["date"])[["Count"]].sum().sort_values(by="Count", ascending=False)
    if st.checkbox('Top 5 days I played maximum number of songs'):
        # Scatter plot
        average_songs_played_daily = (total_songs / days_spotify).round()
        fig,ax = plt.subplots(figsize=(15,8))
        ax.scatter(most_songs.head(5).index,most_songs["Count"].head(5),color='green',label='Top 5',marker='x')
        ax.scatter(most_songs.index[5:],most_songs["Count"][5:],color='blue',label='other',marker='s')
        ax.set(title="Maximum number of songs played in a day",xlabel="Date",ylabel="Count")
        ax.axhline(average_songs_played_daily, linestyle=":", color="r")
        ax.legend(loc='upper left')
        st.pyplot(fig)
        # Top 5 display
        st.subheader('The top 5 days when I listened to Spotify the most are: ')
        st.table(most_songs.head(5))

    # What is the average numbers of songs I played ?
    if st.checkbox('Average numbers of songs played '):
        total_songs = SH["trackName"].count()
        average_songs_played_daily = (total_songs / days_spotify).round()
        average_songs_played_weekly= (total_songs / days_spotify*7 ).round()
        col1, col2 = st.columns(2)
        col1.metric("Daily",int(average_songs_played_daily))
        col2.metric("Weekly",int(average_songs_played_weekly))

    # End
    if st.checkbox('The End'):
        st.title('Thank you for your attention !!')
        st.balloons()

if agree=='Yours':
    st.header('I will be analysing and visualizing your Spotify streaming history data. Hope you enjoy it !')
    st.subheader('We are going to concatinate your files into one dataframe to do the vizualisations. Choose how many files you are going to use :')

    uploaded_files = st.file_uploader("Upload JSON", type=["JSON"], accept_multiple_files=True) # I think that Spotify only lets you upload you Streaming History as a JSON file
    if uploaded_files:
        for file in uploaded_files:
            file.seek(0) # I saw this line that solved the issue in Streamlit discussions
        uploaded_data_read = [pd.read_json(file) for file in uploaded_files]
        SH = pd.DataFrame(pd.concat(uploaded_data_read,ignore_index=True))
        # Sample of the original data
        if st.checkbox('Show original Dataset'):
            st.header("Here's an insigth of what your data originally looked like :")
            number = st.number_input('Insert the number of random rows you want to display',value=5,step=1,key='1')
            st.write(SH.sample(number))

        # Formatting the 'endTime' and 'msPlayed' columns
        SH["end-Time"]= pd.to_datetime(SH["endTime"])
        SH['year'] = pd.DatetimeIndex(SH["end-Time"]).year
        SH['month'] = pd.DatetimeIndex(SH["end-Time"]).month
        SH['day'] = pd.DatetimeIndex(SH["end-Time"]).day
        SH['weekday'] = pd.DatetimeIndex(SH["end-Time"]).weekday
        SH['time'] = pd.DatetimeIndex(SH["end-Time"]).time
        SH['hours'] = pd.DatetimeIndex(SH["end-Time"]).hour
        SH['day-name'] = SH["end-Time"].apply(lambda x: x.day_name())
        SH['Count'] = 1
        SH["duration (hh-mm-ss)"] = pd.to_timedelta(SH["msPlayed"], unit='ms')
        # This function converts milliseconds to hours
        def hours(x):
            return x.seconds/3600
        # This function converts milliseconds to minutes
        def minutes(x):
            return (x.seconds/60)%60
        SH["Duration(Hours)"] = SH["duration (hh-mm-ss)"].apply(hours).round(2)
        SH["Duration(Minutes)"] = SH["duration (hh-mm-ss)"].apply(minutes).round(2)
        SH.drop(columns=["endTime","duration (hh-mm-ss)","msPlayed"], inplace=True)

        # Sample of the transformed data
        if st.checkbox('Show transformed Dataset'):
            st.header("Now this is what your data looks like :")
            number = st.number_input('Insert the number of random rows you want to display',value=5,step=1,key='2')
            st.write(SH.sample(number))

        # Percentage of unique songs I streamed
        unique_songs = SH["trackName"].nunique()
        total_songs = SH["trackName"].count()
        unique_songs_percentage = unique_songs/total_songs*100
        unique_songs_list = np.array([unique_songs, total_songs-unique_songs])
        unique_songs_list_labels = [" Unique Songs", "Non Unique Songs"]
        if st.checkbox('Pie chart of your unique tracks'):
            fig, ax1 = plt.subplots(figsize=(12,6))
            ax1.pie(unique_songs_list, labels= unique_songs_list_labels, autopct='%1.1f%%', explode=[0.05,0.05], startangle=180,colors=['#ff9999','#66b3ff']);
            centre_circle = plt.Circle((0,0),0.70,fc='white')
            fig =plt.gcf()
            fig.gca().add_artist(centre_circle)
            plt.title("Unique Songs Percentage")
            st.pyplot(fig)

        # Top 5 most streamed artists
        # top_artists_time_df = SH.groupby(["artistName"])[["Duration(Hours)","Duration(Minutes)","Count"]].sum().sort_values(by="Duration(Hours)",ascending=False)
        # top_artists_count_df = SH.groupby(["artistName"])[["Duration(Hours)","Duration(Minutes)","Count"]].sum().sort_values(by="Count",ascending=False)
        # if st.checkbox('Top 5 most streamed artists'):
        #     fig, (ax1,ax2) = plt.subplots(1,2,figsize=(15,10))
        #     #first graph
        #     ax1.bar(top_artists_time_df.head(5).index,top_artists_time_df["Duration(Hours)"].head(5),color='#99ff99')
        #     ax1.set(title="Your Top 5 Favourite Artists (based on Hours)",xlabel="Artists",ylabel="For how many hours did you stream the artist");
        #     ax1.tick_params(labelrotation=75);
        #     #second graph
        #     ax2.bar(top_artists_count_df.head(5).index,top_artists_count_df["Count"].head(5),color='#ffcc99')
        #     ax2.set(title="Your Top 5 Favourite Artists (based on Counts)",xlabel="Artists",ylabel="How many times did you stream the artist");
        #     ax2.tick_params(labelrotation=75);
        #     fig.suptitle('Your Top 5 Favourite Artists')
        #     st.pyplot(fig)

        # Favourite 100 artists
        top_artists_track_df=SH.groupby(["artistName"])
        top_artists_count_df = SH.groupby(["artistName"])[["Duration(Hours)","Duration(Minutes)","Count"]].sum().sort_values(by="Count",ascending=False)
        fav_tracks = SH.groupby(["trackName"])["Count"].count()
        if st.checkbox('Favourite 100 artists'):
            fig, ax = plt.subplots(figsize=(20,15))
            mask = np.array(Image.open("/Users/asma/Desktop/S7/DataVisualisation/pic.jpeg"))
            wordcloud = WordCloud(width=1000,height=600, max_words=100,background_color="white",contour_color='#023075',contour_width=3,colormap='rainbow',relative_scaling=1,normalize_plurals=False,mask=mask).generate_from_frequencies(fav_tracks)
            ax.imshow(wordcloud, interpolation='bilinear')
            plt.axis(False)
            st.pyplot(fig)

        # Top 5 most streamed tracks
        top_tracks_time_df = SH.groupby(["trackName"])[["Duration(Hours)","Duration(Minutes)","Count"]].sum().sort_values(by="Duration(Hours)",ascending=False)
        top_tracks_count_df = SH.groupby(["trackName"])[["Duration(Hours)","Duration(Minutes)","Count"]].sum().sort_values(by="Count",ascending=False)
        if st.checkbox('Top 5 most streamed songs'):
            fig, (ax1,ax2) = plt.subplots(1,2,figsize=(15,10))
            #first graph
            ax1.bar(top_tracks_time_df.head(5).index,top_tracks_time_df["Duration(Hours)"].head(5), color="lightblue")
            ax1.set(title="Your Top 5 Favourite tracks (based on Hours)",xlabel="Artists",ylabel="For how many hours did you stream the song");
            ax1.tick_params(labelrotation=75);
            #second graph
            ax2.bar(top_tracks_count_df.head(5).index,top_tracks_count_df["Count"].head(5), color="pink")
            ax2.set(title="Your Top 5 Favourite tracks (based on Counts)",xlabel="Artists",ylabel="How many times did you stream the song");
            ax2.tick_params(labelrotation=75);
            fig.suptitle('Your Top 5 Favourite tracks')
            st.pyplot(fig)

        # Favourite 100 tracks
        fav_artist = SH.groupby(["artistName"])["Count"].count()
        if st.checkbox('Favourite 100 tracks'):
            fig, ax = plt.subplots(figsize=(20,15))
            mask = np.array(Image.open("/Users/asma/Desktop/S7/DataVisualisation/Guitarehorizontale.png"))
            wordcloud = WordCloud(width=1000,height=600, max_words=100,background_color="white",contour_color='#023075',contour_width=3,colormap='rainbow',relative_scaling=1,normalize_plurals=False,mask=mask).generate_from_frequencies(fav_artist)
            ax.imshow(wordcloud, interpolation='bilinear')
            plt.axis(False)
            st.pyplot(fig)

        # On which day to I listen to Spotify the most ?
        if st.checkbox('Days on which you listen to Spotify the most '):
            genre=st.radio('Choose how you want to plot it',('Box plot','Pie chart'))
            if genre=='Box plot':
                fig, ax = plt.subplots(figsize=(12,8))
                ax = sns.countplot(x=SH["day-name"],ax=ax)
                plt.xticks(rotation=75);
                ax.set(title="Average Spotify Usage over Week",xlabel="Days of the Week",ylabel="Counts of Songs Played")
                st.pyplot(fig)
            if genre=='Pie chart':
                fig, ax = plt.subplots(figsize=(10,8))
                ax.pie(SH["day-name"].value_counts(),labels=SH["day-name"].value_counts().index, autopct='%1.2f%%',startangle=180);
                centre_circle = plt.Circle((0,0),0.70,fc='white')
                fig = plt.gcf()
                fig.gca().add_artist(centre_circle)
                ax.set(title="Day wise % of Spotify Streaming")
                st.pyplot(fig)

        # When do I listen to Spotify the most ?
        if st.checkbox('Average Usage of Spotify'):
            # When do I listen to Spotify the most during a day ?
            genre=st.radio('chooso the frequency',('Daily', 'Weekly', 'Yearly'))
            if genre=='Daily':
                fig, ax = plt.subplots(figsize=(12,8))
                ax.set(title="Average Distribution of Streaming Over Day",xlabel="Hours (in 24 hour format)", ylabel="Songs Played")
                sns.histplot(SH['hours'], bins=24)
                st.pyplot(fig)

            # When do I use Spotify the most in a week ?
            active_usage = SH.groupby(['hours', 'day-name'])['artistName'].size().reset_index()
            active_usage_pivot = active_usage.pivot("hours", 'day-name', 'artistName')
            days = ["Monday", 'Tuesday', "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            if genre=='Weekly':
                fig, ax = plt.subplots(figsize=(10,18))
                ax = sns.heatmap(active_usage_pivot[days].fillna(0), robust=True, cmap="BuPu", ax = ax);
                ax.set(title="Heat Map of Spotify Usage", xlabel="Days of the Week",ylabel="Time (in 24 hrs format)")
                st.pyplot(fig)

            # When do I use Spotify the most in a year ?
            if genre=='Yearly':
                fig, ax = plt.subplots(figsize=(12,6))
                ax = sns.countplot(y=SH["month"], ax=ax)
                ax.set(title="Average Spotify Usage over Years", xlabel="Songs Played in Counts", ylabel="Months (1-12)")
                st.pyplot(fig)

        # How many hours did I spent on Spotify Streaming since the day I signed up for it?
        date_df = SH["end-Time"]
        days_spotify=(date_df.iloc[SH.index[-1]] - date_df.iloc[0]) / np.timedelta64(1,"D")
        #st.write(SH.index[-1])
        # st.write(date_df.iloc[SH.index[-1]] - date_df.iloc[0])
        # st.write(days_spotify)
        time_spent_hours = SH["Duration(Hours)"].sum()
        Nb_days=SH['end-Time'][SH.index[-1]]-SH['end-Time'][0]
        if st.checkbox('Total time spent on Spotify'):
            st.write('Since the first this data has been collected, you have streamed for exactly',round(time_spent_hours), 'hours of in a year.')
            time_spent_days=time_spent_hours/24
            time_spent_weeks=time_spent_days/7
            st.write('Which is equal to',round(time_spent_days), 'days. Or also to',round(time_spent_weeks),'weeks worth of listeneing to spotify non stop.')
            st.write('Which means out of the', 52 ,'weeks in the year, you have spent',round(time_spent_weeks),'of them listening to music on Spotify.')
            col1, col2, col3 = st.columns(3)
            col1.metric("Hours",round(time_spent_hours))
            col2.metric("Days", round(time_spent_days))
            col3.metric("Weeks", round(time_spent_weeks))
            # if st.checkbox('Pie chart'):
            #     fig, ax = plt.subplots(figsize=(10,8))
            #     ax.pie([time_spent_weeks,days_spotify/7], autopct='%1.2f%%',startangle=180)
            #     ax.set(title="Year wise % of Spotify Streaming")
            #     st.pyplot(fig)

        # What are the top 5 days I played maximum number of songs ?
        SH["date"] = SH["end-Time"].dt.date
        most_songs = SH.groupby(["date"])[["Count"]].sum().sort_values(by="Count", ascending=False)
        if st.checkbox('Top 5 days I played maximum number of songs'):
            # Scatter plot
            average_songs_played_daily = (total_songs / days_spotify).round()
            fig,ax = plt.subplots(figsize=(15,8))
            ax.scatter(most_songs.head(5).index,most_songs["Count"].head(5),color='green',label='Top 5',marker='x')
            ax.scatter(most_songs.index[5:],most_songs["Count"][5:],color='blue',label='other',marker='s')
            ax.set(title="Maximum number of songs played in a day",xlabel="Date",ylabel="Count")
            ax.axhline(average_songs_played_daily, linestyle=":", color="r")
            ax.legend(loc='upper left')
            st.pyplot(fig)
            # Top 5 display
            st.subheader('The top 5 days when you listened to Spotify the most are: ')
            st.table(most_songs.head(5))

        # What is the average numbers of songs I played ?
        # if st.checkbox('Average numbers of songs played '):
        #     total_songs = SH["trackName"].count()
        #     average_songs_played_daily = (total_songs / days_spotify).round()
        #     average_songs_played_weekly= (total_songs / days_spotify*7 ).round()
        #     col1, col2 = st.columns(2)
        #     col1.metric("Daily",int(average_songs_played_daily))
        #     col2.metric("Weekly",int(average_songs_played_weekly))

        # End
        if st.checkbox('The End'):
            st.title('Thank you for your attention !!')
            st.balloons()
