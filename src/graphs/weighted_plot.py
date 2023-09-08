import plotly.express as px

# Weighted polarity Score
def weighted_polarity_line_chart(df):
    # grouping the dataframe
    group_data = df.groupby(
        ['daily']
    ).mean().groupby('daily')['tweet_polarity_score'].median().reset_index()
    # plot code
    fig = px.line(
        group_data, 
        x = 'daily',
        y = "tweet_polarity_score",
        title = 'weighted polarity hourly plot'
    )
    # Add range slider
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(
                        label="1 day",
                        step="day",
                    ),
                    dict(
                        count=1,
                        label="1m",
                        step="month",
                        stepmode="backward"
                    ),
                    dict(
                        count=6,
                        label="6m",
                        step="month",
                        stepmode="backward"
                    ),
                    dict(
                        count=1,
                        label="1y",
                        step="year",
                        stepmode="backward"
                    ),
                    dict(
                        step="all"
                    )
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="-"
        ),
        hovermode = 'x'
    )
    return fig