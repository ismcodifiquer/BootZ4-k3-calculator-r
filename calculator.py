from tkinter import *
from tkinter import ttk
from romannumber import *

HEIGHTBTN = 50    
WIDTHBTN = 68

class CalcButton(ttk.Frame):
    def __init__(self, parent, text, command, wbtn=1, hbtn=1):
        ttk.Frame.__init__(self, parent, width=wbtn*WIDTHBTN, height=hbtn*HEIGHTBTN)

        self.pack_propagate(0)

        s = ttk.Style()
        s.theme_use('alt')
        s.configure('my.TButton', font=('Helvetica', '14', 'bold'))
        
        self.__btn = ttk.Button(self, text=text, command=command, style='my.TButton')
        self.__btn.pack(side=TOP, fill=BOTH, expand=True)

class Display(ttk.Frame):
    cadena = '_'
    __maxnumbers = 12
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, width=4*WIDTHBTN, height=HEIGHTBTN)

        self.pack_propagate(0)
        

        s = ttk.Style()
        s.theme_use('alt')
        s.configure('my.TLabel', font='Helvetica 30')

        self.__lbl = ttk.Label(self, text=self.cadena, style='my.TLabel', anchor=E, background='black', foreground='white')
        self.__lbl.pack(side=TOP, fill=BOTH, expand=True)

    def addChar(self, caracter):
        if len(self.cadena) >= self.__maxnumbers:
            return

        if self.cadena == '_':
            self.cadena = ''
        self.cadena += caracter

        try:
            nr = RomanNumber(self.cadena)
        except ValueError:
            self.cadena = self.cadena[:-1]

        self.__lbl.config(text=self.cadena)
        

    def clear(self):
        self.cadena = '_'
        self.__lbl.config(text=self.cadena)
        
    def muestra(self, cadena):
        self.cadena = str(cadena)
        self.__lbl.config(text=cadena)



class Selector(ttk.Frame):
    tipus = 'R'

    def __init__(self, parent, command):
        ttk.Frame.__init__(self, parent, width=WIDTHBTN*2, height=HEIGHTBTN)

        self.pack_propagate(0)

        self.__rbR = ttk.Radiobutton(self, text='Romano', variable=self.tipus, value='R', command=lambda: command('R'))
        self.__rbA = ttk.Radiobutton(self, text='Arábigo', variable=self.tipus, value='A', command=lambda: command('A'))

        self.__rbR.pack(side=TOP, fill=BOTH, expand=True)
        self.__rbA.pack(side=TOP, fill=BOTH, expand=True)

        

class Calculator(ttk.Frame):
    op1 = None
    operacion = None
    op2 = None

    def __createLayoutRoman(self):
        layoutRoman = ttk.Frame(self, name='layoutRoman')
        self.buttonAC = CalcButton(layoutRoman, text='AC', command=self.pantalla.clear, wbtn=3)
        self.buttonAC.grid(column=0, row=1, columnspan=3)
        

        self.buttonC = CalcButton(layoutRoman, text='C', command=lambda: self.pantalla.addChar('C'))
        self.buttonC.grid(column=0, row=2)
        self.buttonD = CalcButton(layoutRoman, text='D', command=lambda: self.pantalla.addChar('D'))
        self.buttonD.grid(column=1, row=2)
        self.buttonM = CalcButton(layoutRoman, text='M', command=lambda: self.pantalla.addChar('M'))
        self.buttonM.grid(column=2, row=2)
        

        self.buttonX = CalcButton(layoutRoman, text='X', command=lambda: self.pantalla.addChar('X'))
        self.buttonX.grid(column=0, row=3)
        self.buttonL = CalcButton(layoutRoman, text='L', command=lambda: self.pantalla.addChar('L'))
        self.buttonL.grid(column=1, row=3)
        self.buttonPL = CalcButton(layoutRoman, text='(', command=lambda: self.pantalla.addChar('('))
        self.buttonPL.grid(column=2, row=3)
        


        self.buttonI = CalcButton(layoutRoman, text='I', command=lambda: self.pantalla.addChar('I'))
        self.buttonI.grid(column=0, row=4)
        self.buttonV = CalcButton(layoutRoman, text='V', command=lambda: self.pantalla.addChar('V'))
        self.buttonV.grid(column=1, row=4)
        self.buttonPR = CalcButton(layoutRoman, text=')', command=lambda: self.pantalla.addChar(')'))
        self.buttonPR.grid(column=2, row=4)

        self.buttonAdd = CalcButton(layoutRoman, text='+', command=lambda: self.operar('+'))
        self.buttonAdd.grid(column=3, row=4)
        self.buttonSub = CalcButton(layoutRoman, text='-', command=lambda: self.operar('-'))
        self.buttonSub.grid(column=3, row=3)
        self.buttonMul = CalcButton(layoutRoman, text='x', command=lambda: self.operar('x'))
        self.buttonMul.grid(column = 3, row=2)
        self.buttonDiv = CalcButton(layoutRoman, text='÷', command=lambda: self.operar('/'))
        self.buttonDiv.grid(column=3, row=1)
        


        self.buttonEqu = CalcButton(layoutRoman, text='=', command=lambda: self.operar('='), wbtn=2)
        self.buttonEqu.grid(column=2, row=5, columnspan=2)

        return layoutRoman



    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)

        self.pantalla = Display(self)
        self.pantalla.grid(column = 0, row = 0, columnspan = 4)

        self.layoutRoman = self.__createLayoutRoman()
        self.layoutRoman.grid(column=0, row=1, columnspan=4, rowspan=5)

        self.selector = Selector(self, command=self.eligeModo)
        self.selector.grid(column=0, row=5, columnspan=2, sticky=W+S)

        
       

    def operar(self, operacion):
        if operacion in ('+', '-', '/', 'x'):
            self.op1 = RomanNumber(self.pantalla.cadena)
            self.operacion = operacion  
            self.pantalla.clear()
        elif operacion == '=':
            self.op2 = RomanNumber(self.pantalla.cadena)

            if self.operacion == '+':
                resultado = self.op1 + self.op2

            if self.operacion == '-':
                resultado = self.op1 - self.op2

            if self.operacion == '/':
                resultado = self.op1 / self.op2

            if self.operacion == 'x':
                resultado = self.op1 * self.op2
                
            self.pantalla.muestra(resultado)

    def eligeModo(self, modo):
        if modo == 'A':
            print('Tengo que se alfanumérica')
            self.layoutRoman.grid_forget()

        elif modo == 'R':
            print('Tengo que ser romana')
            self.layoutRoman.grid(column=0, row=1, columnspan=4, rowspan=5)

        else:
            print('Modo "{}" erróneo'.format(modo))

        