import pandas as pd

def load_data(DATA_PATH):
    data = pd.read_csv(DATA_PATH, encoding='utf-8')
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data['daily'] = pd.to_datetime(data['daily'], format='%Y-%m-%d').dt.date
    return data