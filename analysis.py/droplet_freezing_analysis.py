# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 14:28:21 2022

@author: eeslb
"""
import os
import tkinter as tk
from tkinter import *
import cv2
import PIL.Image, PIL.ImageTk
import datetime as dt
import tkinter
from tkinter import messagebox
from datetime import datetime
import numpy as np
#import imutils
from tkinter import font as tkfont
from tkinter import filedialog
#import pygame

class App:
    def __init__(self, window, window_title, video_source):
        #pygame.init()
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        self.window.geometry('820x570+0+0')
        
        self.ok=False
        self.quit = False
        self.paused = True
        self.drawing = True
        self.previous_frame = None
        self.analysing = False
        
        self.freeze = []
        self.del_idx = []
        self.marks = []
        self.manual = []
        self.manual_d = []
        self.circles = []
        self.next_analysis = []
        self.draw_x = []
        self.draw_y = []
        self.draw_r = []
        self.del_events = False
        self.iframe = 0
        self.events = 0
        self.ndrops = 0
        
        self.vpath = (self.video_source + '/run.avi')
        self.ipath = (self.video_source + '/run.jpg')

        self.vid = VideoCapture(self.vpath)
        self.nframes = int(self.vid.vid.get(cv2.CAP_PROP_FRAME_COUNT))
        
        #self.top = tk.Frame(self.window, borderwidth=2, relief="ridge",width = 700, height = 30)
        #self.top.grid(column = 0, row = 0, sticky=tk.E+tk.W, padx = 10, pady = 5)
        
        self.canv_frame = tk.Frame(self.window, borderwidth=2, relief="ridge")
        self.canv_frame.grid(column = 0, row = 1,sticky=tk.E+tk.W, padx = 5,pady = 5)

        self.buttons = tk.Frame(self.window, borderwidth=2, relief="ridge",width = 800, height = 50)
        self.buttons.grid(column = 0, row = 2, sticky=tk.E+tk.W, padx = 5, pady = 5)
        
        self.canvas = tk.Canvas(self.canv_frame, width = 800, height = 450)
        self.canvas.grid(column = 0, row = 0, sticky = tk.E)
        myFont = tkfont.Font(size=12, weight='bold')
        myFont2 = tkfont.Font(size=11)
        myFont3 = tkfont.Font(size=10)
        
        #self.help_btn = tk.Button(self.top, text = 'Help!', wraplength=150, command=self.detect_drops, 
         #               width = 15, height = 1, font = myFont, bg = 'gray')
        #self.help_btn.grid(column = 0, row = 0, sticky=tk.E ,padx = 3, pady =3)
        
        self.detect_btn=tk.Button(self.buttons, text='DETECT DROPS', command=self.detect_drops, 
                        width = 13, height = 1, font = myFont, bg = 'gray')
        self.detect_btn.grid(column = 1, row = 0, rowspan=1, sticky=tk.NS ,padx = 3, pady =5)
   
        self.start_btn=tk.Button(self.buttons, text='AUTO ANALYSIS',wraplength=150, command=self.analysis_btn,
                             width = 13, height = 1, font = myFont, bg = 'gray')
        self.start_btn.grid(column = 1, row = 1, rowspan=1, sticky=tk.NS, padx = 3, pady =5)
        

        self.d_thresh = tk.IntVar()
        self.d_thresh.set(7)
        self.d_slider = tk.Scale(self.buttons, from_=0, to=18, length = 150, 
                                 orient=tk.HORIZONTAL, 
                                 showvalue = 0, variable = self.d_thresh, 
                                 command = self.drop_slider)
        self.d_slider.grid(column = 0, row = 0, padx = 3, pady =(3,3),  sticky = tk.S)
        self.d_lab = tk.Label(self.buttons, text = 'Droplet threshold:', font = myFont3).grid(column = 0, row = 0,  
                                                                      sticky = tk.NW, padx = 5, pady = 0)
        self.d_var = tk.Label(self.buttons, textvariable = self.d_thresh).grid(column = 0, row = 0,  
                                                                      sticky = tk.NE, padx = (0,10), pady = 0)


        self.f_thresh = tk.DoubleVar()
        self.f_thresh.set(3.5)
        self.freeze_slider = tk.Scale(self.buttons, from_=0, to=20,resolution =0.25, length = 150, 
                                      orient=tk.HORIZONTAL, showvalue = 0, variable = self.f_thresh,
                                      command = self.freeze_slider)
        self.freeze_slider.grid(column = 0, row = 1, padx = 3, pady =(3,3),  sticky = tk.S)
        self.f_lab = tk.Label(self.buttons, text = 'Freezing threshold:', font = myFont3).grid(column = 0, row = 1,  
                                                                      sticky = tk.NW, padx = 5,pady = 0)

        self.f_var = tk.Label(self.buttons, textvariable = self.f_thresh).grid(column = 0, row = 1,  
                                                                      sticky = tk.NE, padx = (0,10), pady = 0)


        
        self.add_btn=tk.Button(self.buttons, text='+', command=self.add_btn,
                        width = 4, height = 1, font = myFont, bg = 'gray')
        self.add_btn.grid(row = 0, column = 2, padx = 3, pady =6, sticky = tk.N+tk.S)
        
        self.del_btn=tk.Button(self.buttons, text='-', command=self.delete_btn,
                        width = 4, height = 1, font = myFont, bg = 'gray')
        self.del_btn.grid(row = 1, column = 2, padx = 3, pady =6, sticky = tk.NS)
        
 
        
        myFont = tkfont.Font(family='arial', size=12)
        buttons = [('\u25C0\u25C0 10') ,('\u25C0 1'),('\u25B6ll'),('\u25B6 1'), ('\u25B6\u25B6 10')]
        commands = [self.back_frame, self.back_one , self.pause_btn, self.forward_one, self.forward_frame]
        
        for idx,btn in enumerate(buttons):
            self.btn=tk.Button(self.buttons, text=btn, command=commands[idx],
            width = 5, height = 1, font = myFont)
            self.btn.grid(row = 0, column = idx+4, rowspan = 2, sticky = tk.E + tk.N ,padx = 5, pady =6)    
            

        self.slider = tk.Scale(self.buttons, from_=0, to=self.nframes,font=myFont3,label = 'Frame',
                               orient=tk.HORIZONTAL, showvalue = 0, command = self.slider_frame)
        self.slider.grid(column = 3, row = 1, columnspan = 6,padx = 3, pady =0,  sticky = tk.EW+tk.N)

        
        myFont = tkfont.Font(size=12, weight='bold')
        
        self.finish_btn=tk.Button(self.buttons, text='FINISH', command=self.finish,
                        width = 8, height = 1, font = myFont, bg = 'green')
        self.finish_btn.grid(row = 0, column = 11, padx = (10,0), pady =5, sticky = tk.N+tk.S+tk.E)
        
        self.cancel_btn=tk.Button(self.buttons, text='CANCEL', command=self.cancel_btn,
                        width = 8, height = 1, font = myFont, bg = 'red')
        self.cancel_btn.grid(row = 1, column = 11, padx = (4,0), pady =5, sticky = tk.NS+tk.E)
    
        self.canvas.bind('<Button-1>', self.add_drops)
        self.canvas.bind('<Button-2>', self.delete)
        self.delay = 10
        self.get_first_frame()
        
    def update(self, frame):
        self.output = frame
        try:
            self.col = cv2.cvtColor(self.output, cv2.COLOR_BGR2RGB)
            # self.col = cv2.resize(self.col, (800,450))
            if self.drawing: 
                if self.circles is not None:
                    for (x, y, r) in self.circles:
                        cv2.circle(self.col, (int(x), int(y)), int(r)+3, (255, 0, 0), 2) 
                if self.draw_x is not None:
                    for i in np.arange(0,len(self.draw_x)):
                        x = self.draw_x[i]
                        y = self.draw_y[i]
                        r = self.draw_r[i]
                        cv2.circle(self.col, (int(x), int(y)), int(r+3), (0, 0, 255), 2)
    
            cv2.putText(self.col, ('Frame: ' + str(self.iframe)),(55,  self.output.shape[0]-630), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.putText(self.col, ('Droplets detected: ' + str(self.ndrops)),(900,  self.output.shape[0]-670), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.putText(self.col, ('Events detected: ' + str(len(self.freeze))),(900, self.output.shape[0]-630), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    
            self.full = PIL.Image.fromarray(self.col) 
            self.resized = self.full.resize((800,450))
            #self.resized = self.full
            self.photo = PIL.ImageTk.PhotoImage(image = self.resized)
            self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)
        except cv2.error:
            pass
        
    def finish(self):
        dpath = (self.video_source + '\\log.csv')
        rpath = (self.video_source + '\\run')
        otpath = (self.video_source + '\\temps.csv')
        data=np.genfromtxt(dpath,delimiter=',',dtype=None, encoding='utf-8')#converters = {1: getSec})
        #headers=data[0,:]    
        data=data[1:,:]
        run_times=np.genfromtxt(rpath,skip_header=1,dtype=None, encoding=None)
        temp_frame=np.linspace(0,len(run_times),len(run_times))
        i=0
        for i in range(len(run_times)):
            if run_times[i] in data[:,1]:
                temp_frame[i]=data[data[:,1].tolist().index(run_times[i]),2]
            else:
                if int(run_times[i][-1])>0:
                    run_times[i]=run_times[i][:(len(run_times[i])-1)]+str(int(run_times[i][-1])-1)
                else :
                    run_times[i]=run_times[i][:(len(run_times[i])-1)]+str(int(run_times[i][-1])+1)
            if run_times[i] in data[:,1]:
                temp_frame[i]=data[data[:,1].tolist().index(run_times[i]),2]
            else:
                temp_frame[i]=999
                
                
        events=np.sort(self.freeze)     
        temps=np.zeros(len(events))
        i=0
        for i in range(len(events)):
            if run_times[int(events[i])] in data[:,1]:
                temps[i]=float(data[data[:,1].tolist().index(run_times[int(events[i])]),2])
            else:
                if int(run_times[int(events[i])][-1])>0:
                    run_times[int(events[i])]=run_times[int(events[i])][:(len(run_times[int(events[i])])-1)]+str(int(run_times[int(events[i])][-1])-1)
                else :
                    run_times[int(events[i])]=run_times[int(events[i])][:(len(run_times[int(events[i])])-1)]+str(int(run_times[int(events[i])][-1])+1)
                temps[i]=float(data[data[:,1].tolist().index(run_times[int(events[i])]),2])
                
        if len(temps) == 0:
            print("No values entered, the file was not written")
            tk.messagebox.showwarning(title='Uh oh', message = 'Temps file not written, check for error and try again')

        else:
            np.savetxt(otpath,temps,delimiter=',')
            tk.messagebox.showinfo(title='Woohoo', message = 'Temps file written')

    def cancel_btn(self):
        self.previous_frame = None
        self.analysing = False
        self.del_events = False
        self.freeze = []
        self.marks = []
        self.manual = []
        self.manual_d = []
        self.circles = []
        self.next_analysis = []
        self.draw_x = []
        self.draw_y = []
        self.draw_r = []
        self.iframe = 0
        self.ndrops = len(self.circles)
        self.slider.set(0)
        self.vid.vid.set(cv2.CAP_PROP_POS_FRAMES,self.iframe)
        ret,frame = self.vid.vid.read()
        
        self.update(frame)
        
    def get_first_frame(self):
        self.vid.vid.set(cv2.CAP_PROP_POS_FRAMES,self.iframe)
        ret,frame = self.vid.vid.read()
        #image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        cv2.imwrite(self.ipath, frame) 
        self.update(frame)
        #self.frame = cv2.imread(self.ipath)
        
    def freeze_slider(self, v):
       # self.f_thresh = self.freeze_slider.get()
        self.f_thresh = self.f_thresh
    def drop_slider(self, v):
        #self.d_thresh = self.d_slider.get()
        self.d_thresh = self.d_thresh
    
    def slider_frame(self, v):
        self.iframe = self.slider.get()
        self.vid.vid.set(cv2.CAP_PROP_POS_FRAMES,self.iframe)
        ret, frame = self.vid.vid.read()
        self.update(frame)
        
    def forward_frame(self):
        self.iframe = self.iframe +10
        self.vid.vid.set(cv2.CAP_PROP_POS_FRAMES,self.iframe)
        ret, frame, ts = self.vid.get_frame()
        self.update(frame)
            
    def back_frame(self):
        self.iframe = self.iframe -10
        self.vid.vid.set(cv2.CAP_PROP_POS_FRAMES,self.iframe)
        ret, frame, ts = self.vid.get_frame()
        self.update(frame)

    def forward_one(self):
        self.iframe = self.iframe +1
        self.vid.vid.set(cv2.CAP_PROP_POS_FRAMES,self.iframe)
        ret, frame, ts = self.vid.get_frame()
        self.update(frame)
            
    def back_one(self):
        self.iframe = self.iframe -1
        self.vid.vid.set(cv2.CAP_PROP_POS_FRAMES,self.iframe)
        ret, frame, ts = self.vid.get_frame()
        self.update(frame)
        
    def start(self):
        self.paused = False
        self.vid.vid.set(cv2.CAP_PROP_POS_FRAMES,self.iframe)
        ret, frame = self.vid.vid.read()
        self.update(frame)
        self.iframe = self.iframe+1
        self.after_start = self.window.after(1,self.start)
            
    def pause(self):
        self.paused = True
        self.window.after_cancel(self.after_start)

    def pause_btn(self):
        if self.paused == True:
            self.start()
        elif self.paused == False:
            self.pause()

    def start_analysis(self):
        self.paused = False
        self.del_events == True
        self.analyse_video()

    def pause_analysis(self):
        self.paused = True
        self.window.after_cancel(self.after_timer)
    
    def analysis_btn(self):
        if self.paused == True:
            self.start_btn.configure(bg = "green")
            self.analysing = True
            self.add_btn.configure(relief = tk.RAISED)
            self.del_btn.configure(relief = tk.RAISED)
            self.start_analysis()

        elif self.paused == False:
            self.pause_analysis()
            self.start_btn.configure(bg = "gray")
    
    def labels(self):
        self.show_mask()
        # if self.drawing == True:
        #     self.drawing = False
        # elif self.drawing == False:
        #     self.drawing = True
    
    def delete_btn(self):
        #self.del_btn.configure(bg = "green")
        self.add_btn.configure(bg = 'gray')
        self.add_btn.configure(relief = tk.RAISED)
        self.del_btn.configure(relief = tk.SUNKEN)
        if self.analysing == False:
            self.canvas.bind('<Button-1>', self.delete)
        if self.del_events == True:
            self.canvas.bind('<Button-1>', self.delete_event)
        
    def add_btn(self):
        #self.del_btn.configure(bg = "gray")
        self.add_btn.configure(relief = tk.SUNKEN)
        self.del_btn.configure(relief = tk.RAISED)
        if self.analysing == False:
            self.canvas.bind('<Button-1>', self.add_drops)
        elif self.analysing == True:
            self.canvas.bind('<Button-1>', self.event_click) 

        
    def delete(self,event):
        self.vid.vid.set(cv2.CAP_PROP_POS_FRAMES,self.iframe)
        ret, frame = self.vid.vid.read()
        
        events = len(self.circles)
        tot = 0
        for idx in np.arange(0,events):
            idx = idx-tot
            (x,y,r) = self.circles[idx]
            if x-10 < (self.canvas.canvasx(event.x)/0.6248) < x+10 and y-10 < (self.canvas.canvasx(event.y)/0.6248) < y+10:
                self.circles = np.delete(self.circles,idx, 0)
                tot = tot+1
        self.intensity = np.zeros((int(self.vid.vid.get(cv2.CAP_PROP_FRAME_COUNT)),len(self.circles)))
        self.analysis_circles = self.circles
        self.ndrops = len(self.circles)
        self.update(frame)
        


    def detect_drops(self):
        self.vid.vid.set(cv2.CAP_PROP_POS_FRAMES,self.iframe)
        ret, frame = self.vid.vid.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (3, 3), 0)

        self.circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT,1,33,param1=160,param2=self.d_thresh.get(),minRadius=4,maxRadius=12)
        
        if self.circles is not None:
            self.circles = np.round(self.circles[0, :]).astype("int")
            #self.ndrops = len(self.circles)
            #self.update(frame)
            # for idx, circ in enumerate(self.circles): 
            #     (x,y,r) = circ
            #     if x < 200:
            #         self.circles = np.delete(self.circles,idx,None)
            
            
            
        self.intensity = np.zeros((int(self.vid.vid.get(cv2.CAP_PROP_FRAME_COUNT)),len(self.circles)))
        self.analysis_circles = self.circles
        self.ndrops = len(self.circles)
        self.update(frame)
        
    def add_drops(self, event):
        self.vid.vid.set(cv2.CAP_PROP_POS_FRAMES,self.iframe)
        ret, frame = self.vid.vid.read()
        r = 10
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

        wx = (x/0.6248)
        wy = (y/0.6248)
        circle = (int(wx),int(wy),int(r))

        self.circles = np.vstack([self.circles,circle])
        
        
          
        self.intensity = np.zeros((int(self.vid.vid.get(cv2.CAP_PROP_FRAME_COUNT)),len(self.circles)))
        self.analysis_circles = self.circles
        self.ndrops = len(self.circles)
        self.update(frame)
        
    def event_click(self, eventorigin):
        self.vid.vid.set(cv2.CAP_PROP_POS_FRAMES,self.iframe)
        ret, frame = self.vid.vid.read()
        x = self.canvas.canvasx(eventorigin.x)
        y = self.canvas.canvasy(eventorigin.y)
        r = 10

        wx = (x/0.6248)
        wy = (y/0.6248)
        
        for idx, circ in enumerate(self.analysis_circles):
            (ox, oy, rad) = circ
            ox = int(ox)
            oy = int(oy)
            rad = int(rad)
            if ox-10 < wx < ox+10 and oy-10 < wy < oy+10:
                self.analysis_circles[idx] = (0,0,0)
                
        self.manual.append((int(wx),int(wy),8,8))
        self.freeze = np.append(self.freeze, self.iframe)
        self.draw_x = np.append(self.draw_x,wx)
        self.draw_y = np.append(self.draw_y,wy)
        self.draw_r = np.append(self.draw_r,r)
        self.update(frame)

    def delete_event(self,event):
        self.vid.vid.set(cv2.CAP_PROP_POS_FRAMES,self.iframe)
        ret, frame = self.vid.vid.read()
        
        wx = self.canvas.canvasx(event.x)/0.6248
        wy = self.canvas.canvasy(event.y)/0.6248
        
        self.events = len(self.draw_x)
        tot = 0
        
        for idx in np.arange(0,self.events):
            idx = idx-tot
            x = self.draw_x[idx]
            y = self.draw_y[idx]

            if x-10 < wx < x+10 and y-10 < wy < y+10:
                tot = tot+1
                self.draw_x = np.delete(self.draw_x,idx,None)
                self.draw_y = np.delete(self.draw_y,idx,None)
                self.draw_r = np.delete(self.draw_r,idx,None)
                self.freeze = np.delete(self.freeze,idx,None)
                circle = (int(wx),int(wy),int(10))
                self.circles = np.vstack([self.circles,circle])
                self.intensity = np.zeros((int(self.vid.vid.get(cv2.CAP_PROP_FRAME_COUNT)),len(self.circles)))
                self.analysis_circles = self.circles
                self.update(frame)

    def analyse_video(self):
        self.del_events = True
        #self.canvas.bind('<Button-1>', self.event_click) 
        self.vid.vid.set(cv2.CAP_PROP_POS_FRAMES,self.iframe)
        ret, current_frame = self.vid.vid.read()
        output = current_frame

        if self.vid.vid.isOpened():
            try:
                current_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
                count = 0
    
                for idx, circ in enumerate(self.analysis_circles):
                    
                    (x,y,r) = circ
                    x = int(x)
                    y = int(y)
                    r = int(r)
                    current_circ = current_gray[y-r:y+r, x-r:x+r]
                    self.intensity[self.iframe,idx] = np.mean(current_circ)
                    #cv2.circle(output, (x, y), r+2, (0, 0, 255), 2)
                    if self.intensity[self.iframe-1,idx]-self.intensity[self.iframe,idx]>self.f_thresh.get():
                        #pygame.mixer.music.load(r"C:\Users\eeslb\Downloads\sfx-boing4\sfx-boing4.mp3") #Loading File Into Mixer
                        #pygame.mixer.music.play()
                        self.analysis_circles[idx] = (0,0,0)
                        self.freeze = np.append(self.freeze, self.iframe)
                        cv2.circle(output, (x, y), r+2, (0, 255, 0), -2)
                        self.draw_x = np.append(self.draw_x,x)
                        self.draw_y = np.append(self.draw_y,y)
                        self.draw_r = np.append(self.draw_r,r)
                    
                        count = count+1
    
    
                
                self.iframe = self.iframe+1
                ret, current_frame = self.vid.vid.read()
                ret, output = self.vid.vid.read()
                self.update(output)
                    
                # if count > 5:
    
                #     answer = tk.messagebox.askyesno(title='Confirmation', message='Are you sure that you want to quit?')
                #     if answer:

            #         #self.intensity = np.zeros((int(self.vid.vid.get(cv2.CAP_PROP_FRAME_COUNT)),len(self.circles)))
            #         #self.analysis_circles = self.circles
            #         self.update(output)
                
                
            # if self.draw_x is not None:
            #     for i in np.arange(0,len(self.draw_x)):
            #         x = self.draw_x[i]
            #         y = self.draw_y[i]
            #         r = self.draw_r[i]
            #         cv2.circle(current_frame, (int(x), int(y)), int(r+2), (0, 0, 0), -2)
            #self.slider.set(self.iframe)
                self.after_timer = self.window.after(1,self.analyse_video)
        
            except cv2.error:
                answer = tk.messagebox.askyesno(message = 'End of video: do you want to write temps file?')
                if answer:
                    self.finish()
                    self.window.after_cancel(self.after_timer)

class VideoCapture:
    def __init__(self, video_source):
        # Open the video source
        
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source, check if webcam is connected", video_source)
            messagebox.showerror("Unable to open video source, check if webcam is connected")
       # Command Line Parser
        #args=CommandLineParser().args
        
        res=(1280, 720)

        #set video sourec width and height
        self.vid.set(3,res[0])
        self.vid.set(4,res[1])

        # Get video source width and height
        self.width,self.height=res

    # To get frames
    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                fr_t = dt.datetime(1, 1, 1).now()
                time_stamp = fr_t.strftime('%H:%M:%S')
                return (ret, frame, time_stamp)
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
            cv2.destroyAllWindows()
            
if __name__ == "__main__":
    # s=ttk.Style()
    # s.theme_use('clam')
    #style = ttk.Style("flatly"
    root = tk.Tk()
    root.withdraw()
    video_source = tk.filedialog.askdirectory()
    #video_source = r"C:\Users\eeslb\OneDrive - University of Leeds\PhD\3_projects\2_alaska\1_nipi-data\real_runs\all_unheated\191013\191013_stageB_run3_ef6001"
    if video_source:
        App(root, 'Video Analysis', video_source)
        root.deiconify()
        #root.protocol('WM_DELETE_WINDOW', root.destroy())
        root.mainloop()
    else:
        root.destroy()
        cv2.destroyAllWindows()

