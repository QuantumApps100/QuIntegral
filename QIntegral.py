#!/usr/bin/env python
# coding: utf-8
# Made by Noble Huang

from QMul import *

def extractVarFromExpr(expr):
    return [_ for _ in expr.atoms() if type(_) is sympy.Symbol]

def QIntegrals(RawEqParts, interfaceWindow=None, debugPrint=False):
    Eqn_Integrated = []
    if debugPrint: factorsSet = []
    
    for RawEqPart in RawEqParts:
        if RawEqPart == sympy.core.numbers.Integer(0):
            continue
        
        var = extractVarFromExpr(RawEqPart)
        
        if var == []:
            var = sympy.Symbol('x')
            Eqn_Integrated.append(RawEqPart*var)
            continue
        
        else:
            var = var[0]
        
        coeffExp = RawEqPart.as_coeff_exponent(var)
        if debugPrint: print('(RawEqPart, var), coeffExp =', (RawEqPart, var), coeffExp)
        
        coeffExpFrac = [Fraction(str(eqNum)).limit_denominator().as_integer_ratio() for eqNum in coeffExp]

        # # Add 1 due to integration
        # Add by a value equal to the denominator of the 2nd/Divisor Fraction (e.g. if denominator=2, then 2/2=1, so add by two)

        factors = np.transpose(coeffExpFrac)
        denominator = factors[1, 1]

        # factors[:, 1][0] is the Numerator of the 2nd Fraction
        factors[:, 1][0] += denominator

        # # Fraction division is a multiplication by its reciprocal of the 2nd/Divisor Fraction
        factors[:, 1] = factors[:, 1][::-1]
        result = []

        if debugPrint: factorsSet.append(factors)

        for A, B in factors:
            # Execute the Multiplication with QMul_w_QAdd()
            resultMul = QMul_w_QAdd(A, B)
            if debugPrint: print('QIntegral', 51, resultMul)
            result.append(resultMul)
            
            if debugPrint: print(f'Expression: {A}*{B} = {resultMul}')

        # New Coefficient for the integrated expression
        if debugPrint: print('QIntegral', 57, result)
        integCoef = Fraction( int(result[0]), int(result[1]) )

        # New Exponent for the integrated expression
        # Add by a value equal to the denominator of the 2nd/Divisor Fraction (e.g. if denominator=2, then 2/2=1, so add by two)
        integExp = QAdd(*[coeffExpFrac[1][0], denominator])
        integExp /= denominator
        
        if debugPrint: print('QIntegral', 65, [coeffExpFrac[1][0], denominator])
        if debugPrint: print('QIntegral', 66, integExp)
        if integExp % 1 == 0: integExp = int(integExp)
        
        Eqn_Integrated.append(integCoef*var**integExp)
        
        if debugPrint: print(factorsSet)
        
        if interfaceWindow: interfaceWindow.update()
        
    return Eqn_Integrated
