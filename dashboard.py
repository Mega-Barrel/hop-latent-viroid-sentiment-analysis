import pandas as pd
import streamlit as st

from src.graphs import (
    tweet_trend as tt,
    weighted_plot as wt,
    polarity_pie as pp,
    top_hashtag as th,
    polarity_bar as pb
)


st.set_page_config(layout="wide")

st.title('Twitter Sentiment Analytics')

DATA_PATH = 'data/data.csv'

@st.cache_data
def load_data():
    data = pd.read_csv(DATA_PATH, encoding='utf-8')
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    return data

# load the data
data = load_data()

tweet_analysis, image_tweets, raw_data = st.tabs([
    'Tweet Analysis',
    'Tweets With Images',
    'Raw Data'
])

with tweet_analysis:
    # Metrics
    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric('Total Tweets', value=len(data))
    col2.metric('Total Contributors', value=len(data['username'].unique()))
    col3.metric('Avg Sentiment Score', value=round(data.loc[:, 'tweet_polarity_score'].mean(), 2))

    weekday = data.loc[data['is_weekday'] == 'weekday']
    weekend = data.loc[data['is_weekday'] == 'weekend']

    col4.metric('Total Weekday Tweets', value=len(weekday))
    col5.metric('Total Weekend Tweets', value=len(weekend))

    # Daily tweets
    st.plotly_chart(tt.tweet_trend_chart(data['daily']), use_container_width = True)

    # Tweet Polarity Distribution and Weighted plot
    row1_col1, row1_col2 = st.columns(2)
    row1_col1.plotly_chart(pp.polarity_pie_chart(data), use_container_width=True)
    row1_col2.plotly_chart(wt.weighted_polarity_line_chart(data[['daily', 'tweet_polarity_score']]), use_container_width = True)

    row2_col1, row2_col2 = st.columns(2)
    row2_col1.plotly_chart(th.plot_hashtag(data['text']), use_container_width=True)
    row2_col2.plotly_chart(pb.pos_neg_chart(data), use_container_width = True)

with image_tweets:
    filtered_data = data[data['images'].notna()]
    filtered_data = filtered_data[['timestamp', 'text', 'images', 'polarity_label', 'likes', 'retweets', 'quotes', 'replies']]
    st.write(filtered_data)

with raw_data:
    st.subheader('Raw Data')
    st.write(data)
