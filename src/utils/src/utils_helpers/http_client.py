import requests


class HttpClient:

    @staticmethod
    def get(url,  *args, **kwargs):
        return requests.get(url,  *args, verify=False, timeout=1, **kwargs)

    @staticmethod
    def post(url,  *args, **kwargs):
        return requests.post(url,  *args, verify=False, timeout=1, **kwargs)

    @staticmethod
    def put(url,  *args, **kwargs):
        return requests.put(url,  *args, verify=False, timeout=1, **kwargs)

    @staticmethod
    def delete(url,  *args, **kwargs):
        return requests.delete(url,  *args, verify=False, timeout=1, **kwargs)



