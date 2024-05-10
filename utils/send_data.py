import pandas as pd
from datetime import datetime
import os
import requests
from dotenv import load_dotenv

load_dotenv()

CLASSIFICATION_ENDPOINT = os.getenv('CLASSIFICATION_ENDPOINT')
API_KEY = os.getenv('API_KEY')

def send_track_data(track_id, save_path, rec_start_format):
    if not os.path.exists(os.path.join(save_path, f"{rec_start_format}_metadata.csv")):
        return
    metadata = pd.read_csv(os.path.join(save_path, f"{rec_start_format}_metadata.csv"))
    track_data = metadata[metadata['track_ID'] == track_id]
    if track_data.empty:
        return
    start_date = datetime.strptime(track_data['timestamp'].min(), '%Y-%m-%dT%H:%M:%S.%f')
    end_date = datetime.strptime(track_data['timestamp'].max(), '%Y-%m-%dT%H:%M:%S.%f')
    duration = int((end_date - start_date).total_seconds())
    
    track_files = [f for f in os.listdir(os.path.join(save_path, 'crop', 'insect')) if f'ID{track_id}' in f.split('_')]
    file_paths = [os.path.join(save_path, 'crop', 'insect', f) for f in track_files]

    endpoint = f'{CLASSIFICATION_ENDPOINT}/{track_id}'
    
    payload = {'start_date': start_date, 'end_date': end_date, 'duration_s': duration}
    files = [('files', open(fp, 'rb')) for fp in file_paths]
    
    response = requests.post(endpoint, data=payload, files=files, headers={'access_token': API_KEY})
    print(response)