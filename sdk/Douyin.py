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
        self.vedioInfo={}#{vedioUrl:xx,music:xx,bgImage:xx}
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
            if vedioInfo['status_code']==0:
                for info in vedioInfo['item_list']:
                    self.vid=info['video']['vid']
                    print('获取视频vid成功--------'+self.vid)
                    self.vedioInfo['music']=info['music']['play_url']['uri']

                    #-----------获取视频封面
                    if info['video']['origin_cover']['url_list']!=None:
                        for cover in info['video']['origin_cover']['url_list']:
                            self.vedioInfo['bgImage']=cover
                            break
                    elif info['video']['origin_cover']['url_list']!=None:
                        for cover in info['video']['cover']['url_list']:
                            self.vedioInfo['bgImage']=cover
                            break
                    else:
                        self.vedioInfo["bgImage"]=""
                    break;
            else:
                print("服务器返回异常！")
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
    def getBgImage(self):
        self.vedioInfo['bgImage']='https://p26-sign.douyinpic.com/tos-cn-p-0015/90c6c6892e2f42f783c460cff2395331_1643435174~tplv-dy-360p.jpeg?x-expires=1647673200&x-signature=xbZWPIBc3HhMQ80niNgxpP52GWc%3D&from=4257465056&se=false&biz_tag=feed_cover&l=202203051538280101940320430F59BC45'
        try:
            if self.vedioInfo['bgImage']!= None and self.vedioInfo['bgImage']!= "":
                res=requests.get(self.vedioInfo['bgImage'])
                print(res.content)
                return res.content
            else:
                return None
        except Exception as err:
            print("获取背景图片内容异常："+err)