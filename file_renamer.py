import os
from tkinter import *
from tkinter import messagebox, filedialog, ttk



# Browse Files for GUI

def browse_files():
    folder = filedialog.askdirectory()
    if folder:
        # Update the folder path in the entry box
        entry_box.delete(0, END)
        entry_box.insert(0, folder)

        # Get list of all files in the folder (ignore subfolders)
        all_items = os.listdir(folder)
        only_files = [f for f in all_items if os.path.isfile(os.path.join(folder, f))]

        # Extract file extensions (e.g. '.txt', '.jpg'), remove duplicates
        extensions = {os.path.splitext(f)[1] for f in only_files if os.path.splitext(f)[1]}

        # Sort and update the dropdown values
        ext_option['values'] = sorted(list(extensions))

        # Optional: Set dropdown to default empty or first value
        ext_var.set('')  # or ext_var.set('.txt') to auto-select one

    
# Run Program for GUI

def run_rename():

    folder = entry_box.get().strip()
    ext = ext_var.get()
    prefix = prefix_option.get().strip()

    files = get_files(folder, ext)
    rename_pairs = preview_files(folder, files, prefix)

    file_listbox.delete(0, END)
    for old, new in rename_pairs:
        file_listbox.insert(END, f"{old} → {new}")


    if messagebox.askyesno("Confirm", "Rename these files?"):
        rename_files(rename_pairs, folder)

    # Get Files for GUI
def get_files(folder, ext):
    files = os.listdir(folder)
    only_files = [
        f for f in files
        if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith(ext)
    ]
    return only_files





# Preview Files for GUI

def preview_files(folder, files, prefix):
    rename_pairs = []
    prefix_name = prefix
    for i, filename in enumerate(files, start=1):
        original_filename = filename  # keep the raw original for renaming
        
        number = str(i).zfill(3)
        _, ext = os.path.splitext(original_filename)
        
        # Now clean the name only for new_name construction
        new_name = f"{prefix_name}_{number}{ext}"
        
  
        rename_pairs.append((original_filename, new_name))

    
    return rename_pairs

    # Rename Files for GUI
def rename_files(rename_pairs, folder_path):
    for old, new in rename_pairs:
        os.rename(
            os.path.join(folder_path, old),
            os.path.join(folder_path, new)
        )
    messagebox.showinfo('Success', 'All selected extension types have been renamed')




#Tkinter setup


window = Tk()
ext_var = StringVar()


window.geometry("600x600")
window.eval('tk::PlaceWindow . center')
window.configure(bg='lightblue')
window.title('File Renamer')

INPUT_WIDTH = 300
INPUT_HEIGHT = 30

# Header Frame (Title)

header_frame = Frame(window, bg='black')
header_frame.pack(pady=5)

title = Label(header_frame, text='File Renamer', font=('Ariel', 24), bg='lightblue')
title.pack(pady=5)

# Entry Frame (Folder Path, Browse Button,  Ext Option, Custom Prefix)

entry_frame = Frame(window, bg='lightblue', width=600, height=140)
entry_frame.pack(pady=5)
entry_frame.pack_propagate(False) 



    # Folder Path
entry_label = Label(entry_frame, text='Folder Path', font=('Ariel', 16), bg='lightblue')
entry_label.place(x=0, y=5)

folder_input_frame = Frame(entry_frame, width=INPUT_WIDTH, height=INPUT_HEIGHT)
folder_input_frame.place(x=150, y=0)
entry_box = ttk.Entry(folder_input_frame, font=('Ariel', 16))
entry_box.place(x=0, y=0, width=INPUT_WIDTH, height=INPUT_HEIGHT)


    # Browse Button
browse_button = Button(entry_frame, text='Browse', font=('Ariel', 12), command=browse_files, bg='lightblue')
browse_button.place(x=460, y=0, height=INPUT_HEIGHT)

    # File Extension
ext_label = Label(entry_frame, text='File Ext.', font=('Ariel', 16), bg='lightblue')
ext_label.place(x=0, y=50)

ext_input_frame = Frame(entry_frame, width=INPUT_WIDTH, height=INPUT_HEIGHT)
ext_input_frame.place(x=150, y=45)
ext_option = ttk.Combobox(ext_input_frame, textvariable=ext_var, font=('Ariel', 16), state='readonly')
ext_option.place(x=0, y=0, width=INPUT_WIDTH, height=INPUT_HEIGHT)

    # Custom Prefix
prefix_label = Label(entry_frame, text='Custom Prefix', font=('Ariel', 16), bg='lightblue')
prefix_label.place(x=0, y=95)

prefix_input_frame = Frame(entry_frame, width=INPUT_WIDTH, height=INPUT_HEIGHT)
prefix_input_frame.place(x=150, y=90)
prefix_option = ttk.Entry(prefix_input_frame, font=('Ariel', 16))
prefix_option.place(x=0, y=0, width=INPUT_WIDTH, height=INPUT_HEIGHT)


# Entry Frame 2 (Rename Button)
entry_frame_2 = Frame(window, bg='lightblue')
entry_frame_2.pack(pady=10)
rename_button = Button(entry_frame_2, text='Rename', command=run_rename, font=('Ariel', 16), bg='lightblue')
rename_button.pack(pady=5)

# Listbox_Frame (Listbox)
listbox_frame = Frame(window, bg='lightblue')
listbox_frame.pack(pady=(5, 10))
listbox_label = Label(listbox_frame, text='Preview Renamed Files', font=('Ariel', 16), bg='lightblue')
file_listbox = Listbox(listbox_frame, width=50, height=50, bg='lightgrey', font=('Ariel', 14))
listbox_label.pack(pady=(5, 10))
file_listbox.pack(pady=(5, 10))



window.mainloop()
