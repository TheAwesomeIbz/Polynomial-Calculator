import math

__thresholdValue = 1e-5
__doubleDecimalPlaces = 5

def cbrt(complex : complex) -> complex:
    if (abs(complex.imag) < 1e-5):
        return math.cbrt(complex.real)
    else:
        return (complex ** (1/3))
        
#simplifies complex number
#complex number postprocessing function to prevent calculations outputting negligible real or imaginary components
def simplify(complex : complex):
    if abs(complex.imag) < __thresholdValue:
        return round(complex.real, __doubleDecimalPlaces)
    elif abs(complex.real) < __thresholdValue:
        return round(complex.imag, __doubleDecimalPlaces)*1j
    else:
        return round(complex.real, __doubleDecimalPlaces) + round(complex.imag, __doubleDecimalPlaces)*1j



#calculates powers applied onto the complex number x
def Demoivre(number : float, power : float, isprinting : bool = False):
    modulus = math.sqrt(abs(number.real)**2 + abs(number.imag)**2)
    if modulus == 0:
        theta = 0
    else:
        theta = math.acos(number.real / modulus) + (math.pi * int(number.imag < 0))

        outputlist = []
        if (power < 1 and power > 0):
            inversepower = int(1/power)
        for i in range(inversepower):
            newtheta = (2*math.pi*i + theta) / inversepower
            output = (modulus**power)*(math.cos(newtheta) + (math.sin(newtheta) * 1j))
            outputlist.append(simplify(output))
            
        if (isprinting):
            print(f'{number} to the power of {power} :\nANGLE = {simplify(theta)} Radians or {simplify(theta * 180/math.pi)} Degrees \nMODULUS = {simplify(modulus)}')
            for i in outputlist:
                print(f"ROOTS = {simplify(i)}")
        else:
            output = (modulus**power)*(math.cos(theta*power) + (math.sin(theta*power) * 1j))
            
            
        if (isprinting):
            print(f'{number} to the power of {power} :\nANGLE = {theta} Radians or {theta * 180/math.pi} Degrees \nMODULUS = {modulus}\nRESULT = {simplify(outputlist[0])}')


        return outputlist
    
#calculates roots of unity of complex number 1
def RootsOfUnity(power:int, isprinting : bool = False):
    if (isprinting):
        print(f'The {power}th roots of unity are:')
        for i in Demoivre(1, 1/power):
            print(simplify(i))
    return Demoivre(1, 1/power)

def sortBySize(element):
    return len(element)
    
def FindCongugates(roots : list) -> list:
    __localRoots = list(roots)
    outputList = []
    
    for i in __localRoots:
        if (i.imag == 0):
            outputList.append(simplify(i))
        else:
            for j in __localRoots:
                imaginaryComponent = (i + j).imag
                if (abs(imaginaryComponent) < __thresholdValue):
                    outputList.append([simplify(i), simplify(j)])
                    __localRoots.remove(j)

    return outputList

def GenerateEquationFromConjugates(roots : list):
    outputString = ""
    for root in roots:
        if (type(root) == list):
            outputString += GenerateQuadratic([root[0], root[1]]) + "\n"
    return outputString
    

def GenerateQuadratic(Roots : list) -> str:
    a = simplify(-(Roots[0] + Roots[1]))
    b = simplify(Roots[0] * Roots[1])
    return f"x² + {a}x + {b}"
    

def GenerateCubic(Roots : list) -> str:
    a = simplify(-(Roots[0] + Roots[1] + Roots[2]))
    b = simplify((Roots[0]*Roots[2]) + (Roots[1]*Roots[2]) + (Roots[0]*Roots[1]))
    c = simplify(-(Roots[0] * Roots[1] * Roots[2]))
    return f"is x³ + {a}x² + {b}x + {c}"
        
def GenerateQuartic(Roots : list) -> str:
    a = simplify(-(Roots[0]+Roots[1]+Roots[2]+Roots[3]))
    b = simplify(Roots[0]*(Roots[1]+Roots[2]+Roots[3]) + Roots[1]*(Roots[2]+Roots[3]) + (Roots[2]*Roots[3]))
    c = simplify(-((Roots[0]*Roots[1])*(Roots[2]+Roots[3]) + (Roots[2]*Roots[3])*(Roots[0]+Roots[1])))
    d = simplify(Roots[0]*Roots[1]*Roots[2]*Roots[3])
    return f"x⁴ + {a}x³ + {b}x² + {c}x + {d}"
    #STEPHEN 28:05