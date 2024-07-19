#!/usr/bin/env python
# coding: utf-8
# Made by Noble Huang

from tkinter import *
from tkinter import messagebox

from QMul import *
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1)

window = Tk()
window.title('Quantum Calculator for Basic Operations')
window.geometry('500x500+175+80')
TextStyle = ('Arial', 16)

def calculate():
    try:
        inputEntryText = inputEntry.get()
        ExprParsed = parse_expr(inputEntryText, evaluate=False)
        ExprTree = sympy.srepr(ExprParsed)
        
        ExprTreeEval = eval(ExprTree)
        
        result['text'] = f"\n\nResult: {ExprTreeEval}\n\n"
        
    except:
        messagebox.showerror('Error: Invalid Expression!', format_exc())
            
instruction = Label(window, text='\n\nPlease input the expression below:')
inputEntry = Entry(window)

calculateBtn = Button(window, text='Calculate', command=calculate)
result = Label(window, text='\n\nResult goes here...\n\n')

widgets = [instruction, inputEntry, calculateBtn, result]

for widget in widgets:
    widget['font'] = TextStyle
    widget.pack()

window.bind('<Return>', lambda event: calculate())

window.mainloop()