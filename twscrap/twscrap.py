from requests_html import requests
from requests_html import HTMLSession, requests
import re, time, json, urllib.parse

from .profiles import Profile
from .tweets import get_params, parse_tweets

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0"

class TwitterScrap:

    def __init__(self):
        self.session = HTMLSession()
        self.x_guest_token = None
        self.headers = {
            "User-Agent": USER_AGENT
        }

    def get_profile(self, username):
        profile = Profile()
        profile.profile_url = f"https://twitter.com/{username}/"
        
        self.__get_token(profile.profile_url)

        self.headers["x-guest-token"] = self.x_guest_token
        self.headers["Authorization"] = "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs=1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"

        self.headers["Referer"] = profile.profile_url

        params = {'variables': json.dumps({'screen_name': username, 'withHighlightedLabel': True}, separators = (',', ':'))}

        prepared_request = self.session.prepare_request(requests.Request("GET", "https://api.twitter.com/graphql/-xfUfZsnR_zqjFd-IfrN5A/UserByScreenName", headers = self.headers, params=urllib.parse.urlencode(params, quote_via=urllib.parse.quote)))    
        res = self.session.send(prepared_request, allow_redirects = True, timeout = 15)
        profile.parse_profile(res.json())
        return profile

    def get_tweets(self, profile : Profile, include_replies = False, include_rt = False, count = 40):
        prepared_request = self.session.prepare_request(requests.Request("GET", f"https://twitter.com/i/api/2/timeline/profile/{profile.id}.json", headers = self.headers, params=urllib.parse.urlencode(get_params(profile.id, include_replies, count), quote_via=urllib.parse.quote)))    
        res = self.session.send(prepared_request, allow_redirects = True, timeout = 10) 
        if res.status_code != 200:
            raise Exception(f"Could not get tweets, status_code {res.status_code}")

        data = res.json()
        tweets = parse_tweets(data, include_rt, profile.id)
        return tweets

    def __get_token(self, url):
        if self.x_guest_token == None:
            request = self.session.prepare_request(requests.Request("GET", url, headers=self.headers))
            res = self.session.send(request, allow_redirects = True, timeout = 20)
            possible_token = re.search(r'decodeURIComponent\("gt=(\d+); Max-Age=10800;', res.text)
            if possible_token:
                self.x_guest_token = possible_token.group(1)
                self.session.cookies.set("gt", self.x_guest_token, domain = '.twitter.com', path = '/', secure = True, expires = time.time() + 10800)
            else:
                raise Exception(f"Could not retrieve guest token, status_code {res.status_code}") 
        else:
            return