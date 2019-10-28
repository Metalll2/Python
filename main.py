import tkinter as tk
from tkinter import DoubleVar
import time

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()


    def init_main(self):

        toolbar = tk.Frame(bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)



        label = tk.Label(toolbar, bd=2)
        label.pack(side=tk.LEFT)
        self.update_label(label)





    def update_label(self, label):
        def hashrate():
            update = 1000
            nowtime = time.asctime(time.localtime(time.time()))
            speed = nowtime
            label.config(text=speed)
            label.after(update, hashrate)
        hashrate()

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    app.pack()
    root.title("Household finance")
    root.geometry("300x250+300+200")
    root.resizable(False, False)
    root.mainloop()
