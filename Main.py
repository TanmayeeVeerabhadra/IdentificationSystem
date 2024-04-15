from tkinter import messagebox
from tkinter import *
from tkinter import simpledialog
import tkinter
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from Block import *
from Blockchain import *
from hashlib import sha256
import os
import datetime
import webbrowser
import requests
import hashlib

main = Tk()
main.title("Fake Product Identification System")
main.geometry("1000x1000")

global filename

blockchain = Blockchain()
if os.path.exists('blockchain_contract.txt'):
    with open('blockchain_contract.txt', 'rb') as fileinput:
        blockchain = pickle.load(fileinput)
    fileinput.close()
def addProduct():
    global filename
    text.delete('1.0', END)
    c=0
    d=0
    pid = tf1.get()
    name = tf2.get()
    user = tf3.get()
    address = tf4.get()
    if len(pid) > 0 and len(name) > 0 and len(user) > 0 and len(address) > 0:
        for i in range(len(blockchain.chain)-1,-1,-1):
            if i > 0:
                b = blockchain.chain[i]
                data = b.transactions[0]
                arr = data.split("#")
                if arr[0] == pid:
                    c=1
                    break
        if(c==0):
                qr_code_url = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=" + pid
                response = requests.get(qr_code_url)

                if response.status_code == 200:
                    qr_code_data = response.content
                    
                    directory = r"E:/FinalYearProject/FPI/FPIS/Source code/IdentificationSystem/barcodes"
                    
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    
                    file_path = os.path.join(directory, pid + ".png")  
                    
                    with open(file_path, "wb") as f:
                        f.write(qr_code_data)
                    
                    print("QR code downloaded successfully at", file_path)
                    digital_signature = hashlib.sha256(qr_code_data).hexdigest()
                    current_time = datetime.datetime.now() 
                    data = pid+"#"+name+"#"+user+"#"+address+"#"+str(current_time)+"#"+digital_signature
                    blockchain.add_new_transaction(data)
                    hash = blockchain.mine()
                    b = blockchain.chain[len(blockchain.chain)-1]
                    text.insert(END,"Product is successfully Registered\n")
                    text.insert(END,"Blockchain Previous Hash : "+str(b.previous_hash)+"\nBlock No : "+str(b.index)+"\nCurrent Hash : "+str(b.hash)+"\n")
                    text.insert(END,"Barcode Blockchain Digital Signature : "+str(digital_signature)+"\n\n")
                    blockchain.save_object(blockchain,'blockchain_contract.txt')
                    tf1.delete(0, 'end')
                    tf2.delete(0, 'end')
                    tf3.delete(0, 'end')
                    tf4.delete(0, 'end')
                else:
                    print("Failed to download QR code. Status code:", response.status_code)

        else:
            text.insert(END,"Product Id Already Exists")
    else:
        text.insert(END,"Please enter all details")

def authenticateProduct():
    text.delete('1.0', END)
    filename = askopenfilename(initialdir = "barcodes")
    with open(filename,"rb") as f:
        bytes = f.read()
    f.close()
    pid = tf1.get()
    digital_signature = sha256(bytes).hexdigest()
    flag = True
    if len(pid) > 0:
        for i in range(len(blockchain.chain)-1,-1,-1):
            if i > 0:
                b = blockchain.chain[i]
                data = b.transactions[0]
                arr = data.split("#")
                if arr[0] == pid:
                    if arr[5] == digital_signature:
                        output = ''
                        text.insert(END,"This is a Genuine Product \n ")
                        text.insert(END,"Details extracted from Blockchain after Validation\n\n")
                        text.insert(END,"Product ID                   : "+arr[0]+"\n")
                        text.insert(END,"Product Name                 : "+arr[1]+"\n")
                        text.insert(END,"Company Name         : "+arr[2]+"\n")
                        text.insert(END,"Contact Details              : "+arr[3]+"\n")
                        text.insert(END,"Scan Date & Time             : "+arr[4]+"\n")
                        text.insert(END,"Product Barcode Digital Sign : "+arr[5]+"\n")
                        output='<html><body><table border=1>'
                        output+='<tr><th>Block No</th><th>Product ID</th><th>Product Name</th><th>Company Name</th><th>Contact Details</th><th>Scan Date & Time</th>'
                        output+='<th>Product Barcode Digital Signature</th></tr>'
                        output+='<tr><td>'+str(i)+'</td><td>'+arr[0]+'</td><td>'+arr[1]+'</td><td>'+arr[2]+'</td><td>'+arr[3]+'</td><td>'+arr[4]+'</td><td>'+arr[5]+'</td></tr>'
                        f = open("output.html", "w")
                        f.write(output)
                        f.close()
                        webbrowser.open("output.html",new=1)
                        flag = False
                        break
    if flag:
        text.insert(END,"This is a Fake Product")
            

def searchProduct():
    text.delete('1.0', END)
    pid = tf1.get()
    flag = True
    if len(pid) > 0:
        for i in range(len(blockchain.chain)-1,-1,-1):
            if i > 0:
                b = blockchain.chain[i]
                data = b.transactions[0]
                arr = data.split("#")
                if arr[0] == pid:
                    output = ''
                    text.insert(END,"Product Details extracted from Blockchain using Product ID : "+pid+"\n\n")
                    text.insert(END,"Product ID                   : "+arr[0]+"\n")
                    text.insert(END,"Product Name                 : "+arr[1]+"\n")
                    text.insert(END,"Company Name         : "+arr[2]+"\n")
                    text.insert(END,"Contact Details              : "+arr[3]+"\n")
                    text.insert(END,"Scan Date & Time             : "+arr[4]+"\n")
                    text.insert(END,"Product Barcode Digital Sign : "+arr[5]+"\n")
                    output='<html><body><table border=1>'
                    output+='<tr><th>Block No</th><th>Product ID</th><th>Product Name</th><th>Company Name</th><th>Contact Details</th><th>Scan Date & Time</th>'
                    output+='<th>Product Barcode Digital Signature</th></tr>'
                    output+='<tr><td>'+str(i)+'</td><td>'+arr[0]+'</td><td>'+arr[1]+'</td><td>'+arr[2]+'</td><td>'+arr[3]+'</td><td>'+arr[4]+'</td><td>'+arr[5]+'</td></tr>'
                    f = open("output.html", "w")
                    f.write(output)
                    f.close()
                    webbrowser.open("output.html",new=1)
                    flag = False
                    break
    if flag:
        text.insert(END,"Given product id does not exists")

def searchProductbyDS():
    text.delete('1.0', END)
    ds = tf5.get()
    flag = True
    if len(ds) > 0:
        for i in range(len(blockchain.chain)-1,-1,-1):
            if i > 0:
                b = blockchain.chain[i]
                data = b.transactions[0]
                arr = data.split("#")
                if arr[5] == ds:
                    output = ''
                    text.insert(END,"Product Details extracted from Blockchain using Digital Signature : "+ds+"\n\n")
                    text.insert(END,"Product ID                   : "+arr[0]+"\n")
                    text.insert(END,"Product Name                 : "+arr[1]+"\n")
                    text.insert(END,"Company Name         : "+arr[2]+"\n")
                    text.insert(END,"Contact Details              : "+arr[3]+"\n")
                    text.insert(END,"Scan Date & Time             : "+arr[4]+"\n")
                    text.insert(END,"Product Barcode Digital Sign : "+arr[5]+"\n")
                    output='<html><body><table border=1>'
                    output+='<tr><th>Block No</th><th>Product ID</th><th>Product Name</th><th>Company Name</th><th>Contact Details</th><th>Scan Date & Time</th>'
                    output+='<th>Product Barcode Digital Signature</th></tr>'
                    output+='<tr><td>'+str(i)+'</td><td>'+arr[0]+'</td><td>'+arr[1]+'</td><td>'+arr[2]+'</td><td>'+arr[3]+'</td><td>'+arr[4]+'</td><td>'+arr[5]+'</td></tr>'
                    f = open("output.html", "w")
                    f.write(output)
                    f.close()
                    webbrowser.open("output.html",new=1)
                    flag = False
                    break
    if flag:
        text.insert(END,"Given Digital Signature doesnot exist")

def uploadQR():
    text.delete('1.0', END)
    filename = askopenfilename(initialdir = "barcodes")
    with open(filename,"rb") as f:
        bytes = f.read()
    f.close()
    digital_signature = sha256(bytes).hexdigest()
    for i in range(len(blockchain.chain)-1,-1,-1):
        if i > 0:
            b = blockchain.chain[i]
            data = b.transactions[0]
            arr = data.split("#")
            if arr[5] == digital_signature:
                output = ''
                text.insert(END,"Product Details extracted from Blockchain uploading Digital Signature : "+digital_signature+"\n\n")
                text.insert(END,"Product ID                   : "+arr[0]+"\n")
                text.insert(END,"Product Name                 : "+arr[1]+"\n")
                text.insert(END,"Company Name         : "+arr[2]+"\n")
                text.insert(END,"Contact Details              : "+arr[3]+"\n")
                text.insert(END,"Scan Date & Time             : "+arr[4]+"\n")
                text.insert(END,"Product Barcode Digital Sign : "+arr[5]+"\n")
                output='<html><body><table border=1>'
                output+='<tr><th>Block No</th><th>Product ID</th><th>Product Name</th><th>Company Name</th><th>Contact Details</th><th>Scan Date & Time</th>'
                output+='<th>Product Barcode Digital Signature</th></tr>'
                output+='<tr><td>'+str(i)+'</td><td>'+arr[0]+'</td><td>'+arr[1]+'</td><td>'+arr[2]+'</td><td>'+arr[3]+'</td><td>'+arr[4]+'</td><td>'+arr[5]+'</td></tr>'
                f = open("output.html", "w")
                f.write(output)
                f.close()
                webbrowser.open("output.html",new=1)
                flag = False
                break
    if flag:
        text.insert(END,"The Product with the QR code doesnot exist")

def updateProduct():
    global filename
    text.delete('1.0', END)
    filename = askopenfilename(initialdir = "barcodes")
    with open(filename,"rb") as f:
        bytes = f.read()
    f.close()
    c=0
    pid = tf1.get()
    name = tf2.get()
    user = tf3.get()
    address = tf4.get()
    digital_signature = sha256(bytes).hexdigest()
    if len(pid) > 0 and len(name) > 0 and len(user) > 0 and len(address) > 0:
        for i in range(len(blockchain.chain)-1,-1,-1):
            if i > 0:
                b = blockchain.chain[i]
                data = b.transactions[0]
                arr = data.split("#")
                if arr[0] == pid and arr[5]==digital_signature:
                    c=1
                    break
        if(c==1):
            current_time = datetime.datetime.now() 
            data = pid+"#"+name+"#"+user+"#"+address+"#"+str(current_time)+"#"+digital_signature
            blockchain.add_new_transaction(data)
            hash = blockchain.mine()
            b = blockchain.chain[len(blockchain.chain)-1]
            text.insert(END,"Product is successfully updated \n")
            text.insert(END,"Blockchain Previous Hash : "+str(b.previous_hash)+"\nBlock No : "+str(b.index)+"\nCurrent Hash : "+str(b.hash)+"\n")
            text.insert(END,"Barcode Blockchain Digital Signature : "+str(digital_signature)+"\n\n")
            blockchain.save_object(blockchain,'blockchain_contract.txt')
            tf1.delete(0, 'end')
            tf2.delete(0, 'end')
            tf3.delete(0, 'end')
            tf4.delete(0, 'end')
        else:
            text.insert(END,"Product Id and its Qr doesn't match")
    else:
        text.insert(END,"Please enter all details")   
    

font = ('times', 15, 'bold')
title = Label(main, text='Fake Product Identification System')
title.config(bg='yellow', fg='blue')  
title.config(font=font)           
title.config(height=3, width=120)       
title.place(x=0,y=5)

font1 = ('times', 13, 'bold')

l1 = Label(main, text='Product ID :')
l1.config(font=font1)
l1.place(x=50,y=100)

tf1 = Entry(main,width=20)
tf1.config(font=font1)
tf1.place(x=240,y=100)

l2 = Label(main, text='Product Name :')
l2.config(font=font1)
l2.place(x=50,y=150)

tf2 = Entry(main,width=20)
tf2.config(font=font1)
tf2.place(x=240,y=150)

l3 = Label(main, text='Product Company:')
l3.config(font=font1)
l3.place(x=50,y=200)

tf3 = Entry(main,width=60)
tf3.config(font=font1)
tf3.place(x=240,y=200)

l4 = Label(main, text='Contact Details:')
l4.config(font=font1)
l4.place(x=50,y=250)

tf4 = Entry(main,width=80)
tf4.config(font=font1)
tf4.place(x=240,y=250)

l5 = Label(main, text='Digital Signature')
l5.config(font=font1)
l5.place(x=500,y=100)

tf5 = Entry(main,width=60)
tf5.config(font=font1)
tf5.place(x=650,y=100)

saveButton = Button(main, text="Register Product", command=addProduct)
saveButton.place(x=50,y=310)
saveButton.config(font=font1)

searchButton = Button(main, text="Product Details", command=searchProduct)
searchButton.place(x=250,y=310)
searchButton.config(font=font1)

scanButton = Button(main, text="Verify Product", command=authenticateProduct)
scanButton.place(x=450,y=310)
scanButton.config(font=font1)

scanButton = Button(main, text="Update Product", command=updateProduct)
scanButton.place(x=650,y=310)
scanButton.config(font=font1)

scanButton = Button(main, text="Details by DS", command=searchProductbyDS)
scanButton.place(x=850,y=310)
scanButton.config(font=font1)

scanButton = Button(main, text="Upload DS", command=uploadQR)
scanButton.place(x=1050,y=310)
scanButton.config(font=font1)

font1 = ('times', 13, 'bold')
text=Text(main,height=15,width=120)
scroll=Scrollbar(text)
text.configure(yscrollcommand=scroll.set)
text.place(x=10,y=350)
text.config(font=font1)

main.config(bg='pink')
main.mainloop()
