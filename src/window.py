import tkinter as tk
from tkinter import messagebox
import random

import components
import config
from data import Data, Result, SortMode, SortCategory


class MainWindow:
    def __init__(self, size: tuple[int, int]):
        self.root = tk.Tk()
        self.root.title("Fodboldtur")
        self.root.minsize(size[0], size[1])
        self.root.maxsize(size[0], size[1])
        self.root.configure(bg=config.current_theme.base)

        # SortMode
        self.sort_mode = SortMode.AlphabeticalDown

        # Container
        self.people_container = tk.Frame(self.root, bg=config.current_theme.surface1, width=200, height=300)
        self.people_container.propagate(False)
        self.people_container.grid(row=1, column=0, rowspan=4, sticky=tk.W, padx=20, pady=2)

        self.sort_buttons_frame = tk.Frame(self.people_container, width=200, bg=config.current_theme.surface1)

        self.sort_paying_btn = components.Button(self.sort_buttons_frame, "$",
                                                 command=lambda: self.toggle_sort_mode(SortCategory.Payment))
        self.sort_paying_btn.component.grid(row=0, column=0, padx=20)
        self.sort_alpha_btn = components.Button(self.sort_buttons_frame, "A ↓",
                                                command=lambda: self.toggle_sort_mode(SortCategory.Alphabetical))
        self.sort_alpha_btn.component.grid(row=0, column=1, padx=20)

        self.sort_random_btn = components.Button(self.sort_buttons_frame, "R",
                                                 command=lambda: self.toggle_sort_mode(SortCategory.Random))
        self.sort_random_btn.component.grid(row=0, column=2, padx=20)
        self.sort_buttons_frame.pack()

        self.people: list[components.PersonEntry] = []
        for (i, name) in enumerate(Data.people.keys()):
            val = Data.people[name]
            self.people.append(components.PersonEntry(self.people_container, name, val, (200, 20)))
            self.people[i].component.pack(pady=5)

        # Progress bar
        self.progress_bar_text = tk.StringVar()
        self.progress_bar_text.set(f"{Data.get_sum()} kr af {Data.goal} kr")
        self.progress_bar_label = components.Text(self.root, textvar=self.progress_bar_text)
        self.progress_bar_label.component.grid(row=0, column=1, sticky=tk.W, pady=2)

        self.progress_bar = components.ProgressBar(self.root, Data.goal)
        self.progress_bar.set_value(Data.get_sum())
        self.progress_bar.component.grid(row=1, column=1, rowspan=3, sticky=tk.W, padx=20, pady=2)

        # Buttons
        self.edit_btn = components.Button(self.root, "Edit people", command=lambda: EditWindow(self))
        self.edit_btn.component.grid(row=1, column=2, sticky=tk.E, pady=2)

        self.add_payment_btn = components.Button(self.root, "Add Payment",
                                                 command=lambda: AddPaymentWindow(self))
        self.add_payment_btn.component.grid(row=2, column=2, sticky=tk.E, pady=2)

        self.lowest_btn = components.Button(self.root, "View lowest payers", command=lambda: LeastPayingWindow(self))
        self.lowest_btn.component.grid(row=3, column=2, sticky=tk.E, pady=2)

        self.save_btn = components.Button(self.root, "Save Data", command=Data.save)
        self.save_btn.component.grid(row=4, column=2, sticky=tk.E, pady=2)

        self.root.mainloop()

    def toggle_sort_mode(self, category: SortCategory):
        pay_btn_text = "$"
        alpha_btn_text = "A"
        match category:
            case SortCategory.Payment:
                if self.sort_mode == SortMode.MostPaying:
                    self.sort_mode = SortMode.LeastPaying
                    pay_btn_text = "$ ↓"

                elif self.sort_mode == SortMode.LeastPaying:
                    self.sort_mode = SortMode.MostPaying
                    pay_btn_text = "$ ↑"

                else:
                    self.sort_mode = SortMode.MostPaying
                    pay_btn_text = "$ ↑"

            case SortCategory.Alphabetical:
                if self.sort_mode == SortMode.AlphabeticalUp:
                    self.sort_mode = SortMode.AlphabeticalDown
                    alpha_btn_text = "A ↓"

                elif self.sort_mode == SortMode.AlphabeticalDown:
                    self.sort_mode = SortMode.AlphabeticalUp
                    alpha_btn_text = "A ↑"

                else:
                    self.sort_mode = SortMode.AlphabeticalUp
                    alpha_btn_text = "A ↑"

            case SortCategory.Random:
                self.sort_mode = SortMode.Random

        self.sort_paying_btn.component.configure(text=pay_btn_text)
        self.sort_alpha_btn.component.configure(text=alpha_btn_text)
        self._sorted_data = Data.people.copy()
        match self.sort_mode:
            case SortMode.MostPaying:
                self._sorted_data = dict(
                    sorted(self._sorted_data.items(), key=lambda item: item[1]))
            case SortMode.LeastPaying:
                temp = sorted(self._sorted_data.items(), key=lambda item: item[1])
                temp.reverse()
                self._sorted_data = dict(temp)

            case SortMode.AlphabeticalUp:
                self._sorted_data = dict(sorted(self._sorted_data.items()))
            case SortMode.AlphabeticalDown:
                temp = sorted(self._sorted_data.items())
                temp.reverse()
                self._sorted_data = dict(temp)

            case SortMode.Random:
                temp = sorted(self._sorted_data.items())
                random.shuffle(temp)
                self._sorted_data = dict(temp)

        self.update_people(data=self._sorted_data)

    def update_paid_value(self):
        self.progress_bar_text.set(f"{Data.get_sum()} kr af {Data.goal} kr")
        self.progress_bar.set_value(Data.get_sum())
        for person in self.people:
            person.paid_var.set(f"{Data.people[person.name]} kr")

    def update_people(self, data: dict[str, float] | None = None):
        for person in self.people:
            person.component.pack_forget()
        self.people.clear()

        data = Data.people if data is None else data

        for (i, name) in enumerate(data.keys()):
            val = Data.people[name]
            self.people.append(components.PersonEntry(self.people_container, name, val, (200, 20)))
            self.people[i].component.pack(pady=5)


class SubWindow:
    def __init__(self, master: MainWindow, title: str, size: tuple[int, int]):
        self.master = master
        self.title = title
        self.window = tk.Toplevel(self.master.root)
        self.window.minsize(size[0], size[1])
        self.window.maxsize(size[0], size[1])
        self.window.title(title)
        self.window.configure(bg=config.current_theme.base)


class FormPopUp(SubWindow):
    def __init__(self, master: MainWindow, title: str, on_confirm=None):
        super().__init__(master, title, (250, 150))

        self.on_confirm = on_confirm

        self.name_field_text = components.Text(self.window, text="Name:")
        self.name_field_text.component.pack(pady=5)

        self.name_field = components.Input(self.window)
        self.name_field.component.pack(pady=5)

        self.value_field_text = components.Text(self.window, text="DKK:")
        self.value_field_text.component.pack(pady=5)

        self.value_field = components.Input(self.window)
        self.value_field.component.pack(pady=5)

        self.submit_btn = components.Button(self.window, "Submit", command=self.submit)
        self.submit_btn.component.configure(bg=config.current_theme.green, fg=config.current_theme.mantle)
        self.submit_btn.component.pack(pady=5)

    def submit(self):
        name = self.name_field.get_buffer()
        value_str = self.value_field.get_buffer()

        if len(name) == 0 or len(value_str) == 0:
            print("Missing fields")
            messagebox.showerror("Input Error", "Missing Fields")
            return

        try:
            global value
            value = float(value_str)
        except:
            print(f"{self.value_field.get_buffer()} is not a number!")
            messagebox.showerror("Input Error", f"{self.value_field.get_buffer()} is not a number!")
            self.value_field.delete_buffer()
            return

        if self.on_confirm(name, value) == Result.Err:
            self.value_field.delete_buffer()
            self.name_field.delete_buffer()
            return

        self.window.destroy()


class EditWindow(SubWindow):
    def __init__(self, master: MainWindow):
        super().__init__(master, "Edit people", (400, 350))
        self.new_data = Data.people.copy()

        self.add_btn = components.Button(self.window, "Add", size=(25, 1),
                                         command=lambda: FormPopUp(self.master, "Add Person",
                                                                   on_confirm=self.add_person))
        self.add_btn.component.configure(bg=config.current_theme.accent, fg=config.current_theme.mantle,
                                         activebackground=config.current_theme.overlay1)
        self.add_btn.component.pack(pady=25)

        self.people_container = tk.Frame(self.window, bg=config.current_theme.surface1, width=250, height=300)
        self.people_container.pack(pady=10)

        self.people: list[components.PersonEntry] = []
        for (i, name) in enumerate(Data.people.keys()):
            val = Data.people[name]
            self.people.append(components.PersonEntry(self.people_container, name, val, (250, 20), edit_mode=True,
                                                      edit_func=self.delete_person))
            self.people[i].component.pack(pady=5)

        self.confirm_btn = components.Button(self.window, "Confirm", size=(25, 1), command=self.confirm)
        self.confirm_btn.component.configure(bg=config.current_theme.green, fg=config.current_theme.mantle)
        self.confirm_btn.component.pack(pady=25)

    def add_person(self, name: str, initial_payment: float) -> Result:
        if name in self.new_data.keys():
            messagebox.showerror("ERROR", f"{name} is already in dataset!")
            print(f"{name} is already in dataset!")
            return Result.Err

        self.new_data[name] = initial_payment
        self.people.append(
            components.PersonEntry(self.people_container, name, initial_payment, (250, 20), edit_mode=True,
                                   edit_func=self.delete_person))
        self.people[len(self.people) - 1].component.pack(pady=5)
        return Result.Ok

    def delete_person(self, person: components.PersonEntry):
        person.component.pack_forget()
        self.new_data.pop(person.name)
        self.people.remove(person)

    def confirm(self):
        Data.people = self.new_data
        self.master.update_people()
        self.master.update_paid_value()
        self.window.destroy()


class AddPaymentWindow:
    def __init__(self, master: MainWindow):
        self.master = master
        FormPopUp(self.master, "Add Payment", on_confirm=self.submit_payment)

    def submit_payment(self, name: str, value: float) -> Result:
        if Data.make_payment(name, value) == Result.Ok:
            self.master.update_paid_value()
            return Result.Ok

        return Result.Err


class LeastPayingWindow(SubWindow):
    def __init__(self, master: MainWindow):
        super().__init__(master, "Least paying people", (400, 150))
        self.people_container = tk.Frame(self.window, bg=config.current_theme.surface1, width=250, height=300)
        self.people_container.pack(pady=10)

        self.people: list[components.PersonEntry] = []
        new_data = sorted(Data.people.items(), key=lambda x: x[1])
        for (i, person) in enumerate(new_data[:3]):
            self.people.append(components.PersonEntry(self.people_container, person[0], person[1], (250, 20)))
            self.people[i].component.pack(pady=5)
