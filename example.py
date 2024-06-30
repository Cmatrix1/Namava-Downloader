from downloader import Downloader
from namava import NamavaClient

cookies = {
    'guest_token': 'YOUR_guest_token',
    'auth_v2': 'YOUR_auth_v2',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Priority': 'u=1',
}

media_id = 232802

client = NamavaClient(cookies=cookies, headers=headers)
play_info = client.get_play_info(media_id=media_id)
m3u8_urls = client.get_m3u8_urls(master_url=play_info['absolutePath']).values()
downloader = Downloader(m3u8_url=tuple(m3u8_urls)[3], uniqe_identifier=media_id)
downloader.main()