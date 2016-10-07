# -*- coding: utf-8 -*-

import datetime
from nt import mkdir
import os
import re
from test.support import forget
from threading import Lock
import threading
from time import sleep
import time
from tkinter import *
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter.messagebox import showerror
from tkinter.test.support import destroy_default_root
from _ctypes import alignment


class BroMans():
    def __init__(self, initdir=None):
        self.top = Tk()        
        
        self.top.wm_title('Bromans')
        self.top.geometry('600x540')

        self.repeat_Cnt = 0
        
        self.Op_Toggle = [False, False, False]
        
        Browse_Frame = Frame(self.top)
        
     
        self.browseButton = Button(Browse_Frame, text="Browse", command=self.load_Browse, width=15)
        self.browseButton.pack(side=LEFT)
        
        Browse_Frame.pack()

        Op_Frame = Frame(self.top)
        
        self.FileExtention = Button(Op_Frame, text='FileNameExtention', command = self.click_Extention_event, width=15)
        self.FileExtention.pack()
        
        self.FileDate = Button(Op_Frame, text='FileDate',command = self.click_Date_event, width=15)
        self.FileDate.pack()
        
        self.None_op = Button(Op_Frame, text = 'None', command = self.click_None_event, width =15)
        self.None_op.pack()
        
        Op_Frame.pack()
        
        self.current_Route_Label = Label(self.top, fg='blue', font=('Helvetica', 12, 'bold'))
        self.current_Route_Label.pack()
        
        self.filelist_Frame_above = Label(self.top)   ## Directory 를 나열해주는 List
        self.filelist_Frame_below = Label(self.top)   ## File 을 나열해주는 List
        
        self.Above_Scroll = Scrollbar(self.filelist_Frame_above)
        self.Above_Scroll.pack(side=RIGHT, fill=Y)
        
        self.Below_Scroll = Scrollbar(self.filelist_Frame_below)
        self.Below_Scroll.pack(side=RIGHT, fill=Y)
        
        self.Above_List = Listbox(self.filelist_Frame_above, height=10, width=75, yscrollcommand=self.Above_Scroll.set)
        self.Above_List.bind('<Double-1>', self.list_event)
        self.Above_Scroll.config(command=self.Above_List.yview)
        self.Above_List.pack(side=TOP, fill=BOTH)
        
        self.Below_List = Listbox(self.filelist_Frame_below, height=10, width=75, yscrollcommand=self.Below_Scroll.set)
        self.Below_List.bind('<Double-1>', self.list_event)
        self.Below_Scroll.config(command=self.Below_List.yview)
        self.Below_List.pack(side=BOTTOM, fill=BOTH)
        
        self.filelist_Frame_above.pack()
        self.filelist_Frame_below.pack()
        
        self.Quit_Frame = Frame(self.top)

        self.quit = Button(self.Quit_Frame, text='Quit', command=self.quit_Event, activeforeground='white', \
                           activebackground='red')
        self.quit.pack(side=LEFT)
        
        self.Quit_Frame.pack()
        
        if initdir:
            self.Refresh_List()
            th.start()
            
    def quit_Event(self):
        self.top.destroy()
        
    def load_Browse(self):
        Route_dir = askdirectory(initialdir = os.curdir)
        os.curdir = Route_dir
        self.click_None_event()
        
    def click_Extention_event(self):
        self.Op_Toggle = [True, False, False]
        self.Th_cnt = 5
        self.Refresh_List()
        
    def click_Date_event(self):
        self.Op_Toggle = [False, True, False]
        self.Th_cnt = 5
        self.Refresh_List()
    
    def click_None_event(self):
        self.Op_Toggle = [False, False, False]
        self.Refresh_List()
        
    def list_event(self, ev=None):
        
        self.Above_List.config(selectbackground='red')
        getFilename = self.Above_List.get(self.Above_List.curselection())

        os.curdir = os.getcwd() + '/' + getFilename
        
        if getFilename :
            self.click_None_event()
            
        elif not getFilename:
            getFilename = os.curdir
        
 
        self.Refresh_List()

    def Refresh_List(self, ev=None):
        
        error = ''
        route_check = os.curdir
        
        if not route_check:
            route_check = os.curdir
        if not os.path.exists(route_check):
            error = route_check + ': no such file'
        elif not os.path.isdir(route_check):
            error = route_check + ':not a directory'
            
        if error:
            self.top.update()
            sleep(2)
            if not (hasattr(self, 'last') and self.last):
                self.last = os.curdir
       
            self.Above_List.config(selectbackground='LightSkyBlue')
            self.top.update()
            return

        self.top.update()
        self.Current_allFile = os.listdir(route_check)
        
        os.chdir(route_check)
        
        self.current_Route_Label.config(text=os.getcwd())
        
        self.Above_List.delete(0, END)
        self.Above_List.insert(END, os.pardir)
        
        self.Below_List.delete(0, END)
        self.Below_List.insert(END, os.pardir)
        
        Above_Array = []
        Below_Array = []
        Folder_cnt= 0
        File_cnt=0
        
        for eachFile in self.Current_allFile:
            if os.path.isdir(eachFile):
                Above_Array.insert(Folder_cnt, eachFile)
                
            if os.path.isfile(eachFile):
                Below_Array.insert(File_cnt, eachFile)
                
        
        for eachFile in Below_Array:
            self.Below_List.insert(END, eachFile)
            self.Below_List.config(fg = 'black')
            
            if self.Op_Toggle[0]:
                if os.path.isfile(eachFile):
                    self.buffer_split_name = os.path.splitext(eachFile)[1]
                    self.buffer_split_name = re.sub("[.]", "" , self.buffer_split_name)
                    Forder_name = self.buffer_split_name.upper()
                
                    if not os.path.exists('../' + Forder_name + ' Files'):
                        try:
                            os.renames(eachFile, Forder_name + ' Files/' + eachFile)
                        except FileExistsError:
                            while True:
                                try:
                                    os.renames(eachFile, Forder_name + ' Files/' + os.path.splitext(eachFile)[0] + '(' + str(self.repeat_Cnt) + ')' + os.path.splitext(eachFile)[1])
                                    break
                                except FileExistsError:
                                    self.repeat_Cnt += 1
                            self.repeat_Cnt = 1
                            
            elif self.Op_Toggle[1]:
                Date_str = datetime.datetime.fromtimestamp(os.path.getatime(eachFile))
                self.Month_dir = os.path.splitext(str(Date_str))[0][5] + os.path.splitext(str(Date_str))[0][6]
                self.Year_dir = os.path.splitext(str(Date_str))[0][0] + os.path.splitext(str(Date_str))[0][1] +os.path.splitext(str(Date_str))[0][2] +os.path.splitext(str(Date_str))[0][3]
                self.Day_dir = os.path.splitext(str(Date_str))[0][8] + os.path.splitext(str(Date_str))[0][9]
                
                if os.path.isfile(eachFile):
                    try:
                        if not os.path.exists('../' + self.Year_dir + '-' + self.Month_dir + '/'):
                            os.renames(eachFile, self.Year_dir + '-' + self.Month_dir + '/' + eachFile)
                    except FileExistsError:
                        while True:
                            try:
                                os.renames(eachFile, self.Year_dir + '-' + self.Month_dir+'/' + os.path.splitext(eachFile)[0] + '(' + str(self.repeat_Cnt) + ')' + os.path.splitext(eachFile)[1])
                                break
                            except FileExistsError:
                                self.repeat_Cnt += 1
                        self.repeat_Cnt = 1
                
        for eachFile in Above_Array:
            self.Above_List.insert(END, eachFile)
            self.Above_List.config(fg = 'red')
            
            
        self.Buffer_List = os.listdir(os.curdir)
        
        self.Above_List.config(selectbackground='LightSkyBlue')

class Thread(threading.Thread):
    def run(self):
        
        while True:
            try:
                if os.listdir(os.curdir) == BROMANS.Buffer_List:
                    if BROMANS.Op_Toggle[0] or BROMANS.Op_Toggle[1]:
                        BROMANS.Refresh_List()
                        
                    else :
                        BROMANS.Refresh_List()
                
                        time.sleep(2)
                        
            except FileNotFoundError:
                pass                
            
init_Address = "C:\\Arrange_Forder"

if not os.path.exists(init_Address):   
    os.mkdir(init_Address)

th = Thread()
th.daemon = True  ## EXIT ON CLOSE

os.curdir = init_Address

BROMANS = BroMans(os.curdir)
mainloop()