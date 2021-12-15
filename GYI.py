from tkinter import *
import cv2
from subprocess import Popen
import tensorflow as tf
import numpy as np
import datetime
from datetime import datetime
import csv
from PIL import Image,ImageTk
from tkinter import filedialog
def _from_rgb(rgb):
    return "#%02x%02x%02x" % rgb 
root=Tk("Food Waste Classifier")
root.title("Food Waste Classifier")
root.geometry("1920x1080")
root.configure(background=_from_rgb((255,178,102)))
#Image part starts
img1=Image.open("KPMG.jpeg").resize((250,125), Image.ANTIALIAS)
img2=Image.open("ihcl3.jpeg").resize((250,125), Image.ANTIALIAS)
image1=ImageTk.PhotoImage(img1)
image2=ImageTk.PhotoImage(img2)
label1 =Label(image=image1,background=_from_rgb((255,178,102)))
label1.image = image1
label2 =Label(image=image2,background=_from_rgb((255,178,102)))
label2.image = image2
label2.grid(row=5,column=2,padx=(0,150),pady=(100,0))
label1.grid(row=5,column=4,padx=(150,0),pady=(100,0))
#Image part ends
b=0 
TextLabel=Label(root,text="Please click or upload a picture", background=_from_rgb((255,178,102)), fg="white",font=("Arial", 25)).grid(row=1,column=3,pady=(90,20))
def write(p):
    k='Bread'
    if p==0:
        k=("Bread")
    if p==1:
        k=("Dairy")
    if p==2:
        k=("Dessert")
    if p==3:
        k=("Egg")
    if p==4:
        k=("Fried product")
    if p==5:
        k=("Meat")
    if p==6:
        k=("Noodles")
    if p==7:
        k=("Rice")
    if p==8:
        k=("Seafood")
    if p==9:
        k=("Soup")
    if p==10:
        k=("Vegetable")
    return k
def doeverything(filename):
    model=tf.keras.models.load_model("fclass.h5")
    imagein=Image.open(filename)
    imagein=imagein.resize((250,250))
    img = np.array(imagein)
    z=model.predict(img[None,:,:])
    p=z[0]
    #load the model and test image on it ends
    #CSV part start
    fields=['Food_Type', 'Weight', 'Date+Time', 'Carbon_Footprint']
    name="GarbageRecords.csv"
    """with open(name, 'w') as csvfile: 
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(fields)"""
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    lis=[write(p[0]),'0',dt_string,'0']
    with open(name, 'a') as csvfile: 
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow(lis) 
        #csvwriter.close()
    #csv part end
    return write(p[0])
def click1():
    filename1 = filedialog.askopenfilename(initialdir = "/",title = "Select a File",filetypes = (("Image files","*.jpg*"),("all files", "*.*")))
    """ButtonLabel1=Button(root,text="Select Image",state=DISABLED).pack()
    ButtonLabel2=Button(root,text="Click Image",state=DISABLED).pack()
    ButtonLabel3=Button(root,text="View CSV File",state=DISABLED).pack()"""
    Textl=Label(root,text="Detected "+doeverything(filename1), background="green", fg="white",font=("Arial", 15)).grid(row=6,column=3)
def click3():
    p = Popen('GarbageRecords.csv', shell=True)
    """ButtonLabel1=Button(root,text="Select Image",state=DISABLED).pack()
    ButtonLabel2=Button(root,text="Click Image",state=DISABLED).pack()
    ButtonLabel3=Button(root,text="View CSV File",state=DISABLED).pack()"""
def click2():
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("test")
    img_counter = 0
    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test", frame)
        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            # SPACE pressed
            img_name = "opencv_frame_{}.jpg".format(img_counter)
            cv2.imwrite(img_name, frame)
            img_counter += 1
    cam.release()
    cv2.destroyAllWindows()
    """ButtonLabel1=Button(root,text="Select Image",state=DISABLED).pack()
    ButtonLabel2=Button(root,text="Click Image",state=DISABLED).pack()
    ButtonLabel3=Button(root,text="View CSV File",state=DISABLED).pack()"""
    Textl=Label(root,text="Detected "+doeverything("opencv_frame_0.jpg"), background="green", fg="white",font=("Arial", 15)).grid(row=6,column=3)
h=5
w=25
bg=_from_rgb((36, 83, 151))
ButtonLabel1=Button(root,text="Select Image",command=click1,height=h,width=w,background=bg,fg='white',font=('Arial',12)).grid(row=2,column=2,padx=(0,100),pady=(50,0))
ButtonLabel2=Button(root,text="Click Image",command=click2,height=h,width=w,background=bg,fg='white',font=('Arial',12)).grid(row=2,column=4,padx=(100,00),pady=(50,0))
ButtonLabel3=Button(root,text="View CSV File",command=click3,height=h,width=w,background=bg,fg='white',font=('Arial',12)).grid(row=2,column=3,pady=(50,0))
root.mainloop()