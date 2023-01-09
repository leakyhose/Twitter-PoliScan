import snscrape.modules.twitter as sntwitter
import json
import csv
import math
from urllib.parse import urlparse



biased_hashtags_scores = {}
biased_news_scores = {}

with open('bias_scores.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        biased_news_scores[row[0]] = row[1]

with open('hashtags.json', 'r', encoding='utf-8') as outfile:
    reader = json.load(outfile)
    for row in reader:
        biased_hashtags_scores[row[0]] = row[1]

def get_political_score(handle, n):
    score = 0.0

    for i, tweet in enumerate(sntwitter.TwitterSearchScraper("(from:" + handle + ") AND filter:links AND include:nativeretweets AND -filter:media").get_items()):
        if i > n:
            break

        if tweet.links:
            for link in tweet.links:
                web_domain = urlparse(link.url).netloc.replace("www.", "").lower()

                if web_domain in biased_news_scores:
                    score += float(biased_news_scores[web_domain])
                    print(web_domain,biased_news_scores[web_domain] )

        if tweet.hashtags:
            for hashtag in tweet.hashtags:
                if hashtag.lower() in biased_hashtags_scores:
                    print("#" + hashtag.lower(),biased_hashtags_scores[hashtag.lower()])
                    score += float(biased_hashtags_scores[hashtag.lower()] * 2.5)

    if score >= 0:
        return 1 - math.exp(-0.05 * score)
    else:
        return -(1 - math.exp(0.05 * score))


print(get_political_score("CharlieCrist",1500))
