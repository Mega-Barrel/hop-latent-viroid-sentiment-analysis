import streamlit as st
from src.utils import ( load_dataset as ld )
from src.graphs import (
    polarity_pie as pp,
    tweet_trend as tt
)

def sample_page():

    st.markdown(
    """
        ⬇️ Compare **Virus VS Mould** keyword tweets
    """
    )
    kwd_1, kwd_2 = st.columns(2)
    kwd_1.subheader('Keyword 1')
    kwd_2.subheader('Keyword 2')

    VIRUS_kEYWORDS_NAMES = {
        'Bud Rot': 'data/bud_rot_data.csv',
        'Hop Latent Viroid': 'data/hop_latent.csv'
    }
    
    MOLD_kEYWORDS_NAMES = {
        'Cannabis Mold': 'data/cannabis_mold_data.csv',
        'Cannabis Mould': 'data/cannabis_mould_data.csv',
    }

    V_DATA_PATH = kwd_1.selectbox('Select Virus Keywords', VIRUS_kEYWORDS_NAMES)
    M_DATA_PATH = kwd_2.selectbox('Select Mold Keywords', MOLD_kEYWORDS_NAMES)

    vdata = ld.load_data(VIRUS_kEYWORDS_NAMES[V_DATA_PATH])
    mdata = ld.load_data(MOLD_kEYWORDS_NAMES[M_DATA_PATH])

    # Create metrics for Virus keywords
    col1, col2, col3 = kwd_1.columns(3)
    col1.metric('Total Tweets', value=len(vdata))
    col2.metric('Total Contributors', value=len(vdata['username'].unique()))
    col3.metric('Avg Sentiment Score', value=round(vdata.loc[:, 'tweet_polarity_score'].mean(), 2))

    kwd_1.plotly_chart(tt.tweet_trend_chart(vdata['daily']), use_container_width = True)
    kwd_1.plotly_chart(pp.polarity_pie_chart(vdata), use_container_width=True)
    # Raw data
    kwd_1.subheader('Raw Data')
    kwd_1.write(vdata)

    # Create metrics for mold keywords
    col1, col2, col3 = kwd_2.columns(3)
    col1.metric('Total Tweets', value=len(mdata))
    col2.metric('Total Contributors', value=len(mdata['username'].unique()))
    col3.metric('Avg Sentiment Score', value=round(mdata.loc[:, 'tweet_polarity_score'].mean(), 2))
    kwd_2.plotly_chart(tt.tweet_trend_chart(mdata['daily']), use_container_width = True)
    kwd_2.plotly_chart(pp.polarity_pie_chart(mdata), use_container_width=True)

    # Raw data
    kwd_2.subheader('Raw Data')
    kwd_2.write(mdata)
