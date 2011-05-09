import logging
from django.conf import settings
from vendor.colorama import Fore, Back, Style
import re

class NullHandler(logging.Handler): #exists in python 3.1
    def emit(self, record):
        pass

def getlogger():
    logger = logging.getLogger('newsblur')
    return logger

def user(u, msg):
    premium = '*' if u.is_authenticated() and u.profile.is_premium else ''
    info(' ---> [%s%s] %s' % (u, premium, msg))
    
def debug(msg):
    logger = getlogger()
    logger.debug(colorize(msg))

def info(msg):
    logger = getlogger()
    logger.info(colorize(msg))

def error(msg):
    logger = getlogger()
    logger.error(msg)
    
def colorize(msg):
    params = {
        r'\-\-\->'        : '~FB~SB--->~FW',
        r'\*\*\*>'        : '~FB~SB~BB--->~BT~FW',
        r'\['             : '~SB~FB[~SN~FM',
        r'AnonymousUser'  : '~FBAnonymousUser',
        r'\*\]'           : '~SN~FR*]',
        r'\]'             : '~FB~SB]~FW~SN',
    }
    colors = {
        '~SB' : Style.BRIGHT,
        '~SN' : Style.NORMAL,
        '~SK' : Style.BLINK,
        '~SU' : Style.UNDERLINE,
        '~ST' : Style.RESET_ALL,
        '~FK': Fore.BLACK,
        '~FR': Fore.RED,
        '~FG': Fore.GREEN,
        '~FY': Fore.YELLOW,
        '~FB': Fore.BLUE,
        '~FM': Fore.MAGENTA,
        '~FC': Fore.CYAN,
        '~FW': Fore.WHITE,
        '~FT': Fore.RESET,
        '~BK': Back.BLACK,
        '~BR': Back.RED,
        '~BG': Back.GREEN,
        '~BY': Back.YELLOW,
        '~BB': Back.BLUE,
        '~BM': Back.MAGENTA,
        '~BC': Back.CYAN,
        '~BW': Back.WHITE,
        '~BT': Back.RESET,
    }
    for k, v in params.items():
        msg = re.sub(k, v, msg)
    msg = msg + '~ST~FW~BT'
    msg = re.sub(r'(~[A-Z]{2})', r'%(\1)s', msg)
    try:
        msg = msg % colors
    except (TypeError, ValueError, KeyError):
        pass
    return msg