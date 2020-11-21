# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 14:40:21 2020

@author: Xavier
"""

import tkinter as tk
import tkinter.font as tkf
from tkinter import filedialog,ttk,messagebox
from PIL import Image,ImageTk
#import imageio
#import skimage as ski
#import numpy as np

class Application(tk.Tk):
    
    def __init__(self):
        
        tk.Tk.__init__(self)
        self.wm_iconbitmap('telecorp6.ico')
        self.minsize(600,400)
        self.maxsize(600,400)
        self.create_widgets()
        
    def create_widgets(self):
        
        #FUNCTIONS
        def browseFiles_one():
            filepath = filedialog.askopenfilename(filetypes = (("Gif files","*.gif*"),("Png files","*.png*"),("Jpg files","*.jpg*"),))
            entry_path_one.delete(0,'end')
            entry_path_one.insert(0, filepath)
            
        def browseFiles_two():
            filepath = filedialog.askopenfilename(filetypes = (("Gif files","*.gif*"),))
            entry_path_two.delete(0,'end')
            entry_path_two.insert(0, filepath)
            
        def start(progress):
            progress["value"]=0
            progress["maximum"]= img.n_frames
            
        def imagesFusion(stringpath1, stringpath2):
            
            try:
                img1 = Image.open(stringpath1)
            except:
                print("No acces to Image one")
                tk.messagebox.showinfo("No acces one", "No acces to Image one")
                return -1
                
            try:
                img2 = Image.open(stringpath2)
            except:
                print("No acces to Image two")
                tk.messagebox.showinfo("No acces two","No acces to Image two")
                return-1
                
            giffusion = []
            
            if var_invert.get() == 0:
                
                if var_progressive.get() == 0:
                               
                    for frame in range(0,img2.n_frames):
                        img2.seek(frame)
                        img_alpha = img2.copy().convert("RGBA")
                        img_alpha.putalpha(int((int(opacity_two.get())*255)/100))
                        htarget_difference = abs(img2.height-img1.height)
                        wtarget=img2.width-(htarget_difference*(img2.width/img2.height))
                        img_alpha=img_alpha.resize((int(wtarget),img1.height))
                        (left,upper,right,lower) = (img_alpha.width/2-img1.width/2,0,img_alpha.width/2+img1.width/2,img_alpha.height)
                        print(left,upper,right,lower)
                        print(img1.size,".....",img_alpha.size)
                        img_aplha = img_alpha.crop((left,upper,right,lower))
                        img_paste = img1.copy().convert("RGBA")
                        print(img1.size,".....",img_alpha.size)
                        img_paste.paste(img_alpha, (0,0), img_alpha)
                        giffusion.append(img_paste)
                        progress["value"] += 1
                        
                    tk.messagebox.showinfo("Processing", "Process finished")
                    progress["value"]=0
                    giffusion[0].save("result.gif", save_all=True, append_images=giffusion, duration=100, loop=0)
                else:
                    
                    alphaprogress = 0
                    
                    for frame in range(0,img2.n_frames):
                        img2.seek(frame)
                        img_alpha = img2.copy().convert("RGBA")
                        if alphaprogress >= int((int(opacity_two.get())*255)/100):
                            img_alpha.putalpha(int((int(opacity_two.get())*255)/100))
                        else:
                            img_alpha.putalpha(alphaprogress)
                            alphaprogress += 7
                        img_alpha=img_alpha.resize(img1.size)
                        #(left,upper,right,lower) = (0,0,150,150,)
                        #img_aplha=img_alpha.crop((left,upper,right,lower))
                        img_paste=img1.copy().convert("RGBA")
                        img_paste.paste(img_alpha, (0,0), img_alpha)
                        giffusion.append(img_paste)
                        progress["value"] += 1
                        
                    tk.messagebox.showinfo("Processing", "Process finished")
                    progress["value"]=0
                    img1.save("result.gif", save_all=True, append_images=giffusion, duration=100, loop=0)
            
            else:
                
                for frame in range(0,img2.n_frames):
                    img2.seek(frame)
                    img_alpha = img1.copy().convert("RGBA")
                    pixeldata = list(img_alpha.getdata())
                    for i, pixel in enumerate(pixeldata):
                        if pixel[3] >= 20:
                            pixeldata[i] = (pixel[0], pixel[1], pixel[2], int((int(opacity_one.get())*255)/100))

                    img_alpha.putdata(pixeldata)
                    #img_alpha.putalpha(int((int(opacity_two.get())*255)/100))
                    img_alpha = img_alpha.resize(img2.size)
                    #img_alpha = img_alpha.copy().convert("L")
                    #(left,upper,right,lower) = (0,0,150,150,)
                    #img_aplha=img_alpha.crop((left,upper,right,lower))
                    img_mask=img_alpha.convert('L')
                    img_paste=img2.copy().convert("P")
                    img_paste.paste(img_mask, (0, 0),img_alpha)
                    giffusion.append(img_paste)
                    progress["value"] += 1
            
                tk.messagebox.showinfo("Processing invert", "Process finished")
                progress["value"]=0
                giffusion[0].save("result.gif", save_all=True, append_images=giffusion, duration=55, loop=0)
                
            
        #FONT
        bold10 = tkf.Font(weight='bold', size = 10)#BOLD SIZE 10
        bold8 = tkf.Font(weight='bold', size = 8)#BOLD SIZE 8
        
        #FRAMES
        frame_head = tk.Frame(self, bg='#7a2121')
        frame_core = tk.Frame(self)
        frame_end = tk.Frame(self, bg='#7a2121')
        frame_param = tk.Frame(self, highlightthickness=3)
        frame_one = tk.Frame(frame_core)
        frame_two = tk.Frame(frame_core)
        frame_one_one = tk.Frame(frame_one)
        frame_one_two = tk.Frame(frame_one)
        frame_one_three = tk.Frame(frame_one)
        frame_two_one = tk.Frame(frame_two)
        frame_two_two = tk.Frame(frame_two)
        frame_two_three = tk.Frame(frame_two)
        
        #PROGRESS BAR
        progress = ttk.Progressbar(frame_param, orient="horizontal", length=100, mode="determinate")
        
        #LABELS
        label_title = tk.Label(frame_head, text="Dynamic Pictures Editor", bg ='#7a2121', font=bold10, fg="#ffffff")
        label_one = tk.Label(frame_one, text="Picture One", font=bold10)
        label_two = tk.Label(frame_two, text="Picture Two", font=bold10)
        avert_one = tk.Label(frame_one, text="*Must be in JPG/PNG/GIF format", font=bold8, fg="#B22222")
        avert_two = tk.Label(frame_two, text="*Must be in GIF format", font=bold8, fg="#B22222")
        label_path_one = tk.Label(frame_one_one, text="Path :")
        label_path_two = tk.Label(frame_two_one, text="Path :")
        #label_priority_one = tk.Label(frame_one_two, text="Order (1-2) :")
        #label_priority_two = tk.Label(frame_two_two, text="Order (1-2):")
        label_opacity_one = tk.Label(frame_one_three, text="Opacity level (0-100%):")
        label_opacity_two = tk.Label(frame_two_three, text="Opacity level (0-100%):") 
        #avert_size = tk.Label(self,text="Note that the gif will automaticly resize one the pict one size")
        
        #IMAGES
        img = Image.open("telecorp6.gif")
        limg = ImageTk.PhotoImage(img)
        logo = tk.Label(frame_end, image = limg, bg="#7a2121")
        logo.image=limg
        logo.pack(side = tk.LEFT)
            
        #ENTRY
        entry_path_one = tk.Entry(frame_one_one)
        entry_path_one.insert(0,"C:/")
        entry_path_two = tk.Entry(frame_two_one)
        entry_path_two.insert(0,"C:/")
        #priority_one = tk.Entry(frame_one_two, width=4) #cursor="arrow"
        #priority_two = tk.Entry(frame_two_two, width=4)
        opacity_one = tk.Entry(frame_one_three, width=7)
        opacity_one.insert(0,"100")
        opacity_two = tk.Entry(frame_two_three, width=7)
        opacity_two.insert(0,"100")
        
        #BUTTON
        button_exit = tk.Button(frame_end, text="Close", font=bold10, command=self.destroy, bg="#000000", fg="#ffffff", highlightthickness=2, highlightbackground="#ffffff", activebackground="#ffffff", borderwidth=1, width=12, relief='groove')
        button_browse1 = tk.Button(frame_one_one,text="Browse file", command = browseFiles_one)
        button_browse2 = tk.Button(frame_two_one,text="Browse file", command = browseFiles_two)
        button_proceed = tk.Button(frame_param, text="Proceed", command =lambda: imagesFusion(entry_path_one.get(), entry_path_two.get()))
        
        #CHECKBUTTON  
        var_invert = tk.IntVar()
        var_delayed = tk.IntVar()
        var_progressive = tk.IntVar()
        check_delay = tk.Checkbutton(frame_param, text="Delayed (1s)",variable=var_delayed)
        check_progressive = tk.Checkbutton(frame_param, text="Progressive", variable=var_progressive)
        check_invert = tk.Checkbutton(frame_param, text="Invert order", variable=var_invert)
        
        ##############################PACKING################################
        
        #FRAMES INIT
        frame_head.pack(side=tk.TOP,padx=2, pady=2, fill = "x")
        frame_end.pack(side=tk.BOTTOM, padx=2, pady=2, fill = "x")
        frame_core.pack(fill='x')
        frame_one.pack(side=tk.LEFT, padx=1, pady=2, fill = "y")
        frame_two.pack(side=tk.RIGHT, padx=1, pady=2, fill = "y")
        frame_param.pack(side=tk.BOTTOM, fill='x', padx=2, pady='4')
        frame_param.config(highlightbackground="#000000")
        
        #FRAME HEAD
        label_title.pack()
        
        #FRAME ONE
        label_one.pack()
        avert_one.pack()
        frame_one_one.pack(padx=2, pady=5, fill ='x')
        frame_one_two.pack(padx=2, pady=5, fill ='x')
        frame_one_three.pack(padx=2, pady=5, fill ='x')
        #label_priority_one.pack(side=tk.LEFT)
        #priority_one.pack(side=tk.LEFT)
        label_opacity_one.pack(side=tk.LEFT)
        opacity_one.pack(side=tk.LEFT)
        label_path_one.pack(side=tk.LEFT)
        entry_path_one.pack(side=tk.LEFT)
        button_browse1.pack(side=tk.LEFT)
        
        #FRAME TWO
        label_two.pack()
        avert_two.pack()
        frame_two_one.pack(padx=2, pady=5, fill ='x')
        frame_two_two.pack(padx=2, pady=5, fill ='x')
        frame_two_three.pack(padx=2, pady=5, fill ='x')
        #label_priority_two.pack(side=tk.LEFT)
        #priority_two.pack(side=tk.LEFT)
        label_opacity_two.pack(side=tk.LEFT)
        opacity_two.pack(side=tk.LEFT)
        label_path_two.pack(side=tk.LEFT)
        entry_path_two.pack(side=tk.LEFT)
        button_browse2.pack(side=tk.LEFT)
        
        #Frame PARAMETERS
        check_invert.pack(pady='1')
        check_delay.pack(pady='1')
        check_progressive.pack(pady='1')
        progress.pack()
        button_proceed.pack(pady='6')
        
        #FRAME END
        button_exit.pack(side=tk.RIGHT)

if __name__ == "__main__":
    app = Application()
    app.title("Dynamic Picture Editor")
    app.mainloop()


