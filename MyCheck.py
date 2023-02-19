from tkinter import *
from tkinter.ttk import * 
from tkinter.messagebox import *
from tkinter.filedialog import *
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

    def auto_record(self):
        self.state = menuapp.return_state()
        global start
        if self.state == 1:
            for self.tre in self.tree.get_children():
                    print(self.tree.item(self.tre, 'value'))
                    self.item = self.tree.item(self.tre, 'value')
                    self.id = self.item[0]
                    self.Rate = Application2.returnRate(self)
                    if self.item[1]:
                        db.cursor.execute("UPDATE mycheck SET (Ruble, Dollar, EURO, YUAN) = (?,?,?,?) WHERE id = (?)",(float(self.item[1]),round(float(self.item[1])/float(self.Rate['USD']),2),round(float(self.item[1])/float(self.Rate['EUR']),2),round(float(self.item[1])/float(self.Rate['CNY']),2), self.id))
                    elif self.item[2]: 
                        self.ruble = round(float(self.item[2])*float(self.Rate['USD']),2)
                        db.cursor.execute("UPDATE mycheck SET (Ruble, Dollar, EURO, YUAN) = (?,?,?,?) WHERE id = (?)",(float(self.ruble),round(float(self.item[2]),2),round(float(self.ruble)/float(self.Rate['EUR']),2),round(float(self.ruble)/float(self.Rate['CNY']),2), self.id))
                    elif self.item[3]: 
                        self.ruble = round(float(self.item[3])*float(self.Rate['EUR']),2)
                        db.cursor.execute("UPDATE mycheck SET (Ruble, Dollar, EURO, YUAN) = (?,?,?,?) WHERE id = (?)",(float(self.ruble),round(float(self.ruble)/float(self.Rate['USD']),2),round(float(self.item[3]),2),round(float(self.ruble)/float(self.Rate['CNY']),2), self.id))
                    elif self.item[4]: 
                        self.ruble = round(float(self.item[4])*float(self.Rate['CNY']),2)
                        db.cursor.execute("UPDATE mycheck SET (Ruble, Dollar, EURO, YUAN) = (?,?,?,?) WHERE id = (?)",(float(self.ruble),round(float(self.ruble)/float(self.Rate['USD']),2),round(float(self.ruble)/float(self.Rate['EUR']),2),round(float(self.item[4]),2), self.id))
                    else:
                        pass
            db.sql.commit()
            self.view_records()
            start = root.after(5000, self.auto_record)
        else:
            root.after_cancel(start)

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

            for i in range(len(self.listValute)):
                Application2.Rate[self.listValute[i]] = self.dataRate['Valute'][self.listValute[i]]['Value']
            for __id in Application2.Rate:
                self.tree_right.insert('',END ,iid= __id, text = __id+"/RUB = " + str(round(Application2.Rate[__id], 3)))
            root.after(10000, self.setRate)
        
        except Exception as ex:
            print("Set Rate: Connection is falled: ", ex)
            pass
    Rate={}  
    def returnRate(self):
        return Application2.Rate
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
            root.after(60000,self.setWeather)
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

        check_validate = (self.register(self.is_valid), '%P')

        self.labelRuble = Label(self, text = "Рубль:")
        self.labelRuble.place(x=0 , y=40)
        self.entryRuble = Entry(self, validate='key', validatecommand=check_validate)
        self.entryRuble.place(x=60, y=40)
        self.labelDollar = Label(self, text = "Доллар:")
        self.labelDollar.place(x=0, y=80)
        self.entryDollar = Entry(self, validate='key', validatecommand=check_validate)
        self.entryDollar.place(x=60, y=80)
        self.labelEuro = Label(self, text = "Евро:")
        self.labelEuro.place(x=0, y=120)
        self.entryEuro = Entry(self, validate='key', validatecommand=check_validate)
        self.entryEuro.place(x=60, y=120)
        self.labelYuan= Label(self, text = "Юань:")
        self.labelYuan.place(x=0, y=160)
        self.entryYuan = Entry(self, validate='key', validatecommand=check_validate)
        self.entryYuan.place(x=60, y=160)
        self.labelGold = Label(self, text = "Золото:")
        self.labelGold.place(x=0, y=200)
        self.entryGold= Entry(self, validate='key', validatecommand=check_validate)
        self.entryGold.place(x=60, y=200)
        self.labelSerebro = Label(self, text = "Серебро:")
        self.labelSerebro.place(x=0, y=240)
        self.entrySerebro = Entry(self, validate='key', validatecommand=check_validate)
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
                self.entryDollar.insert(0, str(round((self.rub/float(Application2.Rate['USD'])),2)))
                self.entryEuro.delete(0,END)
                self.entryEuro.insert(0,str(round(self.rub/float(Application2.Rate['EUR']),2)))
                self.entryYuan.delete(0,END)
                self.entryYuan.insert(0,str(round(self.rub/float(Application2.Rate['CNY']),2)))
            elif(self.entryDollar.get() != ""):
                self.dollars = float(self.entryDollar.get())
                self.entryRuble.delete(0,END)
                self.entryRuble.insert(0, str(round((self.dollars*float(Application2.Rate['USD'])),2)))
                self.rub = float(self.entryRuble.get())
                self.entryEuro.delete(0,END)
                self.entryEuro.insert(0,str(round(self.rub/float(Application2.Rate['EUR']),2)))
                self.entryYuan.delete(0,END)
                self.entryYuan.insert(0,str(round(self.rub/float(Application2.Rate['CNY']),2)))
            elif(self.entryEuro.get() != ""):
                self.cny = float(self.entryEuro.get())
                self.entryRuble.delete(0,END)
                self.entryRuble.insert(0, str(round((self.cny*float(Application2.Rate['EUR'])),2)))
                self.rub = float(self.entryRuble.get())
                self.entryDollar.delete(0,END)
                self.entryDollar.insert(0, str(round((self.rub/float(Application2.Rate['USD'])),2)))
                self.entryYuan.delete(0,END)
                self.entryYuan.insert(0,str(round(self.rub/float(Application2.Rate['CNY']),2)))
            elif(self.entryYuan.get() != ""):
                self.cny = float(self.entryYuan.get())
                self.entryRuble.delete(0,END)
                self.entryRuble.insert(0, str(round((self.cny*float(Application2.Rate['CNY'])),2)))
                self.rub = float(self.entryRuble.get())
                self.entryDollar.delete(0,END)
                self.entryDollar.insert(0, str(round((self.rub/float(Application2.Rate['USD'])),2)))
                self.entryEuro.delete(0,END)
                self.entryEuro.insert(0,str(round(self.rub/float(Application2.Rate['EUR']),2)))
            else:
                 pass
        else:
            pass     
    def is_valid(self, newval):
        #self.result =  re.match(r'[0-9.]+[0-9]+[^a-zA-Z]{1,}',newval)
        try:
            x = float(newval)
            return True
        except ValueError:     
            return False
            

class popupSave:
    def __init__(self):
        self.initSavePopup()
    
    def initSavePopup(self):
        self.file = asksaveasfile()
        if self.file:
            self.get_datas = app1.tree
            for self.get_data in self.get_datas.get_children():
                self.item = self.get_datas.item(self.get_data)
                self.file.write(f"id: {str(self.item['values'][0]):5}"  f"Ruble: {str(self.item['values'][1]):15}"  f"Dollar: {str(self.item['values'][2]):15}"  f"EURO: {str(self.item['values'][3]):15}"  f"CNY: {str(self.item['values'][4]):15}\n")
            self.file.close()
       
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
        self.auto_update = IntVar()
        self.auto_update.set(0)
        self.file_menu.add_command(label='Новый', command=app1.new_file)
        self.file_menu.add_checkbutton(label='Обновлять счет', variable= self.auto_update, command=self.checkbutton_changed)
        self.file_menu.add_command(label='Сохранить', command=popupSave)
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
        
        self.about_app = Menu()
        self.about_app.add_command(label='О программе', command=self.show_info)

        self.main_menu.add_cascade(label='Файл', menu=self.file_menu)
        self.main_menu.add_cascade(label='Создать', menu=self.file_menuedit)
        self.main_menu.add_cascade(label='Вид', menu=self.theme_menu)
        self.main_menu.add_cascade(label='Справка', menu = self.about_app)     
    
    def setTheme(self):
        self.style.theme_use(self.theme.get())
    def show_info(self):
        showinfo(title="MyCheck", message="Программа отслеживает время, погоду и курсы валют. Можно вносить в БД кол-во рублей," 
        "евро, долларов, золото и серебро.Есть галочка для автоматического расчета. Допустим есть рубли, на основе курса валют "
        "можно сделать расчет сколько это в других валютах.")

    def checkbutton_changed(self):
        app1.auto_record()
    def return_state(self):
        return self.auto_update.get()  
               
            
    
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

