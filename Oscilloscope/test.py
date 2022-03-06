from tkinter import *


main = Tk()

width = 600
height = 600

def submit():  # Callback function for SUBMIT Button
    text = textbox.get("1.0", END)  # For line 1, col 0 to end.
    print(f'{text=!r}')

c = Canvas(main, width=width, height=height, highlightthickness=0)
c.pack()

submitbutton = Button(c, width=10, height=1, text='SUBMIT', command=submit)
submitbutton.pack()

textbox = Text(c, width=30, height=2)
textbox.pack()

tboxlabel = Label(c, text='label')
tboxlabel.pack()

quitbutton = Button(c, width=10, height=1, text='QUIT', command=quit)
quitbutton.pack()

mainloop()