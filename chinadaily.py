import requests
import re
import os
import time
from bs4 import BeautifulSoup


def craw_p(url_b):
    # 运行前先删除china文件夹，防止重复读
    html = []
    print("obtain HTML")
    # 通过useragent反爬
    agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/5.1.2.3000 Chrome/55.0.2883.75 Safari/537.36'

    for i in range(101, 452):
        print("start！！")
        time.sleep(0.5)
        url = url_b + "page_" + str(i) + ".html"
        print(url)
        header = {'user-agent': agent}
        r = requests.get(url, headers=header)
        r.raise_for_status()
        r.encoding = "utf-8"
        text = r.text
        # print(text)

        html_all = re.findall(r'www.chinadaily.com.cn/a/.*.html', text)
        html_all_unique = list(set(html_all))
        print(len(html_all_unique))
        for v in html_all_unique:
            # print(i).encode("utf-8")
            html.append(v)
    print("end")
    print("page number : " + str(len(html)))
    # r = 0
    cont = 0
    for h in html:
        time.sleep(0.5)
        cont += 1
        print("download text .......................", cont)
        # print(h)
        try:
            header = {'user-agent': agent}
            ri = requests.get("https://" + h, headers=header)
            ri.raise_for_status()
            ri.encoding = "utf-8"
            texti = ri.text
            # print(texti)
            try:
                soup = BeautifulSoup(texti, 'html.parser')

                # 提取标题
                title = soup.find('h1').get_text(strip=True)
                # print(title)

                # 提取时间
                time_match = re.search(r'Updated: (\d{4}-\d{2}-\d{2})', texti)

                if time_match:
                    time_text = time_match.group(1)
                    # print(time_text)
                else:
                    time_text = "Unknown"

                # 提取正文内容
                content_div = soup.find('div', id='Content')
                if content_div:
                    paragraphs = content_div.find_all('p')
                    content = '\n'.join([paragraph.get_text() for paragraph in paragraphs])
                    # print(content)
                else:
                    content = "No content found."

                # 指定保存目录
                save_directory = 'D:\\陈林\\中国日报\\data'

                # 创建并写入到txt文件
                filename = os.path.join(save_directory, f"{time_text}_{title}.txt")
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(f"Title: {title}\n")
                    file.write(f"Time: {time_text}\n\n")
                    file.write(content)

                print(f"提取并保存到文件：{filename}")


            except:
                print("error")

        except:
            print("do not find")
    print("over!!!")


htmlall = ["https://www.chinadaily.com.cn/china/governmentandpolicy/"]

craw_p(htmlall[0])
