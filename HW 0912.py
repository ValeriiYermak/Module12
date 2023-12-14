"""Реалізуйте метод __copy__ для класу Person.

Реалізуйте методи __copy__ та __deepcopy__ для класу Contacts."""

from copy import copy, deepcopy
import pickle


class Person:
    def __init__(self, name: str, email: str, phone: str, favorite: bool):
        self.name = name
        self.email = email
        self.phone = phone
        self.favorite = favorite

    def __copy__(self):
        copy_obj = Person(name=self.name, email=self.email, phone=self.phone,
                          favorite=self.favorite)
        return copy_obj


class Contacts:
    def __init__(self, filename: str, contacts: list[Person] = None):
        if contacts is None:
            contacts = []
        self.filename = filename
        self.contacts = contacts
        self.is_unpacking = False
        self.count_save = 0

    def save_to_file(self):
        with open(self.filename, "wb") as file:
            pickle.dump(self, file)

    def read_from_file(self):
        with open(self.filename, "rb") as file:
            content = pickle.load(file)
        return content

    def __getstate__(self):
        attributes = self.__dict__.copy()
        attributes["count_save"] = attributes["count_save"] + 1
        return attributes

    def __setstate__(self, value):
        self.__dict__ = value
        self.is_unpacking = True

    def __copy__(self):
        copy_obj = Contacts(filename=self.filename, contacts=self.contacts)
        copy_obj.is_unpacking = self.is_unpacking
        copy_obj.count_save = self.count_save
        return copy_obj

    def __deepcopy__(self, memo):
        copy_obj = Contacts(filename=self.filename,
                            contacts=deepcopy(self.contacts, memo))
        memo[id(copy_obj)] = copy_obj
        copy_obj.is_unpacking = copy(self.is_unpacking)
        copy_obj.count_save = copy(self.count_save)
        return copy_obj