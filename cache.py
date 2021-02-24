cacheMap = {}


def readBy(filename, func):
    if filename not in cacheMap:
        cacheMap[filename] = func(filename)
    return cacheMap[filename]
