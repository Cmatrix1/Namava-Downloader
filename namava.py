import requests


class NamavaClient:
    BASE_URL = "https://www.namava.ir/api"

    def __init__(self, cookies: dict, headers: dict = None):
        self.cookies = cookies
        self.session = requests.Session()
        self.session.cookies.update(cookies)
        self.session.headers.update(headers or {})

    def _send_request(self, *args, **kwargs):
        return self.session.request(*args, **kwargs)

    def get_play_info(self, media_id: int):
        return self._send_request(
            method="GET",
            url=f"{self.BASE_URL}/v1.0/medias/{media_id}/play?isKid=false",
        ).json()

    def get_m3u8_urls(self, master_url: str):
        response_text = self._send_request(method="GET", url=master_url).text
        m3u8_urls = tuple(url for url in response_text.split('\n') if url.startswith('https://'))
        return {
            url.split('/')[7]: url
            for url in m3u8_urls
        }

    def get_seasons_by_series_id(self, series_id: int) -> list:
        return self._send_request(
            method="GET",
            url=f"{self.BASE_URL}/v2.0/medias/{series_id}/single-series",
        ).json()['result']['seasons']

    def get_episodes_by_season_id(self, season_id: int) -> list:
        return self._send_request(
            method="GET",
            url=f"{self.BASE_URL}/v2.0/medias/seasons/{season_id}/episodes",
        ).json()['result']

