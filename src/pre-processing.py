import re
import datetime
import calendar
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initializing sentiment class
analyzer = SentimentIntensityAnalyzer()

def process_df(filepath, encoding):
    df = pd.read_csv(filepath, encoding=encoding)
    df = df[['images', 'text', 'likes', 'replies', 'retweets', 'quotes', 'timestamp', 'url', 'verified', 'username']]
    return df

def transform_data(df):
    df['user_name'] = df['username'].apply(lambda x: x[1:])
    df = df[['timestamp', 'username', 'text', 'url', 'images', 'likes', 'replies', 'retweets', 'quotes', 'verified']]
    return df

def weekday_weekends(x):
    try:
        x = x[:10]
        date = datetime.datetime.strptime(x, '%Y-%m-%d')
        day_name = calendar.day_name[date.weekday()]
        if day_name == 'Sunday' or day_name == 'Saturday':
            return 'weekend'
        else:
            return 'weekday'
    except Exception as e:
        print(e)
    
def get_year(x):
    try:    
        year = x.split('-')[0]
        return year
    except Exception as e:
        pass

def get_daily(x):
    try:
        daily = x[:10]
        return daily
    except Exception as error:
        pass

# Cleaning the text column
def clean_tweet(text):
    # Removing all usernames
    text = re.sub(r'@[A-Za-z0-9_]+', '', str(text))
    # Removing all URLS/LINKS
    text = re.sub(r'https?:\/\/\S+', '', text)
    # Removing all NUMBERS AND PERCENTAGES
    text = re.sub(r'[0-9%?]', '', text)
    # OTHER SPECIAL CHARACTERS LIKE #, @ + ARE REMOVED 
    text = re.sub(r'[#$%^&*()-+]', '', text)
    # REMOVE THE WORD RT
    text = re.sub(r'RT[\s]', '', text)
    # REMOVE NEWLINE AND CARIRIAGE CHARACTERS
    text = re.sub(r'[/\r?\n|\r/]', '' ,text)
    # REMOVE EXTRA WHITESPACES
    text = text.strip()
    # returning the clean text data
    return text

# getting the sentiment polarity scores
def get_polarity_score(tweet_text):
    tweet_polarity = analyzer.polarity_scores(tweet_text)
    polarity_score = tweet_polarity['compound']
    return polarity_score

# Adding lable to the polarity scores
def getsentiment(score):
    if score <= -0.05:
        return 'Negative'
    elif score >= 0.05:
        return 'Positive'
    else:
        return 'Neutral'
    
def main():
    file_1 = '../data/raw_data/cannabis_mould_2020_data.csv'
    file_2 = '../data/raw_data/cannabis_mould_2021_data.csv'
    file_3 = '../data/raw_data/cannabis_mould_2022_data.csv'
    file_4 = '../data/raw_data/cannabis_mould_2023_data.csv'

    df_1 = process_df(file_1, encoding='utf-8')
    print('Reading file 1 done')
    df_2 = process_df(file_2, encoding='utf-8')
    print('Reading file 2 done')
    df_3 = process_df(file_3, encoding='utf-8')
    print('Reading file 3 done')
    df_4 = process_df(file_4, encoding='utf-8')
    print('Reading file 4 done')

    merged_df = pd.concat([df_1, df_2, df_3, df_4], ignore_index=True)
    # merged_df.to_csv('test.csv', index=False)
    merged_df = transform_data(merged_df)
    
    merged_df['daily'] = merged_df['timestamp'].apply(get_daily)
    merged_df['is_weekday'] = merged_df['daily'].apply(weekday_weekends)
    merged_df['year'] = merged_df['timestamp'].apply(get_year)
    merged_df['cleaned_tweet'] = merged_df['text'].apply(clean_tweet)
    # creating a new column 'tweet_polarity_score'
    merged_df['tweet_polarity_score'] = merged_df['cleaned_tweet'].apply(get_polarity_score)
    merged_df['polarity_label'] = merged_df['tweet_polarity_score'].apply(getsentiment)

    print(len(merged_df))
    merged_df.to_csv('../data/cannabis_mould_data.csv', index=False, encoding='utf-8')

if __name__ == '__main__':
    main()