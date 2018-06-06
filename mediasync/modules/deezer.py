import requests
import json
# import re
import random


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    # 'Accept-Charset': 'utf-8, iso-8859-1, utf-16, *;q=0.1',
    # 'Connection': 'keep-alive',
    # 'Keep-Alive': '300',
    'DNT': '1',
}


class Deezer(object):
    def __init__(self, username, passwd):
        self.r = requests.Session()
        self.r.headers = headers
        self.login(username, passwd)

    def login(self, username, passwd):  # looks like there is official api, so this should be patched not to fake browser
        self.r.headers['X-Requested-With'] = 'XMLHttpRequest'
        data = {'type': 'login',
                'mail': 'oczkers@gmail.com',
                'password': 'QtsjxQceetWNh7pzNifP'}
        rc = self.r.post('https://www.deezer.com//ajax/action.php', data=data).text
        open('deezer.log', 'w').write(rc)
        del self.r.headers['X-Requested-With']

        # user data (api key, user_id)
        data = {'method': 'deezer.getUserData',
                'input': 3,
                'api_version': '1.0',
                'api_token': '',
                'cid': random.randint(100000000, 999999999)}
        rc = self.r.post('https://www.deezer.com/ajax/gw-light.php', data=data).json()
        open('deezer.log', 'w').write(json.dumps(rc))
        self.user_id = rc['results']['USER']['USER_ID']
        self.api_key = rc['results']['checkForm']

    def getFavorites(self):
        data = {'user_id': self.user_id,
                'tab': 'loved',
                'nb': 2000}  # what is this?
        params = {'input': 3,
                  'method': 'deezer.pageProfile',
                  'api_version': '1.0',
                  'api_token': self.api_key,
                  'cid': random.randint(100000000, 999999999)}
        rc = self.r.post('https://www.deezer.com/ajax/gw-light.php', data=json.dumps(data), params=params).json()
        open('deezer.log', 'w').write(json.dumps(rc))
        songs = rc['results']['TAB']['loved']['data']
        return songs

    def addFavorite(self, song):
        data = {'SNG_ID': song['SNG_ID']}
        params = {'input': 3,
                  'method': 'favorite_song.add',
                  'api_version': '1.0',
                  'api_token': self.api_key,
                  'cid': random.randint(100000000, 999999999)}
        rc = self.r.post('https://www.deezer.com/ajax/gw-light.php', data=json.dumps(data), params=params).json()
        open('deezer.log', 'w').write(json.dumps(rc))
        return rc['results']
