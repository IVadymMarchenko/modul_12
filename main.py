from collections import UserDict
from datetime import datetime
import pickle

class Field:
    def __init__(self, value):
        self._value = value
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self,new_value):
        self._value=new_value

    def __str__(self):
        return str(self._value)


class Name(Field):

    def __init__(self, name):
        super().__init__(name)

    @property
    def value(self):
        return self._name

    @value.setter
    def value(self,new_value):
        self._name=new_value



class Phone(Field):

    def __init__(self, number):
        self.find_phone(number)
        super().__init__(number)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self.find_phone(new_value)

    def find_phone(self, phone):
        if len(phone) == 10 and phone.isdigit():
            self._value = phone
        else:
            raise ValueError("Invalid phone number format!!!!")


class Birthday:
    def __init__(self,year,month,day):
        self._value=self.valid_birthday(year, month, day)
    @property
    def value(self):
        return self._value
    @value.setter
    def value(self,new_value):
        year,month,day=map(int,new_value.split('-'))
        self.value=self.valid_birthday(year,month,day)

    def valid_birthday(self,year,month,day):
        try:
            return datetime(year,month,day)
        except ValueError:
            raise ValueError('Enter valid date')

    @property
    def year(self):
        return self._value.year

    @property
    def month(self):
        return self._value.month

    @property
    def day(self):
        return self._value.day


class Record(Field):

    def __init__(self, name,birthday=None):
        self.name = name
        self.phone = []
        self.birthday=birthday
        super().__init__(name)

    def add_phone(self,number):
        if number:
            num=Phone(number)
            self.phone.append(num)


    def remove_phone(self, phone):
        if phone in self.phone:
            self.phone.remove(phone)

    def edit_phone(self, phone_old, phone_new):
        for phone_obj in self.phone:
            if phone_obj.value == phone_old:
                phone_obj.find_phone(phone_new)
                break


    def find_phone(self, number):
        if number in self.phone:
            return Phone(number)

    def days_to_birthday(self):
        if self.birthday:
            now_data = datetime.now()
            old_data = datetime(year=self.birthday.year, month=self.birthday.month, day=self.birthday.day)
            if now_data.month <= old_data.month:
                days_before_birthday = old_data.replace(year=now_data.year)
                result = days_before_birthday - now_data
            else:
                days_before_birthday = old_data.replace(year=now_data.year + 1)
                result = days_before_birthday - now_data

            return f'{result.days} days before birthday {self.name}'
        return f'birthday is unknown'

    def __str__(self):
        phones_str = ', '.join(str(phone) for phone in self.phone)
        return f"Contact name: {self.name}, phones: {phones_str}"

class AddressBook(UserDict):
    index_iterator=0

    def add_record(self, record):
        name = record._value
        self.data[name] = record


    def find(self,name):
        if name in self.data.keys():
            return self.data[name]
        else:
            return None


    def delete(self,name):
        if name in self.data.keys():
            del self.data[name]
        else:
            return None

    def iterator(self, note):
        if note > len(self.data):
            note = len(self.data)
        index_iteration = 0
        list_data = list(self.data.items())
        while index_iteration < len(list_data):
            contacts = [f'{record}' for name, record in list_data[index_iteration:index_iteration + note]]
            yield  '\n'.join(contacts)
            index_iteration += note

    def save_to_file(self,file_name):
        with open(file_name, "wb") as file:
            pickle.dump(self.data, file)

    def read_from_file(self,file_name):
        with open(file_name, "rb") as file:
            self.data = pickle.load(file)
        return self.data
    def seach_contact(self,something):
        seach_list=[]
        for name,phone in self.data.items():
            if something.strip().lower() in name.strip().lower() or something.strip() in phone.strip().lower():
                seach_list.append(f'{name}: {phone}\n')
        if seach_list:
            return ''.join(seach_list)
        return None

class ConsoleInterface:
    def __init__(self, address_book):
        self.address_book = address_book

    def display_menu(self):
        print("1. (Add Contact)")
        print("2. Seach contact")
        print("3. Delete Contact")
        print("4. Display All Contacts")
        print("5. Save to file")
        print("6. read from file")
        print("7. Display part contacts")
        print('8. Days to birthday ')

    def add_contacts(self):
        name=input('Enter name: ')
        phone=input('Enter phone: ')
        record=Record(name)
        record.add_phone(phone)
        birthday =input('Enter birthday: ')
        if birthday:
            year, month, day=map(int,birthday.split('-'))
            record.birthday=Birthday(year,month,day)

        self.address_book.add_record(record)
        print('User add')

    def seach_contact(self):
        name_or_phone=input('Enter part name or phone')
        record=self.address_book.seach_contact(name_or_phone)
        if record:
            print(record)
        else:
            print('Contact is not found')

    def delete_contact(self):
        name=input('Enter name to delete: ')
        self.address_book.delete(name)
        print('Contact deleted')

    def display_all_contacts(self):
        for name, phone in self.address_book.items():
            print(f'{phone}')

    def save_to_file(self):
        file_name=input('Enter file name: ')
        self.address_book.save_to_file(file_name)
        print(f'contacts saved in {file_name}')

    def read_from_file(self):
        file_name=input('Enter file name: ')
        self.address_book.read_from_file(file_name)
        print(f'unpack from {file_name}')


    def display_part_contacts(self):
        note=int(input('Enter num'))
        if note > len(self.address_book):
            note = len(self.address_book)
        index_iteration = 0
        list_data = list(self.address_book.items())
        while index_iteration < len(list_data):
            contacts = [f'{record}' for name, record in list_data[index_iteration:index_iteration + note]]
            print('\n'.join(contacts))
            index_iteration += note


    def days_to_birthday(self):
        name=input('Enter name: ')
        if name in self.address_book.keys() and self.address_book[name].birthday:
            record = self.address_book[name]
            print(f"{record.days_to_birthday()}")
        else:
            print('None')

    def run_program(self):
        self.display_menu()
        while True:
            command=input('Enter the command: ')
            if command=='1':
                self.add_contacts()
            elif command=='2':
                self.seach_contact()
            elif command=='3':
                self.delete_contact()
            elif command=='4':
                self.display_all_contacts()
            elif command=='5':
                self.save_to_file()
            elif command=='6':
                self.read_from_file()
            elif command=='7':
                self.display_part_contacts()
            elif command=='8':
                self.days_to_birthday()
            else:
                print('Enter command from 1-8')
if __name__=='__main__':
    book=AddressBook()
    adres_book=ConsoleInterface(book)
    adres_book.run_program()















