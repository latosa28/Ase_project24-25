import requests


class HttpClient:

    @staticmethod
    def get(url, **kwargs):
        return requests.get(url, verify=False, **kwargs)

    @staticmethod
    def post(url, **kwargs):
        return requests.post(url, verify=False, **kwargs)

    @staticmethod
    def put(url, **kwargs):
        return requests.put(url, verify=False, **kwargs)

    @staticmethod
    def delete(url, **kwargs):
        return requests.delete(url, verify=False, **kwargs)



