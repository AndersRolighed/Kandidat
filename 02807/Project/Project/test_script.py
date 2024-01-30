#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Imports
import requests
import base64
import pandas as pd
import time
import json
import numpy as np
from multiprocessing import Pool
import pickle

from fuzzywuzzy import process
import fuzzywuzzy

from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

# Show retriever Class
class ShowRetriever:
    def __init__(self):
        self.show_id = None
        self.client_id = "6dae08f3c799496fad2adfe2657634a7"
        self.client_secret = "2afb39d7abb84e7fa957c2ec76b8e6f4"
        self.auth_response = None
        self.auth_header = base64.b64encode(f'{self.client_id}:{self.client_secret}'.encode()).decode('utf-8')
        self.headers = {
            'Authorization': f'Basic {self.auth_header}'
        }
        self.payload =  payload = {
            'grant_type': 'client_credentials'
        }
        self.descs = []
        self.titles = []
        self.dates = []
        
    #url = f'https://api.spotify.com/v1/shows/{show_id}/episodes?offset=1&limit=20'
        
    def authenticate(self):
        
       
        response = requests.post('https://accounts.spotify.com/api/token', data=self.payload, headers=self.headers)
        
        self.auth_response = response

    def retrieve_episodes(self, show, offset, limit):
        
        while self.auth_response.status_code != 200:
            self.authenticate()
            time.sleep(0.1)
            
    
        url = f'https://api.spotify.com/v1/shows/{show}/episodes?offset={offset}&limit={limit}'
        access_token = self.auth_response.json()['access_token']
        #print(access_token)
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(url, headers=headers)
    
        if response.status_code == 200:
            show_data = response.json()
            for episode in show_data["items"]:
                if type(episode) is not type(None):
                    self.descs.append(episode['description'])
                    self.titles.append(episode['name'])
                    self.dates.append(episode['release_date'])
            
        else:
            print(self.show_id)
            print(f"{self.show_id} gives {response}")
            
        return response
    
    def retrieve_all(self):
        offset=0
        limit=50
        response = self.retrieve_episodes(self.show_id, offset, limit)
        while response.status_code != 404:
            offset += limit
            response = self.retrieve_episodes(self.show_id, offset, limit)
            
            
# Function to run NLP/NER only if the word Podcast exists in the description
def ner_on_descs(desc):
    result = nlp(desc)
    return result


def show_search_by_name(name):
    
    time.sleep(0.1)
    show_id = None
    show_name = None
    if len(name) > 0:
        search_query = name.replace(' ', '%2B')
    else:
        return (show_id, show_name)
    client_id='6dae08f3c799496fad2adfe2657634a7'
    client_secret='2afb39d7abb84e7fa957c2ec76b8e6f4'
    
    #show_id = '4rOoJ6Egrf8K2IrywzwOMk'
    url = f'https://api.spotify.com/v1/search?q={search_query}&type=show&market=US&limit=10'
    #url = 'https://api.spotify.com/v1/search?q=JRE&type=show'
    auth_header = base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode('utf-8')
    
    headers = {
        'Authorization': f'Basic {auth_header}'
    }
    
    payload = {
        'grant_type': 'client_credentials'
    }
    response = requests.post('https://accounts.spotify.com/api/token', data=payload, headers=headers)
    
    if response.status_code == 200:
        access_token = response.json()['access_token']
        
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            show_data = response.json()
            #print(search_query)
           # print(show_data)
            if len(show_data['shows']['items']) > 0:
                #print(len(show_data['shows']['items']))
                try:
                    show_id = show_data['shows']['items'][0]['id']
                    show_name = show_data['shows']['items'][0]['name']
                except TypeError:
                    show_id = None
                    show_name = None
        else:
            print(f"Error: Unable to retrieve show information. Status code {response.status_code}")
    else:
        print(f"Error: Unable to retrieve access token. Status code {response.status_code}")
        
    return (show_id, show_name)

with open("podcasters.pkl", "rb") as f:
    podcasters = pickle.load(f)

def find_closest_match(query_name,name_list=podcasters, threshold=100):
    """
    Find the closest match to 'query_name' in 'name_list'.
    
    :param name_list: List of names to search.
    :param query_name: Name to search for.
    :param threshold: The minimum score for a match (0-100, where 100 is an exact match).
    :return: Closest match name and its score, or None if no match above the threshold.
    """
    # Use the 'extractOne' method to find the closest match
    if query_name is not None:
        best_match = process.extractOne(query_name, name_list, score_cutoff=threshold,scorer= fuzzywuzzy.fuzz.token_set_ratio)
        if best_match:
            return best_match[0]
    else:
        return None
    
def name_extraction_from_ner(ner_results):
    output = ner_results
    
    person_names = []
    current_name = ""
    if output != '':
        for i, token in enumerate(output):
            if token['entity'] in ['B-PER', 'I-PER'] and not token['word'].startswith('##'):
                current_name += ' '
            if token["entity"] in ["B-PER", "I-PER"]:
                current_name += token['word'].replace('##', '')
        
            if i == len(output) - 1 or (i + 1 < len(output) and output[i + 1]['entity'] not in ['I-PER', 'B-PER']):
                if current_name:
                    person_names.append(current_name.strip())  # Strip leading and trailing spaces before appending
                    current_name = ""
        
    #print("Extracted Person Names:", person_names)
    return person_names
    
SR = ShowRetriever()
SR.authenticate()
SR.show_id = '4rOoJ6Egrf8K2IrywzwOMk'
SR.retrieve_all()


tokenizer = AutoTokenizer.from_pretrained("dslim/bert-large-NER")
model = AutoModelForTokenClassification.from_pretrained("dslim/bert-large-NER")

nlp = pipeline("ner", model=model, tokenizer=tokenizer)

df = pd.read_pickle("JRE_DF.pkl")

from queue import Queue
processed_ids = set()  # Initialize an empty set to keep track of processed IDs
final_df = pd.DataFrame(columns=['OriginShow', 'Showname', 'PodcastHosts', 'GuestShowSpotifyId'])


def process_single_id(id_number, showname, queue):
    if id_number in processed_ids and id_number is not None:
        return  # Skip if the ID has already been processed

    SR = ShowRetriever()
    SR.authenticate()
    SR.show_id = id_number
    SR.retrieve_all()
    
    num_processes = 3

    with Pool(num_processes) as pool:
        results = pool.map(ner_on_descs, SR.descs)

    with Pool(num_processes) as pool:
        names = pool.map(name_extraction_from_ner, results)

    guests_and_dates = pd.DataFrame({'Guest':names, 'Dates':SR.dates})
    print(guests_and_dates)
    
    filter = [ x for x in names if len(x)>0]
    single = [x[0] for x in filter]
    with Pool(num_processes) as pool:
        matches = pool.map(find_closest_match, single)
        matches = list(set([x for x in matches if x is not None]))
        matches =  [s.split(' (')[0] for s in matches if s is not None]

    with Pool(num_processes) as pool:
        search_results = pool.map(show_search_by_name, matches)
        guest_show_names = np.transpose(list(search_results))[1]
        guest_show_ids = np.transpose(list(search_results))[0]

    showname_list = [showname for _ in range(len(show_ids))]
    temp_df = pd.DataFrame([showname_list, guest_show_names, matches, guest_show_ids, guests_and_dates],
                           columns=['OriginShow', 'Showname', 'PodcastHosts', 'GuestShowSpotifyId', 'guests_and_dates'])
 
    print(temp_df)
    global final_df
    final_df = pd.concat([final_df, temp_df], ignore_index=True)

    processed_ids.add(id_number)  # Add the current ID to the set of processed IDs, as to not use the same ID twice
    
    for new_id, new_showname in zip(guest_show_ids, guest_show_names): # Recursion
        if new_id is None:
            continue
        else:
            queue.put((new_id, new_showname))

def ids_to_descs(ids: list, start_podcast: str):
    queue = Queue()
    
    # Add initial IDs to the queue
    for id_number in ids:
        if id_number is not None:
            queue.put((id_number, start_podcast))
    print(queue)
    while not queue.empty():
        id_number, showname = queue.get()
        print("QUEUEGET",id_number, showname)
        process_single_id(id_number, showname, queue)
        
podcast_ids = list(df["GuestShowSpotifyId"])
ids_to_descs(podcast_ids, "The Joe Rogan Experience")
    


# In[3]:





# In[ ]:




