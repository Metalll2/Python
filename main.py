import tkinter as tk
from tkinter import filedialog

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()

    def init_main(self):
        toolbar = tk.Frame(bd=1, bg="#d7d8e0", height=1)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        bt_open = tk.Button(toolbar, bd=0, bg="#d7d8e0", text="Открыть", compound=tk.LEFT, width=11, height=1, command=self.onOpen)
        bt_open.pack(side=tk.LEFT)

        bt_save = tk.Button(toolbar, bd=0, bg="#d7d8e0", text="Сохранить", compound=tk.LEFT, width=11, height =1, command=self.saveFile)
        bt_save.pack(side=tk.LEFT)

        bt_delete = tk.Button(toolbar, bd=0, bg="#d7d8e0", text="Удалить", compound=tk.LEFT, width=11, height =1, command=self.deleteFile)
        bt_delete.pack(side=tk.LEFT)

        bt_edit = tk.Button(toolbar, bd=0, bg="#d7d8e0", text="Редактировать", compound=tk.LEFT, width=11, height =1, command=self.editFont)
        bt_edit.pack(side=tk.LEFT)

        frame=tk.Frame(bd=1, bg="#d7d8e0")
        frame.pack()
        self.text=tk.Text(frame, width= 200 , height= 400 , bd=1 )
        self.text.pack(side=tk.LEFT)



    def onOpen(self):
        ftypes = [('Python files', '*.py'), ('All files', '*')]
        dlg = filedialog.Open(self, filetypes=ftypes)
        fl = dlg.show()

        if fl != '':
            text= self.readFile(fl)
            for i in range(len(text)):
                self.text.insert(tk.END, text[i])

    def saveFile(self):
        ftypes = [('Python files', '*.py'), ('All files', '*')]
        dlg = filedialog.SaveAs(self, filetypes=ftypes)
        fl = dlg.show()

        if fl != '':
            fl = open(fl, 'w')
            data = self.text.get('1.0', tk.END + '-1c')
            fl.write(data)
            fl.close()

    def readFile(self, file):
        readfile = open(file, "r")
        text = readfile.readlines()
        readfile.close()
        return text

    def deleteFile(self):
        self.text.delete('1.0', tk.END)

    def editFont(self):
        self.text.configure(font='Arial 14')













if __name__ == "__main__":
    root = tk.Tk()
    application = Main(root)
    application.pack()
    root.title("Текстовый редактор")
    root.geometry("600x400+600+400")
    root.resizable(False, False)
    root.mainloop()
















