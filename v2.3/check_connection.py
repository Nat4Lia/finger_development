import urllib2

def connection_on(address):
    try:
        urllib2.urlopen('http://%s' % address, timeout=1)
        return True
    except urllib2.URLError as err: 
        return False
    except urllib2.HTTPError as err:
        return False
    except Exception as err:
        return False
