import re
import urllib.request

#下载网页
def download(url, user_agent='wswp' ,proxy=None,num_retry = 2):
    print('Downloading : ',url)
    headers = {'User-agent': user_agent}
    request = urllib.request.Request(url, headers = headers)

    opener = urllib.request.build_opener()
    if proxy:
        proxy_params = {urllib.request.urlparse(url).scheme:proxy}
        opener.add_handler(urllib.request.ProxyHandler(proxy_params))

    try:
        html = urllib.request.urlopen(url).read()
    except urllib.request.URLError as e:
        print("Download error:", e.reason)
        html = None
        if num_retry > 0:
            if hasattr(e, 'code') and 500 <=e.code < 600:
                return download(url, user_agent,proxy,num_retry - 1)
    return html

def crawl_sitemap(url):
    sitemap = download(url)
    links = re.findall('<loc>(.*?)</loc>',sitemap)
    for link in links:
        html = download(link)
        print(html)

def get_links(html):
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return webpage_regex.findall(html.decode("utf-8"))


def link_crawler(seed_url, link_regex):
    crawl_queue = [seed_url]
    seen = set(crawl_queue)
    while crawl_queue:
        url = crawl_queue.pop()
        html= download(url)
        for link in get_links(html):
            if re.match(link_regex, link):
                link = urllib.request.urljoin(seed_url, link)
                if link not in seen:
                    crawl_queue.append(link)

if __name__ == '__main__':
   # print(download("https://kindleren.com/forum.php"))
   link_crawler('http://example.webscraping.com', '/(index|view)')