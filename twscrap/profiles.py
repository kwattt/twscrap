from .tweets import Tweet

import requests
import email.utils

class Profile(): 
    def __init__(self):
        self.profile_url = ""
        self.id = 0
        self.followers = 0
        self.likes = 0
        self.following = 0
        self.list_count = 0
        self.username = ""
        self.verified = False
        self.location = ""
        self.real_name = ""
        self.description = ""
        self.description_urls = []
        self.created_at = None
        self.default_profile_image = False
        self.profile_image = ""    
        self.tweets = []

    def parse_profile(self, data):
        self.id = data["data"]["user"]["rest_id"] 
        self.followers = data["data"]["user"]["legacy"]["followers_count"]
        self.likes = data["data"]["user"]["legacy"]["favourites_count"]
        self.following = data["data"]["user"]["legacy"]["friends_count"]
        self.list_count = data["data"]["user"]["legacy"]["listed_count"]
        self.username = data["data"]["user"]["legacy"]["screen_name"]
        self.verified = data["data"]["user"]["legacy"]["verified"]
        self.location = data["data"]["user"]["legacy"]["location"]
        self.real_name = data["data"]["user"]["legacy"]["name"]

        if "description" in data["data"]["user"]["legacy"]:
            self.description = data["data"]["user"]["legacy"]["description"]

        if "url" in data["data"]["user"]["legacy"]["entities"]:
            self.description_urls =  [x["expanded_url"] for x in data["data"]["user"]["legacy"]["entities"]["url"]["urls"]]

        self.created_at = email.utils.parsedate_to_datetime(data["data"]["user"]["legacy"]["created_at"])
        self.default_profile_image = data["data"]["user"]["legacy"]["default_profile_image"] 
    
        if not self.default_profile_image:
            self.profile_image = data["data"]["user"]["legacy"]["profile_image_url_https"] 
            # Try to get 400x400 image
            tmp_image = self.profile_image.replace("normal.jpg", "400x400.jpg")
            r = requests.get(tmp_image)
            if r.status_code == 200:
                self.profile_image = tmp_image