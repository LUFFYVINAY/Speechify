import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Combobox
import pyttsx3
import pytesseract as tsrct
import pytesseract  as tsrct
tsrct.pytesseract.tesseract_cmd=r'C:\Users\Mayureshwar Shinde\AppData\Local\Tesseract-OCR\tesseract.exe'
poppler_path=r'C:\Program Files\poppler-0.67.0_x86\poppler-0.67.0\bin'
import PyPDF2
from pdf2image import convert_from_path
from PIL import Image

'''Image to Text'''
def img():
    img = Image.open(src)
    imgtext = tsrct.image_to_string(img)
    return imgtext

'''PDF to Text'''
def pdf():
    pdfpath=src
    global t
    status=messagebox.askyesno(title='Question',message='Is it a Scanned PDF?')
    book = open(pdfpath,'rb')
    pdfReader = PyPDF2.PdfFileReader(book)

    if(fromTxt.get(1.0, END)=="\n" and toTxt.get(1.0, END)=="\n"):
        start_pgno=0
        end_pgno=pdfReader.numPages
    else:
        start_pgno=int(fromTxt.get(1.0, END))-1 #0
        end_pgno=int(toTxt.get(1.0, END))
    
    if(status==False):
        for i in range(start_pgno, end_pgno):
            currPage=pdfReader.getPage(i)
            t=t+currPage.extractText()
    else:
        pages=convert_from_path(pdf_path=pdfpath,poppler_path=poppler_path)
        for i in range(start_pgno,end_pgno):
            currPage=tsrct.image_to_string(pages[i])
            t=t+currPage
    return t

def tt():
    fo=open(src,"r")
    ip=fo.read()
    fo.close()
    return ip

root=Tk()
root.title("IMG/PDF/TXT to Audiobook")
root.geometry("768x500")
root.resizable(False,False)
root.configure(bg="#292929")
sk = pyttsx3.init()
src=""
t=""
saveText=""
status=False

def get():
    l=src[len(src) - 1]
    if(l=='f'):
        t=pdf()
    elif(l=='g'):
        t=img()
    else:
        t=tt()
    return t

def pth():
    str=""
    idx=0
    for i in range(len(src)-1,0,-1):
        if(src[i]=='/'): break
        idx=idx+1
    for j in range(len(src)-(idx+1),len(src)-4):
        str=str+src[j]
    destination = filedialog.askdirectory()
    return destination+str+".mp3"

def asst():
    global src
    global t
    t=text_area.get(1.0, END)
    gender=gender_combobox.get()
    speed=speed_combobox.get()
    voices = sk.getProperty('voices')

    if(gender=='Male'): sk.setProperty('voice',voices[0].id)
    else: sk.setProperty('voice', voices[1].id)

    if(speed=="Fast"): sk.setProperty('rate',250)
    elif(speed=="Normal"): sk.setProperty('rate', 150)
    else: sk.setProperty('rate', 60)

    sk.asst(t)
    sk.runAndWait()
    src=""

def ready():
    global src
    global saveText
    t=saveText
    if(src==""): 
        t=text_area.get(1.0, END)
        src=filedialog.askdirectory()
        src=src+"/text.mp3"
    else: 
        src=pth()

    gender=gender_combobox.get()
    speed=speed_combobox.get()
    voices = sk.getProperty('voices')

    if(gender=='Male'): sk.setProperty('voice',voices[0].id)
    else: sk.setProperty('voice', voices[1].id)

    if(speed=="Fast"): sk.setProperty('rate',250)
    elif(speed=="Normal"): sk.setProperty('rate', 150)
    else: sk.setProperty('rate', 60)
    
    sk.save_to_file(t,src)
    sk.runAndWait()
    saveText=""
    src=""
    t=""

def setSourcePath():
    global src
    global t
    global saveText
    src=filedialog.askopenfilename()
    t=get()
    text_area.delete(1.0,"end")
    text_area.insert(1.0,t)
    saveText=t
    t=""

image_icon=PhotoImage(file="bin/speaker logo.png")
root.iconphoto(False,image_icon)

Top_frame=Frame(root,bg="#D7D7D7",width=999,height=100)
Top_frame.place(x=0,y=0)

Logo=PhotoImage(file="bin/speaker logo.png")
Label(Top_frame,image=Logo,bg="#D7D7D7").place(x=14,y=7)

Label(Top_frame,text="Speech",font="arial 25 bold", bg="#DCDCDC", fg="black").place(x=115,y=32)
Label(Top_frame,text="ify",font="arial 25 bold", bg="#DCDCDC", fg="#FF6D3F").place(x=234,y=32)

text_area=Text(root,font="Robote 20", bg="white",relief=GROOVE,wrap=WORD)
text_area.place(x=19,y=119,width=500,height=250)

Label(root,text="VOICE",font="arial 15 bold",bg='#292929',fg="white").place(x=599,y=120)
gender_combobox=Combobox(root,values=['Male','Female'],font="arial 14",state='r',width=10)
gender_combobox.place(x =569,y=160)
gender_combobox.set('Male')

Label(root,text="SPEED",font="arial 15 bold",bg='#292929',fg="white").place(x=597,y=220)
speed_combobox=Combobox(root,values=['Fast', 'Normal', 'Slow'],font="arial 14",state='r',width=10)
speed_combobox.place(x=569,y=260)
speed_combobox.set('Normal')

imageicon=PhotoImage(file="bin/speak.png")
btn=Button(root,text="Speak",compound=LEFT,image=imageicon,width=130,bg="#ffeed7",font="arial 14 bold",command=say)
btn.place(x=50,y=400)

imageicon2=PhotoImage(file="bin/download.png")
save=Button(root,text="Save",compound=LEFT,image=imageicon2,width=130,bg="#39c790",font="arial 14 bold",command=ready)
save.place(x=350,y=400)

b1=tk.Button(root,text=' Choose file ',font="bold",command=lambda:setSourcePath(),bg='skyblue')
b1.grid(row=0,column=0,padx=9,pady=18)
b1.place(x=574,y=338)

Label(root,text="From :",font="arial 11 bold",bg='#292929',fg="white").place(x=599,y=420)
fromTxt=Text(root,font="Robote 9 bold", bg="#a7a7a7",fg="black",relief=GROOVE,wrap=WORD)
fromTxt.place(x=655,y=419,width=27,height=19)

Label(root,text="To      :",font="arial 11 bold",bg='#292929',fg="white").place(x=599,y=457)
toTxt=Text(root,font="Robote 9 bold", bg="#a7a7a7",fg="black",relief=GROOVE,wrap=WORD)
toTxt.place(x=655,y=457,width=27,height=19)
root.mainloop()