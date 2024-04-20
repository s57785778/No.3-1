

# midterm.py
import os
import pack.modu as lib

if not os.path.exists('library.db'):
    lib.create_database()
    lib.import_users()
    lib.import_books()

lib.login()
while True:
    lib.show_menu()
    choice = input('選擇要執行的功能(Enter離開)：')
    if choice == '1':
        lib.add_book()
        lib.list_books()
    elif choice == '2':
        lib.delete_book()
        lib.list_books()
    elif choice == '3':
        lib.list_books()
        lib.update_book()
        lib.list_books()
    elif choice == '4':
        lib.query_book()
    elif choice == '5':
        lib.list_books()
    elif choice == '':
        break
    else:
        print('無效的選擇')