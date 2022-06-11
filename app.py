from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk
import cv2
import os 
from db import Database

db = Database('records.db')
break_flag = False

def populate_list():
    personnel_list.delete(0,END)
    for row in db.fetch():
        personnel_list.insert(END,row)

def show_frames():
    global img
        # Get the latest frame and convert into Image
    cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2image)
    # Convert image to PhotoImage
    imgtk = ImageTk.PhotoImage(image = img)
    camera.imgtk = imgtk
    camera.configure(image=imgtk)
    # Repeat after an interval to capture continiously
    camera.after(20, show_frames)
        


def take_photo():
    global new_file_name
    new_file_name = f'personnel_images\\{personnel_text.get()}' + '.jpg'
    img.save(new_file_name)
    

def add_personnel():
    if personnel_text.get() =='':
        messagebox.showerror('Error','Fields are null!')
        return

    db.insert(personnel_text.get(),new_file_name)
    personnel_list.delete(0,END)
    personnel_list.insert(END,(personnel_text.get(),new_file_name))
    populate_list()

def select_item(event):
    global selected_item
    index = personnel_list.curselection()[0]
    selected_item = personnel_list.get(index)

    personnel_entry.delete(0,END)
    personnel_entry.insert(0,selected_item[1])

def remove_personnel():
    db.remove(selected_item[0])
    os.remove(selected_item[2])
    populate_list()

# Window object
app = Tk()

# Personnel
personnel_text = StringVar()
personnel_label = Label(app,text='Personel Name and Surname',font=('bold',14),pady=20)
personnel_label.grid(row=0, column=0, sticky=W)
personnel_entry = Entry(app, textvariable=personnel_text)
personnel_entry.grid(row=0, column=1)

# Personnel List
personnel_list = Listbox(app,height=8,width=76,border=0)
personnel_list.grid(row=3,column=0,columnspan=3,rowspan=6,pady=20,padx=20)

# Create Scrollbar
scrollbar = Scrollbar()
scrollbar.grid(row=3,column=3)

# Set scrollbar to listbox
personnel_list.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=personnel_list.yview)

# Select item from listbox
personnel_list.bind('<<ListboxSelect>>',select_item)

# Buttons
add_button = Button(app,text='Add Personnel',width=12,command=add_personnel)
add_button.grid(row=2,column=0,pady=20)

remove_button = Button(app,text='Remove Personnel',width=20,command=remove_personnel)
remove_button.grid(row=2,column=2,pady=20)

add_button = Button(app,text='Take Photo',width=12,command=take_photo)
add_button.grid(row=2,column=3,pady=20)

app.title('Personel Management')
app.geometry('1000x500')

# Camera
camera = Label(app,width=350,height=350)
camera.grid(row=0,column=5,pady=20)
cap= cv2.VideoCapture(0)

# Populate data
populate_list()
show_frames()
# start program
app.mainloop()