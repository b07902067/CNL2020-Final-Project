import tkinter as tk
import client
import sys

''' Server Information'''
Server_IP=sys.argv[1]
Server_PORT=sys.argv[2]
Server_ADDR="http://{}:{}".format(Server_IP, Server_PORT)
# print(Server_ADDR)

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry('350x600')
        self.resizable(False, False)
        self.title("台灣社交距離")
        self._frame = None
        self.switch_frame(StartPage)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class StartPage(tk.Frame):
    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, master)
        self.bg_color = 'LightSeaGreen'
        self.master.configure(bg = self.bg_color)
        self.configure(bg = self.bg_color, highlightthickness=0)
        tk.Label(self, borderwidth = 5, bg = self.bg_color, height=3, width=10).grid(row=0, column=0)
        tk.Label(self, text="請保持社交距離", borderwidth = 5, font=('Helvetica', 30, "bold"), fg="white", relief="ridge", bg = self.bg_color).grid(row=1, column=0, padx=1, pady=1)
        tk.Label(self, borderwidth = 5, bg = self.bg_color, height=3, width=10).grid(row=2, column=0)
        tk.Button(self, text="取得金鑰",command=self.req_key, font=('', 16, "bold"), height=3, width=10, fg = self.bg_color).grid(row=3, column=0, padx=10, pady=10)
        tk.Label(self, borderwidth = 5, bg = self.bg_color, height=3, width=10).grid(row=4, column=0)
        tk.Button(self, text="確認接觸史",  font=('', 16, "bold"),command=self.check_ID, height=3, width=10, fg = self.bg_color).grid(row=5, column=0, padx=10, pady=10)
        tk.Label(self, borderwidth = 5, bg = self.bg_color, height=3, width=10).grid(row=6, column=0)
        tk.Button(self, text="確診者上傳 ID", font=('', 16, "bold"),
                    command=self.send_key, height=3, width=10, fg = self.bg_color).grid(row=7, column=0, padx=10, pady=10)
    def req_key(self):
        client.reqKEY(Server_ADDR)
        self.master.switch_frame(PageOne)
    def check_ID(self):
        contact = client.checkID(Server_ADDR)
        print(contact)
        if contact == False:
            self.master.switch_frame(PageTwo)
        else:
            self.master.switch_frame(PageThree)
    def send_key(self):
        client.sendKEY(Server_ADDR)
        self.master.switch_frame(PageFour)

class PageOne(tk.Frame):
    def __init__(self, master):
        self.master = master
        self.bg_color = 'LightSeaGreen'
        self.master.configure(bg = self.bg_color)
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='LightSeaGreen')
        tk.Label(self, bg=self.bg_color).grid(row=0, column=0)
        tk.Label(self, bg=self.bg_color).grid(row=1, column=0)
        tk.Label(self, bg=self.bg_color).grid(row=2, column=0)
        tk.Label(self, bg=self.bg_color).grid(row=3, column=0)
        tk.Label(self, bg=self.bg_color).grid(row=4, column=0)
        tk.Label(self, text="已取得金鑰", font=('Helvetica', 25, "bold"), bg=self.bg_color, relief="ridge", fg="white").grid(row=5, column=0, padx=10, pady=10)
        tk.Label(self, text="請記得戴口罩，保持社交距離", font=('Helvetica', 14, "bold"), bg=self.bg_color, fg="white").grid(row=6, column=0, padx=10, pady=10)
        tk.Label(self, bg=self.bg_color).grid(row=7, column=0)
        tk.Button(self, text="返回首頁",
        command=lambda: master.switch_frame(StartPage), bg=self.bg_color).grid(row=8, column=0, ipadx=0, ipady=0)

class PageTwo(tk.Frame):
    def __init__(self, master):
        self.master = master
        self.bg_color = 'LightSeaGreen'
        self.master.configure(bg = self.bg_color)
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='LightSeaGreen')
        tk.Label(self, bg=self.bg_color).grid(row=0, column=0)
        tk.Label(self, bg=self.bg_color).grid(row=1, column=0)
        tk.Label(self, bg=self.bg_color).grid(row=2, column=0)
        tk.Label(self, bg=self.bg_color).grid(row=3, column=0)
        tk.Label(self, bg=self.bg_color).grid(row=4, column=0)
        tk.Label(self, text="目前無與確診者接觸紀錄", font=('Helvetica', 25, "bold"), bg=self.bg_color, relief="ridge", fg="white").grid(row=5, column=0, padx=10, pady=10)
        tk.Label(self, text="請記得戴口罩，保持社交距離", font=('Helvetica', 14, "bold"), bg=self.bg_color, fg="white").grid(row=6, column=0, padx=10, pady=10)
        tk.Label(self, bg=self.bg_color).grid(row=7, column=0)
        tk.Button(self, text="返回首頁",
        command=lambda: master.switch_frame(StartPage), bg=self.bg_color).grid(row=8, column=0, ipadx=0, ipady=0)
class PageThree(tk.Frame):
    def __init__(self, master):
        self.master = master
        self.bg_color = 'LightSeaGreen'
        self.master.configure(bg = self.bg_color)
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='LightSeaGreen')
        tk.Label(self, bg=self.bg_color).grid(row=0, column=0)
        tk.Label(self, bg=self.bg_color).grid(row=1, column=0)
        tk.Label(self, bg=self.bg_color).grid(row=2, column=0)
        tk.Label(self, bg=self.bg_color).grid(row=3, column=0)
        tk.Label(self, bg=self.bg_color).grid(row=4, column=0)
        tk.Label(self, text="發現與確診者接觸紀錄", font=('Helvetica', 25, "bold"), bg=self.bg_color, relief="ridge", fg="darkred").grid(row=5, column=0, padx=10, pady=10)
        tk.Label(self, text="請儘速通報地方衛生局\n或撥打 1922 詢問", font=('Helvetica', 14, "bold"), bg=self.bg_color, fg="darkred").grid(row=6, column=0, padx=10, pady=10)
        tk.Label(self, bg=self.bg_color).grid(row=7, column=0)
        tk.Button(self, text="返回首頁", command=lambda: master.switch_frame(StartPage), bg=self.bg_color).grid(row=8, column=0, ipadx=0, ipady=0)
class PageFour(tk.Frame):
    def __init__(self, master):
        self.master = master
        self.bg_color = 'LightSeaGreen'
        self.master.configure(bg = self.bg_color)
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='LightSeaGreen')
        tk.Label(self, bg=self.bg_color).grid(row=0, column=0)
        tk.Label(self, bg=self.bg_color).grid(row=1, column=0)
        tk.Label(self, bg=self.bg_color).grid(row=2, column=0)
        tk.Label(self, bg=self.bg_color).grid(row=3, column=0)
        tk.Label(self, bg=self.bg_color).grid(row=4, column=0)
        tk.Label(self, text="已上傳完成", font=('Helvetica', 25, "bold"), bg=self.bg_color, relief="ridge", fg="white").grid(row=5, column=0, padx=10, pady=10)
        tk.Label(self, text="望您早日康復", font=('Helvetica', 14, "bold"), bg=self.bg_color, fg="white").grid(row=6, column=0, padx=10, pady=10)
        tk.Label(self, bg=self.bg_color).grid(row=7, column=0)
        tk.Button(self, text="返回首頁", command=lambda: master.switch_frame(StartPage), bg=self.bg_color).grid(row=8, column=0, ipadx=0, ipady=0)

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()


'''
reference :
https://www.delftstack.com/zh-tw/howto/python-tkinter/how-to-switch-frames-in-tkinter/
'''
