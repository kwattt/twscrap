from twscrap import TwitterScrap

target = "evilafm"

TwScrap = TwitterScrap()
Profile = TwScrap.get_profile(target)

print(f"{target} profile info")
print("================")
print("Created at", Profile.created_at)
print("Followers", Profile.followers)
print("Image url", Profile.profile_image)

Tweets = TwScrap.get_tweets(Profile, include_rt=False, include_replies=False)

print(f"{target} last 5 tweets.")
for tweet in Tweets[:5]:
    print("==##########==")
    print("Content:", tweet.text)
    print("Likes:", tweet.likes)
    print("Replies:", tweet.reply_count)
    print("Retweets", tweet.retweet_count)
    if tweet.media:
        print("Media")
        print(tweet.media)
