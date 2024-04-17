from collections import UserDict
from datetime import datetime

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Phone number must be 10 digits")

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, number):
        self.phones.append(Phone(number))

    def remove_phone(self, number):
        updated_phones = []
        for phone in self.phones:
            if phone.value != number:
                updated_phones.append(phone)
        self.phones = updated_phones

    def edit_phone(self, old_number, new_number):
        if not any(phone.value == old_number for phone in self.phones):
            raise ValueError("Old phone number is not exist")    
        
        if len(new_number) != 10 or not new_number.isdigit():
            raise ValueError("New phone number must be 10 digits")
        
        for phone in self.phones:
            if phone.value == old_number:
                phone.value = new_number
                break

    def find_phone(self, number):
        for phone in self.phones:
            if phone.value == number:
                return phone
        return None
    
    def add_birthday(self, value):
        if self.birthday is None:
            self.birthday = Birthday(value)
        else:
            raise ValueError("Only one birthday is allowed per record.")

    def __str__(self):
        phones = "; ".join([phone.value for phone in self.phones])
        birthday_str = f", Birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones}{birthday_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
