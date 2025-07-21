import tkinter as tk
from tkinter import scrolledtext, Toplevel

class Calculator:
    def __init__(self):
        self.history_file = "history.txt"
        self.confirm_history_file()

    def confirm_history_file(self):
        try:
            with open(self.history_file, 'r'):
                pass
        except FileNotFoundError:
            with open(self.history_file, 'w') as file:
                file.write("")

    def calculate(self, expression):
        try:
            result = eval(expression)
            self.save_to_history(expression, result)
            return result
        except ZeroDivisionError:
            return "Error: Div by 0"
        except Exception:
            return "Error"

    def save_to_history(self, expression, result):
        try:
            with open(self.history_file, "a") as file:
                file.write(f"{expression} = {result}\n")
        except Exception as e:
            print("Failed to save history:", e)

    def get_history(self):
        try:
            with open(self.history_file, "r") as file:
                return file.read()
        except Exception as e:
            return "Error reading history"

    def clear_history(self):
        try:
            with open(self.history_file, "w") as file:
                file.write("")
        except Exception as e:
            print("Failed to clear history:", e)


class CalculatorApp:
    def __init__(self, root):
        self.calc = Calculator()
        root.title("Colorful Calculator")
        root.geometry("350x500")  # Height increased for buttons visibility
        root.resizable(False, False)
        root.configure(bg="#2C2C2C")

        self.input = tk.StringVar()
        self.entry = tk.Entry(root, textvariable=self.input, font=("Arial", 20),
                              width=18, bd=5, relief="ridge", bg="#1F1F1F",
                              fg="white", insertbackground="white", justify="right")
        self.entry.grid(row=0, column=0, columnspan=4, padx=10, pady=15)
        self.entry.focus_set()

        self.create_buttons(root)

        # History and Clear History buttons
        history_btn = tk.Button(root, text="Show History", width=14, height=2,
                                font=("Arial", 12), command=self.show_history_window,
                                bg="#007ACC", fg="white", activebackground="#005F99")
        history_btn.grid(row=6, column=0, columnspan=2, pady=5, padx=10)

        clear_history_btn = tk.Button(root, text="Clear History", width=14, height=2,
                                      font=("Arial", 12), command=self.clear_history,
                                      bg="#CC3300", fg="white", activebackground="#A62800")
        clear_history_btn.grid(row=6, column=2, columnspan=2, pady=5, padx=10)

        # Bind Enter and Escape keys only
        root.bind("<Return>", lambda event: self.on_click('='))
        root.bind("<Escape>", lambda event: self.on_click('C'))

    def create_buttons(self, root):
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3),
            ('C', 5, 0)
        ]
        operator_color = "#FF8800"
        number_color = "#3A3A3A"
        for (text, row, col) in buttons:
            if text in '+-*/=':
                bg_color = operator_color
            elif text == 'C':
                bg_color = "#AA0000"
            else:
                bg_color = number_color

            button = tk.Button(root, text=text, width=5, height=2, font=("Arial", 14, "bold"),
                               bg=bg_color, fg="white", activebackground="#666666",
                               relief="raised", bd=3,
                               command=lambda t=text: self.on_click(t))
            button.grid(row=row, column=col, padx=5, pady=5)

    def on_click(self, char):
        if char == '=':
            expr = self.input.get()
            result = self.calc.calculate(expr)
            self.input.set(result)
        elif char == 'C':
            self.input.set("")
        else:
            self.input.set(self.input.get() + char)

    def show_history_window(self):
        try:
            history_win = Toplevel()
            history_win.title("Calculation History")
            history_win.geometry("320x300")
            history_win.configure(bg="#2C2C2C")
            history_win.resizable(False, False)

            history_box = scrolledtext.ScrolledText(history_win, width=38, height=15,
                                                    font=("Consolas", 11), bg="#1F1F1F", fg="white")
            history_box.pack(padx=10, pady=10)
            history_box.insert(tk.END, self.calc.get_history())
            history_box.config(state="disabled")
        except Exception as e:
            print("Failed to show history window:", e)

    def clear_history(self):
        self.calc.clear_history()


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
