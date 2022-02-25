import tkinter as tk
from sdk import Douyin as dy
import webbrowser
import re

# 主界面
# author JCC
class mainWindow():
    def __init__(self):
        self.tkinter=tk.Tk()
        self.w=500
        self.h=200
        self.dyClient=dy.Douyin()
        self.vUrl =""
    #     启动
    def launch(self):
        self.tkinter.title('抖音无水印视频音乐解析_JCC')
        x=(self.tkinter.winfo_screenwidth()-self.w)/2
        y=(self.tkinter.winfo_screenheight()-self.h)/2
        self.tkinter.geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))
        self.initWeget()
        self.tkinter.mainloop()
    #初始界面
    def initWeget(self):
        contorlFrame = tk.Frame(self.tkinter)
        dataFrame=tk.Frame(self.tkinter)

        self.inputText=tk.StringVar()
        self.statusText=tk.StringVar()
        self.statusText.set("状态：")

        label=tk.Label(contorlFrame,text='连接：')
        inputUrl = tk.Entry(contorlFrame, textvariable=self.inputText,show=None,width=50,selectforeground="#ffffff",selectbackground="#000000")
        submitButton = tk.Button(contorlFrame, text='解析', command=self.submitCallbak)
        self.resText=tk.Text(dataFrame,height=10,selectforeground="#ffffff",selectbackground="#000000")
        statusLabel=tk.Label(dataFrame,textvariable=self.statusText,fg="#ff0000")
        # 弹出菜单
        self.menu = tk.Menu(contorlFrame,
                    tearoff=False,
                    )
        self.menu.add_command(label="剪切", command=lambda:self.cut(inputUrl))
        self.menu.add_command(label="复制", command=lambda:self.copy(inputUrl))
        self.menu.add_command(label="粘贴", command=lambda:self.paste(inputUrl))
        inputUrl.bind("<Button-3>",self.popup)
        # inputUrl.bind("<Key>",self.checkInputChange)

        contorlFrame.pack()
        dataFrame.pack()
        label.grid(row=1,column=1)
        inputUrl.grid(row=1,column=2,padx=15,ipady=5)
        submitButton.grid(row=1,column=3,ipady=3,ipadx=5)
        self.resText.pack()
        statusLabel.pack(side='left')

    def cut(self,editor,event=None):
        editor.event_generate('<<Cut>>')
    def copy(self,editor,event=None):
        editor.event_generate('<<Copy>>')
    def paste(self,editor,event=None):
        editor.event_generate('<<Paste>>')
    def popup(self,event):
        self.menu.post(event.x_root, event.y_root)  # post在指定的位置显示弹出菜单
    def checkInputChange(self):
        inputText=self.inputText.get()
        url=self.expToUrl(inputText)
        print(url)
        if url==None or url=="":
            print("请输入正确链接！")
            self.statusText.set("请输入正确链接！")
        else:
            self.statusText.set("已获得输入的链接！")
            self.vUrl=url
    def expToUrl(self,text):
        if text!="" or text !=None:
            pattern="(ht|f)tp(s?)\:\/\/[0-9a-zA-Z]([-.\w]*[0-9a-zA-Z])*(:(0-9)*)*(\/?)([a-zA-Z0-9\-\.\?\,\'\/\\\+&%\$#_]*)?"
            c=re.compile(pattern=pattern)
            return c.search(text).group()

    #     解析提交
    def submitCallbak(self):
        # userUrl=self.inputText.get()
        self.checkInputChange();
        self.statusText.set("正在解析链接！")
        self.resText.delete('1.0', 'end')
        try:
            videoInfo=self.dyClient.getVideoUrl(self.vUrl)
            print(videoInfo)
            if videoInfo!=None:
                resStr='视频连接：'
                resStr+=videoInfo['vedioUrl']+'\n\n背景音乐：'
                resStr+=videoInfo['music']
                webbrowser.open(videoInfo['vedioUrl'])

                self.resText.insert('insert', resStr)
                self.statusText.set('解析成功！')
            else:
                print('返回数据为空！')
                self.statusText.set('返回数据为空！')
        except Exception as err:
            print('解析异常：'+str(err))
            self.statusText.set('解析异常：'+str(err))


