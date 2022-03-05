import tkinter as tk
from sdk import Douyin as dy
import webbrowser
import re
from PIL import Image,ImageTk
import io

# 主界面
# author JCC
class mainWindow():
    def __init__(self):
        self.tkinter=tk.Tk()
        self.w=550
        self.h=280
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
        inputUrl = tk.Entry(contorlFrame, textvariable=self.inputText,show=None,width=60,selectforeground="#ffffff",selectbackground="#000000")
        submitButton = tk.Button(contorlFrame, text='解析', command=self.submitCallbak)
        self.resText=tk.Text(dataFrame,height=16,selectforeground="#ffffff",selectbackground="#000000")
        statusLabel=tk.Label(dataFrame,textvariable=self.statusText,fg="#ff0000")
        # 弹出菜单
        self.menu = tk.Menu(contorlFrame,
                    tearoff=False,
                    )
        self.menu.add_command(label="剪切", command=lambda:self.cut(inputUrl))
        self.menu.add_command(label="复制", command=lambda:self.copy(inputUrl))
        self.menu.add_command(label="粘贴", command=lambda:self.paste(inputUrl))
        inputUrl.bind("<Button-3>",self.popup)

        contorlFrame.pack()
        dataFrame.pack()
        label.grid(row=1,column=1)
        inputUrl.grid(row=1,column=2,padx=15,ipady=5)
        submitButton.grid(row=1,column=3,ipady=3,ipadx=5)
        self.resText.pack()
        statusLabel.pack(side='left')

    # 显示图片窗口
    def showImage(self,douyin):
        bgImage=douyin.getBgImage()
        if bgImage!= None and bgImage!= "":
            imageFrame = tk.Toplevel()
            image = Image.open(io.BytesIO(bgImage))
            img = ImageTk.PhotoImage(image)
            imgCanvas = tk.Canvas(imageFrame, width=image.width, height=image.height, bg='white')
            imgCanvas.create_image(0, 0, image=img, anchor="nw")
            imgCanvas.pack()
            imageFrame.mainloop()
        else:
            print("地址为空")

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
        print("取到输入的地址："+url)
        if url==None or url=="":
            print("请输入正确链接！")
            self.statusText.set("请输入正确链接！")
        else:
            self.statusText.set("已获得输入的链接！")
            self.vUrl=url
    def expToUrl(self,text):
        try:
            if text!="" or text !=None:
                pattern="(ht|f)tp(s?)\:\/\/[0-9a-zA-Z]([-.\w]*[0-9a-zA-Z])*(:(0-9)*)*(\/?)([a-zA-Z0-9\-\.\?\,\'\/\\\+&%\$#_]*)?"
                c=re.compile(pattern=pattern)
                url=c.search(text).group()
                return url
        except Exception as err:
            print("正则取值异常，请输入正确地址："+str(err))
            self.statusText.set("正则取值异常，请输入正确地址:"+str(err))

    #     解析提交
    def submitCallbak(self):
        # userUrl=self.inputText.get()
        self.checkInputChange();
        print("正在解析链接！")
        self.statusText.set("正在解析链接！")
        self.resText.delete('1.0', 'end')
        douyin=dy.Douyin()
        try:
            videoInfo=douyin.getVideoUrl(self.vUrl)
            print(videoInfo)
            if videoInfo!=None:
                resStr='视频连接：'
                resStr+=videoInfo['vedioUrl']+'\n\n背景音乐：'
                resStr+=videoInfo['music']+'\n\n封面：'
                resStr+=videoInfo['bgImage']
                webbrowser.open(videoInfo['vedioUrl'])
                self.resText.insert('insert', resStr)
                self.statusText.set('解析成功！')
                self.showImage(douyin)
            else:
                print('返回数据为空！')
                self.statusText.set('返回数据为空！')
        except Exception as err:
            print('解析异常：'+str(err))
            self.statusText.set('解析异常：'+str(err))


