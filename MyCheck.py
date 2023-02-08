from tkinter import *
from tkinter.ttk import * 
from tkinter.messagebox import *
import time
import requests
import sqlite3
#cntrl +/

KEY = "11a1324bcbefe090f527882d2da3e045"
CITY_ID = 486137
PARAM = {'id':CITY_ID, 'units': 'metric', 'lang': 'ru', 'APPID': KEY}
URL = "http://api.openweathermap.org/data/2.5/weather"
URLRATE = "https://www.cbr-xml-daily.ru/daily_json.js"

class Application1(Frame):
    def __init__(self, master):
        super(Application1, self).__init__(master, borderwidth=0, relief=SOLID)
        self.place(x=0, y=0, width=701, height=420)
        self.create_widgets()
    def create_widgets(self):
        self.__columns = ('Номер строки','Рубль','Доллар','Евро','Юань', 'Золото','Серебро')
        self.tree = Treeview(self, show='headings', columns=self.__columns, height=100)
        db.cursor.execute("SELECT * FROM mycheck")
        db.sql.commit()
        self.data = db.cursor.fetchall()
        for __id in range(len(self.__columns)):
            self.tree.heading('#{}'.format(__id+1), text = self.__columns[__id])
            self.tree.column('#{}'.format(__id+1), width=100, minwidth=50)
        for k in self.data:
            self.tree.insert('', 'end', values = k)
        self.tree.pack()

    def record(self,entryRuble, entryDollar, entryEuro,entryYuan, entryGold,entrySerebro):
        if(entryRuble !="" or entryDollar != "" or entryEuro != "" or entryYuan != "" or entryGold != "" or entrySerebro != ""):
            db.cursor.execute("INSERT INTO mycheck (Ruble, Dollar, EURO, YUAN, GOLD, SEREBRO) VALUES (?,?,?,?,?,?)", (entryRuble, entryDollar, entryEuro, entryYuan, entryGold, entrySerebro))
            db.sql.commit()
            self.view_records()
            self.open_info("Сообщение", "Данные записаны.")
        else:
            self.open_info("Сообщение", "Значения равны нулю.")
            
    def view_records(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        db.cursor.execute("SELECT * FROM mycheck")
        db.sql.commit()
        self.new_data = db.cursor.fetchall()
        for i in self.new_data:
            self.tree.insert('', 'end', values = i)

    def open_info(self, *text):
            showinfo(title=text[0], message=text[1])
    
    def delete_record(self):
        for self.select in self.tree.selection():
            self.item = self.tree.item(self.select)
            self.id = self.item['values'][0]
            db.cursor.execute("DELETE FROM mycheck WHERE id = (?)",(self.id,))
            self.new_id=self.id
            db.sql.commit()
            db.cursor.execute('''UPDATE SQLITE_SEQUENCE SET seq = "self.new_id"  WHERE name = "mycheck"''')
            db.sql.commit()
            self.open_info("Сообщение", "Строка удалена.")
            self.view_records()
    
    def new_file(self):
        db.cursor.execute("DELETE FROM mycheck")
        db.sql.commit()
        db.cursor.execute('''UPDATE SQLITE_SEQUENCE SET seq = 0 WHERE name = "mycheck"''')
        db.sql.commit()
        self.open_info("Сообщение", "Лист пуст.")
        self.view_records()    
class Application2(Frame):
    def __init__(self, master):
        super(Application2, self).__init__(master, borderwidth=0, relief=SOLID)
        self.place(x=700, y=0, width=157, height=420)
        self.create_widgets()
        self.setRate()
        
    def create_widgets(self):
        self.tree_right = Treeview(self, height=100)
        self.tree_right.heading("#0", text="Курс валюты и металлов")
        self.tree_right.column('#0', width=155, minwidth=50)
        self.tree_right.pack()

    def setRate(self):
        try:
            self.d = requests.get(URLRATE)
            self.dataRate = self.d.json()
            self.listValute = ['USD', 'EUR', 'CNY']
            self.Rate = {}
            for i in range(len(self.listValute)):
                self.Rate[self.listValute[i]] = self.dataRate['Valute'][self.listValute[i]]['Value']
            for __id in self.Rate:
                self.tree_right.insert('',END ,iid= __id, text = __id+"/RUB = " + str(round(self.Rate[__id], 2)))
            root.after(1000, self.setRate)
        
        except Exception as ex:
            print("Set Rate: Connection is falled", ex)
            pass
class Application3(Frame):
    def __init__(self, master):
        super(Application3, self).__init__(master, borderwidth=0, relief=SOLID)
        self.place(x=0, y=420, width=857, height=30)
        self.create_widgets()
        self.setTime()
        self.setWeather()

    def create_widgets(self):
        self.lbltime = Label(self)
        self.lbltime.pack(side=RIGHT, padx=1)
        self.lblcity = Label(self, text="Город: Сургут")
        self.lblcity.pack(side=LEFT, padx=1)
        self.lblweather = Label(self)
        self.lblweather.pack(side=LEFT, padx=1)
       
    def setTime(self):
        self.sec = time.time()
        self.time = time.localtime(self.sec)
        self.lbltime['text'] = "Время: " + time.strftime('%H:%M:%S',self.time)
        root.after(1000,self.setTime)

    def setWeather(self):
        try:
            r = requests.get(URL, params=PARAM)
            data = r.json()
            self.lblweather['text'] = "Погода: " + str(data['main']['feels_like']) +', ' + data['weather'][0]['description']
            root.after(10000,self.setWeather)
        except Exception as ex:
            print("Set Weaather: Connection is falled", ex)
            pass
class popupEdit(Toplevel):
    def __init__(self):
        super().__init__(root)
        self.initPopup()
        self.view = app1
    
    def initPopup(self):
        self.title("Новое окно")
        self.geometry("350x300+700+300")
        self.resizable(False, False)
        self.state_check = IntVar()
        self.check = Checkbutton(self, text="Автоматический расчет по курсу ЦБ.", variable=self.state_check, command=self.auto_calculate)
        self.check.place(x=0, y=10)
        self.labelRuble = Label(self, text = "Рубль:")
        self.labelRuble.place(x=0 , y=40)
        self.entryRuble = Entry(self)
        self.entryRuble.place(x=60, y=40)
        self.labelDollar = Label(self, text = "Доллар:")
        self.labelDollar.place(x=0, y=80)
        self.entryDollar = Entry(self)
        self.entryDollar.place(x=60, y=80)
        self.labelEuro = Label(self, text = "Евро:")
        self.labelEuro.place(x=0, y=120)
        self.entryEuro = Entry(self)
        self.entryEuro.place(x=60, y=120)
        self.labelYuan= Label(self, text = "Юань:")
        self.labelYuan.place(x=0, y=160)
        self.entryYuan = Entry(self)
        self.entryYuan.place(x=60, y=160)
        self.labelGold = Label(self, text = "Золото:")
        self.labelGold.place(x=0, y=200)
        self.entryGold= Entry(self)
        self.entryGold.place(x=60, y=200)
        self.labelSerebro = Label(self, text = "Серебро:")
        self.labelSerebro.place(x=0, y=240)
        self.entrySerebro = Entry(self)
        self.entrySerebro.place(x=60, y=240)
        self.btn = Button(self, text="OK")
        self.btn.bind('<Button-1>', lambda event: app1.record(self.entryRuble.get(),  self.entryDollar.get(), self.entryEuro.get(), self.entryYuan.get(), self.entryGold.get(),self.entrySerebro.get()))
        self.btn.place(x=260, y=120)
        self.btn_close = Button(self, text="Закрыть", command=self.destroy)
        self.btn_close.place(x=260, y=160)
    
        self.grab_set()
        self.focus_set()
  
    
    def auto_calculate(self):
        if(self.state_check.get() == 1):
            if(self.entryRuble.get() != ""):#or self.entryDollar.get() != "" or self.entryEuro.get() != "" or self.entryYuan.get() != "" or self.entryGold.get() != "" or self.entrySerebro.get() != ""):
                self.rub = float(self.entryRuble.get())
                self.entryDollar.delete(0,END)
                self.entryDollar.insert(0, str(round((self.rub/float(app2.Rate['USD'])),2)))
                self.entryEuro.delete(0,END)
                self.entryEuro.insert(0,str(round(self.rub/float(app2.Rate['EUR']),2)))
                self.entryYuan.delete(0,END)
                self.entryYuan.insert(0,str(round(self.rub/float(app2.Rate['CNY']),2)))
            elif(self.entryDollar.get() != ""):
                self.dollars = float(self.entryDollar.get())
                self.entryRuble.delete(0,END)
                self.entryRuble.insert(0, str(round((self.dollars*float(app2.Rate['USD'])),2)))
                self.rub = float(self.entryRuble.get())
                self.entryEuro.delete(0,END)
                self.entryEuro.insert(0,str(round(self.rub/float(app2.Rate['EUR']),2)))
                self.entryYuan.delete(0,END)
                self.entryYuan.insert(0,str(round(self.rub/float(app2.Rate['CNY']),2)))
            elif(self.entryYuan.get() != ""):
                self.cny = float(self.entryYuan.get())
                self.entryRuble.delete(0,END)
                self.entryRuble.insert(0, str(round((self.cny*float(app2.Rate['CNY'])),2)))
                self.rub = float(self.entryRuble.get())
                self.entryDollar.delete(0,END)
                self.entryDollar.insert(0, str(round((self.rub/float(app2.Rate['USD'])),2)))
                self.entryEuro.delete(0,END)
                self.entryEuro.insert(0,str(round(self.rub/float(app2.Rate['EUR']),2)))
            else:
                 pass
        else:
            pass     
class DB:
    def __init__(self):
        try:
            self.sql = sqlite3.connect('MyCheck.db')
            self.cursor = self.sql.cursor()
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS mycheck(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                RUBLE REAL,
                Dollar REAL,
                EURO REAL,
                YUAN REAL,
                GOLD REAL,
                SEREBRO REAL
                )''')
            self.sql.commit()
        except self.sql.Error as error:
            print("Сonnection is falled: ", error)
            pass 
        finally:
            if(self.sql):
                print("Сonnection is successful.")
class MainMenu:
    def __init__(self):
        self.main_menu = Menu()
        self.createMenu()

    def createMenu(self):
        self.file_menu = Menu()
        self.file_menu.add_command(label='Новый', command=app1.new_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Закрыть', command=root.destroy)

        self.theme_menu = Menu()
        self.theme = StringVar()
        self.theme.set("default")
        self.style = Style()
        self.theme_menu.add_radiobutton(label="Стандартный",value="default", variable=self.theme, command=self.setTheme)
        self.theme_menu.add_radiobutton(label="Классический",value="classic", variable=self.theme, command=self.setTheme)
        self.theme_menu.add_radiobutton(label="Светлый",value="winnative", variable=self.theme, command=self.setTheme)
        self.theme_menu.add_radiobutton(label="Темный",value="clam", variable=self.theme, command=self.setTheme)

        self.file_menuedit = Menu()
        self.file_menuedit.add_command(label='Добавить запись', command=popupEdit)
        self.file_menuedit.add_command(label='Удалить запись', command=app1.delete_record)

        self.main_menu.add_cascade(label='Файл', menu=self.file_menu)
        self.main_menu.add_cascade(label='Создать', menu=self.file_menuedit)
        self.main_menu.add_cascade(label='Вид', menu=self.theme_menu)
        self.main_menu.add_cascade(label='Справка')     
    
    def setTheme(self):
        self.style.theme_use(self.theme.get())
    
root = Tk()
db = DB()

root.title("My check")
root.geometry('857x450+700+300')
root.resizable(False, False)
root.option_add("*tearOff", FALSE)

app1 = Application1(root)
app2 = Application2(root)
app3 = Application3(root)

menuapp = MainMenu()
root.config(menu=menuapp.main_menu)

root.mainloop()

