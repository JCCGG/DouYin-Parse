import json

import requests
import re

# dy客户端--test
class Douyin():
    def __init__(self):
        self.userUrl=''
        self.vedioApiUrl='https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids='
        self.vedioUrl='https://aweme.snssdk.com/aweme/v1/play/?video_id='
        self.longUrl=''
        self.vedioId=''
        self.vid=''
        # self.musicUrl=''#解析的背景音乐地址
        # self.vedioRealUrl=''#解析的真实视频地址
        self.vedioInfo={}
        self.headers={
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
        }
    # 获取长连接vid
    def __getLongUrl(self):
        try:
            res=requests.get(self.userUrl,headers=self.headers,allow_redirects=False)
            locationStr=res.headers.get('location')
            if res.headers.get('location'):
                print(locationStr)
                self.longUrl=locationStr
                pattern='(?<=/video/).*?(?=\/)'
                vedioId=re.compile(pattern).search(locationStr).group()
                print('获取vedioId成功---'+vedioId)
                self.vedioId=vedioId
            else:
                print('没找到location:'+str(res.headers))
        except Exception as err:
            print('获取视频Id出错：'+str(err))
    #         请求视频信息
    def __getVideoInfo(self):
        self.__getLongUrl()
        try:
            res=requests.get(self.vedioApiUrl+self.vedioId,headers=self.headers)
            vedioInfo=json.loads(res.text)
            # print(vedioInfo)
            for info in vedioInfo['item_list']:
                self.vid=info['video']['vid']
                print('获取视频vid成功--------'+self.vid)
                self.vedioInfo['music']=info['music']['play_url']['uri']
                break;
        except Exception as err:
            print('获取视频信息错误：'+str(err))

    # 获取视频真实地址
    def getVideoUrl(self,url):
        if url=='' or url==None:
            print('输入的连接为空！')
            return
        self.userUrl=url
        self.__getVideoInfo()
        try:
            res=requests.get(self.vedioUrl+self.vid+'&ratio=720p&line=0',headers=self.headers,allow_redirects=False)
            realUrl=res.headers.get('location')
            print('获取视频真实地址成功！')
            print(realUrl)
            self.vedioInfo['vedioUrl']=realUrl
            return self.vedioInfo
        except Exception as err:
            print('获取视频真实地址错误：'+str(err))

