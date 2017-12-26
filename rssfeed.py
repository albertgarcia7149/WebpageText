import urllib3
import certifi
from bs4 import BeautifulSoup
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from tkinter import Tk, Label, Button, Entry, IntVar, END, W, E, Message, Frame, Text, Scrollbar, LEFT, RIGHT, TOP, Y, Listbox, END, StringVar

#get and check the url exists
validate = URLValidator()
running=True
while running:
    i=input("Enter url: ")
    try:
        validate(i)
        running=False
    except ValidationError:
        running=True


class RssFeed:



    def __init__(self, master):
        self.master = master
        #set window name
        master.title("RssFeed")
        #set minimum window size
        master.minsize(width=800, height=800)
        #lock window size
        master.resizable(width=False, height=False)
        #add scroll bar
        scrollbar=Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)
        #define listbox
        listbox=Listbox(master,width=200,height=50,yscrollcommand=scrollbar.set)
        #pack listbox
        listbox.pack()
        url=i
        t=self.get_feed(url)
        t.splitlines()
        for item in t.splitlines():
            listbox.insert(END,item)
        scrollbar.config(command=listbox.yview)


    def get_feed(self,url):
        http=urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where())
        r=http.request('GET',url)
        #pass data into beautifulsoup
        soup=BeautifulSoup(r.data)
        #remove the scripts and styles
        for script in soup(["script","style"]):
            script.extract()
        #get text form remaining html
        text=soup.get_text()
        #break into lines and remove leading and training spaces
        lines=(line.strip() for line in text.splitlines())
        #return lines
        #break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        print(chunks)
        text='\n'.join(chunk for chunk in chunks if chunk)
        return text


root = Tk()
my_gui = RssFeed(root)
root.mainloop()
