import snscrape.modules.twitter as sntwitter
import json
import time

#compiles the set, with the given root hashtags

left = ["EndGunViolence","CancelStudentDebt","ClimateCrisis","GetVaccinated","voteblue","DefendOurDemocracy","democratsdeliver","TrumpShutdown","reasontovoteblue","VoteBlueToSaveDemocracy","votedemocrat", "DNC", "Biden", "Biden2024","lgbtq","FlipTheHouseBlue","abortionishealthcare","TransRightsAreHumanRights"]
right = ["BidenBorderCrisis", "Bidenflation","ProLife",'NationalPoliceWeek',"votered","DemocratsAreDestroyingAmerica","LiberalHypocrisy","Trump2024","SaveAmerica","maga","voteconservative","GOP","Trump", "Trump2024","bordercrisis","backtheblue","FireFauci","HunterBidensLaptop"]
neutral = ["ukrainewar", "abortion", "smallbiz", "PeopleOverPolitics","climatechange","BlackHistoryMonth","NeverForget","PeopleOverPolitics","uspolitics","roevwade","2022midterms","disinformation","potus","scotus"]

sets = []
times = []

rootTags = left + right + neutral
print(rootTags)
print(len(rootTags))
def tweet_scraper(query, n_tweet):


    max_tweet = n_tweet
    hashtags = []
    tic = time.perf_counter()
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):

        if len(hashtags)>max_tweet:
            break
        if tweet.hashtags:
            h = [item.lower() for item in tweet.hashtags]

            if (h not in hashtags and len(h) > 1):
                    hashtags.append(h)
                    # times.append(time.perf_counter() - tic)
                    # tic = time.perf_counter()
                    # print(((sum(times)/len(times) * 400000) - sum(times))/60/60)
                    

    return hashtags
        

for i,root in enumerate(rootTags):
    sets += tweet_scraper(root.lower(), 8000)
    print(i)



count = {}
for sublist in sets:
        for value in sublist:
            if value in count:
                count[value] += 1
            else:
                count[value] = 1
print(count)
result = []
for sublist in sets:
    final_sublist = sublist
    for value in sublist:
        if count[value] == 1:
            if final_sublist:
                final_sublist = final_sublist.remove(value)
                
    print(final_sublist)
    if final_sublist and len(final_sublist) > 2:
        result.append(final_sublist)


json_object = json.dumps(result, indent=4)


with open("sets.json", "w") as outfile:
    outfile.write(json_object)
