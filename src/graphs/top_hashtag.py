import re
import plotly.express as px
import pandas as pd

# Plot for most used hashtags
def count_hashtag(data):
    hash_tag = data
    hashtags = {}
    pattern = re.compile(r"(?<=[\s>])#(\d*[A-Za-z_]+\d*)\b(?!;)")

    for i in hash_tag:
        t = re.findall(pattern, str(i))
        for j in t:
            if j not in hashtags:
                hashtags[j] = 1
            else:
                hashtags[j] += 1
    return hashtags


def create_dataframe(data):
    d = count_hashtag(data)
    name = list(d.keys())
    values = list(d.values())
    hashtag_df = pd.DataFrame({"Hashtags": name, "Frequency": values})
    return hashtag_df


def plot_hashtag(data):
    # Calling the function
    d = create_dataframe(data).sort_values(by="Frequency", ascending=False)
    subset_df = d[d.Frequency >= 5]
    fig = px.bar(
        data_frame=subset_df,
        x="Hashtags",
        y="Frequency",
        barmode="group",
        orientation="v",
        title='Top Trending Hashtags'
    )
    return fig