#!/usr/bin/env python
# coding: utf-8
# Made by Noble Huang

from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer, AerSimulator

from qiskit.circuit.library import RGQFTMultiplier

from qiskit.circuit import Instruction, CircuitInstruction, Qubit, QuantumRegister, Clbit, ClassicalRegister
from qiskit.circuit.library.standard_gates import IGate, XGate, CXGate, CCXGate, C3XGate, C4XGate, MCXGate, RXGate, RYGate, RZGate, HGate
from qiskit.exceptions import QiskitError

import matplotlib.pyplot as plt

from qiskit.visualization import plot_histogram

import os
import sys
import math as m
import numpy as np
import pandas as pd
import sympy

from _functools import *
from traceback import format_exc

def initGates(circuit, qreq, nInputs, inputIndexBegin=0, gateName='id'):
    '''Determine Input Value (Either 0 or 1)
    Initialization Gates
    First, zero it out at the beginning.
    All qubits start from ground state |0>. Create manipulable initialization gates as many as the input qubits.
    The identity gate means that it remains the same state as previous, which, in this case, the ground state |0>.
    Later, the Identity gate can be converted to an X Gate or NOT gate.'''

    circuit.data = [CircuitInstruction(operation=Instruction(name=gateName, num_qubits=1, num_clbits=0, params=[]),
                                    qubits=(Qubit(qreq, inputIndex),),
                                    clbits=()) for inputIndex in range(inputIndexBegin, nInputs)]


def QAdd(addends, BehindDigitsLen=None, aCirc=None, method='matrix_product_state', shots=2000):
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
    
    if BehindDigitsLen is None:
        addendsText = [str(addend) for addend in addends]
        addendsText = [addendText if '.' in addendText else addendText+'.0' for addendText in addendsText]
        addendsBehindDigits = [addendText.split('.') for addendText in addendsText]
        addendsBehindDigitsLen = [len(addendBehindDigits[1]) if '.' in addendText else 0 for addendText, addendBehindDigits in zip(addendsText, addendsBehindDigits)]
    
        BehindDigitsLen = max(addendsBehindDigitsLen)
        
        addends = [int(addendText.replace('.', '')) for addendText in addendsText]
    
    weights = list(addends[:10])
    
    aCirc1 = WeightedAdder(num_state_qubits=len(weights), weights=weights)
    nQubits = aCirc1.num_qubits
    qubits = aCirc1.qubits
    
    sumQubitIndices = [qubitIndex for qubitIndex in range(len(qubits)) if "'sum'" in str(qubits[qubitIndex])]
    nInputs = str(qubits).count("'state'")
    nOutputs = len(sumQubitIndices)
    q = QuantumRegister(nQubits, 'q')
    c = ClassicalRegister(nOutputs, 'c')
    
    if aCirc is None:
        aCirc = QuantumCircuit(q, c)
    
    initGates(aCirc, q, nInputs, gateName='x')
    aCirc.append(aCirc1, range(nQubits))
    aCirc.measure(sumQubitIndices, range(nOutputs))
    
    backend = AerSimulator(method=method)
    job = execute(aCirc, backend, shots=shots)
    result = job.result()
    counts = result.get_counts()
    
    resultNum = int(list(counts)[0], 2)
    
    if len(addends) > 10:
        addends[:10] = [resultNum]
        return QAdd(addends, BehindDigitsLen)
        
    else:
        sum1 = resultNum
        sum2 = list(str(sum1))
        
        if BehindDigitsLen > 0:
            sum2[-BehindDigitsLen:-BehindDigitsLen] = ['.']
        
        sum3 = ''.join(sum2)
        sum4 = sum3.replace('.0', '') if sum3.endswith('.0') else sum3

        return sum4
    
def QAdd1(*addends):
    return QAdd(list(addends))