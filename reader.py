import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo

from functools import cmp_to_key
import urllib
import urllib.request
import time

# Object Event
monthtable = ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
class Event:
    def __init__(self, s, d, t, ha, o, v, sp):
        self.sport = s
        self.date = d
        self.time = t
        self.homeaway = ha
        self.opponent = o
        self.venue = v
        self.special = sp
        self.visible = TRUE
    
    def timevalue(self):
        if 'TBA' in self.time:
            return monthtable.index(self.date[0:3]) * 400000 + int(self.date[4:]) * 10000
        if 'PM' in self.time:
            return monthtable.index(self.date[0:3]) * 400000 + int(self.date[4:]) * 10000 + int(self.time.split(':')[0]) * 100 + int(self.time.split(' ')[0].split(':')[1]) + 5000
        return monthtable.index(self.date[0:3]) * 400000 + int(self.date[4:]) * 10000 + int(self.time.split(':')[0]) * 100 + int(self.time.split(' ')[0].split(':')[1])

    def tostring(self):
        return (self.sport + ' ' + self.date + ' ' + self.time + ' ' + self.homeaway + ' ' + self.opponent + ' ' + self.venue +' ' + self.special).lower()
        
    def totuple(self):
        return self.sport, self.date, self.time, self.homeaway, self.opponent, self.venue, self.special

root = tk.Tk()
root.title('Seven Lakes Sports')
root.geometry('1370x720')
root.resizable(False, False)

# Stores all the events
master_list = []

url_list = [
    "https://www.rankone.com/Schedules/View_Schedule_Web.aspx?P=0&D=E60DB75B-3AB2-4FE7-B746-0735376AFB5B&S=601&Sp=7&Tm=11842&L=1&Mt=0",
    "https://www.rankone.com/Schedules/View_Schedule_Web.aspx?P=0&D=E60DB75B-3AB2-4FE7-B746-0735376AFB5B&S=601&Sp=3&Tm=11757&L=1&Mt=0",
    "https://www.rankone.com/Schedules/View_Schedule_Web.aspx?P=0&D=E60DB75B-3AB2-4FE7-B746-0735376AFB5B&S=601&Sp=1&Tm=15013&L=1&Mt=0",
    "https://www.rankone.com/Schedules/View_Schedule_Web.aspx?P=0&D=E60DB75B-3AB2-4FE7-B746-0735376AFB5B&S=601&Sp=7&Tm=11843&L=2&Mt=0",
    "https://www.rankone.com/Schedules/View_Schedule_Web.aspx?P=0&D=E60DB75B-3AB2-4FE7-B746-0735376AFB5B&S=601&Sp=1&Tm=15014&L=2&Mt=0",
    "https://www.rankone.com/Schedules/View_Schedule_Web.aspx?P=0&D=E60DB75B-3AB2-4FE7-B746-0735376AFB5B&S=601&Sp=1&Tm=15015&L=3&Mt=0",
    "https://www.rankone.com/Schedules/View_Schedule_Web.aspx?P=0&D=E60DB75B-3AB2-4FE7-B746-0735376AFB5B&S=601&Sp=3&Tm=11772&L=2&Mt=0",
    "https://www.rankone.com/Schedules/View_Schedule_Web.aspx?P=0&D=E60DB75B-3AB2-4FE7-B746-0735376AFB5B&S=601&Sp=3&Tm=11774&L=2&Mt=0",
    "https://www.rankone.com/Schedules/View_Schedule_Web.aspx?P=0&D=E60DB75B-3AB2-4FE7-B746-0735376AFB5B&S=601&Sp=3&Tm=11779&L=3&Mt=0",
    "https://www.rankone.com/Schedules/View_Schedule_Web.aspx?P=0&D=E60DB75B-3AB2-4FE7-B746-0735376AFB5B&S=601&Sp=3&Tm=11781&L=3&Mt=0",
    "https://www.rankone.com/Schedules/View_Schedule_Web.aspx?P=0&D=E60DB75B-3AB2-4FE7-B746-0735376AFB5B&S=601&Sp=18&Tm=15751&L=1&Mt=0",
    "https://www.rankone.com/Schedules/View_Schedule_Web.aspx?P=0&D=E60DB75B-3AB2-4FE7-B746-0735376AFB5B&S=601&Sp=18&Tm=15752&L=2&Mt=0",
    "https://www.rankone.com/Schedules/View_Schedule_Web.aspx?P=0&D=E60DB75B-3AB2-4FE7-B746-0735376AFB5B&S=601&Sp=26&Tm=11808&L=1&Mt=0",
    "https://www.rankone.com/Schedules/View_Schedule_Web.aspx?P=0&D=E60DB75B-3AB2-4FE7-B746-0735376AFB5B&S=601&Sp=26&Tm=11814&L=2&Mt=0",
    "https://www.rankone.com/Schedules/View_Schedule_Web.aspx?P=0&D=E60DB75B-3AB2-4FE7-B746-0735376AFB5B&S=601&Sp=26&Tm=11818&L=3&Mt=0",
    "https://www.rankone.com/Schedules/View_Schedule_Web.aspx?P=0&D=E60DB75B-3AB2-4FE7-B746-0735376AFB5B&S=601&Sp=26&Tm=11823&L=3&Mt=0",
    "https://www.rankone.com/Schedules/View_Schedule_Web.aspx?P=0&D=E60DB75B-3AB2-4FE7-B746-0735376AFB5B&S=601&Sp=24&Tm=15043&L=1&Mt=0",
    "https://www.rankone.com/Schedules/View_Schedule_Web.aspx?P=0&D=E60DB75B-3AB2-4FE7-B746-0735376AFB5B&S=601&Sp=24&Tm=15044&L=2&Mt=0",
    "https://www.rankone.com/Schedules/View_Schedule_Web.aspx?P=0&D=E60DB75B-3AB2-4FE7-B746-0735376AFB5B&S=601&Sp=34&Tm=15753&L=1&Mt=0",
    "https://www.rankone.com/Schedules/View_Schedule_Web.aspx?P=0&D=E60DB75B-3AB2-4FE7-B746-0735376AFB5B&S=601&Sp=34&Tm=15754&L=2&Mt=0",
    "https://www.rankone.com/Schedules/View_Schedule_Web.aspx?P=0&D=E60DB75B-3AB2-4FE7-B746-0735376AFB5B&S=601&Sp=5&Tm=11809&L=1&Mt=0",
    "https://www.rankone.com/Schedules/View_Schedule_Web.aspx?P=0&D=E60DB75B-3AB2-4FE7-B746-0735376AFB5B&S=601&Sp=5&Tm=11812&L=2&Mt=0",
    "https://www.rankone.com/Schedules/View_Schedule_Web.aspx?P=0&D=E60DB75B-3AB2-4FE7-B746-0735376AFB5B&S=601&Sp=5&Tm=11817&L=3&Mt=0",
    "https://www.rankone.com/Schedules/View_Schedule_Web.aspx?P=0&D=E60DB75B-3AB2-4FE7-B746-0735376AFB5B&S=601&Sp=5&Tm=11830&L=3&Mt=0",
    "https://www.rankone.com/Schedules/View_Schedule_Web.aspx?P=0&D=E60DB75B-3AB2-4FE7-B746-0735376AFB5B&S=601&Sp=186&Tm=122095&L=1&Mt=0",
    "https://www.rankone.com/Schedules/View_Schedule_Web.aspx?P=0&D=E60DB75B-3AB2-4FE7-B746-0735376AFB5B&S=601&Sp=186&Tm=122096&L=2&Mt=0",
    "https://www.rankone.com/Schedules/View_Schedule_Web.aspx?P=0&D=E60DB75B-3AB2-4FE7-B746-0735376AFB5B&S=601&Sp=181&Tm=121751&L=1&Mt=0",
    "https://www.rankone.com/Schedules/View_Schedule_Web.aspx?P=0&D=E60DB75B-3AB2-4FE7-B746-0735376AFB5B&S=601&Sp=181&Tm=121752&L=2&Mt=0"
]

for url in url_list:

    f = open('temp.txt', 'w')
    f.write(urllib.request.urlopen(url).read().decode('utf-8'))
    f.close()

    f = open('temp.txt', 'r')
    lines = f.readlines()

    for line in lines:
        if '<p style="font-size:16px;margin-bottom:4px;">' in line.strip():
            sport = line[line.index('p style="font-size:16px;margin-bottom:4px;">'):].strip()[line[line.index('p style="font-size:16px;margin-bottom:4px;">'):].strip().index('>')+1:line[line.index('p style="font-size:16px;margin-bottom:4px;">'):].strip().index('<')]
        elif '<span id="rpt_Games_lbl_Start_Date' in line.strip():
            date = line.strip()[1:][line.strip()[1:].index('>')+1:line.strip()[1:].index('<')]
        elif '<span id="rpt_Games_lbl_Start_Time' in line.strip():
            ttime = line.strip()[1:][line.strip()[1:].index('>')+1:line.strip()[1:].index('<')]
        elif '<span id="rpt_Games_lbl_Location_' in line.strip():
            homeaway = line.strip()[1:][line.strip()[1:].index('>')+1:line.strip()[1:].index('<')]
        elif '<span id="rpt_Games_lbl_Opponent' in line.strip():
            opponent = line.strip()[1:][line.strip()[1:].index('>')+1:line.strip()[1:].index('<')]
        elif '<span id="rpt_Games_lbl_SpecialNote' in line.strip():
            try:
                special = line.strip()[1:][line.strip()[1:].index('>')+1:line.strip()[1:].index('<')]
            except:
                special = ''
        elif '<span id="rpt_Games_lbl_Venue' in line.strip():
            venue = line.strip()[1:][line.strip()[1:].index('>')+1:line.strip()[1:].index('<')]
            master_list.append(Event(sport, date, ttime, homeaway, opponent, venue, special))

def compare(event1, event2):
    return event1.timevalue() - event2.timevalue()
master_list.sort(key = cmp_to_key(compare))

fb = Text(root, height = 1, width = 200, padx = 10, pady = 10)
fb.pack(side = TOP)

tree = ttk.Treeview(root, height = 660, columns = ('s', 'd', 't', 'ha', 'o', 'v', 'sp'), show = 'headings')
tree.column('s', width = 300)
tree.heading('s', text = 'Sport and Team')
tree.column('d', width = 60)
tree.heading('d', text = 'Date')
tree.column('t', width = 60)
tree.heading('t', text = 'Time')
tree.column('ha', width = 30)
tree.heading('ha', text = '')
tree.column('o', width = 300)
tree.heading('o', text = 'Opponent')
tree.column('v', width = 300)
tree.heading('v', text = 'Venue')
tree.column('sp', width = 300)
tree.heading('sp', text = 'Speical Notes')
tree.pack(side = LEFT, fill = BOTH)

sb = ttk.Scrollbar(root, orient=VERTICAL)
sb.pack(side = RIGHT, fill = Y)
sb.config(command=tree.yview)

tree.config(yscrollcommand=sb.set)

for event in master_list:
    print(event.tostring())
    print(str(event.timevalue()))
    tree.insert('', tk.END, values=event.totuple())

querystring = ''
iscontrola = ''

def filt():
    global querystring
    for item in tree.get_children():
        tree.delete(item)
    for event in master_list:
        if querystring.lower() in event.tostring():
            tree.insert('', tk.END, values=event.totuple())

def keydown(e):
    global querystring
    global iscontrola
    print(e)
    if iscontrola:
        if str(e).__contains__('BackSpace'):
            querystring = ''
        elif str(e).__contains__('space key'):
            querystring = ' '
        else:
            querystring = str(e)[str(e).index('keysym=') + 7:str(e).index('keysym=') + 8]
        iscontrola = False
    elif str(e).__contains__('Control|Mod1 keysym=a'):
        iscontrola = True
    elif str(e).__contains__('Control'):
        pass
    elif str(e).__contains__('BackSpace'):
        try:
            querystring = querystring[0:len(querystring) - 1]
        except:
            pass
    elif str(e).__contains__('space key'):
        querystring += ' '
    else:
        querystring = querystring + str(e)[str(e).index('keysym=') + 7:str(e).index('keysym=') + 8]
    print(querystring)
    filt()

fb.bind('<KeyPress>', keydown)

root.mainloop()
