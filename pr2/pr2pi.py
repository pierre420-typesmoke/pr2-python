import os
import pickle

class person:
    def __init__(self, name):
        self.__name = name
    
    def get_name(self):
        return self.__name
    
    def set_name(self, name):
        self.__name = name

class user(person):
    def __init__(self, name):
        super().__init__(name)
        self.borrowed_books = []

class librarian(person):
    def __init__(self, name):
        super().__init__(name)

class book:
    def __init__(self, title, author, status="доступна"):
        self.__title = title
        self.author = author
        self.status = status
    
    def get_title(self):
        return self.__title
    
    def set_title(self, title):
        self.__title = title

class librarysystem:
    def __init__(self):
        self.books = []
        self.users = []
        self.librarians = []
        self.current_user = None
        self.current_librarian = None
        self.load_data()
    
    def load_data(self):
        if os.path.exists("books.pkl"):
            try:
                with open("books.pkl", "rb") as f:
                    self.books = pickle.load(f)
                print("книги загружены")
            except:
                print("ошибка загрузки книг")
        
        if os.path.exists("users.pkl"):
            try:
                with open("users.pkl", "rb") as f:
                    self.users = pickle.load(f)
                print("пользователи загружены")
            except:
                print("ошибка загрузки пользователей")
        
        if os.path.exists("librarians.pkl"):
            try:
                with open("librarians.pkl", "rb") as f:
                    self.librarians = pickle.load(f)
                print("библиотекари загружены")
            except:
                print("ошибка загрузки библиотекарей")
    
    def save_data(self):
        try:
            with open("books.pkl", "wb") as f:
                pickle.dump(self.books, f)
            print("книги сохранены")
        except:
            print("ошибка сохранения книг")
        
        try:
            with open("users.pkl", "wb") as f:
                pickle.dump(self.users, f)
            print("пользователи сохранены")
        except:
            print("ошибка сохранения пользователей")
        
        try:
            with open("librarians.pkl", "wb") as f:
                pickle.dump(self.librarians, f)
            print("библиотекари сохранены")
        except:
            print("ошибка сохранения библиотекарей")
    
    def show_all_books(self):
        print("\nсписок всех книг")
        if not self.books:
            print("в библиотеке нет книг")
            return
        
        for i, book in enumerate(self.books, 1):
            print(f"{i}. '{book.get_title()}' - {book.author} ({book.status})")
    
    def find_book(self, title):
        for book in self.books:
            if book.get_title().lower() == title.lower():
                return book
        return None
    
    def find_user(self, name):
        for user in self.users:
            if user.get_name().lower() == name.lower():
                return user
        return None
    
    def librarian_menu(self):
        while True:
            print("1. добавить новую книгу")
            print("2. удалить книгу")
            print("3. зарегистрировать пользователя")
            print("4. список пользователей")
            print("5. список книг")
            print("6. выйти")
            
            choice = input("выберите действие (1-6): ")
            
            if choice == "1":
                self.add_book()
            elif choice == "2":
                self.remove_book()
            elif choice == "3":
                self.register_user()
            elif choice == "4":
                self.show_all_users()
            elif choice == "5":
                self.show_all_books()
            elif choice == "6":
                print("выход из системы...")
                break
            else:
                print("неверный выбор")
    
    def add_book(self):
        print("\nдобавление книги")
        title = input("введите название: ")
        author = input("введите автора: ")
        
        new_book = book(title, author, "доступна")
        self.books.append(new_book)
        print(f"книга '{title}' добавлена")
    
    def remove_book(self):
        print("\nудаление книги")
        self.show_all_books()
        
        if not self.books:
            return
        
        try:
            book_num = int(input("введите номер книги для удаления: "))
            if 1 <= book_num <= len(self.books):
                book = self.books[book_num - 1]
                
                if book.status == "выдана":
                    print(f"книга '{book.get_title()}' выдана, удалить нельзя")
                    return
                
                print(f"книга '{book.get_title()}' удалена")
                self.books.pop(book_num - 1)
            else:
                print("неверный номер")
        except ValueError:
            print("ошибка: введите число")
    
    def register_user(self):
        print("\nрегистрация пользователя")
        name = input("введите имя: ")
        
        if self.find_user(name):
            print("пользователь уже существует")
            return
        
        new_user = user(name)
        self.users.append(new_user)
        print(f"пользователь '{name}' зарегистрирован")
    
    def show_all_users(self):
        print("\nсписок пользователей")
        if not self.users:
            print("нет пользователей")
            return
        
        for i, user in enumerate(self.users, 1):
            print(f"{i}. {user.get_name()}")
            if user.borrowed_books:
                print(f"   книги: {', '.join(user.borrowed_books)}")
            else:
                print("   книги: нет")
    
    def user_menu(self):
        while True:
            print(f"\nменю пользователя {self.current_user.get_name()}")
            print("1. доступные книги")
            print("2. взять книгу")
            print("3. вернуть книгу")
            print("4. мои книги")
            print("5. выйти")
            
            choice = input("выберите действие (1-5): ")
            
            if choice == "1":
                self.show_available_books()
            elif choice == "2":
                self.borrow_book()
            elif choice == "3":
                self.return_book()
            elif choice == "4":
                self.show_my_books()
            elif choice == "5":
                print("выход...")
                self.current_user = None
                break
            else:
                print("неверный выбор")
    
    def show_available_books(self):
        print("\nдоступные книги")
        available_books = [book for book in self.books if book.status == "доступна"]
        
        if not available_books:
            print("нет доступных книг")
            return
        
        for i, book in enumerate(available_books, 1):
            print(f"{i}. '{book.get_title()}' - {book.author}")
    
    def borrow_book(self):
        print("\nвзятие книги")
        
        available_books = [book for book in self.books if book.status == "доступна"]
        
        if not available_books:
            print("нет доступных книг")
            return
        
        for i, book in enumerate(available_books, 1):
            print(f"{i}. '{book.get_title()}' - {book.author}")
        
        try:
            choice = int(input("введите номер книги: "))
            if 1 <= choice <= len(available_books):
                book = available_books[choice - 1]
                
                if book.status == "доступна":
                    book.status = "выдана"
                    self.current_user.borrowed_books.append(book.get_title())
                    print(f"вы взяли книгу '{book.get_title()}'")
                else:
                    print("книга уже выдана")
            else:
                print("неверный номер")
        except ValueError:
            print("ошибка: введите число")
    
    def return_book(self):
        print("\nвозврат книги")
        
        if not self.current_user.borrowed_books:
            print("у вас нет книг")
            return
        
        print("ваши книги:")
        for i, book_title in enumerate(self.current_user.borrowed_books, 1):
            print(f"{i}. {book_title}")
        
        try:
            choice = int(input("введите номер книги для возврата: "))
            if 1 <= choice <= len(self.current_user.borrowed_books):
                book_title = self.current_user.borrowed_books[choice - 1]
                
                book = self.find_book(book_title)
                if book:
                    book.status = "доступна"
                
                self.current_user.borrowed_books.pop(choice - 1)
                print(f"книга '{book_title}' возвращена")
            else:
                print("неверный номер")
        except ValueError:
            print("ошибка: введите число")
    
    def show_my_books(self):
        print(f"\nваши книги {self.current_user.get_name()}")
        
        if not self.current_user.borrowed_books:
            print("у вас нет книг")
            return
        
        for i, book_title in enumerate(self.current_user.borrowed_books, 1):
            print(f"{i}. {book_title}")
    
    def main_menu(self):
        while True:
            print("\nбиблиотечная система")
            print("1. войти как библиотекарь")
            print("2. войти как пользователь")
            print("3. выход")
            
            choice = input("выберите (1-3): ")
            
            if choice == "1":
                self.login_librarian()
            elif choice == "2":
                self.login_user()
            elif choice == "3":
                print("сохранение и выход...")
                self.save_data()
                break
            else:
                print("неверный выбор")
    
    def login_librarian(self):
        print("\nвход библиотекаря")
        
        if not self.librarians:
            name = input("введите имя (первый библиотекарь): ")
            librarian = librarian(name)
            self.librarians.append(librarian)
            self.current_librarian = librarian
            print(f"добро пожаловать, {name}")
            self.librarian_menu()
            return
        
        print("выберите библиотекаря:")
        for i, librarian in enumerate(self.librarians, 1):
            print(f"{i}. {librarian.get_name()}")
        
        try:
            choice = int(input("введите номер: "))
            if 1 <= choice <= len(self.librarians):
                self.current_librarian = self.librarians[choice - 1]
                print(f"добро пожаловать, {self.current_librarian.get_name()}")
                self.librarian_menu()
            else:
                print("неверный выбор")
        except ValueError:
            print("ошибка: введите число")
    
    def login_user(self):
        print("\nвход пользователя")
        
        if not self.users:
            print("нет пользователей")
            answer = input("зарегистрироваться? (да/нет): ")
            if answer.lower() == "да":
                name = input("введите имя: ")
                user = user(name)
                self.users.append(user)
                self.current_user = user
                print(f"добро пожаловать, {name}")
                self.user_menu()
            return
        
        print("выберите пользователя:")
        for i, user in enumerate(self.users, 1):
            print(f"{i}. {user.get_name()}")
        print(f"{len(self.users) + 1}. новый пользователь")
        
        try:
            choice = int(input("введите номер: "))
            if 1 <= choice <= len(self.users):
                self.current_user = self.users[choice - 1]
                print(f"добро пожаловать, {self.current_user.get_name()}")
                self.user_menu()
            elif choice == len(self.users) + 1:
                name = input("введите имя: ")
                if self.find_user(name):
                    print("пользователь уже существует")
                    return
                user = user(name)
                self.users.append(user)
                self.current_user = user
                print(f"добро пожаловать, {name}")
                self.user_menu()
            else:
                print("неверный выбор")
        except ValueError:
            print("ошибка: введите число")

if __name__ == "__main__":
    print("библиотечная система")
    
    lib = librarysystem()
    
    if not lib.books and not lib.users and not lib.librarians:
        print("создание начальных данных...")
        lib.books.append(book("преступление и наказание", "достоевский", "доступна"))
        lib.books.append(book("мастер и маргарита", "булгаков", "доступна"))
        lib.books.append(book("1984", "оруэлл", "выдана"))
        
        lib.users.append(user("иван иванов"))
        lib.users.append(user("петр петров"))
        lib.users[0].borrowed_books = ["1984"]
        
        lib.librarians.append(librarian("анна сергеевна"))
        
        print("начальные данные созданы")
    
    lib.main_menu()
    
    print("программа завершена")