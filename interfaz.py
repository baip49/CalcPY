from tkinter import *
import tkinter as tk

app = Tk()
app.title("Calculadora Científica - TECHTITLÁN Team")
app.geometry('525x630')
app.configure(bg='#f5f5f5')
app.resizable(False, False)

# Frame para el input y el resultado
input_frame = Frame(app, bg='#f5f5f5')
input_frame.pack(pady=30)

# Input
input_label = Label(input_frame, text="3*2*(sin(5))", width=50, relief='flat', font=('Arial', 14), fg='#252757', bg='#f5f5f5', anchor='e')
input_label.pack(fill='x', pady=(0, 30))

# Resultado
result_label = Label(input_frame, text="Resultado", width=50, font=('Arial', 18, "bold"), fg='#252757', bg='#f5f5f5', anchor='e')
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

sin_button = Button(first_row, text='sin', **button_config)
sin_button.pack(side='left', expand=True, fill='both')

cos_button = Button(first_row, text='cos', **button_config)
cos_button.pack(side='left', expand=True, fill='both')

tan_button = Button(first_row, text='tan', **button_config)
tan_button.pack(side='left', expand=True, fill='both')

log_button = Button(first_row, text='log', **button_config)
log_button.pack(side='left', expand=True, fill='both')

ln_button = Button(first_row, text='ln', **button_config)
ln_button.pack(side='left', expand=True, fill='both')

pi_button = Button(first_row, text='π', **button_config)
pi_button.pack(side='left', expand=True, fill='both')

ce_button = Button(first_row, text='CE',
                   font=('Arial', 16),
                   bg='#ff9999',
                   fg='#fff',
                   activebackground='lightblue',
                   borderwidth=0,
                   relief='flat',
                   width=5)
ce_button.pack(side='left', expand=True, fill='both')

del_button = Button(first_row, text='DEL',
                    font = ('Arial', 16),
                    bg='#ff4d4d',
                    fg='#fff',
                    activebackground='lightblue',
                    borderwidth=0,
                    relief='flat',
                    width=5)
del_button.pack(side='left', expand=True, fill='both')

# Segunda fila de botones | M, MR, (, ), ^, /, e, sqrt
second_row = Frame(app)
second_row.pack()

button_config['width'] = 5
button_config['height'] = 3
button_config['bg'] = '#fff'

m_button = Button(second_row, text='M', **button_config)
m_button.pack(side='left', expand=True, fill='both')

mr_button = Button(second_row, text='MR', **button_config)
mr_button.pack(side='left', expand=True, fill='both')

left_parenthesis_button = Button(second_row, text='(', **button_config)
left_parenthesis_button.pack(side='left', expand=True, fill='both')

right_parenthesis_button = Button(second_row, text=')', **button_config)
right_parenthesis_button.pack(side='left', expand=True, fill='both')

power_button = Button(second_row, text='^', **button_config)
power_button.pack(side='left', expand=True, fill='both')

division_button = Button(second_row, text='/', **button_config)
division_button.pack(side='left', expand=True, fill='both')

e_button = Button(second_row, text='e', **button_config)
e_button.pack(side='left', expand=True, fill='both')

sqrt_button = Button(second_row, text='√x',
                     font=('Arial', 16),
                     bg='#f9faff',
                     fg='#000',
                     activebackground='lightblue',
                     borderwidth=0,
                     relief='flat',
                     width=5)
sqrt_button.pack(side='left', expand=True, fill='both')

# Tercera fila de botones | 7, 8, 9, x
third_row = Frame(app)
third_row.pack()

button_config['width'] = 11
button_config['font'] = ('Arial', 16, 'bold')

seven_button = Button(third_row, text='7', **button_config)
seven_button.pack(side='left', expand=True, fill='both')

eight_button = Button(third_row, text='8', **button_config)
eight_button.pack(side='left', expand=True, fill='both')

nine_button = Button(third_row, text='9', **button_config)
nine_button.pack(side='left', expand=True, fill='both')

multiplication_button = Button(third_row, text='x',
                               font=('Arial', 16),
                               bg='#f9faff',
                               fg='#000',
                               activebackground='lightblue',
                               borderwidth=0,
                               relief='flat',
                               width=11)
multiplication_button.pack(side='left', expand=True, fill='both')

# Cuarta fila de botones | 4, 5, 6, -
fourth_row = Frame(app)
fourth_row.pack()

four_button = Button(fourth_row, text='4', **button_config)
four_button.pack(side='left', expand=True, fill='both')

five_button = Button(fourth_row, text='5', **button_config)
five_button.pack(side='left', expand=True, fill='both')

six_button = Button(fourth_row, text='6', **button_config)
six_button.pack(side='left', expand=True, fill='both')

subtraction_button = Button(fourth_row, text='-',
                            font=('Arial', 16),
                            bg='#f9faff',
                            fg='#000',
                            activebackground='lightblue',
                            borderwidth=0,
                            relief='flat',
                            width=11)
subtraction_button.pack(side='left', expand=True, fill='both')

# Quinta fila de botones | 1, 2, 3, +
fifth_row = Frame(app)
fifth_row.pack()

one_button = Button(fifth_row, text='1', **button_config)
one_button.pack(side='left', expand=True, fill='both')

two_button = Button(fifth_row, text='2', **button_config)
two_button.pack(side='left', expand=True, fill='both')

three_button = Button(fifth_row, text='3', **button_config)
three_button.pack(side='left', expand=True, fill='both')

addition_button = Button(fifth_row, text='+',
                            font=('Arial', 16),
                            bg='#f9faff',
                            fg='#000',
                            activebackground='lightblue',
                            borderwidth=0,
                            relief='flat',
                            width=11)
addition_button.pack(side='left', expand=True, fill='both')

# Sexta fila de botones | CAM, MIC, 0, ., =
sixth_row = Frame(app)
sixth_row.pack()

button_config['width'] = 7
button_config['font'] = ('Segoe UI Emoji', 16, 'bold')

camera_button = Button(sixth_row, text='📷', **button_config)
camera_button.pack(side='left', expand=True, fill='both')

micro_button = Button(sixth_row, text='🎙️', **button_config)
micro_button.pack(side='left', expand=True, fill='both')

zero_button = Button(sixth_row, text='0', **button_config)
zero_button.pack(side='left', expand=True, fill='both')

dot_button = Button(sixth_row, text='.', **button_config)
dot_button.pack(side='left', expand=True, fill='both')

equal_button = Button(sixth_row, text='=',
                        font=('Arial', 16),
                        bg='#4cc2ff',
                        fg='#fff',
                        activebackground='lightblue',
                        borderwidth=0,
                        relief='flat',
                        width=11)
equal_button.pack(side='left', expand=True, fill='both')

app.mainloop()