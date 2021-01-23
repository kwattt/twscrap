# twscrap
A simple scraping package.  Currently it is possible to scrap the information of a profile and its tweets.
from twscrap import TwitterScrap

### Installation
    python -m pip install -U git+https://github.com/kwattt/twscrap
  
### Example
```python
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
```
### Profile attributes

|attribute|content|type|
|--|--|--|
|profile_url|profile url|string|
|id|profile id|int|
|followers|follower count|int|
|likes|likes count|int|
|following|following count|int|
|list_count|list count|int|
|username|user name|string|
|verified|is verified|bool|
|location|profile location|string|
|real_name|real name|string|
|description|profile description|string|
|description_urls|urls in description|list of strings|
|created_at|profile created date|datetime|
|default_profile_image|has default image|bool|
|profile_image|profile image url|string|
|profile_banner|profile banner url|string|
|private|is private|bool|

### Tweets attributes

|attribute|content|type|
|--|--|--|
|created_at|tweet created date|datetime|
|text|tweet full text|string|
|quote_count|quote count|int|
|lang|language|string|
|reply_count|reply count|int|
|favorite_count|like count|int|
|retweet_count|retweet count|int|
|user_id|owner id|int
|id|tweet id|int
|media|tweet media (photo, gif, image)|list of dict, keys('type', 'url', 'video_url')|
