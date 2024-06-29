import os
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from rich.progress import track


class Downloader:
    def __init__(self, m3u8_url: str, uniqe_identifier: str):
        self.uniqe_identifier = uniqe_identifier
        self.folder_name = f'{uniqe_identifier}_segments'
        os.makedirs(self.folder_name, exist_ok=True)
        
        self.session = requests.Session()
        m3u8_lines = self.session.get(m3u8_url).text.split('\n')
        encryption_key_url = m3u8_lines[4].split('"')[1]
        self.encryption_key_content = self.session.get(encryption_key_url).content
        self.segment_urls = tuple(url for url in m3u8_lines if url.startswith('https://'))

    def download_segment(self, segment_url: str):
        ts_response = requests.get(segment_url)
        encrypted_ts = ts_response.content
        cipher = AES.new(self.encryption_key_content, AES.MODE_CBC, encrypted_ts[:16])
        decrypted_ts = unpad(cipher.decrypt(encrypted_ts[16:]), AES.block_size)
        return decrypted_ts

    def save_segment(self, index: int, segment_content: bytes):
        ts_filename = f'{self.folder_name}/segment_{index}.ts'
        with open(ts_filename, 'wb') as ts_file:
            ts_file.write(segment_content)
        return ts_filename

    def merge_segments_to_video(self):
        segments_list = [f for f in os.listdir(self.folder_name) if f.endswith('.ts')]
        segments_list.sort(key=lambda x: int(x.replace("segment_", '').replace(".ts", '')))
        with open(f'{self.folder_name}/list.txt', 'w') as list_file:
            segments_list_name = tuple(map(lambda x: f"file '{x}'" , segments_list))
            list_file.write('\n'.join(segments_list_name))

        os.chdir(self.folder_name)
        os.system(f'ffmpeg -f concat -safe 0 -i list.txt -c copy {self.uniqe_identifier}.mp4')

        for i in segments_list:
            os.remove(i)

    def main(self):
        for index, segment_url in enumerate(track(self.segment_urls, 'DOWNLOADING ...')):
            segment_content = self.download_segment(segment_url)
            self.save_segment(index, segment_content)
    
        self.merge_segments_to_video()

