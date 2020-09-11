import csv
import requests
import re

class ContactBook:

    contacts = {}

    class Contact:
        def __init__(self, fullname, organization, position, phone, email):
            self.lastname, self.firstname, self.surname = '', '', ''
            self.organization, self.position = None, None
            self.phone, self.email = None, None

            result = re.findall('\w+', fullname)
            if len(result) >= 1:
                self.lastname = result[0]
            if len(result) >= 2:
                self.firstname = result[1]
            if len(result) > 2:
                self.surname = result[2]

            self.organization, self.position = organization, position

            self.phone = ContactBook.PhoneNumber(phone)
            self.email = email

        def __str__(self):
            return f"{self.lastname}, {self.firstname}, {self.surname}, {self.organization}, {self.position}, {self.phone}, {self.email}"

        def __repr__(self):
            return str(self)

        def __iter__(self):
            attr_list =[self.lastname, self.firstname, self.surname, self.organization, self.position, self.phone, self.email]
            return attr_list.__iter__()

    class PhoneNumber:
        def __init__(self, number):
            number = str(number).strip()
            number = re.sub('[-()\s]', '', number)
            number = re.sub('^8', '+7', number)
            self.country_code, self.city_code, self.add_number = '', '', ''
            self.abonent_number = number

            if re.match('\+7', number):
                # russian number
                self.country_code = '+7'
                self.city_code = number[2:5]
                self.abonent_number = f'{number[5:8]}-{number[8:10]}-{number[10:12]}'

            res = re.search('доб.', number)
            if res:
                self.add_number = number[res.end():]

        def __str__(self):
            if len(self.abonent_number) == 0:
                return ''

            phone_repr = f'{self.country_code}({self.city_code}){self.abonent_number}'
            if self.add_number:
                phone_repr = f'{phone_repr} доб.{self.add_number}'
            return phone_repr

        def __repr__(self):
            return str(self)

    @classmethod
    def create_contact(cls, fullname, organisation='', position='', phone='', email=''):

        search_key = (fullname.strip(), organisation.strip())
        result = cls.contacts.get(search_key)
        if result is not None:
            return result

        contact = ContactBook.Contact(fullname, organisation, position, phone, email)
        cls.contacts[search_key] = contact
        return contact

    @classmethod
    def serialize(cls, filename):
        with open(filename, "w", encoding='utf8', newline='') as f:
            datawriter = csv.writer(f, delimiter=',')
            # Вместо contacts_list подставьте свой список
            contact_list = list(cls.contacts.values())
            datawriter.writerows(contact_list)

    @classmethod
    def load_data_from_url(cls, url):
        response = requests.get(url)
        data_iter = response.iter_lines(decode_unicode=True)
        next(data_iter)  # пропуск заголовков
        for line in data_iter:
            contact_data = list(line.split(sep=','))
            fullname = f'{contact_data[0]} {contact_data[1]} {contact_data[2]}'
            ContactBook.create_contact(fullname, organisation=contact_data[3], position=contact_data[4],
                                       phone=contact_data[5], email=contact_data[6])


URL = 'https://raw.githubusercontent.com/netology-code/py-homeworks-advanced/master/5.Regexp/phonebook_raw.csv'
ContactBook.load_data_from_url(URL)
ContactBook.serialize("phonebook.csv")