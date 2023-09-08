import plotly.express as px

# +ve/-ve Chart Code
def pos_neg_chart(df):
    df = df.loc[df["polarity_label"] != 'Neutral']
    group_data = df.value_counts(['daily', 'polarity_label']).reset_index(name='count').sort_values('daily', ascending=True)

    fig = px.line(
        group_data,
        x = 'daily',
        y = 'count',
        color = 'polarity_label',
        color_discrete_map={
            'Positive': 'green',
            'Negative': 'red'
        }
    )

    fig.update_layout(
        autosize=True,
        title='Daily Positive/Negative Tweets',
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(
                        label="1 day",
                        step="day",
                    ),
                    dict(
                        label="1 month",
                        step="month",
                    ),
                    dict(
                        label="6 month",
                        step="month",
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