import tkinter as tk
import tkinter.ttk as ttk

import config

window_frame = tk.Tk | tk.Frame | tk.Toplevel


class Component:
    def __init__(self, root: window_frame, size: tuple[int, int] | None):
        self.root = root
        self.size = size
        self.component = None


class ProgressBar(Component):
    def __init__(self, root: window_frame, max_val: float):
        super().__init__(root, None)
        self.val = 0
        self.max_val = max_val
        self.pct = self.val / self.max_val * 100
        self.component = ttk.Progressbar(
            self.root, orient=tk.VERTICAL, length=250, mode="determinate")
        self.component["value"] = self.pct

        # Styling
        self.color = config.current_theme.red
        if 33 < self.pct <= 66:
            self.color = config.current_theme.yellow
        elif self.pct > 66:
            self.color = config.current_theme.green

        self.style = ttk.Style()
        self.style.theme_use('winnative')
        self.style.configure("1.Vertical.TProgressbar",
                             troughcolor=config.current_theme.surface1,
                             background=self.color,
                             borderwidth=0)
        self.component.configure(style="1.Vertical.TProgressbar")

    def set_value(self, val: float):
        self.val = val
        self.pct = self.val / self.max_val * 100
        self.component["value"] = self.pct

        self.color = config.current_theme.red
        if 33 < self.pct <= 66:
            self.color = config.current_theme.yellow
        elif self.pct > 66:
            self.color = config.current_theme.green

        self.style.configure("1.Vertical.TProgressbar",
                             background=self.color)


class Text(Component):
    def __init__(self, root: window_frame, text: str | None = None, textvar: tk.StringVar | None = None):
        super().__init__(root, None)
        self.textvar = textvar
        if self.textvar is None:
            self.textvar = tk.StringVar()
            self.textvar.set(text)
        else:
            self.textvar = textvar
        self.component = tk.Label(
            self.root, textvariable=self.textvar)

        # Styling
        self.component.configure(bg=config.current_theme.base,
                                 fg=config.current_theme.text,
                                 borderwidth=0)


class Button(Component):
    def __init__(self, root: window_frame, text: str, size: tuple[int, int] | None = None,
                 command=None,
                 is_active=True):
        super().__init__(root, size)
        self.text = text
        self.is_active = tk.ACTIVE if is_active else tk.DISABLED
        self.component = tk.Button(
            self.root, command=command, state=self.is_active, text=self.text)

        # Styling
        self.component.configure(bg=config.current_theme.surface1,
                                 fg=config.current_theme.text,
                                 activebackground=config.current_theme.surface2,
                                 activeforeground=config.current_theme.subtext1,
                                 borderwidth=0)
        if self.size is not None:
            self.component.configure(width=size[0], height=size[1])


class Input(Component):
    def __init__(self, root: window_frame, size: tuple[int, int] | None = None):
        super().__init__(root, size)
        self.buffer = tk.StringVar()
        self.component = tk.Entry(root, textvariable=self.buffer)
        self.component.configure(bg=config.current_theme.overlay1, fg=config.current_theme.mantle, borderwidth=0)

    def get_buffer(self) -> str:
        return self.buffer.get()

    def delete_buffer(self):
        self.component.delete(0, tk.END)


class PersonEntry(Component):
    def __init__(self, root: window_frame, name: str, paid: float, size: tuple[int, int], edit_mode: bool = False,
                 edit_func=None):
        super().__init__(root, size)

        self.editmode = edit_mode

        self.name = name

        self.paid_var = tk.StringVar()
        self.paid_var.set(f"{paid} kr")

        self.component = tk.Frame(self.root, width=self.size[0], height=self.size[1])
        self.component.propagate(False)
        self.component.configure(bg=config.current_theme.overlay1)

        self.name_text = Text(self.component, text=self.name)
        self.name_text.component.configure(bg=config.current_theme.overlay1, fg=config.current_theme.mantle)
        self.name_text.component.pack(padx=25, side=tk.LEFT)
        self.paid_text = Text(self.component, textvar=self.paid_var)

        if self.editmode:
            self.remove_btn = Button(self.component, "x", command=lambda: edit_func(self))
            self.remove_btn.component.configure(bg=config.current_theme.overlay1, fg=config.current_theme.red,
                                                activebackground=config.current_theme.overlay1,
                                                activeforeground=config.current_theme.red)
            self.remove_btn.component.pack(padx=5, side=tk.RIGHT)

        self.paid_text.component.configure(bg=config.current_theme.overlay1, fg=config.current_theme.mantle)
        self.paid_text.component.pack(padx=25, side=tk.RIGHT)
