from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk
import os
from dotenv import load_dotenv
import os
from tkinter import *
from tkinter import messagebox
from tkinter import Tk, Button, Label, StringVar
import tkinter as tk
import ply.lex as lex
import ply.yacc as yacc
import math
# from ocr2 import camera
from ocr import cam as camera

load_dotenv() # Cargar variables de entorno

# Tokens
tokens = (
    'NUMBER', 'DECIMAL', 'PI', 'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE',
    'SIN', 'COS', 'TAN', 'LOG', 'LN', 'EULER', 'EXP', 'SQRT',
    'LPAREN', 'RPAREN', 'EQUALS'
)

# Regex
t_DECIMAL = r'\.'
t_PI = r'π'
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_SIN = r'sin'
t_COS = r'cos'
t_TAN = r'tan'
t_LOG = r'log'
t_LN = r'ln'
t_EULER = r'e'
t_EXP = r'\^'
t_SQRT = r'√'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_EQUALS = r'='

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

# Parser
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE'),
    ('right', 'UMINUS'),
    ('right', 'EXP'),
    ('left', 'SIN', 'COS', 'TAN', 'LOG', 'LN', 'SQRT')
)

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression MULTIPLY expression
                  | expression DIVIDE expression'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]

def p_expression_exp(p):
    'expression : expression EXP expression'
    p[0] = p[1] ** p[3]

def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = -p[2]

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]

def p_expression_pi(p):
    'expression : PI'
    p[0] = 3.14159

def p_expression_euler(p):
    'expression : EULER'
    p[0] = 2.71828

def p_expression_sqrt(p):
    'expression : SQRT expression'
    p[0] = math.sqrt(p[2])

def p_expression_sin(p):
    'expression : SIN expression'
    p[0] = math.sin(p[2])

def p_expression_cos(p):
    'expression : COS expression'
    p[0] = math.cos(p[2])

def p_expression_tan(p):
    'expression : TAN expression'
    p[0] = math.tan(p[2])

def p_expression_log(p):
    'expression : LOG expression'
    p[0] = math.log10(p[2])

def p_expression_ln(p):
    'expression : LN expression'
    p[0] = math.log(p[2])

def p_error(p):
    print("Error de sintaxis: '%s'" % p.value)
    input_label.config(text="")

parser = yacc.yacc()

# Función para evaluar la expresión
def evaluate_expression():
    expression = input_label.cget("text").replace('−', '-')
    try:
        result = parser.parse(expression)
        result_label.config(text=str(result))
    except Exception as e:
        messagebox.showerror("Error", f"Error de sintaxis: {e}")

# Función para actualizar el input_label
def update_input_label(value):
    current_text = input_label.cget("text")
    new_text = current_text + value
    input_label.config(text=new_text)

# Función para borrar el input_label
def clear_input_label():
    input_label.config(text="")
    result_label.config(text="0")

def delete_last_character():
    current_text = input_label.cget("text")
    new_text = current_text[:-1]
    input_label.config(text=new_text)



# Interfaz gráfica
app = Tk()
app.title("Calculadora Científica - TECHTITLÁN Team")
app.geometry('525x630')
app.configure(bg='#f5f5f5')
app.resizable(False, False)

# Frame para el input y el resultado
input_frame = Frame(app, bg='#f5f5f5')
input_frame.pack(pady=30)

# Input
input_label = Label(input_frame, text="", width=50, relief='flat', font=('Arial', 14), fg='#252757', bg='#f5f5f5', anchor='e')
input_label.pack(fill='x', pady=(0, 30))

# Resultado
result_label = Label(input_frame, text="0", width=50, font=('Arial', 18, "bold"), fg='#252757', bg='#f5f5f5', anchor='e')
result_label.pack(fill='x')

# Primera fila de botones | sin, cos, tan, log, ln, π, CE, DEL
first_row = Frame(app)
first_row.pack()

button_config = {
    'font': ('Arial', 16,),
    'bg': '#f9faff',
    'fg': '#252757',
    'activebackground': 'lightblue',
    'borderwidth': 0,
    'relief': 'flat',
    'width': 5,
    'height': 2
}

sin_button = Button(first_row, text='sin', **button_config, command=lambda: update_input_label('sin('))
sin_button.pack(side='left', expand=True, fill='both')

cos_button = Button(first_row, text='cos', **button_config, command=lambda: update_input_label('cos('))
cos_button.pack(side='left', expand=True, fill='both')

tan_button = Button(first_row, text='tan', **button_config, command=lambda: update_input_label('tan('))
tan_button.pack(side='left', expand=True, fill='both')

log_button = Button(first_row, text='log', **button_config, command=lambda: update_input_label('log('))
log_button.pack(side='left', expand=True, fill='both')

ln_button = Button(first_row, text='ln', **button_config, command=lambda: update_input_label('ln('))
ln_button.pack(side='left', expand=True, fill='both')

pi_button = Button(first_row, text='π', **button_config, command=lambda: update_input_label('π'))
pi_button.pack(side='left', expand=True, fill='both')

ce_button = Button(first_row, text='CE',
                   font=('Arial', 16),
                   bg='#ff9999',
                   fg='#fff',
                   activebackground='lightblue',
                   borderwidth=0,
                   relief='flat',
                   width=5, command=clear_input_label)
ce_button.pack(side='left', expand=True, fill='both')

del_button = Button(first_row, text='DEL',
                    font = ('Arial', 16),
                    bg='#ff4d4d',
                    fg='#fff',
                    activebackground='lightblue',
                    borderwidth=0,
                    relief='flat',
                    width=5, command=delete_last_character)
del_button.pack(side='left', expand=True, fill='both')

# Segunda fila de botones | M, MR, (, ), ^, /, e, sqrt
second_row = Frame(app)
second_row.pack()

button_config['width'] = 5
button_config['height'] = 3
button_config['bg'] = '#fff'

memory = None

def memorysave():
    global memory
    memory = result_label.cget("text")

def memoryshow():
    if memory is not None:
        update_input_label(memory)

m_button = Button(second_row, text='M', **button_config, command=memorysave)
m_button.pack(side='left', expand=True, fill='both')

mr_button = Button(second_row, text='MR', **button_config, command=memoryshow)
mr_button.pack(side='left', expand=True, fill='both')

left_parenthesis_button = Button(second_row, text='(', **button_config, command=lambda: update_input_label('('))
left_parenthesis_button.pack(side='left', expand=True, fill='both')

right_parenthesis_button = Button(second_row, text=')', **button_config, command=lambda: update_input_label(')'))
right_parenthesis_button.pack(side='left', expand=True, fill='both')

power_button = Button(second_row, text='^', **button_config, command=lambda: update_input_label('^'))
power_button.pack(side='left', expand=True, fill='both')

division_button = Button(second_row, text='/', **button_config, command=lambda: update_input_label('/'))
division_button.pack(side='left', expand=True, fill='both')

e_button = Button(second_row, text='e', **button_config, command=lambda: update_input_label('e'))
e_button.pack(side='left', expand=True, fill='both')

sqrt_button = Button(second_row, text='√x',
                     font=('Arial', 16),
                     bg='#f9faff',
                     fg='#000',
                     activebackground='lightblue',
                     borderwidth=0,
                     relief='flat',
                     width=5, command=lambda: update_input_label('√('))
sqrt_button.pack(side='left', expand=True, fill='both')

# Tercera fila de botones | 7, 8, 9, x
third_row = Frame(app)
third_row.pack()

button_config['width'] = 11
button_config['font'] = ('Arial', 16, 'bold')

seven_button = Button(third_row, text='7', **button_config, command=lambda: update_input_label('7'))
seven_button.pack(side='left', expand=True, fill='both')

eight_button = Button(third_row, text='8', **button_config, command=lambda: update_input_label('8'))
eight_button.pack(side='left', expand=True, fill='both')

nine_button = Button(third_row, text='9', **button_config, command=lambda: update_input_label('9'))
nine_button.pack(side='left', expand=True, fill='both')

multiplication_button = Button(third_row, text='x',
                               font=('Arial', 16),
                               bg='#f9faff',
                               fg='#000',
                               activebackground='lightblue',
                               borderwidth=0,
                               relief='flat',
                               width=11, command=lambda: update_input_label('*'))
multiplication_button.pack(side='left', expand=True, fill='both')

# Cuarta fila de botones | 4, 5, 6, -
fourth_row = Frame(app)
fourth_row.pack()

four_button = Button(fourth_row, text='4', **button_config, command=lambda: update_input_label('4'))
four_button.pack(side='left', expand=True, fill='both')

five_button = Button(fourth_row, text='5', **button_config, command=lambda: update_input_label('5'))
five_button.pack(side='left', expand=True, fill='both')

six_button = Button(fourth_row, text='6', **button_config, command=lambda: update_input_label('6'))
six_button.pack(side='left', expand=True, fill='both')

subtraction_button = Button(fourth_row, text='-',
                            font=('Arial', 16),
                            bg='#f9faff',
                            fg='#000',
                            activebackground='lightblue',
                            borderwidth=0,
                            relief='flat',
                            width=11, command=lambda: update_input_label('-'))
subtraction_button.pack(side='left', expand=True, fill='both')

# Quinta fila de botones | 1, 2, 3, +
fifth_row = Frame(app)
fifth_row.pack()

one_button = Button(fifth_row, text='1', **button_config, command=lambda: update_input_label('1'))
one_button.pack(side='left', expand=True, fill='both')

two_button = Button(fifth_row, text='2', **button_config, command=lambda: update_input_label('2'))
two_button.pack(side='left', expand=True, fill='both')

three_button = Button(fifth_row, text='3', **button_config, command=lambda: update_input_label('3'))
three_button.pack(side='left', expand=True, fill='both')

addition_button = Button(fifth_row, text='+',
                            font=('Arial', 16),
                            bg='#f9faff',
                            fg='#000',
                            activebackground='lightblue',
                            borderwidth=0,
                            relief='flat',
                            width=11, command=lambda: update_input_label('+'))
addition_button.pack(side='left', expand=True, fill='both')

# Sexta fila de botones | CAM, MIC, 0, ., =
sixth_row = Frame(app)
sixth_row.pack()

button_config['width'] = 7
button_config['font'] = ('Segoe UI Emoji', 16, 'bold')

camera_button = Button(sixth_row, text='📷', **button_config, command=lambda: [camera_button.config(bg="green"), cam()])
camera_button.pack(side='left', expand=True, fill='both')

micro_button = Button(sixth_row, text='🎙️', **button_config, command=lambda: [micro_button.config(bg="green"), mic()])
micro_button.pack(side='left', expand=True, fill='both')

zero_button = Button(sixth_row, text='0', **button_config, command=lambda: update_input_label('0'))
zero_button.pack(side='left', expand=True, fill='both')

dot_button = Button(sixth_row, text='.', **button_config, command=lambda: update_input_label('.'))
dot_button.pack(side='left', expand=True, fill='both')

equal_button = Button(sixth_row, text='=',
                        font=('Arial', 16),
                        bg='#4cc2ff',
                        fg='#fff',
                        activebackground='lightblue',
                        borderwidth=0,
                        relief='flat',
                        width=11, command=evaluate_expression)
equal_button.pack(side='left', expand=True, fill='both')



# Voz a texto

# Comandos de voz
def transformar_comando(texto):
    global comandos
    comandos = {
        "sin": ["sin", "sin de", "seno", "seno de"],
        "cos": ["cos", "cos de", "coseno", "coseno de"],
        "tan": ["tan", "tan de", "tangente", "tangente de"],
        "log": ["log", "logaritmo", "logaritmo de"],
        "ln": ["ln", "logaritmo natural"],
        "pi": ["pi"],
        "(": ["paréntesis izquierdo", "abrir paréntesis", "abre paréntesis"],
        ")": ["paréntesis derecho", "cierra paréntesis", "cerrar paréntesis"],
        "^": ["potencia", "a la", "elevado a"],
        "/": ["entre", "dividir", "división", "sobre"],
        "e": ["euler"],
        "sqrt": ["sqrt", "raíz cuadrada", "raíz", "raíz de", "raíz cuadrada de"],
        "7": ["siete", "número siete", "número 7", "7"],
        "8": ["ocho", "número ocho", "número 8", "8"],
        "9": ["nueve", "número nueve", "número 9", "9"],
        "x": ["por", "multiplicar", "multiplicación", "multiplicado", "multiplicado por"],
        "4": ["cuatro", "número cuatro", "número 4", "4"],
        "5": ["cinco", "número cinco", "número 5", "5"],
        "6": ["seis", "número seis", "número 6", "6"],
        "-": ["menos", "resta", "restar", "resta a", "restar a"],
        "1": ["uno", "número uno", "número 1", "1"],
        "2": ["dos", "número dos", "número 2", "2"],
        "3": ["tres", "número tres", "número 3", "3"],
        "+": ["mas", "más" "suma", "sumar", "sumar a", "suma a"],
        "0": ["cero", "número cero", "número 0", "0"],
        ".": ["punto", "punto decimal"]
    }
    for comando, palabras in comandos.items():
        for palabra in palabras:
            if palabra in texto:
                texto = texto.replace(palabra, comando)
    return texto

# Función para reconocer comandos de voz
def mic():
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
    speech_config.speech_recognition_language = "es-MX"
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    print("Escuchando...")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()
    texto_reconocido = speech_recognition_result.text.replace(',', '').rstrip('.').lower()
    print(texto_reconocido)
    
    comando = transformar_comando(texto_reconocido)

    if "CE" in comando or "limpiar" in comando or "borrar todo" in comando or "borra todo" in comando:
        clear_input_label()
    elif "DEL" in comando or "borra" in comando or "borrar" in comando or "borra uno" in comando or "borrar uno" in comando:
        current_text = input_label.cget("text")
        input_label.config(text=current_text[:-1])
    elif "Resultado" in comando or "resultado" in comando or "igual" in comando or "igual a" in comando:
        evaluate_expression()
    else:
        input_label.config(text=comando)


# Función para capturar una imagen y reconocer el texto
def cam():
    texto_reconocido = camera()
    if texto_reconocido:
        input_label.config(text=texto_reconocido)

app.mainloop()