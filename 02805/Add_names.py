import matplotlib.pyplot as plt
import networkx as nx

# Load the graph with sentiments
G = nx.read_graphml('rapper_network_with_sentiments.graphml')

# Get sentiment scores
sentiments = [G.nodes[node]['sentiment_score'] for node in G.nodes if G.nodes[node]['sentiment_score'] != 0]

# Create a histogram
plt.hist(sentiments, bins=20, color='skyblue', edgecolor='black')
plt.title('Sentiment Scores of Rapper Pages')
plt.xlabel('Sentiment Score')
plt.ylabel('Frequency')
plt.show()

# Find the happiest and saddest rappers
sorted_nodes = sorted(G.nodes, key=lambda x: G.nodes[x]['sentiment_score'])
happiest_rappers = [(node, G.nodes[node]['sentiment_score']) for node in sorted_nodes[-10:] if G.nodes[node]['sentiment_score'] > 0]

# Find the rappers with the lowest sentiment scores (excluding 0)
lowest_sentiment_rappers = [(node, G.nodes[node]['sentiment_score']) for node in G.nodes if G.nodes[node]['sentiment_score'] > 0]

# Sort by sentiment score in ascending order
sorted_rappers = sorted(lowest_sentiment_rappers, key=lambda x: x[1])

# Print the 10 rappers with the lowest sentiment scores
print('\n10 Rappers with the Lowest Sentiment Scores:')
for rapper, sentiment_score in sorted_rappers[:10]:
    print(f'{rapper}: {sentiment_score:.2f}')
    
print(f'\nTop 10 Happiest Rappers:')
for rapper, sentiment_score in happiest_rappers:
    print(f'{rapper}: {sentiment_score:.2f}')