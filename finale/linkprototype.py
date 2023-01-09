import snscrape.modules.twitter as sntwitter
import csv
import math
import pandas as pd
from urllib.parse import urlparse


biased_news_scores = {}
handles = {}
biased_hashtags_scores = {}


with open('bias_scores.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        biased_news_scores[row[0]] = row[1]


with open('handles.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        handles[row[0]] = row[1]


with open('hashtags.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        biased_hashtags_scores[row[0]] = row[1]


def get_political_score(handle, n):
    score = 0.0

    for i, tweet in enumerate(sntwitter.TwitterSearchScraper('(from:'+ handle + ') AND (filter:links OR filter:hashtags) AND include:nativeretweets').get_items()):
        if i > n:
            break

        if tweet.links:
            for link in tweet.links:
                web_domain = urlparse(link.url).netloc.replace('www.', '').lower()

                if web_domain in biased_news_scores:
                    score += float(biased_news_scores[web_domain])

        if tweet.hashtags:
            for hashtag in tweet.hashtags:
                if hashtag.lower() in biased_hashtags_scores:
                    score += float(biased_hashtags_scores[hashtag.lower()]) * 1.5

    if score >= 0:
        return 1 - math.exp(-0.01 * score)
    else:
        return -(1 - math.exp(0.01 * score))


if __name__ == '__main__':
    table = {'Handle': [],
             'Party/Stance': [],
             'Outputted Score': [],
             'Correct': []}

    errors = 0

    for handle in handles.keys():
        score = get_political_score(handle, 1500)
        table['Handle'].append(handle)
        table['Party/Stance'].append(handles[handle])
        table['Outputted Score'].append(score)

        result = ''

        if score > 0:
            result = 'R'
        elif score < 0:
            result = 'D'

        if result != handles[handle]:
            errors += 1
            table['Correct'].append(False)
        else:
            table['Correct'].append(True)

    print(100 - ((errors / len(handles.keys())) * 100))

    df = pd.DataFrame(table, columns=['Handle', 'Party/Stance', 'Outputted Score', 'Correct'])
    df.to_excel('data_table.xlsx')
