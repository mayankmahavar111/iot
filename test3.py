import urllib
import json
import pyttsx3
import os

engine = pyttsx3.init()


def speak(text):
    print text
    engine.say(" finger shown at the camera is {}".format(text))
    engine.runAndWait()


def check():
    x=os.getcwd()
    for name  in os.listdir(x):
        if name == "entry.txt":
            return
    f=open('entry.txt','w')
    f.write("0")
    f.close()

def getEntry():
    f=open('entry.txt','r')
    entry=f.read()
    f.close()
    entry=entry.split("\n")[0]
    return int(entry)

def incEntry(entry):
    f=open('entry.txt','w')
    f.write(str(entry+1))
    f.close()



def display(result):
    for x in result:
        speak(x)
        incEntry(getEntry())


def get():
    data=urllib.urlopen("https://api.thingspeak.com/channels/448910/fields/1.json?api_key=XIHH0VV5FUTQD0PJ&results=100")

    test=data.read()
    f=open('temp.json','w')
    f.write(test)
    f.close()
    input_file=open('temp.json','r')
    decode = json.load(input_file)
    #print decode
    #print len(decode['feeds'])
    """
    for item in decode:
        #print item
        print item[0]
    """
    feeds= decode['feeds']
    entry=getEntry()
    temp=[]
    for x in feeds:
        #print x
        #speak(x['field1'])
        if int(x['entry_id']) > entry:
            temp.append(x['field1'])

    display(temp)



if __name__ == '__main__':
    get()
    """
    check()
    print getEntry()
    incEntry(getEntry())
    print getEntry()
    """