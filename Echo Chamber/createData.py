import networkx as nx
import matplotlib.pyplot as plt
import tweepy
import json
#Rory__gilmartin
ego = "AllenLallen81"
graph = {}
graph[ego] = []
client = tweepy.Client(bearer_token='AAAAAAAAAAAAAAAAAAAAAFj0hwEAAAAACZOCgk6vyIaWdJvXMzG%2BNjYK75o%3D3GKg59g2YXoFcbKD5oyL5oP8rwfTw0kGGbtRd9MpLForplCj8Q',wait_on_rate_limit=True)

consumer_key = "cBFx745dKpTo1emtbhgJr1mAZ" 
consumer_secret = "WFFElpiFHCs9CB0JXnVQTDcNpsqW6VsJ7OV97ugD0vI5qCuoSM" 
access_token = "1299158638217453569-9DTfODUeB5y97e2YMoDrrsxjUClmVC" 
access_secret = "3ZqJgunwK6ML5GIL9j3xcnd974zw89ZctzDYJWB1lV5GJ"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
 
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth,wait_on_rate_limit=True)

G = nx.Graph()

def get_followers(name, n):
    info = client.get_user(username=name)
    user_id = info.data.id
    followers = client.get_users_followers(id=user_id, max_results=n,user_fields=["username"])
    return followers

def get_following(name, n):
    info = client.get_user(username=name)
    user_id = info.data.id
    following = client.get_users_following(id=user_id, max_results=n,user_fields=["username"])
    return following

def remove_single_element_lists(dictionary):


    keys_to_remove = []
    for key, value in dictionary.items():
        if isinstance(value, list) and len(value) == 1:
            keys_to_remove.append(key)
    for key in keys_to_remove:
        del dictionary[key]
    return dictionary

# followerData = get_followers(ego, 100).data
# followingData = get_following(ego, 100).data


# for follower in followerData:
#     graph[ego].append(follower.username)
# for following in followingData:
#     graph[ego].append(following.username)

  

# checked = []


# count = 1
# for name in graph[ego]:
#     graph[name] = [ego]
# for source in graph.keys():
#     for target in graph.keys():

#         if target not in checked and target != source:
#             friendship = api.get_friendship(source_screen_name = source, target_screen_name = target)
#             print(count)
#             count += 1
#             if friendship[0].followed_by == True or friendship[0].following == True:
#                 graph[source].append(target)
#     checked.append(source)

f = open('graph.json')
  

graph = json.load(f)
G = nx.Graph((graph))
print(graph)
node_and_degree = G.degree()
hub_ego = nx.ego_graph(G, ego,radius=100)
d = dict(G.degree)


seed = 20532

#pos = nx.spring_layout(hub_ego,k=1.3, seed=seed)
pos = nx.kamada_kawai_layout(hub_ego)
options = {

    "edgecolors": "black",
    "linewidths": 1,
    "width": 0.3,
}
print(nx.density(G))
print(len(graph))
nx.draw_networkx(hub_ego, pos,node_size=[v * 3 for v in d.values()],with_labels=False,**options)
nx.draw_networkx_nodes(hub_ego,pos,nodelist=[ego],node_size=[v * 3 for v in d.values()][0],node_color="RED",edgecolors="black",linewidths=1)
plt.axis("off")
plt.show()
