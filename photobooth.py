#!/usr/local/bin/python
#Written by Mari DeGrazia
#arizona4n6@gmail.com 
#Based off the All Seeing Pi by the Rasbperry Pi Foundation

from gpiozero import Button
from picamera import PiCamera
from time import gmtime, strftime,sleep
from overlay_functions import *
from shutil import copyfile
import subprocess
import Tkinter
import tkMessageBox
import ttk
from PIL import Image, ImageTk
import pygame
from smtplib import SMTP
from smtplib import SMTPException
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import time
from multiprocessing import Process
import cwiid

###############CHANGE ME###########################
printer_MAC = "70:2C:1F:25:77:F3"
my_email = 'sonwright@gmail.com' # must be gmail account. 
my_email_password = 'StrongPassword'
subject = 'Alexandra\'s First Luau'
####################################################

def start_wii_script():
    cmd = "sudo python /home/pi/Pi-Photobooth/photobooth_wii.py &"
    k = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    message =  k.communicate(input)
    print message[0]

def kill_keyboard():
    cmd = "sudo pkill -f matchbox-keyboard"
    k = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    message =  k.communicate(input)
    return

def next_overlay():
    global overlay
    global current_position
    pygame.mixer.music.load("/home/pi/Pi-Photobooth/audio/slide_and_click.mp3")
    pygame.mixer.music.play()
    current_position = current_position + 1
    if current_position >= len(overlays):
        current_position = 0
    overlay = overlays[current_position]
    if overlay == "":
        remove_overlays(camera)
    else:
        preview_overlay(camera, overlay)

def prev_overlay():
    global overlay
    global current_position
    pygame.mixer.music.load("/home/pi/Pi-Photobooth/audio/slide_and_click.mp3")
    pygame.mixer.music.play()
    
    current_position = current_position - 1
    overlay = overlays[current_position]
    if overlay == "":
        remove_overlays(camera)
    else:
        preview_overlay(camera, overlay)

def take_picture():
    global output
    global latest_photo
    global current_position
    global overlay
    
    pygame.mixer.music.load("/home/pi/Pi-Photobooth/audio/CameraClick.mp3")
    pygame.mixer.music.play()
    output = strftime("/home/pi/Pi-Photobooth/photos/image-%d-%m_%H_%M_%S.png", gmtime())
    time.sleep(.3)
    camera.stop_preview()
    
    remove_overlays(camera)
    camera.hflip = False
    camera.capture(output)
    
    if overlay:
        output_overlay(output, overlays[current_position])
    else:
        output_no_overlay(output)
    size = 400, 400
    gif_img = Image.open(output)
    gif_img.thumbnail(size, Image.ANTIALIAS)
    
    gif_img.save(latest_photo, 'gif')
    loadImage(latest_photo)
    camera.hflip = True
    just_taken = True

def new_picture():
    global overlay  
    kill_keyboard()
    camera.start_preview()
    time.sleep(1)
    copyfile('/home/pi/Pi-Photobooth/images/loading.gif', '/home/pi/Pi-Photobooth/images/latest.gif')    
    remove_overlays(camera)
    current_position = 0
    loadImage(latest_photo)
    overlay = ""
    
def remove():
    global overlay
    remove_overlays(camera)
    overlay = ""

def print_photo():
    global printer_MAC
    kill_keyboard()

    top = Tkinter.Tk()
    top.title("Printing")
    msg = Tkinter.Label(top, text="Sending to printer. Please wait 1-2 minutes.",width=50,background='#B1B1B1')
    msg.pack()
    top.geometry("%dx%d%+d%+d" % (400, 100, 250, 125))
    top.configure(background='#B1B1B1')
    center(top)
   
    master.config(cursor="watch")
    top.config(cursor="watch")
    master.update()
    top.update()
 
    print ("Print photo")
    pp = subprocess.Popen(["obexftp --nopath --noconn --uuid none --bluetooth " +  printer_MAC +  " --channel 4 -p " + output],shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    message =  pp.communicate(input)
    print (str(message))
    master.config(cursor="")
    top.destroy()
    msg = "failed"
    if msg.encode('utf-8') in message[0]:
        tkMessageBox.showerror("Error", "Print failed. Check paper or make sure printer is on and paired and print again")
        
    else:
        tkMessageBox.showinfo("Printing", "Photo successfully sent. Now printing...")
        
    return True
    
def get_email_address():
    
    top = Tkinter.Tk()
    top.title("Email")
    msg = Tkinter.Label(top, text="Enter Email Address.",width=50,background='#B1B1B1')
    msg.pack()
    ttk.e = Tkinter.Entry(top,width=50)
    ttk.e.pack()
    
    b4 = Tkinter.Button(top, text='Send', command=lambda: send_picture(top))
    b4.pack()
   
    top.geometry("%dx%d%+d%+d" % (400, 100, 250, 125))
    top.configure(background='#B1B1B1')
    lower(top)
    subprocess.Popen(['matchbox-keyboard'])
    return

def send_picture(toplevel):
    global output
    global my_email
    global my_email_password
    global subject
    master.config(cursor="watch")
    master.config(cursor="watch")
    
    #kill keyboard if its still there
    email_address = ttk.e.get()
    toplevel.destroy()
    kill_keyboard()
    print email_address
    
    toaddr = email_address
    me = my_email # redacted
    
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = my_email
    msg['To'] = toaddr
    msg.preamble = "Photo @ " 

    fp = open(output, 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    msg.attach(img)

    try:
       s = smtplib.SMTP('smtp.gmail.com',587)
       s.ehlo()
       s.starttls()
       s.ehlo()
       s.login(user = my_email,password = my_email_password)
       
       s.sendmail(me, toaddr, msg.as_string())
       s.quit()
       master.config(cursor="")
       tkMessageBox.showinfo("Info", "Email sent")
 
    except SMTPException as error:
          master.config(cursor="")
          tkMessageBox.showerror("Error", "Error: unable to send email :  {err}".format(err=error))
          print "Error: unable to send email :  {err}".format(err=error)

def center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2

    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

def lower(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2

    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y+150)))

    
def loadImage(latest_photo):
    global picture3
    picture3 = Tkinter.PhotoImage(file=latest_photo)
    c.itemconfigure(picture2, image = picture3)

  
current_position = 0
pygame.mixer.init()


#reset image
copyfile('/home/pi/Pi-Photobooth/images/loading.gif', '/home/pi/Pi-Photobooth/images/latest.gif') 

# next_overlay_btn = Button(23)
# take_pic_btn = Button(11)


# next_overlay_btn.when_pressed = next_overlay
# take_pic_btn.when_pressed = take_picture

camera = PiCamera()
camera.resolution = (800, 480)
camera.hflip = True
overlay = "alex_001"

camera.start_preview()
output = ""
latest_photo = '/home/pi/Pi-Photobooth/images/latest.gif'

# p = Process(target=start_wii_script)
# p.start()
   

# next_overlay_Wii_button = Button(17)
# picture_Wii_button = Button(9)
# prev_overlay_Wii_Button = Button(21)
# newpic_Wii_button = Button(20)
# rem_overlays_Wii_button = Button(16)
# 
# newpic_Wii_button.when_pressed = new_picture
# next_overlay_Wii_button.when_pressed = next_overlay
# prev_overlay_Wii_Button.when_pressed = prev_overlay
# picture_Wii_button.when_pressed = take_picture
# 
# 
# rem_overlays_Wii_button.when_pressed = remove
master = Tkinter.Tk()
master.wm_title(subject)
master.attributes("-fullscreen", True)
c = Tkinter.Canvas(master, width=400, height=300)

picture = Tkinter.PhotoImage(file=latest_photo)
picture2 = c.create_image(200,150,image=picture)
c.pack()

photo1 = Tkinter.PhotoImage(file='/home/pi/Pi-Photobooth/images/button_new.gif')
photo2 = Tkinter.PhotoImage(file='/home/pi/Pi-Photobooth/images/button_print.gif')
photo3 = Tkinter.PhotoImage(file='/home/pi/Pi-Photobooth/images/button_email.gif')

b1 = Tkinter.Button(master, text="New Picture",command=take_picture,image=photo1)
b2 = Tkinter.Button(master, text="Print Picture",command=print_photo,image=photo2)
b3= Tkinter.Button(master, text="Email Picture",command=get_email_address,image=photo3)
#b4 = Tkinter.Button(master, text="Take Picture",command=take_picture, image=photo1)

b1.image = photo1
b2.image = photo2
b3.image = photo3
#b4.image = photo1

b1.pack()
b2.pack()
b3.pack()
#b4.pack()
print "about to take picture"
take_picture()
print "after take_picture"

Tkinter.mainloop( )


