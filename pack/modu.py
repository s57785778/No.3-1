import sqlite3
import csv
import json

def create_database():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE users (
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL)''')
    cursor.execute('''CREATE TABLE books (
                        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        author TEXT NOT NULL,
                        publisher TEXT NOT NULL,
                        year INTEGER NOT NULL)''')
    conn.commit()
    conn.close()

def import_users():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    with open('users.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (row['username'], row['password']))
    conn.commit()
    conn.close()

def import_books():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    with open('books.json', 'r' ,encoding='utf-8') as file:
        data = json.load(file)
        for book in data:
            cursor.execute('INSERT INTO books (title, author, publisher, year) VALUES (?, ?, ?, ?)', (book['title'], book['author'], book['publisher'], book['year']))
    conn.commit()
    conn.close()

def login():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    while True:
        username = input('請輸入帳號：')
        password = input('請輸入密碼：')
        cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        if cursor.fetchone():
            break
        else:
            print('帳號或密碼錯誤，請重新輸入')
    conn.close()

def show_menu():
    print('''
-------------------
    資料表 CRUD
-------------------
    1. 增加記錄
    2. 刪除記錄
    3. 修改記錄
    4. 查詢記錄
    5. 資料清單
-------------------''')

def add_book():
    title = input('請輸入要新增的標題：')
    author = input('請輸入要新增的作者：')
    publisher = input('請輸入要新增的出版社：')
    year = input('請輸入要新增的年份：')
    if title and author and publisher and year:
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO books (title, author, publisher, year) VALUES (?, ?, ?, ?)', (title, author, publisher, year))
        conn.commit()
        conn.close()
        print('異動 1 記錄')
    else:
        print('=>給定的條件不足，無法進行新增作業')

def delete_book():
    title = input('請問要刪除哪一本書？：')
    if title:
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM books WHERE title=?', (title,))
        conn.commit()
        conn.close()
        print('異動 1 記錄')
    else:
        print('=>給定的條件不足，無法進行刪除作業')

def update_book():
    old_title = input('請問要修改哪一本書的標題？：')
    new_title = input('請輸入要更改的標題：')
    new_author = input('請輸入要更改的作者：')
    new_publisher = input('請輸入要更改的出版社：')
    new_year = input('請輸入要更改的年份：')
    if old_title and (new_title or new_author or new_publisher or new_year):
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE books SET title=?, author=?, publisher=?, year=? WHERE title=?', (new_title, new_author, new_publisher, new_year, old_title))
        conn.commit()
        conn.close()
        print('異動 1 記錄')
    else:
        print('=>給定的條件不足，無法進行修改作業')

def query_book():
    keyword = input('請輸入想查詢的關鍵字：')
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("SELECT title, author, publisher, year FROM books WHERE title LIKE ? OR author LIKE ?", ('%'+keyword+'%', '%'+keyword+'%'))
    results = cursor.fetchall()
    for result in results:
        print('|  title  |   author   |  publisher  |publisher|')
        print(f'|{result[0]:<10}|{result[1]:<12}|{result[2]:<15}|{result[3]:<10}|')
    conn.close()

def list_books():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('SELECT title, author, publisher, year FROM books')
    results = cursor.fetchall()
    print('|    title   |     author      |     publisher        |   year    |')
    for result in results:
        print(f'|{result[0]:<10}|{result[1]:<12}|{result[2]:<15}|{result[3]:<10}|')
    conn.close()