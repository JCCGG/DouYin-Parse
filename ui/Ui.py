import tkinter as tk
from sdk import Douyin as dy
import webbrowser

# 主界面
# author JCC
class mainWindow():
    def __init__(self):
        self.tkinter=tk.Tk()
        self.w=500
        self.h=200
        self.dyClient=dy.Douyin()
    #     启动
    def launch(self):
        self.tkinter.title('抖音无水印视频音乐解析_JCC')
        x=(self.tkinter.winfo_screenwidth()-self.w)/2
        y=(self.tkinter.winfo_screenheight()-self.h)/2
        self.tkinter.geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))
        self.tkinter.resizable(False,False)
        self.initWeget()
        self.tkinter.mainloop()
    #初始界面
    def initWeget(self):
        contorlFrame = tk.Frame(self.tkinter)
        dataFrame=tk.Frame(self.tkinter)
        label=tk.Label(contorlFrame,text='连接：')
        self.inputText=tk.StringVar()
        self.statusText=tk.StringVar()

        inputUrl = tk.Entry(contorlFrame, textvariable=self.inputText,show=None,width=50)
        submitButton = tk.Button(contorlFrame, text='解析', command=self.submitCallbak)
        self.resText=tk.Text(dataFrame,height=10)
        statusLabel=tk.Label(dataFrame,text='状态：',textvariable=self.statusText)
        contorlFrame.pack()
        dataFrame.pack()
        label.grid(row=1,column=1)
        inputUrl.grid(row=1,column=2,padx=15,ipady=5)
        submitButton.grid(row=1,column=3,ipady=3,ipadx=5)
        self.resText.pack()
        statusLabel.pack(side='left')
    #     解析提交
    def submitCallbak(self):
        print(self.inputText.get())
        userUrl=self.inputText.get()
        self.resText.delete('1.0', 'end')
        try:
            videoInfo=self.dyClient.getVideoUrl(userUrl)
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


