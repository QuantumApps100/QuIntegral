#!/usr/bin/env python
# coding: utf-8
# Made by Noble Huang

# import sys
# sys.path += [r'C:\Users\mulia\Documents\Others\Sci and Tech\C&R\MyPython\Projects\QProjects\QuTable']
from QBasicOperation import *

import matplotlib.pyplot as plt
import os
import sys
import math as m
import numpy as np
import pandas as pd
import sympy

from fractions import Fraction

from _functools import *
from traceback import format_exc

from QAdd import *

# import sys
# sys.path += [r'C:\Users\mulia\Documents\Others\Sci and Tech\C&R\MyPython\Projects\QProjects\QuTable']
# import QBasicOperation as QBO

Integer = int
Float = lambda num, precision: float(num)

QAdd = sum
# QMul_w_QAdd = multiplier

del sum
    
def QMul_w_QAdd1(*factors):
    return reduce(QMul_w_QAdd, list(factors))
    
Add = QAdd1
Mul = QMul_w_QAdd1

parse_expr = sympy.parsing.sympy_parser.parse_expr

def QExp(a, b):
    return reduce(QMul_w_QAdd, [a]*b) if b else 1

# Create a dictionary that allows faster multiplication due to memorizations of multiplications from 0 x 0 to 9 x 9
mulDict = {(0, 0): 0, (0, 1): 0, (0, 2): 0, (0, 3): 0, (0, 4): 0, (0, 5): 0, (0, 6): 0, (0, 7): 0, (0, 8): 0, (0, 9): 0, (1, 0): 0, (1, 1): 1, (1, 2): 2, (1, 3): 3, (1, 4): 4, (1, 5): 5, (1, 6): 6, (1, 7): 7, (1, 8): 8, (1, 9): 9, (2, 0): 0, (2, 1): 2, (2, 2): 4, (2, 3): 6, (2, 4): 8, (2, 5): 10, (2, 6): 12, (2, 7): 14, (2, 8): 16, (2, 9): 18, (3, 0): 0, (3, 1): 3, (3, 2): 6, (3, 3): 9, (3, 4): 12, (3, 5): 15, (3, 6): 18, (3, 7): 21, (3, 8): 24, (3, 9): 27, (4, 0): 0, (4, 1): 4, (4, 2): 8, (4, 3): 12, (4, 4): 16, (4, 5): 20, (4, 6): 24, (4, 7): 28, (4, 8): 32, (4, 9): 36, (5, 0): 0, (5, 1): 5, (5, 2): 10, (5, 3): 15, (5, 4): 20, (5, 5): 25, (5, 6): 30, (5, 7): 35, (5, 8): 40, (5, 9): 45, (6, 0): 0, (6, 1): 6, (6, 2): 12, (6, 3): 18, (6, 4): 24, (6, 5): 30, (6, 6): 36, (6, 7): 42, (6, 8): 48, (6, 9): 54, (7, 0): 0, (7, 1): 7, (7, 2): 14, (7, 3): 21, (7, 4): 28, (7, 5): 35, (7, 6): 42, (7, 7): 49, (7, 8): 56, (7, 9): 63, (8, 0): 0, (8, 1): 8, (8, 2): 16, (8, 3): 24, (8, 4): 32, (8, 5): 40, (8, 6): 48, (8, 7): 56, (8, 8): 64, (8, 9): 72, (9, 0): 0, (9, 1): 9, (9, 2): 18, (9, 3): 27, (9, 4): 36, (9, 5): 45, (9, 6): 54, (9, 7): 63, (9, 8): 72, (9, 9): 81}

def afmtsd(the_list_original, chara, ndigits):
    '''afmtsd stands for "Add for making the same digits"
    This function can add some letters or numbers to the front for various purposes, including sorting purposes. For example, if one desires to sort an array ['00011', '100'], making '100' (3 digits) to become '00100' (5 digits) can make use of this function by calling afmtsd('100', '0', 5).'''
    
    the_list = list(the_list_original)
    a = [chara]*(ndigits-len(the_list)) + the_list
    
    if type(the_list_original) == type(''): return ''.join(a)
    else: return a

def QMul_w_QAdd(a, b):
    '''
    The quantum circuit is in the addition parts.
    It uses a type of qiskit circuit called WeightedAdder.
    
    Here is a documentation:
    https://qiskit.org/documentation/stubs/qiskit.circuit.library.WeightedAdder.html
    
    Suppose there are two factors, a = 168 and b = 185
    During multiplication, a and b are going to be broken up into additions to be process using long multiplication algorithm, like this:
    a = 100+60+8
    b = 100+80+5
    
    a*b = 168*185
        = (100+60+8)*(100+80+5)
        = 10000+8000+500+6000+4800+300+800+640+40 = 31080
    '''
    
    aText = str(a)
    bText = str(b)
    
    aBehindDigits = aText.split('.')
    bBehindDigits = bText.split('.')
    
    aBehindDigitsLen = len(aBehindDigits[1]) if '.' in aText and aBehindDigits[1] != '0' else 0
    bBehindDigitsLen = len(bBehindDigits[1]) if '.' in bText and bBehindDigits[1] != '0' else 0
    
    BehindDigitsLen = aBehindDigitsLen + bBehindDigitsLen
    
    aMod = int(aText.replace('.', ''))
    bMod = int(bText.replace('.', ''))
    
    aReversed = str(abs(aMod))[::-1]
    bReversed = str(abs(bMod))[::-1]

    productList = []

    for aDigit, aDigitIndex in zip(aReversed, range(len(aReversed))):
        for bDigit, bDigitIndex in zip(bReversed, range(len(bReversed))):
            rawNum = str(mulDict[(int(aDigit),int(bDigit))])
            numPlaceValuedStr = rawNum + '0'*(aDigitIndex+bDigitIndex)
            numPlaceValued = int(numPlaceValuedStr)
            productList.append(numPlaceValued)
    
    ASign = [-1, 1][aMod >= 0]
    BSign = [-1, 1][bMod >= 0]
    
    product1 = ASign*BSign*QAdd(*productList)
    product2 = list(str(product1))
    # print('QMul', 114, product1)
    # print('QMul', 114, product2)
    
    if BehindDigitsLen > 0:
        product2[-BehindDigitsLen:-BehindDigitsLen] = ['.']
    
    product3 = ''.join(product2)
    # print('QMul', 121, product2)
    # print('QMul', 122, product3)
    
    if '.' in product3:
        product3Split = product3.split('.')
        if set(list(product3Split[1])) == {'0'}:
            productFinal = product3Split[0]
        else:
            productFinal = product3
    else:
        productFinal = product3
        
    return productFinal
    