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

def btn_command(root, entry):
    print("ceva")
    global received_nr_of_osc
    received_nr_of_osc = entry.get()
    

def det_number_of_osc():
    root = tkinter.Tk()
    root.resizable()
    root.geometry("650x250")
    entry_ext = tkinter.Entry(root, width=50, font=("Helvetica", 20))
    entry_ext.pack(padx=10, pady=10)
    entry_ext.insert(0, "")
    button = tkinter.Button(root, text="Submit", command=btn_command(root, entry_ext))
    button.pack()
    root.mainloop()
    print(received_nr_of_osc)
    root.quit()
    root.withdraw()
    return entry_ext.get()

class Line():
    
    def __init__(self, a, om, th, ph, decay=0):
        self.a = a
        self.om = om
        self.th = th
        self.ph = ph
        self.decay = decay
        
    def draw_graph(self, amps):
        global fig
        fig = plt.figure()
        max_a = max(amps)
        ax = plt.axes(xlim=(0, 100), ylim=(max_a * -2, max_a * 2))
        
    
    def animate(self, t, line, a, om, th, ph, decay=0):
        t = np.arange(0, t, 0.1)
        y = a * (1/(t ** decay)) * np.sin(om * t + th) + ph
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
        root = tkinter.Tk()
        root.resizable()
        root.geometry("650x250")
        entries = list()
        for idx in range(int(self.number_of_ec)):
            entries.append(tkinter.Entry(root, width=50, font=("Helvetica", 20)))
            entries[idx].pack(padx=10, pady=10)
            entries[idx].insert(idx, "")
            print(idx)
        root.mainloop()
            

line = Line(10, 0.3, 2, 1)
line2 = Line(12, 0.5, 1, 2)
line3 = Line(7, 0.5, 1, 2)
line4 = Line(20, 0.5, 1, 2)

line.draw_graph([7, 10, 12, 20])
line.show_osc()
line2.show_osc()
line3.show_osc()
line4.show_osc()

plt.grid()
plt.show()



# 10 * sin ( 0.5 * 2 + 1 )

# plt.grid()
# plt.show() 