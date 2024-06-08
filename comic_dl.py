import requests
from bs4 import BeautifulSoup
import re
import os
import concurrent.futures

# 設置目標網址
url = 'https://comic.acgn.cc/view-191065.htm'

# 設置圖片存儲文件夾
folder_name = 'comic_images'
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# 發送GET請求
response = requests.get(url)
response.encoding = 'utf-8'

# 解析網頁
soup = BeautifulSoup(response.text, 'html5lib')

# 查找所有圖片 URL 的正則表達式
img_regex = re.compile(r'https://img\.acgn\.cc/img/\d+/\d+/\d+\.jpg')

# 獲取所有符合條件的圖片 URL
img_urls = img_regex.findall(response.text)

# 列出圖片總數並詢問是否下載
print(f'Total images found: {len(img_urls)}')
user_input = input('Do you want to download all images? (Y/N): ')

if user_input.strip().lower() != 'y':
    print('Download aborted.')
else:
    def download_image(img_url, idx):
        img_data = requests.get(img_url).content
        with open(os.path.join(folder_name, f'image_{idx+1}.jpg'), 'wb') as img_file:
            img_file.write(img_data)
        print(f'Downloaded image_{idx+1}.jpg')

    # 使用多線程下載圖片
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(download_image, img_url, idx)
                   for idx, img_url in enumerate(img_urls)]
        concurrent.futures.wait(futures)

    print('All images downloaded successfully.')
