import tkinter as tk
#import OS
#from PIL import ImageTk, Image

window = tk.Tk()
window.title("The Super Awesome Hangman Game")
window.geometry("300x300")


button = tk.Button(text="SinglePlayer").grid(row=0,column=1,padx=10,pady=10)

button2 = tk.Button(text="Multiplayer").grid(row=1,column=1,padx=10,pady=10)
button3 = tk.Button(text="Theme selection").grid(row=2,column=1,padx=10,pady=10)
button4 = tk.Button(text="Help").grid(row=3,column=1,padx=10,pady=10)
# frame = tk.Frame(master =window, width=500,height=500, bg='red')
# frame.pack()
tk.mainloop()