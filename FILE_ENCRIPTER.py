from os import name
from sys import path
import threading
from cryptography.fernet import Fernet, InvalidToken
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os.path

key = b''
key_ = b''
def ramdom_key():
    global key_
    key_ = Fernet.generate_key()
    Key_Entry.delete(0,"end")
    Key_Entry.config(state=NORMAL)
    Key_Entry.insert(0,key_[:len(key)-1])
    #Key_Entry.config(state="readonly")

def Start_Decrypt():
    global key
    if len(Key_Entry.get()) <= 42:
        messagebox.showerror(title="pocos caracteres",message="Debe tener 44 caracteres (más de eso será eliminado)")
    else:
        if len(Key_Entry.get()) >= 43:
                l = Key_Entry.get()
                Key_Entry.delete(0,"end")
                Key_Entry.insert(0,l[:43])
                key = str.encode(Key_Entry.get())
                
        if str(key) == "b''":
            messagebox.showwarning(message="Necesita una llave",title="Llave no definida")
        else:
            if str(key[len(key)-1:]) != "b'='":
                key = key + str.encode(("="))
        
        hilo2 = threading.Thread(target=Decrypt_file,daemon=True)
        hilo2.start()
    print(key)

def Decrypt_file():
    if root.filename != None:
        try:
            global key                
            Mas = Fernet(key)
            f = open(root.filename.name, "rb")
            data = f.read()
            data_un = Mas.decrypt(data)
            f.close()
            
            # Create 'decrypted' directory if it doesn't exist
            if not os.path.exists('decrypted'):
                os.makedirs('decrypted')
            
            done = True
            i = 0
            while done:
                name = os.path.join('decrypted', 'uncrypted.cry')
                if os.path.isfile(name):
                    name = os.path.join('decrypted', 'uncrypted.cry ' + str(i))
                if not os.path.isfile(name):
                    done = False
                else:
                    i = i + 1
            
            f = open(name, "wb")
            f.write(data_un)
            f.close()
        except InvalidToken:
            messagebox.showerror(title="Llave invalida", message="Introdujo una llave incorrecta")
        except:
            messagebox.showerror(title="ERROR", message="Error de descifrado")
        else:
            messagebox.showinfo(title="Completado", message="Cambie la extension del archivo a la original")

def start_encrypt():
    global key_
    if root.filename != None:
        print(len(Key_Entry.get()))
        if len(Key_Entry.get()) <= 42:
            messagebox.showerror(title="Pocos caracteres",message="Debe tener 44 caracteres (más de eso será eliminado)")
        else:
            if len(Key_Entry.get()) > 43:
                    l = Key_Entry.get()
                    Key_Entry.delete(0,"end")
                    Key_Entry.insert(0,l[:43])
                    key_ = str.encode(Key_Entry.get())
            if str(key_) == "b''":
                if len(Key_Entry.get()) >= 43:
                    key_ = str.encode(Key_Entry.get() + "=")
                else:
                    messagebox.showwarning(message="Necesita una llave",title="Llave no definida")
            else:
                if str(key_[len(key_)-1:]) != "b'='":
                    key_ = key_ + str.encode(("="))
            
        
        
            hilo = threading.Thread(target=encrypt_file,daemon=True)
            hilo.start()
        print(len(Key_Entry.get()))
        print(key_)

def encrypt_file():
    global key_
    
    print(key_)
    path = root.filename.name
    f = open(path, "rb")
    data = f.read()
    Mas = Fernet(key_)
    token = Mas.encrypt(data)
    f.close()
    
    # Create 'data' directory if it doesn't exist
    if not os.path.exists('encrypted'):
        os.makedirs('encrypted')
    
    done = True
    i = 0
    while done:
        name = os.path.join('encrypted', 'encrypted')
        if os.path.isfile(name):
            name = os.path.join('encrypted', 'encrypted ' + str(i))
        if not os.path.isfile(name):
            done = False
        else:
            i = i + 1
    
    f = open(name, "wb")
    f.write(token)
    f.close()
    
def openfile():
    root.filename = filedialog.askopenfile(initialdir="/Users",title="Select File",filetypes = (("all files",""),("all files","*.*")))
    if root.filename != None:
        print(root.filename.name)
        i = 0
        path = ""
        for c in root.filename.name:
            
            if i > 36:
                path = path + "..." 
                break
            path = path+c
            i=i+1
        
        Path_Varible.set("File:  "+path)
        Decrypt_buton.config(state=NORMAL)
        Encrypt_buton.config(state=NORMAL)
        #hilo = threading.Thread(target=encrypt_file,daemon=True)
        #hilo.start()
    else:
        Path_Varible.set("File: ")
        Decrypt_buton.config(state=DISABLED)
        Encrypt_buton.config(state=DISABLED)

root = Tk()
root.title("Encriptador de archivos")
Path_Varible = StringVar()
root.resizable(width=False, height=False)
root.geometry("400x300")

#Label(text="Key: "+str(key)).pack()

File_Path_Label = ttk.Label(root,textvariable=Path_Varible)
File_Path_Label.place(x=110,y=53)
Path_Varible.set("Archivo: ")

Open_File = ttk.Button(root,text="Seleccionar",command=openfile)
Open_File.place(x=30,y=50)

Encrypt_buton = ttk.Button(root,text="Encriptar",command=start_encrypt,state=DISABLED)
Encrypt_buton.place(x=30,y=120,width=160)

Decrypt_buton = ttk.Button(root,text="Desencriptar",command=Start_Decrypt,state=DISABLED)
Decrypt_buton.place(x=200,y=120,width=160)

Ramdon_key_buton = ttk.Button(root,text="Llave aleatoria",command=ramdom_key)
Ramdon_key_buton.place(x=30,y=180)

Key_Entry = ttk.Entry(root)#,state="readonly")
Key_Entry.place(x=120,y=181,width=240,height=23)

warn = ttk.Label(text="Nota: Si pierdes la llave aleatoria no podrás desencriptar el archivo")
warn.place(x=30,y=280)

root.mainloop()