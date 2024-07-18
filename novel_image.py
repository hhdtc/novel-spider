import subprocess
import requests

class downloader:
    def __init__(self, url, path):
        self.url = url
        self.path = path
    
    def download(self):
        headers = {
            'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'i',
            'referer': 'https://www.linovelib.com/',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'image',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        }
        response = requests.get(self.url, headers=headers)
        with open(self.path, 'wb') as file:
            file.write(response.content)

    

if __name__ == '__main__':
    downloader('https://img3.readpai.com/2/2680/126599/116025.jpg','./test.jpg').download()
    