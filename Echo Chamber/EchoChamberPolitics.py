import snscrape.modules.twitter as sntwitter
import json
import csv
import math
from urllib.parse import urlparse
import networkx as nx
import matplotlib.pyplot as plt
ego = 'AllenLallen81'

color_map = []
biased_news_scores = {}
biased_hashtags_scores = {}


with open('graph.json', 'r', encoding='utf-8') as outfile:
    graph = json.load(outfile)
with open('hashtags.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        biased_hashtags_scores[row[0]] = row[1]
with open('bias_scores.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        biased_news_scores[row[0]] = row[1]


def colorConvert(score):
    if score > 0:
        return [1, 0, 0,float(abs(score))]
    if score < 0:
        return [0,0,1,float(abs(score))]
    else:
        return [0,0,0,0]


def get_political_score(handle, n):
    score = 0.0
    count = 0
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper('(from:'+ handle + ') AND (filter:links OR filter:hashtags) AND include:nativeretweets').get_items()):
        count += 1
        if i > n:
            break

        if tweet.links:
            for link in tweet.links:
                web_domain = urlparse(link.url).netloc.replace("www.", "").lower()

                if web_domain in biased_news_scores:
                    score += float(biased_news_scores[web_domain])

        if tweet.hashtags:
            for hashtag in tweet.hashtags:
                if hashtag.lower() in biased_hashtags_scores:
                    score += float(float(biased_hashtags_scores[hashtag.lower()]) * 1.5)
    if count < 5:
        return 0
    if score >= 0:
        return 1 - math.exp(-0.05 * score)
    else:
        return -(1 - math.exp(0.05 * score))

for key in graph.keys():
    color_map.append(colorConvert(get_political_score(key,1500)))
    print(key)


G = nx.Graph((graph))
node_and_degree = G.degree()
hub_ego = nx.ego_graph(G, ego,radius=100)
d = dict(G.degree)

print(color_map)
seed = 20532


pos = nx.kamada_kawai_layout(hub_ego)
#pos = nx.spring_layout(hub_ego, k=2, iterations=20)
options = {

    "edgecolors": "black",
    "linewidths": 1,
    "width": 0.2,
}
print(nx.density(G))
print(len(graph))

bing = 5
nx.draw_networkx(hub_ego, pos,node_size=[v * bing for v in d.values()],with_labels=False,node_color=color_map,**options)
nx.draw_networkx_nodes(hub_ego,pos,nodelist=[ego],node_size=[v * bing for v in d.values()][0],node_color=(0,1,0),edgecolors="black",linewidths=1)
plt.axis("off")
plt.show()

