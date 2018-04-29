import urllib
import json
import pyttsx3
import os

engine = pyttsx3.init()



def comments(finger):
    print finger
    dic=[]
    for i in range(20):
        dic.append("")
    dic[1] = "What is your name ?"
    dic[2] = "Where am i ?"
    dic[3] = "How to reach Police Station ?"
    dic[4] = "How to reach Hospital ?"
    dic[5] = "Is there any good Restaurent around ?"
    dic[6] = "Can I use Your Phone ?"
    dic[7] = "Do you Know someone who knows Sign Language ?"
    dic[8] = "Will You Help Me out ?"
    dic[9] = "Where is Airport ?"
    dic[10] = "My Name is Manohar"
    dic[11] = "I am from NITK."
    dic[12] = "Go to Highway. Keep going for 2.5km towards south. You Will find police station on left side."
    dic[13] = "Go to Highway. Keep going for 1km towards north. You Will find hospital on right side."
    dic[14] = "Yes, there are. Try sea food which is 1 km away from here towards north direction."
    dic[15] = "Ya , Sure."
    dic[16] = "Yes. I know sign language. One of my friend also know sign language and he can speak too."
    dic[17] = "Ya , sure . In what ways ?"
    dic[18] = "Airport is on the outskirt of mangalore"
    finger=str(finger)
    #print len(finger)
    if len(finger)==3:
        if finger[0] ==  finger[2]:
            return dic[int(finger[1])+9]
    if len(finger) == 1:
        return dic[int(finger)]
    return "Unable To reply"





def speak(text):
    #print text
    #engine.say(" finger shown at the camera is {}".format(text))
    text=comments(text)
    engine.say(text)
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
    #digit=123
    #print str(digit)[1]
    #print len("123")