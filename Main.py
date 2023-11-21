
from tkinter import messagebox
from tkinter import *
from tkinter import simpledialog
import tkinter
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tkinter import filedialog

main = tkinter.Tk()
main.title("Student Attendance Visualization") #designing main screen
main.geometry("1300x1200")

global filename

def upload():
    global filename
    filename = filedialog.askopenfilename(initialdir="dataset")
    text.delete('1.0', END)
    text.insert(END,filename+" loaded\n");
    
     
def pieChart():
    text.delete('1.0', END)
    global filename
    all_attendence = []
    rows = 'Semester,WeekNum,Status\n'
    with open(filename, "r") as file:
        for line in file:
            line = line.strip('\n')
            line = line.strip()
            line = line[1:len(line)-3]
            line = line.strip()
            line = line.replace("\"""\"","\"")
            data = eval(line)
            status = data['Status']
            weekNum = data['WeekNum']
            semester = data['ModuleCode']
            if status == 'P':
                rows+=semester+","+weekNum+","+status+"\n"
            all_attendence.append(status)

    f = open("semester.csv", "w")
    f.write(rows)
    f.close()

    all_attendence = np.asarray(all_attendence)
    unique, frequency = np.unique(all_attendence, return_counts = True)
    presence = 0
    absent = 0
    with_permission = 0
    without_permission = 0
    for i in range(len(unique)):
        if unique[i] == 'P':
            presence = frequency[i]
        if unique[i] == 'ABS':
            absent = frequency[i]
        if unique[i] == 'AA':
            with_permission = frequency[i]
        if unique[i] == 'U':
            without_permission = frequency[i]
    text.insert(END,"Number of attended students : "+str(presence)+"\n")
    text.insert(END,"Number of absent students : "+str(absent)+"\n")
    text.insert(END,"Number of authorised absents students : "+str(with_permission)+"\n")
    text.insert(END,"Number of unauthorised absents students : "+str(without_permission)+"\n")
    plt.pie([presence,absent,with_permission,without_permission],labels=['Number of Present','Number of Absent','With Permission','Without Permission'],autopct='%1.1f%%')
    plt.title('Number of present & Absent students graph')
    plt.axis('equal')
    plt.show()


def histoChart():
    dataset = pd.read_csv('semester.csv')
    dataset = dataset.groupby(['Semester','WeekNum'],)['Status'].count().reset_index()
    dataset = dataset.values
    week = dataset[:,1]
    attended = dataset[:,2]
    print(str(week))
    print(str(attended))
    week = week.sort()

    plt.hist(attended)
    plt.xlabel('Week No')
    plt.ylabel('Attended Students')
    plt.title('Week wise attendance of students across semester')
    plt.show()

font = ('times', 16, 'bold')
title = Label(main, text='Student Attendance Visualization')
title.config(bg='LightGoldenrod1', fg='medium orchid')  
title.config(font=font)           
title.config(height=3, width=120)       
title.place(x=0,y=5)

font1 = ('times', 12, 'bold')
text=Text(main,height=20,width=100)
scroll=Scrollbar(text)
text.configure(yscrollcommand=scroll.set)
text.place(x=10,y=200)
text.config(font=font1)


font1 = ('times', 12, 'bold')
uploadButton = Button(main, text="Upload Attendance Dataset", command=upload)
uploadButton.place(x=50,y=100)
uploadButton.config(font=font1)  

pieButton = Button(main, text="Pie Chart Attended, Not Attended", command=pieChart)
pieButton.place(x=340,y=100)
pieButton.config(font=font1) 

histButton = Button(main, text="Week Wise Attendance Histogram Chart", command=histoChart)
histButton.place(x=640,y=100)
histButton.config(font=font1) 



main.config(bg='OliveDrab2')
main.mainloop()
