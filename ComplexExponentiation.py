import tkinter.messagebox
import PolynomialLibrary as pl
from tkinter import *
import webbrowser
from PIL import Image, ImageTk
import os
from ComplexFunctions import Demoivre
from tkinter import messagebox as mb
import tkinter

def MainApplication():

    def ValidInput() -> list:
        try:
            exponent = int(exponentEntry.get())
            
            if (exponent < 2):
                return []
            formattedComplexNumber = numberEntry.get().lower().replace("i","j")
            complexNumber = complex(formattedComplexNumber)
            return [exponent, complexNumber]
        except:
            return []
        

    def OnEqualsButtonPressed():
        formattedNumbers = ValidInput()
        if (len(formattedNumbers) == 0):
            tkinter.messagebox.showwarning(title = "Invalid input",message = "Please input whole numbers greater than 1 within the exponent field and complex numbers within the other field.")
            return
        
        exponent = formattedNumbers[0]
        complexNumber = formattedNumbers[1]
        allRoots = Demoivre(complexNumber, 1/exponent)

        primaryRootLabel.config(text=str(allRoots[0]).replace("(", "").replace(")", "").replace("j", "i"))
        listbox.delete(0, END)
        for root in allRoots[1:]:
            formattedRoot = str(root).replace("(", "").replace(")", "").replace("j", "i")
            listbox.insert(END, formattedRoot)
        listbox.select_set(0) 
        


    master = Tk()
    width = 550
    height = 450
    master.geometry(f"{width}x{height}")

    equalsButton = Button(master, text="=", font=('Arial 30'), width=2, height=1, command=OnEqualsButtonPressed)
    equalsButton.config(fg='white', bg='black')
    equalsButton.place(x=470, y=80)

    exponentEntry = Entry(master, width=3, font=('Arial 18'))
    exponentEntry.place(x=20,y=40)

    numberEntry = Entry(master, width=15, font=('Arial 30'))
    numberEntry.place(x=120,y=90)


    primaryRootHeading = Label(master, text="Primary Root", font=('Arial 20'))
    primaryRootHeading.place(relx = 0.5, rely = 0.45, anchor = CENTER)

    primaryRootLabel = Label(master, text="232.344+354.432i", font=('Arial 15'), fg='green')
    primaryRootLabel.place(relx = 0.5, rely = 0.55, anchor = CENTER)

    primaryRootHeading = Label(master, text="Other Roots", font=('Arial 20'))
    primaryRootHeading.place(relx = 0.5, rely = 0.65, anchor = CENTER)

    listbox = Listbox(master, height=6, font=('Arial 12'), selectmode=EXTENDED)

    listbox.place(relx = 0.5, rely = 0.7, anchor = N)

    master.mainloop()


    
MainApplication()

