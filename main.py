#!/usr/bin/python
# -*- coding: utf-8
 
#import mysql.connector
#from mysql.connector import Error

import pymysql
import create_table_db as mydb

def connect():
	"""Подключение к базе"""
	conn = None
	try:
		conn = pymysql.connect(
			host='localhost',
			database='test_DSJ',
			user='root',
			password='12345678')
		if conn:
			print('Подключились к базе')
	except Exception as e:
		print(f'Ошибка подключения к БД {e}')
	finally:
		#conn.close()
		#print('Подключение закрыто')
		pass
	return conn


def execute_read(connection, sql):
	'''функция принимает connection и SELECT-запрос, а возвращает выбранную запись'''
	cursor = connection.cursor()
	result = None
	try:
		cursor.execute(sql)
		result = cursor.fetchall()
		return result
	except Exception as e:
		print(f'Ошибка запроса {e}')


def work1(connection):
	'''Вывести для каждого продукта количество заявок, 
	поданных на нее за период с 1 янв 2014 до 31 декабря 2015 включительно'''
	sql = """
		SELECT ProductName AS Product, count(*) AS cnt
		FROM ProductRequest AS p
		INNER JOIN Product c ON p.ProductId  = c.ProductId 
		WHERE p.AppDate BETWEEN '2020-01-01' AND '2020-10-31'
		GROUP BY p.ProductId
	"""
	products = execute_read(connection, sql)
	for prod in products:
		print(f'{prod[1]} запросов продукта "{prod[0]}"')
		

def work2(connection):
	'''Вывести те продукты, на которые хотя бы раз за календарный месяц 
	в период с 1 янв 2014 по 31 декабря 2015 было подано заявок на сумму больше 10 000 000 руб.'''
	n = 1000000
	sql = f"""
		SELECT p.ProductName, SUM(pr.RequestedAmount) AS SumProduct, MONTH(pr.AppDate) AS month
    	FROM ProductRequest AS pr
    	INNER JOIN Product AS p ON p.ProductId = pr.ProductId 
    	WHERE pr.AppDate BETWEEN '2020-01-01' AND '2020-07-31'
    	GROUP BY month
    	HAVING SumProduct > {n}
	"""
	products = execute_read(connection, sql)
	print(f'продукты сумма которых в месяц больше {n}')
	for prod in products:
		print(f'У продукта "{prod[0]}" сумма = {prod[1]}')


def work3(connection):
	'''Вывести помесячный денежный поток для каждого продукта от кредитов, 
	выданных  с 1 по 30 августа 2015 года (клиент мог вносить в один месяц несколько платежей).'''
	sql = """
		SELECT Product.ProductName, SUM(Payments.PayAmount)
		FROM Payments, Debt, ProductRequest, Product
		WHERE
			Payments.DebtId = Debt.DebtId
		AND
			Debt.AppId = ProductRequest.AppID
		AND
			ProductRequest.ProductId = Product.ProductID
		AND 
			Payments.PayDate BETWEEN '2020-02-01' AND '2020-05-31'
		GROUP BY ProductRequest.ProductId, MONTH(Payments.PayDate)
	"""
	payments = execute_read(connection, sql)
	for pay in payments:
		print(f'Продукт "{pay[0]}", сумма платежей = {pay[1]}')


def work3_b(connection):
	'''Вывести помесячный денежный поток для каждого продукта от кредитов, 
	выданных  с 1 по 30 августа 2015 года (клиент мог вносить в один месяц несколько платежей).'''
	sql = """
		SELECT Product.ProductName, SUM(Payments.PayAmount), Debt.DebtAmount
		FROM Payments
		LEFT JOIN 
			Debt ON Payments.DebtId = Debt.DebtId
		LEFT JOIN 
			ProductRequest ON Debt.AppId = ProductRequest.AppID 
		LEFT JOIN 
			Product ON ProductRequest.ProductId = Product.ProductID
		WHERE 
			Payments.PayDate BETWEEN '2020-01-01' AND '2020-07-31'
		GROUP BY ProductRequest.ProductId, MONTH(Payments.PayDate)	
	"""
	payments = execute_read(connection, sql)
	for pay in payments:
		print(f'Продукт "{pay[0]}", сумма платежей = {pay[1]}, Сумма кредита={pay[2]}')



if __name__ == '__main__':
	conn = connect()
	with conn:
		# создание таблиц в бд
		#mydb.execute_tables(conn, mydb.tables)
		
		#добавление данных в таблицы
		#mydb.execute_sql(conn, mydb.create_Product)

		print('=' * 50)
		work1(conn)
		print('=' * 50)
		work2(conn)
		print('=' * 50)
		work3(conn)
		print('=' * 50)
		work3_b(conn)
