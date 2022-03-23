class BaseAPI:
    def __init__(self, rum=None):
        self._rum = rum

    def _get(self, url):
        return self._rum.get(url)

    def _post(self, url, **kwargs):
        return self._rum.post(url, **kwargs)