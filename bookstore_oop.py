import sqlite3
class BookStoreApp:
    def main(self):
        database = Database()
        print("===== ГЛАВНОЕ МЕНЮ =====")
        while True:
            choice = input("Выберете действие:\n1 - Показать все книги\n2 - Поиск книг по стране\n3 - Поиск книг по диапазону цен\n4 - Статистика по странам авторов книг\n5 - Изменение цены по ID\n0 - Выход\n")
            if choice == "1":
                pass
            elif choice == "2":
                find_books_by_country(connection)
            elif choice == "3":
                find_books_by_price_range(connection)
            elif choice == "4":
                show_country_stats(connection)
            elif choice == "5":
                update_book_price(connection)
            elif choice == "0":
                print("До свидания!")
                connection.close()
                break
            else:
                print("ШТА?")

class BookStore:
    def __init__(self, database):
        self.database = database

    def show_all_books(self):
        cursor = self.database.connection.cursor()
        cursor.execute("SELECT * FROM books")
        for row in cursor.fetchall():
            print(f"ID: {row['id']}, Название: {row['title']}, Автор: {row['author']}, Год: {row['year']}, Цена: {row['price']}")

    def find_books_by_country(self):
        country = input("Введите страну автора: ")
        cursor = self.database.connection.cursor()
        cursor.execute("""
            SELECT b.id, b.title, b.author, b.year, b.price
            FROM books b
            JOIN author_info a ON b.author = a.author
            WHERE a.country = ?
        """, (country,))
        results = cursor.fetchall()
        if results:
            for row in results:
                print(f"ID: {row['id']}, Название: {row['title']}, Автор: {row['author']}, Год: {row['year']}, Цена: {row['price']}")
        else:
            print(f"Книги авторов из страны '{country}' не найдены.")

    def find_books_by_price_range(self):
        try:
            min_price = float(input("Введите минимальную цену: "))
            max_price = float(input("Введите максимальную цену: "))
        except ValueError:
            print("Ошибка! Введите корректные числовые значения для цен.")
            return
        if min_price > max_price:
            print("Ошибка ! Минимальная цена должна быть меньше максимальной.")
            return
        if min_price == max_price:
            print("Ага... ищем фиксированный прайс ёпта!...\n")
        cursor = self.database.connection.cursor()
        cursor.execute('''
            SELECT * FROM books WHERE price BETWEEN ? AND ?
            ORDER BY price ASC
        ''', (min_price, max_price))
        results = cursor.fetchall()
        if results:
            for row in results:
                print(f"ID: {row['id']}, Название: {row['title']}, Автор: {row['author']}, Год: {row['year']}, Цена: {row['price']}")
        else:
            print(f"Книги в ценовом диапазоне от {min_price} до {max_price} не найдены.")

    def show_country_stats(self):
        cursor = self.database.connection.cursor()
        cursor.execute('''
        SELECT COUNT(b.author) AS book_count, a.country, AVG(b.price) AS avg_price
        FROM books b INNER JOIN author_info a ON b.author = a.author
        GROUP BY a.country
        ''')
        results = cursor.fetchall()
        if results:
            print("Статистика по странам авторов книг:")
            for row in results:
                print(f"Страна {row['country']}: {row['book_count']} книги")
                if row['avg_price'] is None:
                    print("Средняя цена книги: Нет данных")
                else:
                    print(f"Средняя цена книги: {row['avg_price']:.2f}")
            print("Такая вот херня\n")
        else:
            print("Нет данных о странах авторов книг.")

    def update_book_price(self):
        cursor = self.database.connection.cursor()
        try:
            book_id = int(input("Введите ID книги, чью цену хотите изменить: "))
            new_price = float(input("Введите новую цену книги: "))
            if book_id < 1 or new_price < 0:
                return False
        except ValueError:
            return False
        cursor.execute('''UPDATE books SET price = ? WHERE id = ?''', (new_price, book_id))
        if cursor.rowcount == 0:
            return False
        self.database.connection.commit()
        return True


class Database:
    def __init__(self):
        self.connection = sqlite3.connect("bookstore_oop.db")
        self.connection.row_factory = sqlite3.Row
    def close(self):
        self.connection.close()
