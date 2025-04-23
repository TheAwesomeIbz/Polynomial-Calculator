from ast import Pass
import cmath
import math
from matplotlib import pyplot as plt
import numpy as np
import ComplexFunctions
from numpy import sign
import webbrowser


class Polynomial():
    
    Roots = []
    __coefficients = []
    __equation = ""
    
    def __init__(self, *args, **kwargs) -> None:
        self.__coefficients = args
        self.Solve()
        pass
    
    def Equation(self):
        print(self.__equation)
        
    def SortedRoots(self, index : int):
        return self.__sortedRoots[index]
    
    def Solve(self):
        
        length = len(self.__coefficients)
        if length == 5: return self.quartic(self.__coefficients)   
        elif length == 4: return self.cubic(self.__coefficients)
        elif length == 3: return self.quadratic(self.__coefficients)
        elif length == 2: return self.linear(self.__coefficients)
        elif length < 2:
            print("This is not a function that can be solved with this program.")
            return None
        else:
            return self.generalPolynomial()
        
    def EquationFromRoots(self):
        print("The equation defined by the roots")

        for i in range(len(self.Roots)):
            print(f"x = {self.Roots[i]}")
        coeflist = []
        
        if len(self.Roots) == 2:
            coeflist.append(-(self.Roots[0] + self.Roots[1]))
            coeflist.append(self.Roots[0] * self.Roots[1])
            for i in range(len(coeflist)):
                coeflist[i] = ComplexFunctions.simplify(coeflist[i])
            print(f"is x² + {coeflist[0]}x + {coeflist[1]}")
            
        if len(self.Roots) == 3:
            coeflist.append(-(self.Roots[0] + self.Roots[1] + self.Roots[2]))
            coeflist.append((self.Roots[0]*self.Roots[2]) + (self.Roots[1]*self.Roots[2]) + (self.Roots[0]*self.Roots[1]))
            coeflist.append(-(self.Roots[0] * self.Roots[1] * self.Roots[2]))
            for i in range(len(coeflist)):
                coeflist[i] = ComplexFunctions.simplify(coeflist[i])
            print(f"is x³ + {coeflist[0]}x² + {coeflist[1]}x + {coeflist[2]}")

        if len(self.Roots) == 4:
            a = self.Roots[0]
            b = self.Roots[1]
            c = self.Roots[2]
            d = self.Roots[3]
            signlist = []
            coeflist.append(-(a+b+c+d))
            coeflist.append(a*(b+c+d) + b*(c+d) + (c*d))
            coeflist.append(-((a*b)*(c+d) + (c*d)*(a+b)))
            coeflist.append(a*b*c*d)
            for i in range(len(coeflist)):
                if ComplexFunctions.simplify(coeflist[i].imag) != 0:
                    signlist.append("+")
                else:
                    signlist.append("+" if coeflist[i].real >= 0 else "-") 
                    coeflist[i] = ComplexFunctions.simplify(coeflist[i].real)
                
                
            print(f"is x⁴ + {coeflist[0]}x³ + {coeflist[1]}x² + {coeflist[2]}x + {coeflist[3]}")
            
            ComplexFunctions.FindCongugates(self.Roots)
            
    def plusOrMinusSign(self, complexNumber) -> str:
        return "+" if complexNumber.real > 0 else "-"     

    def linear(self, coefficients : list) -> list:
        Roots = []
        a = coefficients[0]
        b = coefficients[1]
        if a == 0:
            self.__equation = f"This is not a polynomial. This equation only consists of the constant line; f(x) = {b}"
        else:
            Roots.append((- b) / a)
            self.__equation = f'The root of the equation f(x) = {"" if a == 1 else a}x {self.plusOrMinusSign(b)} {b} is:\nx = {Roots[0]}'
            return Roots   

    def quadratic(self, coefficients : list) -> list:
        Roots = []
        a = coefficients[0]
        b = coefficients[1]
        c = coefficients[2]
        if a == 0:
            self.linear([b,c])
        else:
            x1 = (-b + cmath.sqrt(b**2 - 4*a*c)) / (2*a)
            x2 = (-b - cmath.sqrt(b**2 - 4*a*c)) / (2*a)
            Roots.append(x1)
            Roots.append(x2)
            self.__equation = f"The roots of equation f(x) = {a}x² {self.plusOrMinusSign(b)} {abs(b)}x {self.plusOrMinusSign(c)} {abs(c)} are:\nx = {x1}\nx = {x2}"
            return Roots
            
    def cubic(self, coefficients : list) -> list:
        w2 = ComplexFunctions.RootsOfUnity(3)[1]
        w3 = ComplexFunctions.RootsOfUnity(3)[2]
        a = coefficients[0]
        b = coefficients[1]
        c = coefficients[2]
        d = coefficients[3]
        if a == 0:
            self.quadratic([b,c,d])
        else:
            part1 = -(b / (3*a))
            part2 = -((b**3)/(27*(a**3))) + ((b*c) / (6*(a**2))) - (d / (2*a))
            part3 = (c / (3*a)) - ((b**2) / (9*(a**2)))
            
            segment = (part2**2 + part3**3) ** (1/2)
            cubeRoot1 = ComplexFunctions.cbrt(part2 + segment)
            cubeRoot2 = ComplexFunctions.cbrt(part2 - segment)
            
            x1 = part1 + cubeRoot1 + cubeRoot2
            x2 = part1 + w2*(cubeRoot1) + w3*(cubeRoot2)
            x3 = part1 + w3*(cubeRoot1) + w2*(cubeRoot2)
            
            Roots = [
                ComplexFunctions.simplify(x1),
                ComplexFunctions.simplify(x2),
                ComplexFunctions.simplify(x3)
            ]
            
            #made with the help of https://www.desmos.com/calculator/oy6e4l2gnl to evaluate values
            self.__equation = f"""
            f(x) = {a}x³ + {b}x² + {c}x + {d}
            
            [OR f(x) = x³ + {b}/{a}x² + {c}/{a}x + {d}/{a} => f(x) = x³ + {b/a}x² + {c/a}x + {d/a}]
            ROOTS
            x = {Roots[0]}
            x = {Roots[1]}
            x = {Roots[2]}
            
            CONJUGATE SUB-FUNCTIONS:
            {ComplexFunctions.GenerateEquationFromConjugates(ComplexFunctions.FindCongugates(Roots))}
            """
            self.Roots = Roots
            return Roots

    def quartic(self, coefficients : list) -> list:
        a = coefficients[0]
        b = coefficients[1]
        c = coefficients[2]
        d = coefficients[3] 
        e = coefficients[4]
        if a == 0:
            self.cubic([b,c,d,e])
        else:
            Roots = []
            
            parsedB = b / a
            parsedC = c / a
            parsedD = d / a
            parsedE = e / a
            
            segment1 = parsedC - 3*(parsedB ** 2) / 8
            segment2 = (parsedD + ((parsedB**3) / 8) - (parsedB*parsedC/2) )
            segment3 = parsedE - (3*(parsedB**4)/256) + ((parsedB**2) * (parsedC/16)) - (parsedB*parsedD/4)
            
            cubicCoefficients = [
                1,
                segment1 / 2,
                ((segment1 ** 2) - (4*segment3)) / 16,
                - (segment2**2) / 64
            ]
            
            cubicRoots = self.cubic(cubicCoefficients)
            nonZeroCubicRoots = []
            
            for root in cubicRoots:
                if (root.imag != 0): nonZeroCubicRoots.append(root)
            
            
            if (len(nonZeroCubicRoots) < 2):
                for root in cubicRoots:
                    if (root != 0) : nonZeroCubicRoots.append(root)
                
            
            part1 = cmath.sqrt(nonZeroCubicRoots[0] if len(nonZeroCubicRoots) > 0 else 0)
            part2 = cmath.sqrt(nonZeroCubicRoots[1] if len(nonZeroCubicRoots) > 0 else 0)
            part3 = (-segment2 / (8 * part1 * part2)) if (part1 != 0 or part2 != 0) else 0
            part4 = b / (4*a)
            
            self.__coefficients = [a, b, c, d, e]
            Roots = [
                ComplexFunctions.simplify(part1 + part2 + part3 - part4),
                ComplexFunctions.simplify(part1 - part2 - part3 - part4),
                ComplexFunctions.simplify(-part1 + part2 - part3 - part4),
                ComplexFunctions.simplify(-part1 - part2 + part3 - part4),
            ]
                
            
            
            self.__equation = f"""
            f(x) = {a}x⁴ + {b}x³ + {c}x² + {d}x + {e} 
            
            ROOTS:
            x = {Roots[0]}
            x = {Roots[1]}
            x = {Roots[2]}
            x = {Roots[3]}
            
            DEPRESSED QUARTIC
            [OR f(x) = x⁴ + {b}/{a}x³ + {c}/{a}x² + {d}/{a}x + {e}/{a}]]
            [OR f(x) = x⁴ + {parsedB}x³ + {parsedC}x² + {parsedD}x + {parsedE}]
            
            CONJUGATE SUB-FUNCTIONS:
            {ComplexFunctions.GenerateEquationFromConjugates(ComplexFunctions.FindCongugates(Roots))}
            """
            self.Roots = Roots
            return Roots

    def generalPolynomial(self) -> list:
        self.Roots = np.roots(self.__coefficients)
        __function = ""
        
        for i in range(len(self.__coefficients)):
            if (i == len(self.__coefficients) - 1):
                __function += f"{self.__coefficients[i]}"
            else:
               __function += f"{self.__coefficients[i]}x^{len(self.__coefficients) - i - 1} + " 
            
        __roots = [ComplexFunctions.simplify(i) for i in self.Roots]
        __displayRoots = ""
        
        for i in __roots:
            __displayRoots += "x = " + str(i) + "\n"
        
        self.__equation = f"""
f(x) = {__function}
        
ROOTS
{__displayRoots}
        
CONJUGATE SUB-FUNCTIONS:
{ComplexFunctions.GenerateEquationFromConjugates(ComplexFunctions.FindCongugates(__roots))}

"""
        
    def OpenDesmos(self):
        if (len(self.Roots) == 3):
            webbrowser.open('https://www.desmos.com/calculator/oy6e4l2gnl')
        elif (len(self.Roots) == 4):
            webbrowser.open('https://www.desmos.com/calculator/jnzdoivao5')
            
    


polynomial = Polynomial(1,-1.6,-120,780)
print(polynomial.Roots)


import cmath


print(ComplexFunctions.cbrt(327.161j + -231))





