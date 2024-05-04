#Модель данных в файле
class FinancialRecord:
    def __init__(self, date, category, amount, description):
        self.date = date
        self.category = category
        self.amount = amount
        self.description = description

#Чтение/Запись
class DataHandler:
    def __init__(self, file_name):
        self.file_name = file_name

    def read_data(self):
        records = []
        try:
            with open(self.file_name, 'r') as file:
                lines = file.readlines()
                record_info = {}
                for line in lines:
                    line = line.strip()
                    if line:
                        key, value = line.split(': ')
                        record_info[key] = value
                    else:
                        records.append(FinancialRecord(**record_info))
                        record_info = {}
                # Добавляем последнюю запись
                if record_info:
                    records.append(FinancialRecord(**record_info))
        except FileNotFoundError:
            # Если файл не найден, возвращаем пустой список записей
            return []
        return records

    def write_data(self, data):
        with open(self.file_name, 'w') as file:
            for record in data:
                file.write(f"Дата: {record.date}\n")
                file.write(f"Категория: {record.category}\n")
                file.write(f"Сумма: {record.amount}\n")
                file.write(f"Описание: {record.description}\n")
                file.write("\n")

# Операции над данными
class FinancialManager:
    def __init__(self, data_handler):
        self.data_handler = data_handler
        self.records = self.data_handler.read_data()

    def add_record(self, record):
        self.records.append(record)
        self.data_handler.write_data(self.records)

    def edit_record(self, index, record):
        if 0 <= index < len(self.records):
            self.records[index] = record
            self.data_handler.write_data(self.records)
        else:
            print("Некорректный индекс")

    def search_records(self, criteria):
        results = []
        for record in self.records:
            if criteria.lower() in record.date.lower() or \
                    criteria.lower() in record.category.lower() or \
                    criteria.lower() in record.description.lower() or \
                    criteria.lower() in str(record.amount):
                results.append(record)
        return results

    def display_balance(self):
        total_income = sum(record.amount for record in self.records if record.category == 'Доход')
        total_expense = sum(record.amount for record in self.records if record.category == 'Расход')
        balance = total_income - total_expense
        print(f"Текущий баланс: {balance}")
        print(f"Сумма доходов: {total_income}")
        print(f"Сумма расходов: {total_expense}")


def print_menu():
    print("1. Вывести баланс")
    print("2. Добавить запись")
    print("3. Редактировать запись")
    print("4. Поиск записей")
    print("5. Выйти")


if __name__ == "__main__":
    file_name = "financial_records.txt"
    data_handler = DataHandler(file_name)
    manager = FinancialManager(data_handler)

    while True:
        print_menu()
        choice = input("Выберите действие: ")

        if choice == "1":
            manager.display_balance()
        elif choice == "2":
            date = input("Введите дату: ")
            category = input("Введите категорию (Доход/Расход): ")
            amount = float(input("Введите сумму: "))
            description = input("Введите описание: ")
            new_record = FinancialRecord(date, category, amount, description)
            manager.add_record(new_record)
        elif choice == "3":
            index = int(input("Введите индекс записи для редактирования: "))
            date = input("Введите новую дату: ")
            category = input("Введите новую категорию (Доход/Расход): ")
            amount = float(input("Введите новую сумму: "))
            description = input("Введите новое описание: ")
            manager.edit_record(index, FinancialRecord(date, category, amount, description))
        elif choice == "4":
            criteria = input("Введите критерий для поиска: ")
            search_results = manager.search_records(criteria)
            for i, record in enumerate(search_results):
                print(
                    f"Индекс: {i}, Дата: {record.date}, Категория: {record.category}, Сумма: {record.amount}, Описание: {record.description}")
        elif choice == "5":
            break
        else:
            print("Некорректный выбор. Попробуйте еще раз.")
