#!/usr/bin/env python
# coding: utf-8
# Made by Noble Huang

import os
import sys
import ctypes
import threading

from tkinter import *
import tkinter.scrolledtext as st

from PIL import Image, ImageTk

from sympy.parsing.sympy_parser import parse_expr

from QIntegral import *
from QuIntegral_icons import imageDict

ctypes.windll.shcore.SetProcessDpiAwareness(1)

def evaluate(event):
    # After 1 ms call "evaluate"
    # in order to make sure that tkinter has handled the keyboard press
    editText(IntEqnsText, 'Calculating...')
    window.after(1, evaluateRaw)

def editText(textbox, content=''):
    textbox['state'] = 'normal'
    textbox.delete('1.0', 'end')
    textbox.insert('end', content)
    textbox['state'] = 'disabled'

def evaluateRaw():
    try:
        EqnsList1 = EqnsText.get(1.0, 'end').replace('^', '**').split('\n')
        EqnsList2 = [sympy.parsing.sympy_parser.parse_expr(el1) for el1 in EqnsList1 if el1 != '']
        EqnsList3 = [sympy.Add.make_args(el2) for el2 in EqnsList2]
        # print('QCalc', 34, EqnsList3)
        EqnsList4 = [QIntegrals(el3, window) for el3 in EqnsList3]
        # print('QCalc', 36, EqnsList4)
        EqnsList5 = [[el4Expr.as_coeff_exponent(extractVarFromExpr(el4Expr)[0])+(extractVarFromExpr(el4Expr)[0],) for el4Expr in el4] for el4 in EqnsList4]; ErrMsgText.insert('end', str(EqnsList5))
        EqnsList6 = [[sympy.Mul(sympy.UnevaluatedExpr(el5Expr[0]), sympy.UnevaluatedExpr(sympy.Pow(el5Expr[2], el5Expr[1]))) for el5Expr in el5] for el5 in EqnsList5]
        EqnsList7 = [str(sum(el6)+sympy.UnevaluatedExpr(sympy.Symbol('C'))) for el6 in EqnsList6]
        
        result = '\n\n'.join(EqnsList7)
        
        editText(ErrMsgText)
        editText(IntEqnsText, result.replace('**', '^'))
    
    except:
        editText(IntEqnsText, 'Error!')
        editText(ErrMsgText, format_exc())

window = Tk()

icon = ImageTk.PhotoImage(image=imageDict['QuIntegral-Icon-Small'] , master=window )
window.iconphoto(True, icon)

window.title('QuIntegral')  # title of the GUI window
window.geometry('1010x960+175+20')  # specify the max size the window can expand to
window.resizable(False, False)
window.config(bg='white')  # specify background color

# Create left and right frames
left_frame = Frame(window, width=200, height=400, bg='grey')
left_frame.grid(row=0, column=0, padx=10, pady=5)

right_frame = Frame(window, width=650, height=400, bg='grey')
right_frame.grid(row=0, column=1, padx=10, pady=5)

warning = Label(window, text='Note: This QuIntegral calculator currently only supports polynomial equations.\nAny other types of equations, such as trigonometric and exponential functions will only generate errors or unexpected, inaccurate results.\nMoreover, if you want to type 2x^3, you must type it 2*x^3, instead of 2x^3, which will generate error in the meantime.\nI will continue to tackle this problem along with other problems due to still under development.', bg='white')
warning.grid(row=1, column=0, padx=10, pady=5, columnspan=2)

bottom_frame = Frame(window, width=650, height=400, bg='grey')
bottom_frame.grid(row=2, column=0, padx=10, pady=5, columnspan=2)

# Create title for Original Equations
Label(left_frame, text='Equations:', font=('Arial', 20)).grid(row=0, column=0, padx=5, pady=5)

# Textbox for Original Equations in left_frame
EqnsText = st.ScrolledText(left_frame, width=30, height=10, font=('Arial', 16))
EqnsText.grid(row=2, column=0, padx=5, pady=5)

# Create title for Integrated Equations
Label(right_frame, text='Integrated Equations:', font=('Arial', 20)).grid(row=0, column=1, padx=5, pady=5)

# Textbox for Integrated Equations in right_frame
IntEqnsText = st.ScrolledText(right_frame, width=30, height=10, font=('Arial', 16))
IntEqnsText['state'] = 'disabled'
IntEqnsText.grid(row=2, column=1, padx=5, pady=5)

# Create title for Error Message Display
Label(bottom_frame, text='Error Message Display (in case there are errors)', font=('Arial', 20)).grid(row=0, column=0, padx=5, pady=5, columnspan=2)

# Textbox for Display Error Messages in right_frame
ErrMsgText = st.ScrolledText(bottom_frame, width=100, height=20, font=('Arial', 10))
ErrMsgText['state'] = 'disabled'
ErrMsgText.grid(row=2, column=0, padx=10, pady=5, columnspan=2)

# Create Key Event so when EqnsText is given input, IntEqnsText is already updated
EqnsText.bind('<Key>', evaluate)

if getattr(sys, 'frozen', False):
    window.mainloop()
