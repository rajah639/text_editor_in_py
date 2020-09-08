import os
from tkinter import *
from tkinter import filedialog
from tkinter import font\


root = Tk()

root.title('My title!')
# Icon bitmap location uncomment and add the path to your icon
# root.iconbitmap(./your/icon/path)
root.geometry("1200x660")

# set variable for open file name
global open_status_name
open_status_name = False

# sets variable for selected text
global selected
selected = False

# Create New File Func
def new_file():
    my_text.delete("1.0", END)
    root.title('New File')
    status_bar.config(text="New File        ")

    global open_status_name
    open_status_name = False

# Open Files
def open_file():
    my_text.delete("1.0", END)

    # Grab filename
    text_file = filedialog.askopenfilename(initialdir="", title="Open File", filetypes=(("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Python Files", "*.py"), ("All Files", "*.*")))
    
    # check to see if ther is a filename
    if text_file:
        # Make filename global so we can access it later
        global open_status_name
        open_status_name = text_file

    # Update Status Bar
    name = text_file
    # Gives just the files name
    name = os.path.basename(name)
    status_bar.config(text=f'{name}        ')
    root.title(f'{name} - File')

    # Open The File
    text_file = open(text_file, 'r')
    stuff = text_file.read()
    # Add file to textbox
    my_text.insert(END, stuff)
    # close the opened file
    text_file.close()

# Save File
def save_file():
    global open_status_name
    if open_status_name:
        # Save the file
        text_file = open(open_status_name, 'w')
        text_file.write(my_text.get(1.0, END))
        # Close the file
        text_file.close()
        # Put status update or popup code


        status_bar.config(text=f"Saved: {open_status_name}        ") 
    else:
        save_as_file()




# Save As Function
def save_as_file():
    text_file = filedialog.asksaveasfilename(defaultextension=".*", initialdir="", title="Save File", filetypes=(("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Python Files", "*.py"), ("All Files", "*.*")))
    if text_file:
        name = text_file
        # 
        # Gives just the files name
        name = os.path.basename(name)
        status_bar.config(text=f"Saved: {name}        ")
        root.title(f'{name} - Text Place')

        # Save the file
        text_file = open(text_file, 'w')
        text_file.write(my_text.get(1.0, END))
        # Close the file
        text_file.close()


def cut_text(e):
    global selected
    # Check if keyboard shortcut is used
    if e :
        selected = root.clipboard_get()
    else:
        if my_text.selection_get():
            # Grab Selected text from text box
            selected = my_text.selection_get()
            # Delete Selected text from text box
            my_text.delete("sel.first", "sel.last")
            # Clear the clipboard then append
            root.clipboard_clear()
            root.clipboard_append(selected)

def copy_text(e):
    global selected
    # check to see if we used a keyboard shortcut
    if e:
        selected = root.clipboard_get()

    if my_text.selection_get():
        selected = my_text.selection_get()
        root.clipboard_clear()
        root.clipboard_append(selected)

def paste_text(e):
    global selected
    # Check to see if the keyboard shortcut is used
    if e:
        selected = root.clipeboard_get()
    else:
        if selected:
            position = my_text.index(INSERT)
            my_text.insert(position, selected)


# Create Main Frame
my_frame = Frame(root)
my_frame.pack(pady=5)

# Create Scroll Bar
text_scroll = Scrollbar(my_frame)
text_scroll.pack(side=RIGHT, fill=Y)

# Create Text Box
my_text = Text(my_frame, width=97, height=25, font=("Helvetica", 16), selectbackground="yellow", selectforeground="black", undo=True, yscrollcommand=text_scroll.set)
my_text.pack()

# Confi our scroll bar
text_scroll.config(command=my_text.yview)

# create menu 
my_menu = Menu(root)
root.config(menu=my_menu)

# Add file menu
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(labe="Save As", command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Add Edit Menu
edit_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut", command=lambda: cut_text(False), accelerator="Ctrl+X")
edit_menu.add_command(label="Copy", command=lambda: copy_text(False), accelerator="Ctrl+C")
edit_menu.add_command(label="Paste", command=lambda: paste_text(False), accelerator="Ctrl+V")
# edit_menu.add_seperator()
edit_menu.add_command(label="Undo", command=my_text.edit_undo, accelerator="Ctrl+Z")
edit_menu.add_command(label="Redo", command=my_text.edit_redo, accelerator="Ctrl+Y")

# Add status bar to the bottom of the app
status_bar = Label(root, text='Ready        ', anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=5)



# Edit Bindings

root.bind('<Control-Key-x>', cut_text)
root.bind('<Control-Key-c>', copy_text)
root.bind('<Control-Key-v>', paste_text)


root.mainloop()