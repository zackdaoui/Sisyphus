LOGDEBUG, LOGINFO, LOGWARNING, LOGERROR = 0, 1, 2, 3
LOG = []
BUILTINS = []
CONDITIONS = {}


def log(msg, level=LOGINFO):
    LOG.append((level, msg))


def executebuiltin(function, wait=False):
    BUILTINS.append((function, wait))


def sleep(ms):
    pass


def getCondVisibility(expr):
    return CONDITIONS.get(expr, False)
