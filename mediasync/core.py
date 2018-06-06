import copy
from .modules import deezer
from .exceptions import MediasyncError


class Core(object):
    def __init__(self, provider):
        if provider.lower() == 'deezer':
            self.provider = deezer.Core()
        else:
            raise MediasyncError('unknown provider')

    def sync(self, username1, passwd1, username2, passwd2):
        # acc1 = copy.copy(self.provider)
        # acc1.login(username1, passwd1)
        # favorites = acc1.getFavorites()
        # acc2 = copy.copy(self.provider)
        # acc2.login(username2, passwd2)
        self.provider.login(username1, passwd1)
        favorites = self.provider.getFavorites()
        self.provider.logout()
        self.provider.login(username2, passwd2)
        for s in favorites:
            # TODO: show progress (bar?)
            print(s['SNG_ID'])
            self.provider.addFavorite(s)
