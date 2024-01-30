import csv
import requests
from bs4 import BeautifulSoup
import networkx as nx

# Load CSV files
east_coast_rappers = []
west_coast_rappers = []

with open('EastCoastRappers.csv', 'r') as file:
    east_coast_rappers = [row[1] for row in csv.reader(file)]

with open('WestCoastRappers.csv', 'r') as file:
    west_coast_rappers = [row[1] for row in csv.reader(file)]

# Read the sentiment data
word_sentiments = {}
with open('Data_Set_S1.txt', 'r') as file:
    reader = csv.DictReader(file, delimiter='\t')
    for row in reader:
        word_sentiments[row['word']] = float(row['happiness_average'])

# Initialize a directed graph
G = nx.DiGraph()

# Define functions to get coast information from rapper names
def get_coast(rapper_name):
    if rapper_name in east_coast_rappers:
        return 'East Coast'
    elif rapper_name in west_coast_rappers:
        return 'West Coast'
    else:
        return None

# Function to calculate sentiment score for a text
def calculate_sentiment(text):
    words = text.split()
    sentiment_scores = [word_sentiments.get(word.lower(), 0) for word in words]
    return sum(sentiment_scores)
for rapper_list, coast in [(east_coast_rappers, 'East Coast'), (west_coast_rappers, 'West Coast')]:
    for rapper in rapper_list:
        url = f'https://en.wikipedia.org/wiki/{rapper}'
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            content = soup.find('div', {'class': 'mw-parser-output'}).get_text()

            # Calculate sentiment score
            sentiment_score = calculate_sentiment(content)

            # Check if the linked page corresponds to a rapper in either coast list
            G.add_node(f'{rapper} ({coast})', sentiment_score=sentiment_score, coast=coast, content=content)

            links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('/wiki/') and not a['href'].startswith('/wiki/File')]

            for link in links:
                linked_rapper = link.split('/')[-1]
                linked_coast = get_coast(linked_rapper)
                if linked_coast is not None:
                    G.add_edge(f'{rapper} ({coast})', f'{linked_rapper} ({linked_coast})')

# Save the network as a GraphML file
nx.write_graphml(G, 'rapper_network_with_sentiments.graphml')
