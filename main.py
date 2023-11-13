import pickle

class AdressBook:
    data={}

    def __init__(self,file_name):
        self.file_name=file_name

    def add_contact(self,name,phone):
        AdressBook.data[name]=phone


    def save_to_file(self):
        with open(self.file_name, "wb") as file:
            pickle.dump(AdressBook.data, file)

    def read_from_file(self):
        with open(self.file_name, "rb") as file:
            AdressBook.data = pickle.load(file)
        return AdressBook.data

    def seach_contact(self,something):
        seach_list=[]
        for name,phone in AdressBook.data.items():
            if something.strip().lower() in name.strip().lower() or something.strip() in phone.strip().lower():
                seach_list.append(f'{name}: {phone}\n')
        if seach_list:
            return ''.join(seach_list)
        return None

















