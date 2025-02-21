import requests


def get_proxied_session(proxy: str = None, headers_update: bool = True):
    session = requests.Session()
    if proxy:
        session.proxies = {
            'http': proxy,
            'https': proxy
        }
    if headers_update:
        session.headers.update({'Content-Type': 'application/octet-stream'})
    session.request = lambda *args, **kwargs: requests.Session.request(session, *args, **kwargs)
    return session
