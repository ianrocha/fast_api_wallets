from urllib.request import Request, urlopen


class UrlRepository:
    @staticmethod
    def make_request(url: str, method: str) -> urlopen:
        request = Request(url=url,
                          method=method)
        return urlopen(request)
