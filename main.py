from collections import UserDict

class FieldIsEmpty(Exception):

    def __init__(self, message = 'Field is empty') -> None:
        self.message = message
        super().__init__(self.message)

class PhoneError(Exception):

    def __init__(self, message = 'Phone error') -> None:
        self.message = message
        super().__init__(self.message)

class RecordAlreadyExist(Exception):

    def __init__(self, message = 'Record already exist') -> None:
        self.message = message
        super().__init__(self.message)

class RecordIsNotExist(Exception):

    def __init__(self, message = 'Record is not exist') -> None:
        self.message = message
        super().__init__(self.message)

class Field:

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):

    def __init__(self, value):
        name = str(value).strip()
        if len(name) > 0:
            self.name = name
            super().__init__(self.name)
        else:
            raise FieldIsEmpty('Name is empty')

    def get_name(self):
        return self.name

class Phone(Field):

    def __init__(self, value):
        phone = str(value).strip()
        if len(phone) == 10:
            self.phone = phone
            super().__init__(self.phone)
        else:
            raise PhoneError('Phone number must contain ten digits')

    def __eq__(self, __value: object) -> bool:
        return self.phone == __value.phone

class Record:

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone_str):

        phone = Phone(phone_str)
        try:
            self.phones.index(phone)
        except:
            self.phones.append(phone)

    def find_phone(self, phone_str):

        phone = Phone(phone_str)
        try:
            return self.phones[self.phones.index(phone)]
        except:
            return None

    def delete_phone(self, phone_str):

        phone = Phone(phone_str)
        try:
            self.phones.pop(self.phones.index(phone))
        except:
            raise RecordIsNotExist(f'Phone {phone} is not exist')

    def edit_phone(self, phone_str, new_phone_str):

        phone     = Phone(phone_str)
        new_phone = Phone(new_phone_str)

        try:
            self.phones[self.phones.index(phone)] = new_phone
        except:
            raise RecordIsNotExist(f'Phone {phone} is not exist')

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    
    def add_record(self, record):

        if self.data.get(record.name.name) is None:
            self.data[record.name.name] = record
        else:
            raise RecordAlreadyExist

    def find(self, name):

        record = self.data.get(name)
        if record is None:
            raise RecordIsNotExist
        else:
            return record

    def delete(self, name):

        record = self.data.get(name)
        if record is None:
            raise RecordIsNotExist
        else:
            self.data.pop(name)

if __name__ == '__main__':

	# Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")

    # Видалення телефону у записі John
    john.delete_phone("5555555555")
    
    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)
