import pymysql

class DBConnect:

    def __init__(self):

        try:
            self.conn = pymysql.connect('localhost', 'root', 'password', 'e_library')
            print('Połączenie ustanowione.')
            self.logowanie()

        except:
            print("Podano błędne dane.")

    def logowanie(self):

        login = input("Podaj login")
        password = input("Podaj hasło")

        self.cursor = self.conn.cursor()

        self.cursor.execute("SELECT * from logging_data WHERE login=%s and passwd= %s", (login, password))
        resultsLogs = self.cursor.fetchall()

        if (len(resultsLogs) == 1) and resultsLogs[0][3] == 'admin':
            print("zalogowany w systemie jako administrator")
            self.menu_admin()

        elif (len(resultsLogs) == 1):
            print("zalogowany w systemie")
            self.menu_user()

        else:
            print("niepoprawny login lub haslo")
            self.logowanie()

    def menu_admin(self):

        while (True):
            dec = input("Menu admina: V= Wyświetl dane, I-=Wprowadź nowe dane, U=Zaktualizuj, D= Usuń Q-wyjdź").upper()

            if (dec == "V"):
                self.select_menu_admin()
            elif (dec == "I"):
                self.menu_insert()

            elif (dec == "D"):
                self.menu_delete()

            elif (dec == "Q"):
                break

            elif (dec == "U"):
                self.menu_update()

    def select_menu_admin(self):
        while (True):
            dec = input("Menu podglądu: T= Transakcje, C= Klienci, S= Sprzedaż A= Autorzy, Q- Wyjdz,").upper()

            if (dec == "C"):
                self.patrons()

            if (dec == "T"):
                self.transactions()

            if (dec == "S"):
                self.sales()

            if (dec == "A"):
                self.authors()

            elif (dec == "Q"):
                break

    def transactions(self):
        self.cursor.execute("SELECT * FROM v_transactions ORDER BY transaction_date DESC")
        t = self.cursor.fetchall()

        for row in t:
            TRANSACTION_ID    = 0
            NUMBER_OF_MONTHS  = 1
            TRANSACTION_DATE  = 2
            PATRON_ID         = 3
            PATRON_NAME       = 4
            PATRON_SURNAME    = 5
            BOOK_ID           = 6
            BOOK_NAME         = 7
            PRICE             = 8
            TOTAL_COST        = 9

            print(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])

    def patrons(self):
        self.cursor.execute("SELECT * FROM v_patrons ORDER BY total_spent DESC")
        t = self.cursor.fetchall()

        for row in t:
            PATRON_ID         = 0
            PATRON_NAME       = 1
            PATRON_SURNAME    = 2
            TOTAL_SPENT       = 3
            BOOKS_RENTED      = 4

            print(row[0], row[1], row[2], row[3], row[4])

    def sales(self):
        self.cursor.execute("SELECT * FROM sales_info ORDER BY total_profit DESC")
        t = self.cursor.fetchall()

        for row in t:
            BOOK_ID             = 0
            BOOK_NAME           = 1
            AUTHOR_ID           = 2
            AUTHOR_NAME         = 3
            AUTHOR_SURNAME      = 4
            TOTAL_PROFIT        = 5
            TIMES_LENDED        = 6
            TOTAL_MONTHS_LENDED = 7

            print(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])

    def authors(self):
        self.cursor.execute("SELECT * FROM author_sales ORDER BY total_profit DESC")
        t = self.cursor.fetchall()

        for row in t:
            AUTHOR_ID         = 0
            AUTHOR_NAME       = 1
            AUTHOR_SURNAME    = 2
            TOTAL_PROFIT      = 3

            print(row[0], row[1], row[2], row[3])


    def menu_insert(self):
        while (True):
            dec = input("Menu wprowadzania nowych danych: A= Autorzy, T= Transakcje, P= Klienci, B= Książki, Q= Wyjście ").upper()

            if (dec == "A"):
                self.i_authors()

            if (dec == "B"):
                self.i_books()

            if (dec == "P"):
                self.i_patrons()

            if (dec == "T"):
                self.i_transactions()

            if (dec == "Q"):
                break



    def i_authors(self):

        imie = input("imie")
        nazwisko = input('nazwisko')

        self.cursor.execute("INSERT INTO authors (author_name, author_surname) VALUES (%s, %s)", (imie, nazwisko))
        self.conn.commit()

    def i_books(self):

        tytul = input("tytuł")
        autor = input("autor")
        cena_za_miesiac = input("cena za miesiąc")

        self.cursor.execute("INSERT INTO books (book_name, book_author, price_per_month_zl) VALUES (%s, %i, %i)", (tytul, autor, cena_za_miesiac))
        self.conn.commit()

    def i_patrons(self):

        imie = input("imie")
        nazwisko = input('nazwisko')

        self.cursor.execute("INSERT INTO patrons (patron_name, patron_surname) VALUES (%s, %s)", (imie, nazwisko))
        self.conn.commit()

    def i_transactions(self):

        ilosc_miesiecy = input("ilość miesięcy")
        osoba = input("osoba")
        obiekt = input("obiekt")
        data = input("data")

        self.cursor.execute("INSERT INTO transactions (number_of_months, action_actor, action_object, transaction_date) VALUES (%i, %i, %i, %s)", (ilosc_miesiecy, osoba, obiekt, data))
        self.conn.commit()




    def menu_update(self):
        while (True):
            dec = input("Menu aktualizacji danych: A= Autorzy, T= Transakcje, P= Klienci, B= Książki, Q= Wyjście ").upper()

            if (dec == "A"):
                self.u_authors()

            if (dec == "B"):
                self.u_books()

            if (dec == "P"):
                self.u_patrons()

            if (dec == "T"):
                self.u_transactions()

            if (dec == "Q"):
                break

    def u_authors(self):

        self.cursor.execute("SELECT * FROM authors")
        t = self.cursor.fetchall()

        for row in t:
            AUTHOR_ID         = 0
            AUTHOR_NAME       = 1
            AUTHOR_SURNAME    = 2

            print(row[0], row[1], row[2])

        kolumna = input("Podaj kolumnę:")
        nowa = input("Podaj nową wartość:")
        nowaBuild = "'%s'" % nowa
        id = input("Podaj id:")
        print(nowaBuild)
        query = "UPDATE authors SET %s = %s where author_id = %s" % (kolumna, nowaBuild, id)
        print(query)
        self.cursor.execute(query)

        dec = input("Czy na pewno chcesz wykonac update? T/N").upper()

        if (dec == "T"):
            self.conn.commit()
            print("Wykonano update")

        else:
            self.conn.rollback()

    def u_books(self):

        self.cursor.execute("SELECT * FROM books")
        t = self.cursor.fetchall()

        for row in t:
            BOOK_ID         = 0
            BOOK_NAME       = 1
            PRICE_PER_MONTH = 2
            BOOK_AUTHOR     = 3

            print(row[0], row[1], row[2], row[3])

        kolumna = input("Podaj kolumnę:")
        nowa = input("Podaj nową wartość:")
        nowaBuild = "'%s'" % nowa
        id = input("Podaj id:")
        print(nowaBuild)
        query = "UPDATE books SET %s = %s where book_id = %s" % (kolumna, nowaBuild, id)
        print(query)
        self.cursor.execute(query)

        dec = input("Czy na pewno chcesz wykonac update? T/N").upper()

        if (dec == "T"):
            self.conn.commit()
            print("Wykonano update")

        else:
            self.conn.rollback()

    def u_patrons(self):

        self.cursor.execute("SELECT * FROM patrons")
        t = self.cursor.fetchall()

        for row in t:
            PATRON_ID = 0
            PATRON_NAME = 1
            PATRON_SURNAME = 2

            print(row[0], row[1], row[2])

        kolumna = input("Podaj kolumnę:")
        nowa = input("Podaj nową wartość:")
        nowaBuild = "'%s'" % nowa
        id = input("Podaj id:")
        print(nowaBuild)
        query = "UPDATE patrons SET %s = %s where patron_id = %s" % (kolumna, nowaBuild, id)
        print(query)
        self.cursor.execute(query)

        dec = input("Czy na pewno chcesz wykonac update? T/N").upper()

        if (dec == "T"):
            self.conn.commit()
            print("Wykonano update")

        else:
            self.conn.rollback()

    def u_transactions(self):

        self.cursor.execute("SELECT * FROM transactions")
        t = self.cursor.fetchall()

        for row in t:
            TRANSACTION_ID = 0
            NUMBER_OF_MONTHS = 1
            ACTION_ACTOR = 2
            ACTION_OBJECT = 3
            TRANSACTION_DATE = 4

            print(row[0], row[1], row[2], row[3], row[4])

        kolumna = input("Podaj kolumnę:")
        nowa = input("Podaj nową wartość:")
        nowaBuild = "'%s'" % nowa
        id = input("Podaj id:")
        print(nowaBuild)
        query = "UPDATE transactions SET %s = %s where transaction_id = %s" % (kolumna, nowaBuild, id)
        print(query)
        self.cursor.execute(query)

        dec = input("Czy na pewno chcesz wykonac update? T/N").upper()

        if (dec == "T"):
            self.conn.commit()
            print("Wykonano update")

        else:
            self.conn.rollback()


    def menu_delete(self):
        while(True):
            dec = input("Menu usuwania danych: A= Autorzy, B= Books, P= Klienci, T= transakcje, Q= Wyjście").upper()

            if (dec == "A"):
                self.d_authors()

            if (dec == "B"):
                self.d_books()

            if (dec =="P"):
                self.d_patrons()

            if (dec =="T"):
                self.d_transactions()

            if (dec == "Q"):
                break

    def d_authors(self):

        self.cursor.execute("SELECT * FROM authors")
        t = self.cursor.fetchall()

        for row in t:
            AUTHOR_ID         = 0
            AUTHOR_NAME       = 1
            AUTHOR_SURNAME    = 2

            print(row[0], row[1], row[2])

        id = input("id")
        self.cursor.execute("DELETE FROM authors WHERE author_id = %s", id)

        dec = input("Czy na pewno chcesz usunac rekord T/N").upper()

        if (dec == "T"):
            self.conn.commit()
            print("usunieto rekord")

        else:
            self.conn.rollback()

    def d_books(self):

        self.cursor.execute("SELECT * FROM books")
        t = self.cursor.fetchall()

        for row in t:
            BOOK_ID         = 0
            BOOK_NAME       = 1
            PRICE_PER_MONTH = 2
            BOOK_AUTHOR     = 3

            print(row[0], row[1], row[2], row[3])

        id = input("id")
        self.cursor.execute("DELETE FROM books WHERE book_id = %s", id)

        dec = input("Czy na pewno chcesz usunac rekord T/N").upper()

        if (dec == "T"):
            self.conn.commit()
            print("usunieto rekord")

        else:
            self.conn.rollback()

    def d_transactions(self):

        self.cursor.execute("SELECT * FROM transactions")
        t = self.cursor.fetchall()

        for row in t:
            TRANSACTION_ID = 0
            NUMBER_OF_MONTHS = 1
            ACTION_ACTOR = 2
            ACTION_OBJECT = 3
            TRANSACTION_DATE = 4

            print(row[0], row[1], row[2], row[3], row[4])

        id = input("id")
        self.cursor.execute("DELETE FROM transactions WHERE transaction_id = %s", id)

        dec = input("Czy na pewno chcesz usunac rekord T/N").upper()

        if (dec == "T"):
            self.conn.commit()
            print("usunieto rekord")

        else:
            self.conn.rollback()

    def d_patrons(self):

        self.cursor.execute("SELECT * FROM patrons")
        t = self.cursor.fetchall()

        for row in t:
            PATRON_ID = 0
            PATRON_NAME = 1
            PATRON_SURNAME = 2

            print(row[0], row[1], row[2])

        id = input("id")
        self.cursor.execute("DELETE FROM patrons WHERE patron_id = %s", id)

        dec = input("Czy na pewno chcesz usunac rekord T/N").upper()

        if (dec == "T"):
            self.conn.commit()
            print("usunieto rekord")

        else:
            self.conn.rollback()


    def menu_user(self):

        while (True):
            dec = input("K= Wyświetl książki, B= Bestsellery, A= Top Autorzy Q-wyjdz").upper()

            if (dec == "K"):
                self.v_books()
            elif (dec == "B"):
                self.v_sales()

            elif (dec == "A"):
                self.v_authors()

            elif (dec == "Q"):
                break



    def v_books(self):
        self.cursor.execute("select * from v_books")
        authors = self.cursor.fetchall()

        for row in authors:
            BOOK_NAME        = 0
            PRICE_PER_MONTH  = 1
            AUTHOR_NAME      = 2
            AUTHOR_SURNAAME  = 3

            print(row[0], row[1], row[2], row[3])

    def v_sales(self):
        self.cursor.execute("SELECT * FROM sales_info ORDER BY total_profit DESC")
        authors = self.cursor.fetchall()

        for row in authors:
            BOOK_NAME           = 1
            AUTHOR_NAME         = 3
            AUTHOR_SURNAME      = 4

            print(row[1], row[3], row[4])

    def v_authors(self):
        self.cursor.execute("SELECT * FROM author_sales ORDER BY total_profit DESC")
        authors = self.cursor.fetchall()

        for row in authors:
            AUTHOR_NAME       = 1
            AUTHOR_SURNAME    = 2

            print(row[1], row[2])

DBConnect()