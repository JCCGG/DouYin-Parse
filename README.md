# 抖音视频解析、抖音无水印高清视频解析、抖音背景音乐解析

## 构建

1. python 3.10.2
2. 安装requirements.txt文件的依赖库

~~~python
pip install -r requirements.txt
~~~

3. 进入项目主目录输入命令启动

~~~python
python main.py
~~~

4. 打包

安装好pyinstaller，进入项目主目录

~~~python
pyinstaller main.py -F -w -n 打包名
~~~

## 启动

启动后将抖音视频分享到连接复制到输入框，点击解析按钮后，不出意外的话就可以看得到解析好的视频地址和背景音乐地址，并且程序会自动打开本机电脑默认浏览器

![image-20220221215337057](https://github.com/JCCGG/DouYin-Parse/blob/master/screenshot/image-20220221215337057.png)

后续增加了正则匹配url，所以通过抖音分享过来的链接可以直接复制进输入框，无需将url链接单独复制出来

![Snipaste_2022-02-25_11-38-17.png](https://github.com/JCCGG/DouYin-Parse/blob/master/screenshot/Snipaste_2022-02-25_11-38-17.png)

## 免责声明

本程序及代码仅供学习参考使用，不得用于非法用途，如项目侵犯了您的利益，请联系删除！
