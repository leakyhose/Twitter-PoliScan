import networkx as nx
import matplotlib.pyplot as plt
import tweepy
import json
import accuracyTest as at


client = tweepy.Client(bearer_token='AAAAAAAAAAAAAAAAAAAAAFj0hwEAAAAACZOCgk6vyIaWdJvXMzG%2BNjYK75o%3D3GKg59g2YXoFcbKD5oyL5oP8rwfTw0kGGbtRd9MpLForplCj8Q', wait_on_rate_limit=True)
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

   
def find_followers(ego, graph):
    followerData = get_followers(ego, 100).data
    followingData = get_following(ego, 100).data

    for follower in followerData:
        graph[ego].append(follower.username)
    for following in followingData:
        graph[ego].append(following.username)

      
def color_convert(score):
    if score > 0:
        return [1, 0, 0, float(abs(score))]
    if score < 0:
        return [0, 0, 1, float(abs(score))]
    else:
        return [0, 0, 0, 0]

     
def get_echo_chamber(ego):
	graph = {}
	graph[ego] = []
	
	findFollowers(ego, graph)
    checked = []

    count = 1
    for name in graph[ego]:
        graph[name] = [ego]
      
    for source in graph.keys():
        for target in graph.keys():
        	if target not in checked and target != source:
            	friendship = api.get_friendship(source_screen_name = source, target_screen_name = target)
                count += 1
            
                if friendship[0].followed_by == True or friendship[0].following == True:
                        graph[source].append(target)
               
            checked.append(source)

    color_map = []
    for key in graph.keys():
        color_map.append(colorConvert(at.get_political_score(key, 1500)))
	
	return graph

		
if __name__ == '__main__':
	ego = "AllenLallen81"
	graph = get_echo_chamber(ego)
	
    G = nx.Graph((graph))
    node_and_degree = G.degree()
    hub_ego = nx.ego_graph(G, ego, radius=100)
    d = dict(G.degree)

    print(color_map)
    seed = 20532

    pos = nx.kamada_kawai_layout(hub_ego)
    options = {
        "edgecolors": "black",
        "linewidths": 1,
        "width": 0.2,
    }
    
    print(nx.density(G))
    print(len(graph))

    bing = 5
    nx.draw_networkx(hub_ego, pos, node_size=[v * bing for v in d.values()], with_labels=False,n ode_color=color_map, **options)
    nx.draw_networkx_nodes(hub_ego, pos, nodelist=[ego], node_size=[v * bing for v in d.values()][0], node_color=(0, 1, 0), edgecolors="black", linewidths=1)
    plt.axis("off")
    plt.show()
