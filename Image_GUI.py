#import librery

import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as filedialog
import os
from tkinter import messagebox


window = tk.Tk()
window.wm_title("Image Comparison")
#window.iconbitmap("C:\\Users\davide.zuanon\OneDrive - INPECO SPA\Repository\Python\Image comparison\IconCompare.ico")

# title
J1= tk.Label(window, text="IMAGE COMPARISION")
J1.grid(row=0,column=2)

J2= tk.Label(window, text="")
J2.grid(row=1,column=2)


J3= tk.Label(window, text="Source file Master:")
J3.grid(row=3,column=1, sticky="W")


J4= tk.Label(window, text="Source file to Compare:")
J4.grid(row=4,column=1, sticky="W")

J5= tk.Label(window, text="Source file LOG:")
J5.grid(row=5,column=1, sticky="W")

J6= tk.Label(window, text="Number of files to compare:")
J6.grid(row=6,column=1, sticky="W")

J7= tk.Label(window, text="Cutter:")
J7.grid(row=7,column=1, sticky="W")

J8= tk.Label(window, text="Resolution:")
J8.grid(row=8,column=1, sticky="W")


# Define Entries
# define text box
#------------------------------------------------------------------------------
source_master = tk.StringVar()
E1 = tk.Entry(window, width=80, textvariable= source_master)
E1.grid(row=3,column=2)

def inputSourceMaster():
    source_master = tk.filedialog.askopenfilename()
    E1.delete(1, tk.END)  # Remove current text in entry
    E1.insert(0, source_master)  # Insert the 'path'
    source_master = source_master
    print(source_master)
# Define Button for browse

E9 = tk.Button(window, text="Browse", fg="Black", width=5, command=inputSourceMaster)
E9.grid(row=3, column=3)
#-------------------------------------------------------------------------------

source_file = tk.StringVar()
E2 = tk.Entry(window, width=80, textvariable= source_file)
E2.grid(row=4,column=2)

def inputSourceFile():
    source_file = tk.filedialog.askopenfilename()
    E2.delete(1, tk.END)  # Remove current text in entry
    E2.insert(0, source_file)  # Insert the 'path'
    print(source_file)
# Define Button for browse

E10= tk.Button(window, text="Browse", fg="Black", width=5, command=inputSourceFile)
E10.grid(row=4, column=3)
#-------------------------------------------------------------------------------

source_log = tk.StringVar()
E3 = tk.Entry(window, width=80, textvariable= source_log)
E3.grid(row=5,column=2)

def inputSourceLog():
    source_log = tk.filedialog.askdirectory()
    source_log = os.path.join(source_log +"/LOG Image Comparison")
    E3.delete(1, tk.END)  # Remove current text in entry
    E3.insert(0, source_log)  # Insert the 'path'
    print(source_log)
# Define Button for browse

E10= tk.Button(window, text="Browse", fg="Black", width=5, command=inputSourceLog)
E10.grid(row=5, column=3)
#-------------------------------------------------------------------------------
numbers_file = tk.StringVar()
E4 = tk.Entry(window, width=4, textvariable= "numbers_file")
E4.grid(row=6,column=2,sticky="W")
E4.insert(0, 1)
ValueNumberFile = E4.get()
print(ValueNumberFile)

Resolution = tk.StringVar()
#Resolution = tk.floatVar()
E5 = tk.Scale(window, from_=0.7, to=1,length=450, resolution= 0.00001, orient="horizontal")
E5.grid(row=8,column=2)
E5.set(0.999)
ValueResolution = E5.get()
print(ValueResolution)

#Resolution = tk.StringVar()
#E5 = tk.Entry(window, width=10, textvariable= Resolution)
#E5.grid(row=8,column=2)

# Define CheckBox

Cutter_Check = tk.BooleanVar()
Cutter_Check.set(False)
E6 = tk.Checkbutton(window, text="Enable", variable=Cutter_Check)
E6.grid(row=7,column=2,sticky="W")
ValueCutter = Cutter_Check.get()
print(ValueCutter)

# Define Button


def ButtomComaprePush():
    #Control Chck vaue inside the box
    if len(E1.get()) == 0:
        messagebox.showwarning("Empty Box Master File", "Insert file in the box Master")
    else:
        if len(E2.get()) == 0:
            messagebox.showwarning("Empty Box Compare File", "Insert file in the box Compare")
        else:
            if len(E3.get()) == 0:
                messagebox.showwarning("Empty Box Log File", "Insert file in the box Log")
            else:
                if len(E4.get()) == 0:
                    messagebox.showwarning("Empty Box Number File", "Insert number file in the box Log")
                else:
                    window.quit()

E7 = tk.Button(window, text="COMPARE", fg="Blue", width= 50, command=ButtomComaprePush)
E7.grid(row=9,column=2)


# Progress Bar

#E8 = ttk.Progressbar(window,orient="horizontal",length=450,mode="determinate")
#E8.grid(row = 9, column = 2, pady=10)




window.mainloop()



