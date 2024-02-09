import pickle
import pickle as pk
from enum import Enum
from tkinter import messagebox


class Result(Enum):
    Ok = 0
    Err = 1


class SortCategory(Enum):
    Payment = 0,
    Alphabetical = 1,
    Random = 2,


class SortMode(Enum):
    MostPaying = 0,
    LeastPaying = 1,

    AlphabeticalUp = 2,
    AlphabeticalDown = 3,

    Random = 4


class Data:
    goal: float = 4500.0
    people: dict[str, float] = {}

    @staticmethod
    def get_sum() -> float:
        out: float = 0
        for paid in Data.people.values():
            out += paid
        return out

    @staticmethod
    def make_payment(name: str, amount: float) -> Result:
        if name in Data.people.keys():
            Data.people[name] += amount
            return Result.Ok
        else:
            print(f"{name} not in dataset!")
            messagebox.showerror("Data Error", f"{name} not in dataset!")
            return Result.Err

    @staticmethod
    def set_payment(name: str, total_amount: float) -> Result:
        if name in Data.people.keys():
            Data.people[name] = total_amount
            return Result.Ok
        else:
            print(f"{name} not in dataset!")
            messagebox.showerror("Data Error", f"{name} not in dataset!")
            return Result.Err

    @staticmethod
    def add_person(name: str, start_amount: float = 0) -> Result:
        if name not in Data.people.keys():
            Data.people[name] = start_amount
            return Result.Ok
        else:
            print(f"{name} already in dataset!")
            messagebox.showerror("Data Error", f"{name} already in dataset!")
            return Result.Err

    @staticmethod
    def remove_person(name: str) -> Result:
        if name in Data.people.keys():
            Data.people.pop(name)
            return Result.Ok
        else:
            print(f"{name} not in dataset!")
            messagebox.showerror("Data Error", f"{name} not in dataset!")
            return Result.Err

    @staticmethod
    def save():
        with open('data.pickle', 'wb') as handle:
            pk.dump(Data.people, handle, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load():
        with open('data.pickle', 'rb') as handle:
            Data.people = pk.load(handle)
