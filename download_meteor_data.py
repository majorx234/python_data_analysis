import requests
import pandas as pd

response = requests.get(
    'https://data.nasa.gov/resource/gh4g-9sfh.json',
    params={'$limit': 50_000}
)

if response.ok:
    payload = response.json()
    df = pd.DataFrame(payload)
    df.to_csv('data/meteor_data.csv')
else:
    print(f'Request was not successful and returned code: {response.status_code}.')
    payload = None
