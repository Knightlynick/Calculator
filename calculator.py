import tkinter as tk
import csv
from datetime import datetime

class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Order of Operations Calculator")
        
        # This string holds the current expression
        self.expression = ""
        
        # Create the display field
        self.display = tk.Entry(master, font=("Arial", 20), bd=10, relief=tk.RIDGE, justify="right")
        self.display.grid(row=0, column=0, columnspan=4, pady=10)
        
        # Create buttons with grid layout
        # Row 1: Parentheses, Clear, Division
        self.create_button("(", 1, 0)
        self.create_button(")", 1, 1)
        self.create_button("C", 1, 2)
        self.create_button("/", 1, 3)
        
        # Row 2: 7, 8, 9, Multiplication
        self.create_button("7", 2, 0)
        self.create_button("8", 2, 1)
        self.create_button("9", 2, 2)
        self.create_button("x", 2, 3)
        
        # Row 3: 4, 5, 6, Subtraction
        self.create_button("4", 3, 0)
        self.create_button("5", 3, 1)
        self.create_button("6", 3, 2)
        self.create_button("-", 3, 3)
        
        # Row 4: 1, 2, 3, Addition
        self.create_button("1", 4, 0)
        self.create_button("2", 4, 1)
        self.create_button("3", 4, 2)
        self.create_button("+", 4, 3)
        
        # Row 5: 0, Decimal, Equals (spanning two columns)
        self.create_button("0", 5, 0)
        self.create_button(".", 5, 1)
        self.create_button("=", 5, 2, columnspan=2)
    
    def create_button(self, value, row, column, columnspan=1):
        """Helper to create a button and place it on the grid."""
        btn = tk.Button(self.master, text=value, font=("Arial", 20), bd=5, relief=tk.RIDGE,
                        command=lambda: self.button_press(value))
        btn.grid(row=row, column=column, columnspan=columnspan, sticky="nsew", padx=5, pady=5)
        # Ensure grid cells expand proportionately
        self.master.grid_rowconfigure(row, weight=1)
        self.master.grid_columnconfigure(column, weight=1)
    
    def button_press(self, value):
        """Processes button presses: appends digits/operators or triggers evaluation/clearing."""
        if value == "C":
            self.clear()
        elif value == "=":
            self.calculate()
        else:
            self.expression += value
            self.update_display(self.expression)
            self.log_keypress(value)
    
    def update_display(self, text):
        """Updates the calculator display field."""
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, text)
    
    def clear(self):
        """Clears the current expression and updates the display."""
        self.expression = ""
        self.update_display("")
        self.log_keypress("C")
    
    def calculate(self):
        """Evaluates the expression, respecting operator precedence and brackets."""
        # Replace 'x' with '*' for multiplication
        expression_to_eval = self.expression.replace("x", "*")
        try:
            result = eval(expression_to_eval)
            self.update_display(result)
            # Store the result as the new expression to allow for chaining calculations
            self.expression = str(result)
        except Exception:
            self.update_display("Error")
            self.expression = ""
        self.log_keypress("=")
    
    def log_keypress(self, key):
        """Logs each key press with a timestamp to a CSV file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        with open("calculator_log.csv", "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([timestamp, key])

if __name__ == "__main__":
    root = tk.Tk()
    calc = Calculator(root)
    root.mainloop()