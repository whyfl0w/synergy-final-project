import tkinter as tk
from tkinter import ttk
import sqlite3

# создаем главное окно приложения
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    # метод для хранения и инициализации объектов GUI
    def init_main(self):
        # создаем панель инструментов
        toolbar = tk.Frame(bg='#d7d7d7', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file='./img/add.png')
        # создание кнопки добавления
        btn_open_dialog = tk.Button(toolbar, bg='#d7d7d7', bd=0,
                                    image=self.add_img, command=self.open_dialog)
        btn_open_dialog.pack(side=tk.LEFT) # упаковка и выравнивание по левому краю окна

        # создание кнопки изменения данных
        self.update_img = tk.PhotoImage(file='./img/update.png')
        btn_edit_dialog = tk.Button(toolbar, bg='#d7d7d7', bd=0, 
                                    image=self.update_img, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        # создание кнопки удаления записи
        self.delete_img = tk.PhotoImage(file='./img/delete.png')
        btn_delete = tk.Button(toolbar, bg='#d7d7d7', bd=0, 
                               image=self.delete_img, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        # кнопка поиска
        self.search_image = tk.PhotoImage(file='./img/search.png')
        btn_search = tk.Button(toolbar, bg='#d7d7d7', bd=0,
                               image=self.search_image, command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        # кнопка обновления
        self.refresh_image = tk.PhotoImage(file='./img/refresh.png')
        btn_refresh = tk.Button(toolbar, bg='#d7d7d7', bd=0, 
                                image=self.refresh_image, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        # добавляем Treeview
        self.tree = ttk.Treeview(self, columns=('id', 'name', 'phone_number', 'email', 'salary'),
                                 height=45, show='headings')
        
        # добавляем параметры колонкам
        self.tree.column("id", width=30, anchor=tk.CENTER)
        self.tree.column("name", width=300, anchor=tk.CENTER)
        self.tree.column("phone_number", width=150, anchor=tk.CENTER)
        self.tree.column("email", width=150, anchor=tk.CENTER)
        self.tree.column("salary", width=150, anchor=tk.CENTER)

        # подписи колонок
        self.tree.heading("id", text='id')
        self.tree.heading("name", text='ФИО')
        self.tree.heading("phone_number", text='Номер телефона')
        self.tree.heading("email", text='E-mail')
        self.tree.heading("salary", text='Зарплата')

        # упаковка
        self.tree.pack(side=tk.LEFT)

        # добавление скроллбара
        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    # добавление данных
    def records(self, name, phone_number, email, salary):
        self.db.insert_data(name, phone_number, email, salary)
        self.view_records()

    # обновление (изменение) данных
    def update_record(self, name, phone_number, email, salary):
        self.db.cursor.execute('''UPDATE db SET name=?, phone_number=?, email=?, salary=? WHERE id=?''',
                          (name, phone_number, email, salary, 
                           self.tree.set(self.tree.selection()[0], '#1')))
        self.db.connection.commit()
        self.view_records()

    # вывод данных в виджет таблицы
    def view_records(self):
        # выбираем информацию из БД
        self.db.cursor.execute('''SELECT * FROM db''')
        # удаляем все из виджета таблицы
        [self.tree.delete(i) for i in self.tree.get_children()]
        # добавляем в виджет таблицы всю информацию из БД
        [self.tree.insert('', 'end', values=row)
         for row in self.db.cursor.fetchall()]
        
    # удаление записей
    def delete_records(self):
        # цикл по выделенным записям
        for selection_item in self.tree.selection():
            # удаление из БД
            self.db.cursor.execute('''DELETE FROM db WHERE id=?''', 
                              (self.tree.set(selection_item, '#1'),))
        # сохранение изменений в БД
        self.db.connection.commit()
        # обновление виджета таблицы
        self.view_records()

    # поиск записи по name (ФИО)
    def search_records(self, name):
        name = ('%' + name + '%',)
        self.db.cursor.execute(
            '''SELECT * FROM db WHERE name LIKE ?''', name)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row)
         for row in self.db.cursor.fetchall()]

    # метод отвечающий за вызов дочернего окна
    def open_dialog(self):
        Child()

    # метод отвечающий за вызов окна для изменения данных
    def open_update_dialog(self):
        Update()

    # метод отвечающий за вызов окна для поиска
    def open_search_dialog(self):
        Search()

# класс дочерних окон
class Child(tk.Toplevel): # Toplevel - окно верхнего уровня
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        # заголовок окна
        self.title('Добавить сотрудников')
        # размер окна
        self.geometry('400x200')
        # запрет на изменение размеров окна
        self.resizable(False, False)

        # перехватываем все события происходящие в приложении
        self.grab_set()
        # перехватываем фокус
        self.focus_set()

        # подписи
        label_name = tk.Label(self, text='ФИО:')
        label_name.place(x=50, y=50)
        label_select = tk.Label(self, text='Номер телефона')
        label_select.place(x=50, y=80)
        label_sum = tk.Label(self, text='E-mail')
        label_sum.place(x=50, y=110)
        label_pay = tk.Label(self, text='Зарплата')
        label_pay.place(x=50, y=140)

        # добавляем строку ввода для наименования
        self.entry_name = ttk.Entry(self)
        # меняем координаты объекта
        self.entry_name.place(x=200, y=50)

        # добавляем строку ввода для email
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=80)

        # добавляем строку ввода для номера телефона
        self.entry_phone_number = ttk.Entry(self)
        self.entry_phone_number.place(x=200, y=110)

        # добавляем строку ввода для зарплаты
        self.entry_wage = ttk.Entry(self)
        self.entry_wage.place(x=200, y=140)

        # кнопка закрытия дочернего окна
        self.btn_cancel = ttk.Button(
            self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=300, y=170)

        # кнопка добавления
        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=170)
        # срабатывание по нажатию ЛКМ
        # при нажатии кнопки вызывается метод records, которому передаюся значения из строк ввода
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_name.get(),
                                                                       self.entry_email.get(),
                                                                       self.entry_phone_number.get(),
                                                                       self.entry_wage.get()))

# класс окна для обновления, наследуемый от класса дочернего окна
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title('Редактировать позицию')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_name.get(),
                                                                          self.entry_email.get(),
                                                                          self.entry_phone_number.get(),
                                                                          self.entry_wage.get()))

        # закрываем окно редактирования
        btn_edit.bind('<Button-1>', lambda event: self.destroy(), add='+')
        self.btn_ok.destroy()

    def default_data(self):
        self.db.cursor.execute('''SELECT * FROM db WHERE id=?''',
                          (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        # получаем доступ к первой записи из выборки
        row = self.db.cursor.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_email.insert(0, row[2])
        self.entry_phone_number.insert(0, row[3])
        self.entry_wage.insert(0, row[4])

# класс поиска записи
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск по ФИО')
        self.geometry('300x100')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', 
                        lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', 
                        lambda event: self.destroy(), add='+')

# класс БД
class DB:
    def __init__(self):
        # создаем соединение с БД
        self.connection = sqlite3.connect('db.db')
        # создание объекта класса cursor, используемый для взаимодействия с БД
        self.cursor = self.connection.cursor()
        # выполнение запроса к БД
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS db (
            id INTEGER PRIMARY KEY, 
            name TEXT, 
            phone_number TEXT, 
            email TEXT, 
            salary TEXT
            )''')
        # сохранение изменений в БД
        self.connection.commit()

    # метод добавления записей в БД
    def insert_data(self, name, phone_number, email, salary):
        self.cursor.execute('''INSERT INTO db (name, phone_number, email, salary) VALUES (?, ?, ?, ?)''',
                       (name, phone_number, email,salary))
        self.connection.commit()

if __name__ == '__main__':
    root = tk.Tk() # объект экземпляра класса tk
    db = DB() # экземпляр класса DB
    app = Main(root) # экземпляр класса Main (главного окна)
    app.pack() # упаковка приложения
    root.title('Список сотрудников компании') # заголовок главного окна 
    root.geometry('800x600') # размеры главного окна
    root.resizable(False, False) # ограничение изменения размеров окна
    root.mainloop() # запуск цикла событий