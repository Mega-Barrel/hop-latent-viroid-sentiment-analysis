import streamlit as st

from src.graphs import (
    tweet_trend as tt,
    weighted_plot as wt,
    polarity_pie as pp,
    top_hashtag as th,
    polarity_bar as pb
)
from src.utils import ( load_dataset as ld )
from datetime import ( timedelta )

def home_page():
    # Keywords dict
    kEYWORDS_NAMES = {
        'Bud Rot': 'data/bud_rot_data.csv',
        'Cannabis Mold': 'data/cannabis_mold_data.csv',
        'Cannabis Mould': 'data/cannabis_mould_data.csv',
        'Hop Latent': 'data/hop_latent.csv'
    }

    DATA_PATH = st.selectbox('Select the Keyword', kEYWORDS_NAMES)
    # load the data
    data = ld.load_data(kEYWORDS_NAMES[DATA_PATH])

    # Double ended date slider
    start_dt = data['daily'].min()
    end_dt = data['daily'].max()

    st.subheader('Date Filter')
    date_filter = st.slider(
        "Select a date range",
        min_value = start_dt,
        max_value = end_dt,
        value = (
            start_dt, 
            end_dt
        ),
        step = timedelta(days=1),
        format="YYYY/MM/DD"
    )

    filtered_data = data[ ( data["daily"] >= date_filter[0] ) & ( data["daily"] <= date_filter[1] ) ]

    tweet_analysis, image_tweets, raw_data = st.tabs([
        'Tweet Analysis',
        'Tweets With Images',
        'Raw Data'
    ])

    with tweet_analysis:
        # Metrics
        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric('Total Tweets', value=len(filtered_data))
        col2.metric('Total Contributors', value=len(filtered_data['username'].unique()))
        col3.metric('Avg Sentiment Score', value=round(filtered_data.loc[:, 'tweet_polarity_score'].mean(), 2))

        weekday = filtered_data.loc[filtered_data['is_weekday'] == 'weekday']
        weekend = filtered_data.loc[filtered_data['is_weekday'] == 'weekend']

        col4.metric('Total Weekday Tweets', value=len(weekday))
        col5.metric('Total Weekend Tweets', value=len(weekend))

        # Daily tweets
        st.plotly_chart(tt.tweet_trend_chart(filtered_data['daily']), use_container_width = True)

        # Tweet Polarity Distribution and Weighted plot
        row1_col1, row1_col2 = st.columns(2)
        row1_col1.plotly_chart(pp.polarity_pie_chart(filtered_data), use_container_width=True)
        row1_col2.plotly_chart(wt.weighted_polarity_line_chart(filtered_data[['daily', 'tweet_polarity_score']]), use_container_width = True)

        row2_col1, row2_col2 = st.columns(2)
        row2_col1.plotly_chart(th.plot_hashtag(filtered_data['text']), use_container_width=True)
        row2_col2.plotly_chart(pb.pos_neg_chart(filtered_data), use_container_width = True)

    with image_tweets:
        image_filter = filtered_data[filtered_data['images'].notna()]
        image_filter = image_filter[['timestamp', 'text', 'images', 'polarity_label', 'likes', 'retweets', 'quotes', 'replies']]
        st.write(image_filter)

    with raw_data:
        st.subheader('Raw Data')
        st.write(data)