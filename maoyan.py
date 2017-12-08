import requests
import time
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool

def get_one_page(url,headers):
    try:
        response=requests.get(url,headers=headers)
        if response.status_code==200:
            return response.text
        return None
    except RequestException:
        print('None')

#解析网页
def parser_on_page(html):
    pattern=re.compile('<dd>.*?data-src="(.*?)".*?<a.*?data-act.*?>(.*?)</a>'+
                       '.*?"star">(.*?)</p>'+
                       '.*?releasetime">(.*?)</p>'+
                       '.*?"integer">(.*?)</i>.*?"fraction">(.*?)</i>',re.S)
    item=re.findall(pattern,html)

    # list2=[]
    for eves in item:
        yield {
            'image':eves[0],
            'title':eves[1],
            'actor':eves[2].strip()[3:],
            'time':eves[3].strip()[5:],
            'score':eves[4]+eves[5]
        }
        # list1 = []
        # for eve in eves:
        #     #去除换行符
        #     clear=re.sub('[\n ]','',eve)
        #     # clear=eve.strip()
        #     list1.append(clear)
        # list1[-2]=list1[-2]+list1[-1]
        # list1[:-1]


#生成url列表
def all_url():
    url_list=[]
    for i in range(1,11):
        if i==1:
            url = 'http://maoyan.com/board/4'
            url_list.append(url)
        else:
            url='http://maoyan.com/board/4'+'?offset='+str((i-1)*10)
            url_list.append(url)
    return url_list

def main(url):
    headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/62.0.3202.94 Chrome/62.0.3202.94 Safari/537.36'}
    conten=get_one_page(url,headers)
    for item in parser_on_page(conten):
        write_page_mess(item)

def write_page_mess(file):
    #file是字典形式 需要转换成字符串
    with open('maoyan.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(file,ensure_ascii=False)+'\n')
        f.close()

if __name__=='__main__':
    #多进程
    start_time=time.time()
    pool=Pool()
    pool.map(main,all_url())
    print(time.time()-start_time)

#普通方法
    # start_time = time.time()
    # for url in all_url():
    #     main(url)
    # print(time.time() - start_time)