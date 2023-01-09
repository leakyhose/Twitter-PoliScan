# Grabs most recent hashtags from handles in handles.csv
import snscrape.modules.twitter as sntwitter
import csv
import time

#556

tweets_list1 = []
times = []

def grabHashtag(username, n):
    tic = time.perf_counter()

    hashtags = []
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper('from:' + username).get_items()): #declare a username 
        if i>n: 
            break
        if tweet.hashtags:
            hashtags = hashtags + tweet.hashtags

    times.append(time.perf_counter() - tic)
    return hashtags
        


def calculateTime(counts):
    return (((sum(counts)/len(counts))*556) - sum(counts))/60/60

    
leftHashtags = {}
rightHashtags = {}
counter = 0


with open('handles.csv', 'r', errors="ignore") as input_file:
    reader = csv.reader(input_file)
    
    for row in reader:
        for i in grabHashtag(row[0], 3000):

            if row[1] == "D":

                if i in leftHashtags:
                    leftHashtags[i] += 1
                else:
                    leftHashtags[i] = 1

            elif row[1] == "R":
                if i in rightHashtags:
                    rightHashtags[i] += 1
                else:
                    rightHashtags[i] = 1
        counter += 1
        print("Count: " + str(counter) + "\nEstimated Time:" + str(calculateTime(times)))


leftHashtags = dict(sorted(leftHashtags.items(), key=lambda item: item[1], reverse=True))
rightHashtags = dict(sorted(rightHashtags.items(), key=lambda item: item[1], reverse=True))





with open('output.csv', 'w', newline='', errors="ignore") as output_file:
    writer = csv.writer(output_file)
    for key in leftHashtags.keys():
        writer.writerow((key , leftHashtags[key]  , "L"))
    for key in rightHashtags.keys():
        writer.writerow((key, rightHashtags[key], "R"))
    
