import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

def uniqueSongs2(SH):
    unique_songs = SH["trackName"].nunique()
    total_songs = SH["trackName"].count()
    fig3 = px.pie(values=np.array([unique_songs, total_songs-unique_songs]), names=["New Songs", "Old Songs"], color=["New Songs", "Old Songs"],
    color_discrete_map={'Sendo':'cyan', 'Tiki':'royalblue','Shopee':'darkblue'})
    fig3.update_layout(
    title="<b>Comparing songs by percentage</b>")
    return fig3

def TopArtists(SH,n):
    top_artists_time_df = SH.groupby(["artistName"])[["Duration(Hours)","Duration(Minutes)","Count"]].sum().sort_values(by="Duration(Hours)",ascending=False)
    top_artists_count_df = SH.groupby(["artistName"])[["Duration(Hours)","Duration(Minutes)","Count"]].sum().sort_values(by="Count",ascending=False)
    fig = make_subplots(rows=1, cols=2,subplot_titles=("By Hours", "By Count"))
    fig.add_trace(go.Bar(x=top_artists_time_df.head(n).index, y=top_artists_time_df["Duration(Hours)"].head(n)),row=1, col=1)
    fig.add_trace(go.Bar(x=top_artists_count_df.head(n).index,y=top_artists_count_df["Count"].head(n)),row=1, col=2)
    fig.update_layout(height=600, width=800, title_text="Favourite Artists")
    return fig
def TopArtistsPieChart(SH,n):
    fvrtArtists=SH["artistName"].value_counts()[SH["artistName"].value_counts()>100][:n]
    fig3 = px.pie(values=fvrtArtists.values, names=fvrtArtists.keys(), color=fvrtArtists.keys(),
    color_discrete_sequence=px.colors.sequential.RdBu)
    fig3.update_layout(
    title="<b>Top Artists</b>")
    fig3.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    return fig3


def TopTracks(SH,n):
    top_tracks_time_df = SH.groupby(["trackName"])[["Duration(Hours)","Duration(Minutes)","Count"]].sum().sort_values(by="Duration(Hours)",ascending=False)
    top_tracks_count_df = SH.groupby(["trackName"])[["Duration(Hours)","Duration(Minutes)","Count"]].sum().sort_values(by="Count",ascending=False)
    
    fig = make_subplots(rows=1, cols=2,subplot_titles=("By Hours", "By Count"))
    fig.add_trace(go.Bar(x=top_tracks_time_df.head(n).index, y=top_tracks_time_df["Duration(Hours)"].head(n), marker_color='blue'),row=1, col=1)
    fig.add_trace(go.Bar(x=top_tracks_count_df.head(n).index,y=top_tracks_count_df["Count"].head(n),marker_color="crimson"),row=1, col=2)
    fig.update_layout(height=600, width=800, title_text="Favourite Tracks")
    return fig

def TopTracksPieChart(SH,n):
    fvrtArtists=SH["trackName"].value_counts()[SH["trackName"].value_counts()>100][:n]
    fig3 = px.pie(values=fvrtArtists.values, names=fvrtArtists.keys(), color=fvrtArtists.keys(),
    color_discrete_sequence=px.colors.sequential.Blugrn)
    fig3.update_layout(
    title="<b>Top Tracks</b>")
    fig3.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    return fig3

def daywiseUsage(SH,t):
    days=SH['day-name'].value_counts()
    if t=='Bar Chart':
        fig3 = px.bar(y=days.values, x=days.keys(),color=days.keys())
        fig3.update_layout(
        title="<b>Day Wise Analysis (Bar Chart)</b>")   
    if t=='Pie Chart':
        fig3 = px.pie(values=days.values, names=days.keys(), color=days.keys(),
        color_discrete_sequence=px.colors.sequential.Agsunset)
        fig3.update_layout(
        title="<b>Day Wise Analysis</b>")
        fig3.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    return fig3

def usageByTime(SH,t):
    if t=='Daily':
        hours=SH['hours'].value_counts()
        fig = px.bar(y=hours.values, x=hours.keys(),color=hours.keys())
        fig.update_layout(
        title="<b>Daily Analysis</b>")
    if t=='Weekly':
        days=SH['day-name'].value_counts()
        fig=px.funnel(days,color=days.keys())
        fig.update_layout(
        title="<b>Weekly Analysis</b>")
    if t=='Yearly':
        days=SH['month-name'].value_counts()
        fig = px.pie(values=days.values, names=days.keys(), color=days.keys(),
        color_discrete_sequence=px.colors.sequential.Agsunset)
        fig.update_layout(title="<b>Yearly Analysis</b>")
    return fig
