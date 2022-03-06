import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import tkinter

root = tkinter.Tk()
root.resizable()
root.geometry("650x250")

entry = tkinter.Entry(root, width=50, font=("Helvetica", 20))
entry.pack(padx=10, pady=10)
entry.insert(0, "")  

text_label_1 = """
General form of the ecuation: A * sin ( ω * θ + φ )
Remember to type space after each item of the formula
(like the general form above)
"""
label_1 = tkinter.Label(root, text=text_label_1, font=("Helvetica", 15))
label_1.pack()

def animate(t, line, a, om, th, ph, decay=0):
    t = np.arange(0, t, 0.1)
    y = a * (1/(t ** decay)) * np.sin(om * t + th) + ph
    line[0].set_data(t, y)
    return line[0]

def get_parameters(list_1):
    a = float(list_1[0])
    omega = float(list_1[4])
    theta = float(list_1[6])
    phi = float(list_1[8])
    return a, omega, theta, phi

def show_osc(a, omega, theta, phi, decay=0):
    # plt.style.use('seaborn-pastel')
    fig = plt.figure()
    ax = plt.axes(xlim=(0, 100), ylim=(a * -2, a * 2))
    line = plt.plot([], [], lw=2)
    line2 = plt.plot([], [], lw=2)
    line_ani = animation.FuncAnimation(fig, animate, frames=np.arange(1, 100, 0.3), fargs=(line, a, omega, theta, phi, decay), interval=20)
    
    plt.style.use('seaborn-pastel')
    line_ani2 = animation.FuncAnimation(fig, animate, frames=np.arange(1, 100, 0.3), fargs=(line2, a+2, omega, theta, phi, decay), interval=20)
    
    plt.grid()
    plt.show() 


def get_input():
    global ecuation
    ecuation = entry.get()
    print(ecuation)
    root.quit()
    root.withdraw()
    
button1 = tkinter.Button(root, text="Generate visuals", command=get_input)
button1.pack()

root.mainloop()

ecuation_elements = ecuation.split(" ")

a, omega, theta, phi = get_parameters(ecuation_elements)

show_osc(a, omega, theta, phi)
