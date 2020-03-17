#!/usr/bin/python
# -*- coding: utf-8

if __name__ == '__main__':
    print('-_-')
else:

    def execute_sql(connection, sql):
        # функция вставляет данные из sql строки к подключенной базе connection
        cursor = connection.cursor()
        try:
            cursor.execute(sql)
            connection.commit()
            print('Запрос выполнен')
        except Exception as e:
            print(f'Ошибка {e}')


    def execute_tables(connection, tables):
        # итерации по словарю с таблицами, вызов функции вставки данных для создания таблиц
        for table_name in tables:
            sql_table = tables[table_name]
            print(f'Создание таблицы: {table_name}')
            execute_sql(connection, sql_table)
        print(f'Создано {len(tables)} таблиц')


    tables = {}  # словарь таблиц

    #заявок ProductRequest (AppID, ProductId, AppDate, RequestedAmount) 
    tables['ProductRequest'] = """
        CREATE TABLE IF NOT EXISTS ProductRequest (
            AppID INT AUTO_INCREMENT, 
            ProductId INT NOT NULL, 
            AppDate DATE NOT NULL, 
            RequestedAmount INT, 
            PRIMARY KEY (AppID)
        ) ENGINE = InnoDB
    """

    #продуктов Product (ProductID, ProductName)
    tables['Product'] = """
        CREATE TABLE IF NOT EXISTS Product (
            ProductID INT AUTO_INCREMENT, 
            ProductName TEXT NOT NULL, 
            PRIMARY KEY (ProductID)
        ) ENGINE = InnoDB
    """

    #кредитов Debt (DebtId, AppId, DebtDate, DebtAmount)
    tables['Debt'] = """
        CREATE TABLE IF NOT EXISTS Debt (
            DebtId INT AUTO_INCREMENT, 
            AppId INT NOT NULL, 
            DebtDate DATE NOT NULL, 
            DebtAmount INT NOT NULL, 
            PRIMARY KEY (DebtId)
        ) ENGINE = InnoDB
    """

    #платежей Payments (PayId, PayDate, PayAmount)
    tables['Payments'] = """
        CREATE TABLE IF NOT EXISTS Payments (
            PayId INT AUTO_INCREMENT, 
            DebtId INT NOT NULL, 
            PayDate DATE NOT NULL, 
            PayAmount INT NOT NULL, 
            PRIMARY KEY (PayId)
        ) ENGINE = InnoDB
    """