import pefile
import os
import hashlib
import datetime
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from customtkinter import CTk, CTkButton, CTkLabel, CTkFrame
import sys
import time
import platform
import hashlib
from time import sleep
from datetime import datetime
import customtkinter 
from PIL import Image, ImageTk
import requests
from io import BytesIO
import threading
import psutil
from plyer import notification

pe_file = None 

from datetime import datetime

def extract_strings():
    global pe_file  
    if not pe_file:
        return
    file_name = os.path.splitext(os.path.basename(pe_file))[0]
    txt_name = file_name + "-strings.txt"
    with open(txt_name, "w") as file:
        file_name2 = os.path.basename(pe_file)
        file.write("File Name: " + file_name2 + "\n")
        file_size = os.path.getsize(pe_file)
        file.write("File Size: " + str(file_size) + " bytes\n")
        pe = pefile.PE(pe_file)

        # md5 string
        md5_hash = hashlib.md5(pe.__data__).hexdigest()
        file.write("MD5: " + md5_hash + "\n")

        # pcasvc string
        pcasvc_string = (hex(pe.OPTIONAL_HEADER.SizeOfImage))
        file.write("PcaSvc: " + pcasvc_string + "\n")

        # dps string
        timestamp = pe.FILE_HEADER.TimeDateStamp
        timestamp_dt = datetime.utcfromtimestamp(timestamp)
        timestamp_str = timestamp_dt.strftime("%Y/%m/%d:%H:%M:%S")
        DPS_string = "!" + timestamp_str
        file.write("DPS: " + DPS_string + "\n")

def browse_file():
    global pe_file
    pe_file = filedialog.askopenfilename(filetypes=[("Executable Files", "*.exe")])
    if pe_file:
        file_label.configure(text=f"Selected File: {os.path.basename(pe_file)}") 
        extract_button.pack()  

def extract_and_display_strings():
    if not pe_file:
        return
    extract_strings()
    result_label.configure(text="Strings extracted successfully!", foreground="green")
    display_strings()

def display_strings():
    if not pe_file:
        return
    file_name = os.path.splitext(os.path.basename(pe_file))[0]
    txt_name = file_name + "-strings.txt"
    with open(txt_name, "r") as file:
        strings_text = file.read()
        if strings_text:
            strings_text_widget.pack() 
            strings_text_widget.delete("1.0", "end")  
            strings_text_widget.insert("1.0", strings_text)
        else:
            strings_text_widget.pack_forget()  

def cargar_imagen(url, width, height):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    image = image.resize((width, height))
    photo = ImageTk.PhotoImage(image)
    return photo

root = CTk()
root.geometry("650x400")
root.title('')
root.overrideredirect(True)
customtkinter.set_appearance_mode("dark")
frame = customtkinter.CTkFrame(master=root) 
root.attributes('-alpha', 0.99)

url_imagen_medio = 'https://cdn.discordapp.com/attachments/1212081700692172800/1238790320695541770/sWvEraX.png?ex=664090e4&is=663f3f64&hm=5c8ba26b945c02ac7ef327e589fa4fc20a5a6bb7967db45bb0ad619405223b12&'
width_imagen_medio = 750
height_imagen_medio = 300
imagen_cargar_medio = cargar_imagen(url_imagen_medio, width_imagen_medio, height_imagen_medio)
label_imagen_medio = CTkLabel(root, image=imagen_cargar_medio, text="", compound="top")
label_imagen_medio.place(relx=0.5, rely=0.45, anchor="center")

file_label = CTkLabel(master=root, text="No file selected")
file_label.place(relx=0.5, rely=0.85, anchor='center')
browse_button = CTkButton(master=root, text="Browse", command=browse_file)
browse_button.place(relx=0.5, rely=0.95, anchor='center')

extract_button = CTkButton(master=root, text="Extract String", corner_radius=10, fg_color='#470701', hover_color='#210300', command=extract_and_display_strings)
extract_button.place(relx=0.5, rely=0.77, anchor='center')
result_label = CTkLabel(master=root, text="")
strings_text_widget = customtkinter.CTkTextbox(root, height=10, width=40)
text_widget_font = ("Arial Black", 9)
strings_text_widget = customtkinter.CTkTextbox(root, height=10, width=40, font=text_widget_font)

root.mainloop()
