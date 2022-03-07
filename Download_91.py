import requests
import threading
import os
import convert
import PageDataFetcher


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9"
}


class MyThread_Download_91(threading.Thread):

    def __init__(self, src, client_src, dir_name):
        super(MyThread_Download_91, self).__init__()
        self.src = src
        self.dir_name = dir_name
        self.client_src = client_src

    def mkdir(self, path):
        path = path.strip()
        path = path.rstrip("\\")
        if not os.path.exists(path):
            os.makedirs(path) 
            return True
        else:
            return False

    def run(self):
        base_dir = "https://la.killcovid2021.com/m3u8/"
        # base_dir = "https://ccn.killcovid2021.com//m3u8/"
        fragment = 0
        while True:
            url = base_dir+self.src+"/"+self.src+str(fragment)+".ts"

            print(threading.current_thread().name + f" — {self.dir_name} — " + url)
            r = requests.get(url, headers=headers)
            if r.ok:
                ts_src = self.client_src + self.dir_name
                self.mkdir(ts_src)
                file_name = ts_src + "//" + str(fragment).rjust(10, "0") + ".ts"
                with open(file_name, "wb") as f:
                    f.write(r.content)

                # file_name = ts_src + "/" + dir_name + ".mp4"
                # print(threading.current_thread().name + " " + file_name)
                # with open(file_name, "ab+") as f:
                #     f.write(r.content)
                fragment = fragment + 1
            else:
                break

        print("-" * 50)
        # print(number, self.dir_name)
        convert.create_file(os.path.join(self.client_src, self.dir_name), self.dir_name)


if __name__ == "__main__":
    # client_src:下载后保存在本地什么位置。
    client_src = "/Users/jackie/Desktop/ThirdParty/Download_91Porn/video/"

    # requests.adapters.DEFAULT_RETRIES = 1
    s = requests.session()
    s.keep_alive = False

    page_url = "http://91porn.com/v.php?category=top&viewtype=basic&page=2"
    # numbers, dir_names = [601164, 601053], ["大鸟十八玲酱回归撸先生日本街边豪车搭讪千金mp4", "《探总奉上》贵在真实"]
    numbers, dir_names = PageDataFetcher.get_page_data(page_url)

    for number, dir_name in zip(numbers, dir_names):
        t = MyThread_Download_91(str(number), client_src, dir_name)
        t.start()

    # print("-" * 50)
    # dir_name = "日常推送分享"
    # convert.create_file(os.path.join(client_src, dir_name), dir_name)