import plotly.express as px

def tweet_trend_chart(df):    
    # grouping the dataframe
    group_data = df.value_counts(['daily']).reset_index(name='count').sort_values('daily', ascending=False)
    
    # plot code
    fig = px.line(
        group_data, 
        x = 'daily', 
        y = 'count',
        title = 'Daily Tweet trend'
        # width=1500
    )
    # Add range slider
    fig.update_layout(
        autosize=True,
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
                    dict(count=1,
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
    
    fig.update_yaxes(
        automargin=True
    )
    
    return fig