import requests
import re
from lxml import etree

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9"
}

proxy = {
    "https": "127.0.0.1:1087",
    "http": "127.0.0.1:1087"
}


def get_page_data(page_url):
    s = requests.session()
    page_resp = s.get(url=page_url, headers=headers, proxies=proxy)
    # print(page_resp.text)
    html = etree.HTML(page_resp.text)
    src_list = html.xpath("//div/img[@class='img-responsive']/@src")
    time_list = html.xpath("//div/span[@class='duration']/text()")
    file_names = html.xpath("//span[@class='video-title title-truncate m-t-5']/text()")

    min_list, number_list, dir_names = [], [], []

    index = 0
    for src, time, name in zip(src_list, time_list, file_names):
        min_str = time.split(":")[0]
        if int(min_str) > 2:
            index += 1
            min_list.append(time)
            # 文件下载序列号
            src_number = src.split("/")[-1].split(".")[0]
            number_list.append(src_number)
            # 文件名
            dir_name = re.sub("[\[\]，+=：:。！、/？“”（）()原创~.～\s]+", "", name)
            dir_names.append(dir_name)

            print(str(index) + " - " + dir_name + " - " + src_number + " - "  + time)

    print("-" * 50)
    return (number_list, dir_names)
