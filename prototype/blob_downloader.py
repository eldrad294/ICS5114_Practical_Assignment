# python3
import urllib.request as request

def record_video():
    url = 'blob:https://www.youtube.com/8f7b279c-1461-4bbe-8288-8b7db0d94f4f'
    # fake user agent of Safari
    fake_useragent = 'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25'
    r = request.Request(url, headers={'User-Agent': fake_useragent})
    f = request.urlopen(r)

    # print or write
    print(f.read())