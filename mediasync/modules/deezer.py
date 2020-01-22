import requests
import json
import re
# import random


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


class Core(object):
    def __init__(self):
        self.r = requests.Session()
        self.r.headers = headers

    def login(self, access_token=None):  # looks like there is official api, so this should be patched not to fake browser
        if not access_token:
            params = {'app_id': 341662,
                      'redirect_uri': 'http://127.0.0.1/auth',
                      'perms': 'basic_access, email, offline_access, manage_library, manage_community, delete_library, listening_history'}
            rc = self.r.get('https://connect.deezer.com/oauth/auth.php', params=params)
            print(rc.url)
            key = input('open this shit, login and paste key: ')
            params = {'app_id': 341662,
                      'secret': 'c9d343d6bb0725b667e7c73e83d28322',
                      'code': key}
            rc = self.r.get('https://connect.deezer.com/oauth/access_token.php', params=params).text
            self.access_token = re.match('access_token=(.+?)&expires=[0-9]+', rc).group(1)
            print(self.access_token)
        else:
            self.access_token = access_token

    def getFavorites(self):
        params = {'access_token': self.access_token}
        rc = self.r.get('https://api.deezer.com/user/me/tracks', params=params).json()
        open('mediasync.log', 'w').write(json.dumps(rc))
        favs = [i['id'] for i in rc['data']]
        while len(favs) < rc['total']:
            print('%s/%s' % (len(favs), rc['total']))
            rc = self.r.get(rc['next']).json()
            favs.extend([i['id'] for i in rc['data']])
        return favs

    def getPlaylist(self, playlist_id):
        params = {'access_token': self.access_token}  # is it needed here?
        rc = self.r.get('https://api.deezer.com/playlist/%s/tracks' % playlist_id, params=params).json()
        open('mediasync.log', 'w').write(json.dumps(rc))
        tracks = [i['id'] for i in rc['data']]
        while len(tracks) < rc['total']:
            print('%s/%s' % (len(tracks), rc['total']))
            rc = self.r.get(rc['next']).json()
            tracks.extend([i['id'] for i in rc['data']])
        return tracks

    def addTrack(self, playlist_id, track_id):  # TODO: playlist should be an object
        params = {'access_token': self.access_token,
                  'songs': [track_id]}
        rc = self.r.post('https://api.deezer.com/playlist/%s/tracks' % playlist_id, params=params).json()
        open('mediasync.log', 'w').write(json.dumps(rc))
        return rc

    def addFavorite(self, song_id):
        params = {'access_token': self.access_token,
                  'track_id': song_id}
        rc = self.r.post('https://api.deezer.com/user/me/tracks', params=params).text
        print(rc)

    def deleteFavorite(self, song_id):
        params = {'access_token': self.access_token,
                  'track_id': song_id}
        rc = self.r.delete('https://api.deezer.com/user/me/tracks', params=params).text
        print(rc)

    def logout(self):
        self.access_token = None
