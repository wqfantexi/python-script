import requests
import os
import logging
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED, FIRST_COMPLETED

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] [thread %(thread)d] : %(message)s',datefmt='%Y-%m-%d %H:%M:%S')

def download(root, url):
    logging.debug(url)
    r = requests.get(url, stream=True)
    filename=r.headers['content-disposition'].split('; filename=')[1]
    filename = bytes(filename, 'ISO-8859-1').decode('GBK')

    filepath = os.path.join(root, filename)
    if os.path.exists(filepath):
        logging.debug('文件%s已经存在，不需要下载'%(filepath,))
        return
    
    logging.debug('准备下载文件:%s'% (filepath,))
    with open(filepath, 'wb') as fp:
        for chunk in r.iter_content(4000):
            fp.write(chunk)
    logging.debug('文件下载完成:%s'% (filepath,))


def downloadRange(start, end):
    executor = ThreadPoolExecutor(max_workers=20)
    urls=['http://www.yz5.org/modules/article/txtarticle.php?id=%d'%(x,) for x in range(start, end)]
    all_task = [executor.submit(download, r'F:\\小说', url) for url in urls]
    wait(all_task, return_when=ALL_COMPLETED)


downloadRange(3000,6000)


