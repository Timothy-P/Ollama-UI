# This will handle the menu, as I don't think a lot of people would prefer a headless experience.
"""if __name__ == "__main__":
    print("Please run \"main.py\" as opposed to this file.")
    exit()"""

# Imports
import tkinter as tk
from tkinter import ttk, messagebox
from interact import sendPrompt,listModels

# Starting window stuff
root = tk.Tk()
root.title("Testing Window")

# Funcs for adding more content -- not used yet(?)
def _addStyledLabel(target, content:str):
    return ttk.Label(target, text=content).pack()
def _addLabel(target, content:str):
    return tk.Label(target, text=content).pack()


# List models
def buttfunc(): 
    modelListL["text"] = ""
    for i in listModels(): 
        modelListL["text"] += i+"\n"
tk.Button(root, text="List models", command=buttfunc).pack()
modelListL = tk.Label(root)
modelListL.pack()



# Basic window stuff
root.geometry("600x600") # widthxlength (self note)
root.resizable(True, False)
try:
    root.iconbitmap('./assets/favicon.ico')
except tk.TclError as E:
    print(f"Couldn't set icon to ico. Error: {E}")
try:
    photo = tk.PhotoImage(file='./assets/favicon.png') #.png or .gif
    root.iconphoto(False, photo)
except tk.TclError as E:
    print(f"Couldn't set icon to png. Error: {E}")

# Keeping this for later
# window.attributes('-topmost', 1)





# Start of redo of the menu

#panedwindow=ttk.Panedwindow(root, orient=tk.HORIZONTAL)
#panedwindow.pack(fill=tk.BOTH, expand=True)
somethingfornow = tk.IntVar()
somethingfornow.set(300)
# Now works, DON'T TOUCH
container = ttk.Frame(root); container.pack(fill=tk.BOTH, expand=True)
framewidth = tk.IntVar(); framewidth.set(300)
frameheight = tk.IntVar(); frameheight.set(400)

container.columnconfigure(1, minsize=300); container.columnconfigure(0, minsize=300); container.rowconfigure(0, minsize=400)

# Unsure, might be used later
# Maybe selection of model? It would have to be a dropdown or something, maybe a listbox?
fram1 = tk.Frame(
    container,
    width=300,
    height=400,
    relief=tk.SUNKEN,
    background="#000000"
)
fram1.grid(row=0, column=0)
fram1.grid_propagate(False)  # Prevent shrinking to fit content

# Model selection section
ttk.Label(fram1, text="Model selection").pack()
ttk.Label(fram1, text="Select a model to interact with:").pack()
modelList = tk.StringVar()
modelList.set("Select a model")
modelSelect = ttk.Combobox(fram1, textvariable=modelList, state="readonly")
temp = []
for i in listModels():
    temp.append(i)
modelSelect["values"] = temp
modelSelect.pack()

# Response/interaction frame? -- Shrinks to fit content for whatever reason, fixing later
fram2 = tk.Frame(
    container,
    width=300,
    height=400,
    relief=tk.SUNKEN,
    bg="#deb887",
)
fram2.grid(row=0, column=1)

# Model messsaging/interacting section
messageCont = tk.StringVar()
ttk.Label(fram2, text="Message:")
field = ttk.Entry(fram2, textvariable=messageCont); field.pack()
def inputThing():
    print(f"Model: {modelList.get()}\nPrompt: {messageCont.get()}")
    result.config(text="Sent!")
    temp = sendPrompt(modelList.get(), messageCont.get())
    messageCont.set("")
    print("Response: "+temp)
    result.config(text=temp)
tk.Button(fram2, command=inputThing, text="Send").pack()
result = tk.Label(fram2, wraplength=450); result.pack()
fram2.grid_propagate(False)  # Prevent shrinking to fit content

container.grid_propagate(False)

#panedwindow.add(fram1, weight=1)
#panedwindow.add(fram2, weight=4)



def window_exit():
    print(container.winfo_width())
    fram2.grid_propagate(False)
    fram2["width"] = 300
    print(fram2.winfo_width())
    exit()
    # Going past this for quicker testing. If you see this, it means I forgot to remove it.
    # Make an issue if I add this to a GitHub repo.
    close = messagebox.askyesno("Exit?", "Are you sure you want to exit?")
    if close:
        exit()

root.protocol("WM_DELETE_WINDOW", window_exit)

# Word-wrap for response text
windowHeight = root.winfo_width()

# Dynamic based on window
def configure_handler(event):
    global windowHeight
    windowHeight = root.winfo_width()
    result["wraplength"] = windowHeight - 50
    framewidth.set(root.winfo_width() // 2)
    frameheight.set(windowHeight)


# Debugging stuff -- commented out because I don't know anymore
#debugtext = tk.StringVar()
#debug = tk.Entry(root, textvariable=debugtext); debug.pack()
#tk.Button(root, text="Run", command=lambda: print(eval(debugtext.get()))).pack()

root.bind("<Configure>", configure_handler)
root.overrideredirect(False)  # Still doesn't work on a Gnome desktop but does on a XFCE desktop

# Never gonna touch stuff
try:
    root.mainloop()
except KeyboardInterrupt:
    print("\nKeyboard interrupt triggered. Exiting...")
    exit()