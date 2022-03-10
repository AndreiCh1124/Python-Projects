from logging import root
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import tkinter



text_label = """
General form of the ecuation: A * sin ( ω * θ + φ )
Remember to type space after each item of the formula
(like the general form above)
"""

line_animator = list()
lines = list()

def get_parameters(list_1):
    a = list()
    omega = list()
    theta = list() 
    phi = list()
    for element in list_1:
        element = element.split(" ")
        a.append(float(element[0]))
        omega.append(float(element[4]))
        theta.append(float(element[6]))
        phi.append(float(element[8]))
    return a, omega, theta, phi

def btn_command():
    global received_nr_of_osc
    received_nr_of_osc = entry_ext.get()
    root.withdraw()
    root.quit()
    root.destroy()

def det_number_of_osc():
    global root
    root = tkinter.Tk()
    root.title("Oscillation Viewer")
    root.resizable()
    root.geometry("650x250")
    global entry_ext
    entry_ext = tkinter.Entry(root, width=50, font=("Helvetica", 20))
    entry_ext.pack(padx=10, pady=10)
    entry_ext.insert(0, "")
    label_1 = tkinter.Label(root, text="Please enter the number of oscillations", font=("Helvetica", 15))
    label_1.pack()
    button = tkinter.Button(root, text="Submit", command=btn_command)
    button.pack()
    root.mainloop()
    return received_nr_of_osc

def button_func():
    global ecuations
    ecuations = list()
    for entry in entries:
        ecuations.append(entry.get())
    root.quit()
    root.withdraw()

class Line():
    
    def __init__(self, a, om, th, ph, decay=0):
        self.a = a
        self.om = om
        self.th = th
        self.ph = ph
        self.decay = decay
        
    def draw_graph(self, amps):
        global fig
        fig = plt.figure("Oscillation Viewer")
        max_a = max(amps)
        ax = plt.axes(xlim=(0, 100), ylim=(max_a * -2, max_a * 2))
        
    
    def animate(self, t, line, a, om, th, ph, decay=0):
        t = np.arange(0, t, 0.1)
        y = a * (1/(t ** decay)) * np.sin(om * t + th + ph)
        line[0].set_data(t, y)
        return line[0]
    
    def show_osc(self, color="default"):
        plt.style.use(color)
        line = plt.plot([], [], lw=2)
        lines.append(line)
        line_animator.append(animation.FuncAnimation(fig, self.animate, frames=np.arange(1, 100, 0.41), \
                fargs=(line, self.a, self.om, self.th, self.ph, self.decay), interval=20))

class Window():
    
    def __init__(self, number_of_ec):
        self.number_of_ec = number_of_ec  
        
    def draw_entries(self):
        global root
        root = tkinter.Tk()
        root.title("Oscillation Viewer")
        root.resizable()
        root.geometry("650x400")
        global entries
        entries = list()
        for idx in range(int(self.number_of_ec)):
            entries.append(tkinter.Entry(root, width=50, font=("Helvetica", 20)))
            entries[idx].pack(padx=10, pady=10)
            entries[idx].insert(idx, "")
        label_1 = tkinter.Label(root, text="Please type an ecuation in each of the text boxes" + text_label, font=("Helvetica", 15))
        label_1.pack()
        button1 = tkinter.Button(root, text="Generate visuals", command=button_func)
        button1.pack()
        
        root.mainloop()
        
nr_of_osc = det_number_of_osc()

window = Window(nr_of_osc)
window.draw_entries()

line_list = list()

a, om, th, ph = get_parameters(ecuations)

for idx in range(int(nr_of_osc)):
    line = Line(a[idx], om[idx], th[idx], ph[idx])
    line_list.append(line)

line_list[0].draw_graph(a)
    
for line in line_list:
    line.show_osc()

plt.grid()
plt.show()

# 11 * sin ( 0.1 * 1 + 1 )
# 12 * sin ( 0.2 * 2 + 2 )
# 13 * sin ( 0.3 * 3 + 3 )
