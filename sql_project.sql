CREATE DATABASE e_library;
USE e_library;
DROP DATABASE e_library;
SELECT DATABASE();


CREATE TABLE authors (

	author_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    author_name TEXT NOT NULL,
    author_surname TEXT NOT NULL

);


INSERT INTO authors (author_name, author_surname) VALUES ('Adrian', 'Skorżyński');
INSERT INTO authors (author_name, author_surname) VALUES ('Mateusz', 'Burkowski');
INSERT INTO authors (author_name, author_surname) VALUES ('Jarosław', 'Jagiej');
INSERT INTO authors (author_name, author_surname) VALUES ('Maria', 'Dakoń');
INSERT INTO authors (author_name, author_surname) VALUES ('Piotr', 'Polny');

DESCRIBE authors;
SELECT * FROM authors;
DROP TABLE authors;


CREATE TABLE books (

	book_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
	book_name TEXT NOT NULL,
    price_per_month_zl INT NOT NULL,
	book_author INT NOT NULL,
    FOREIGN KEY (book_author) REFERENCES authors(author_id)


);

INSERT INTO books (book_name, book_author, price_per_month_zl) VALUES ("Płomienne Serca",5,5);
INSERT INTO books (book_name, book_author, price_per_month_zl) VALUES ("Zamieć",1,6);
INSERT INTO books (book_name, book_author, price_per_month_zl) VALUES ("Pożeracz Dusz",4,7);
INSERT INTO books (book_name, book_author, price_per_month_zl) VALUES ("Ulica 57",3,8);
INSERT INTO books (book_name, book_author, price_per_month_zl) VALUES ("Droga",2,4);
INSERT INTO books (book_name, book_author, price_per_month_zl) VALUES ("Historia Powszechna",2,5);
INSERT INTO books (book_name, book_author, price_per_month_zl) VALUES ("Ognisty Wir",2,10);
INSERT INTO books (book_name, book_author, price_per_month_zl) VALUES ("Mglisty Cel",5,5);
INSERT INTO books (book_name, book_author, price_per_month_zl) VALUES ("Jałowy Trud",4,7);

DESCRIBE books;
SELECT * FROM books;
DROP TABLE books;

SELECT * FROM books JOIN authors ON books.book_author = author_id;

CREATE TABLE patrons (

	patron_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    patron_name TEXT NOT NULL,
    patron_surname TEXT NOT NULL

);


INSERT INTO patrons (patron_name, patron_surname) VALUES ('Marek','Górski');
INSERT INTO patrons (patron_name, patron_surname) VALUES ('Karolina','Kerń');
INSERT INTO patrons (patron_name, patron_surname) VALUES ('Waldemar','Dorosz');
INSERT INTO patrons (patron_name, patron_surname) VALUES ('Jakub','Dereń');
INSERT INTO patrons (patron_name, patron_surname) VALUES ('Magdalena','Opolska');
INSERT INTO patrons (patron_name, patron_surname) VALUES ('Robert','Miesz');
INSERT INTO patrons (patron_name, patron_surname) VALUES ('Konrad','Barkos');
INSERT INTO patrons (patron_name, patron_surname) VALUES ('Julia','Markowska');
INSERT INTO patrons (patron_name, patron_surname) VALUES ('Ewa','Lechter');
INSERT INTO patrons (patron_name, patron_surname) VALUES ('Zygmunt','Chościej');

DESCRIBE patrons;
SELECT * FROM patrons;
DROP TABLE patrons;

CREATE TABLE transactions (

	transaction_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    number_of_months INT NOT NULL,
    action_actor INT NOT NULL,
    action_object INT NOT NULL,
    transaction_date DATE NOT NULL,
    FOREIGN KEY (action_actor) REFERENCES patrons(patron_id),
    FOREIGN KEY (action_object) REFERENCES books(book_id)


);

INSERT INTO transactions (number_of_months, action_actor, action_object, transaction_date) VALUES (2,3,2,'2018-05-10');
INSERT INTO transactions (number_of_months, action_actor, action_object, transaction_date) VALUES (1,3,1,'2018-07-23');
INSERT INTO transactions (number_of_months, action_actor, action_object, transaction_date) VALUES (2,6,5,'2018-08-15');
INSERT INTO transactions (number_of_months, action_actor, action_object, transaction_date) VALUES (3,5,4,'2018-11-02');
INSERT INTO transactions (number_of_months, action_actor, action_object, transaction_date) VALUES (2,1,2,'2018-02-12');
INSERT INTO transactions (number_of_months, action_actor, action_object, transaction_date) VALUES (1,7,3,'2018-07-16');
INSERT INTO transactions (number_of_months, action_actor, action_object, transaction_date) VALUES (1,4,5,'2018-09-26');
INSERT INTO transactions (number_of_months, action_actor, action_object, transaction_date) VALUES (3,2,5,'2018-04-17');
INSERT INTO transactions (number_of_months, action_actor, action_object, transaction_date) VALUES (2,1,3,'2018-06-10');
INSERT INTO transactions (number_of_months, action_actor, action_object, transaction_date) VALUES (1,3,9,'2018-07-03');
INSERT INTO transactions (number_of_months, action_actor, action_object, transaction_date) VALUES (3,7,8,'2018-10-12');
INSERT INTO transactions (number_of_months, action_actor, action_object, transaction_date) VALUES (1,6,4,'2018-03-12');
INSERT INTO transactions (number_of_months, action_actor, action_object, transaction_date) VALUES (2,5,7,'2018-12-12');
INSERT INTO transactions (number_of_months, action_actor, action_object, transaction_date) VALUES (1,10,3,'2018-05-26');
INSERT INTO transactions (number_of_months, action_actor, action_object, transaction_date) VALUES (2,3,5,'2018-03-21');
INSERT INTO transactions (number_of_months, action_actor, action_object, transaction_date) VALUES (3,2,9,'2018-01-17');

DROP TABLE transactions;
SELECT * FROM transactions ORDER BY transaction_date DESC;

CREATE VIEW v_transactions AS SELECT transaction_id, number_of_months, transaction_date, patron_id, patron_name, patron_surname, book_id, book_name, CONCAT(price_per_month_zl, ' ', 'zł') AS cena, CONCAT(price_per_month_zl * number_of_months,' ','zł') AS total_cost FROM transactions JOIN patrons ON transactions.action_actor = patrons.patron_id JOIN books ON transactions.action_object = books.book_id JOIN authors ON books.book_author = authors.author_id;
DROP VIEW transakcje;
SELECT * FROM v_transactions;
SELECT * FROM v_transactions ORDER BY transaction_date DESC;
SELECT * FROM v_transactions WHERE patron_id = 5 ORDER BY transaction_date DESC;
SELECT * FROM v_transactions WHERE book_id = 3 ORDER BY transaction_date DESC;

SELECT patron_id, patron_name, patron_surname, CONCAT(CAST(SUM(price_per_month_zl * number_of_months) AS CHAR), ' zł') AS total_spent, COUNT(transaction_id) AS books_rented FROM transactions JOIN patrons ON transactions.action_actor = patrons.patron_id JOIN books ON transactions.action_object = books.book_id JOIN authors ON books.book_author = authors.author_id GROUP BY patron_id ORDER BY total_spent DESC;
CREATE VIEW v_patrons AS SELECT patron_id, patron_name, patron_surname, SUM(CONCAT(price_per_month_zl * number_of_months,' ','zł')) AS total_spent, COUNT(transaction_id) AS books_rented FROM transactions JOIN patrons ON transactions.action_actor = patrons.patron_id JOIN books ON transactions.action_object = books.book_id JOIN authors ON books.book_author = authors.author_id GROUP BY patron_id;
DROP VIEW v_patrons;
SELECT * FROM v_patrons;
SELECT * FROM v_patrons ORDER BY books_rented DESC;
SELECT * FROM v_patrons ORDER BY total_spent DESC;


CREATE VIEW sales_info AS SELECT book_id, book_name, author_id, author_name, author_surname, SUM(CONCAT(price_per_month_zl * number_of_months,' ','zł')) AS total_profit, COUNT(book_id) AS times_lended, SUM(number_of_months) AS total_months_lended FROM transactions JOIN patrons ON transactions.action_actor = patrons.patron_id JOIN books ON transactions.action_object = books.book_id JOIN authors ON books.book_author = authors.author_id GROUP BY book_name;
SELECT * FROM sales_info ORDER BY total_profit DESC;
DROP VIEW sales_info;

CREATE VIEW author_sales AS SELECT author_id, author_name, author_surname, SUM(CONCAT(price_per_month_zl * number_of_months,' ','zł')) AS total_profit FROM transactions JOIN patrons ON transactions.action_actor = patrons.patron_id JOIN books ON transactions.action_object = books.book_id JOIN authors ON books.book_author = authors.author_id GROUP BY author_id;
DROP VIEW author_sales;
SELECT * FROM author_sales ORDER BY total_profit DESC;

CREATE TABLE logging_data (

	id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    login TEXT NOT NULL,
    passwd TEXT NOT NULL,
    access TEXT NOT NULL
);

DROP TABLE logging_data;

DESCRIBE logging_data;

INSERT INTO logging_data (login, passwd, access) VALUES ('admin1', 'apass1', 'admin');
INSERT INTO logging_data (login, passwd, access) VALUES ('admin2', 'apass2', 'admin');
INSERT INTO logging_data (login, passwd, access) VALUES ('user1', 'pass1', 'user');
INSERT INTO logging_data (login, passwd, access) VALUES ('user2', 'pass2', 'user');
INSERT INTO logging_data (login, passwd, access) VALUES ('user3', 'pass3', 'user');


create view v_books as SELECT book_name, CONCAT(CAST(price_per_month_zl AS CHAR), ' zł') AS price_per_month, author_name, author_surname FROM books JOIN authors ON books.book_author = author_id;
select * from v_books;
