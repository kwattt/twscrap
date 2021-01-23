import email.utils

class Tweet: 
    def __init__(self, created_at, id, text, lang, quote, reply, favorite, retweets, user_id, media):
        self.created_at = created_at
        self.id = id
        self.text = text
        self.quote_count = quote
        self.lang = lang
        self.reply_count = reply
        self.likes = favorite
        self.retweet_count = retweets
        self.user_id = user_id
        self.media = media

def parse_tweets(data, include_rt, user_id):
    tweets = []

    tweet_data = data["globalObjects"]["tweets"]

    for tweet in list(reversed(sorted(tweet_data.keys()))):
        tw = tweet_data[tweet]

        if not include_rt:
            if int(tw["user_id_str"]) != int(user_id):
                continue

        media_t = []
        if "extended_entities" in tw: 
            for obj in tw["extended_entities"]["media"]:
                
                media_t.append({
                    "type": obj["type"],
                    "url": obj["media_url_https"],
                    "video_url": obj["video_info"]["variants"][0]["url"] if "video_info" in obj else ""
                })

        tweets.append(Tweet(
            created_at = email.utils.parsedate_to_datetime(tw["created_at"]),
            id = int(tw["id_str"]),
            text = tw["full_text"],
            lang = tw["lang"],
            quote = tw["quote_count"],
            reply = tw["reply_count"],
            favorite = tw["favorite_count"],
            retweets= tw["retweet_count"],
            user_id = user_id,
            media = media_t 
        ))

    return tweets

def get_params(user_id, include_replies = False, count = 20):
    return {
        "include_profile_interstitial_type": "1",
        "include_blocking": "1",
        "include_blocked_by": "1",
        "include_followed_by": "1",
        "include_want_retweets": "1",
        "include_mute_edge": "1",
        "include_can_dm": "1",
        "include_can_media_tag": "1",
        "skip_status": "1",
        "cards_platform": "Web-12",
        "include_cards": "1",
        "include_ext_alt_text": "true",
        "include_quote_count": "true",
        "include_reply_count": "1",
        "tweet_mode": "extended",
        "include_entities": "true",
        "include_user_entities": "false",
        "include_ext_media_color": "true",
        "include_ext_media_availability": "true",
        "send_error_codes": "true",
        "simple_quoted_tweets": "true",
        "include_tweet_replies": "true" if include_replies else "false",
        "userId": user_id,
        "count": str(count)
    }
