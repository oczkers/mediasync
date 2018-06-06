# -*- coding: utf-8 -*-

"""
mediasync
=========

Usage:
    mediasync PROVIDER USERNAME1 PASSWD1 USERNAME2 PASSWD2
"""

# import sys
from docopt import docopt

from . import __title__, __version__
from .core import Core


version_text = '%s v%s' % (__title__, __version__)


def __main__():
    # TODO: destination
    args = docopt(__doc__, version=version_text)
    print(args)
    ms = Core(args['PROVIDER'])
    ms.sync(args['USERNAME1'], args['PASSWD1'], args['USERNAME2'], args['PASSWD2'])


if __name__ == '__main__':
    __main__()

# TODO: drop docopt, use click
# https://github.com/pallets/click
