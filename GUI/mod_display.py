import sys
import os
import time
import schedule
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from PIL import ImageTk,Image
import matplotlib
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
def split(word):
	return [char for char in word]
def plot(lines):
	plt.clf()
	lastline=lines[-1]
	pred=np.array(split(lastline[:14]),dtype=np.int32)
	true=np.array(split(lastline[14:-2]),dtype=np.int32)
	exec_time_hw=float(lastline[-2])
	x=np.arange(1,15)
	print(len(pred),len(true),exec_time_hw)
	plt.bar(x,pred)
	plt.bar(x,true)
	# plt.draw()
	# plt.show()

def job():
	os.system('echo y | pscp -pw root -P 22 root@192.168.0.10:/mnt/dump.txt .')
	file=open('dump.txt','r')
	lines=file.readlines()
	plot(lines)




# schedule.every(2).seconds.do(job)


# while 1:
# 	schedule.run_pending()
# 	time.sleep(1)


# from tkinter import * 
# from matplotlib.figure import Figure
# from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
# NavigationToolbar2Tk)
  
# # plot function is created for 
# # plotting the graph in 
# # tkinter window
# def plot():
  
#     # the figure that will contain the plot
#     fig = Figure(figsize = (5, 5),
#                  dpi = 100)
  
#     # list of squares
#     y = [i**2 for i in range(101)]
  
#     # adding the subplot
#     plot1 = fig.add_subplot(111)
  
#     # plotting the graph
#     plot1.plot(y)
  
#     # creating the Tkinter canvas
#     # containing the Matplotlib figure
#     canvas = FigureCanvasTkAgg(fig,
#                                master = window)  
#     canvas.draw()
  
#     # placing the canvas on the Tkinter window
#     canvas.get_tk_widget().pack()
  
#     # creating the Matplotlib toolbar
#     toolbar = NavigationToolbar2Tk(canvas,
#                                    window)
#     toolbar.update()
  
#     # placing the toolbar on the Tkinter window
#     canvas.ge
#font={'family': 'normal','weight':'bold','size':15}
#matplotlib.rc('font',**font)
size=12
matplotlib.rc('xtick',labelsize=size)
matplotlib.rc('ytick',labelsize=size)
matplotlib.rc('axes',labelsize=size)
def spectrum(bands):
	samples=14000
	f=np.zeros(samples)
	block=f.shape[0]//14
	
	for b in bands:
		f[block*(b):(b+1)*block]=np.ones(block)
		if b!=0 :

				f[block*(b-1)+block//2:block*b]=np.linspace(0,1,block//2)
		if b!=13:
				f[block*(b)+block//2:block*(b+1)]=np.linspace(1,0,block//2)
	noise=np.random.normal(0,0.25,samples)
	return f+noise


class App:
	def __init__(self,master):
		self.master=master
		self.pred_1=0
		self.true_1=0
		self.pred_1_all=0
		self.true_1_all=0
		self.pd_occ=0
		self.pd_all=0
		self.sample=0
		self.exec_time=0
		self.accs_occ=[]
		self.accs_all=[]

		# self.loop()
	def loop(self):
		os.system('echo y | pscp -pw root -P 22 root@192.168.0.10:/mnt/dump.txt .')
		file=open('dump.txt','r')
		lines=file.readlines()
		lastline=list(map(float,lines[-1].split()))
		pred=np.array(lastline[:14])
		true=np.array(lastline[14:28])
		self.exec_time=lastline[30] /1000
		self.pd_all=lastline[28]*100
		self.pd_occ=lastline[29]*100
		self.sample=lastline[31]
		pd_all="{:.3f}".format(self.pd_all)
		pd_occ="{:.3f}".format(self.pd_occ)
		self.accs_all.append(self.pd_all)
		self.accs_occ.append(self.pd_occ)
		x=np.arange(1,15)
		vec=np.arange(0,14)
		pred_bands=spectrum(vec[pred==1].tolist())
		true_bands=spectrum(vec[true==1].tolist())
		# print(pred_bands)
		plt.figure(figsize=(6,5),dpi=100)
		# print(len(pred),len(true))
		
		plt.plot(np.arange(pred_bands.shape[0])/1000,pred_bands)
		plt.xticks(np.arange(0,14,1))
		plt.xlabel("Bands")
		plt.ylabel("Amplitude")
		plt.savefig("plot_pred.png")
		plt.close()
		plt.figure(figsize=(6,5),dpi=100)
		plt.plot(np.arange(pred_bands.shape[0])/1000,true_bands)
		plt.xlabel("Bands")
		# plt.ylim([40,100])
		plt.ylabel("Amplitude")
		plt.xticks(np.arange(0,14,1))
		plt.savefig("plot_true.png")

		plt.close()
		fig,ax=plt.subplots()
		plt.figure(figsize=(7.3,5),dpi=100)
		plt.scatter(np.arange(0,len(self.accs_occ)),self.accs_occ)
		plt.scatter(np.arange(0,len(self.accs_occ)),self.accs_all)
		plt.legend(["Occupied bands","All bands"])
		plt.xlabel("# of Samples")
		plt.ylabel("Accuracy (%)")
		plt.savefig("plot_accs_progs.png")
		from matplotlib.ticker import FormatStrFormatter
		ax.yaxis.set_major_formatter(FormatStrFormatter('%g'))
		ax.yaxis.set_ticks(np.arange(98,100,0.5))
		plt.close()
		time.sleep(1)

		self.prog_img=ImageTk.PhotoImage(Image.open("plot_accs_progs.png"))
		self.label_pred_img=ImageTk.PhotoImage(Image.open("plot_pred.png"))
		self.label_true_img=ImageTk.PhotoImage(Image.open("plot_true.png"))
		label_pred.configure(image=self.label_pred_img)
		label_true.configure(image=self.label_true_img)

		label_time.configure(image=self.prog_img)

		label_acc_occ_box.delete('1.0',tk.END)
		label_acc_occ_box.insert(tk.END,self.pd_occ)

		label_acc_all_box.delete('1.0',tk.END)
		label_acc_all_box.insert(tk.END,self.pd_all)
		
		sample_count_box.delete('1.0',tk.END)
		sample_count_box.insert(tk.END,self.sample)

		hwtime_box.delete('1.0',tk.END)
		hwtime_box.insert(tk.END,self.exec_time)

		
		win.after(1000,self.loop)


win=tk.Tk()
win.title("DLWSS")
win.geometry("1400x1000")


label_pred=tk.Label(win,text="Predicted Bands",compound='bottom')
label_pred.configure(font=("Arial",25),background="yellow")
label_pred.pack()
label_pred.place(relx=0.17,rely=0.5,anchor='center')
label_true=tk.Label(win,text="Actual Bands",compound='bottom')
label_true.configure(font=("Arial",25),background="yellow")
label_true.pack()
label_true.place(relx=0.48,rely=0.5,anchor='center')
label_time=tk.Label(win,text="Accuracy with time",compound='bottom')
label_time.configure(font=("Arial",25),background="yellow")
label_time.pack()
label_time.place(relx=0.82,rely=0.5,anchor='center')
win['background']='#171616'
label_acc=tk.Label(win,text="Accuracy of all bands")
label_acc.configure(font=("Arial",25),background="yellow")
label_acc.pack()
label_acc.place(relx=0.75,rely=0.95,anchor="center")
label_acc_occ=tk.Label(win,text="Accuracy of occupied bands")
label_acc_occ.configure(font=("Arial",25),background="yellow")
label_acc_occ.pack()
label_acc_occ.place(relx=0.75,rely=0.85,anchor="center")
label_acc_all_box=tk.Text(height=1,width=5,font=("Arial",25),highlightthickness=4)
label_acc_all_box.place(relx=0.9,rely=0.95,anchor="center")

label_title=tk.Label(win,text="Real time Spectrum Sensing on the board")
label_title.configure(font=("Arial",50,'bold'),background="#171616",foreground='yellow',highlightthickness=4)
label_title.pack()
label_title.place(relx=0.5,rely=0.1,anchor="center")



label_acc_occ_box=tk.Text(height=1,width=5,font=("Arial",25),highlightthickness=4)
label_acc_occ_box.place(relx=0.9,rely=0.85,anchor="center")

sample_count_label=tk.Label(master=win,text="Number of samples",font=("Arial",25),background='yellow')
sample_count_label.pack()
sample_count_label.place(relx=0.45,rely=0.8,anchor="center")

sample_count_box=tk.Text(height=1,width=5,font=("Arial",25),highlightthickness=4)
sample_count_box.place(relx=0.58,rely=0.8,anchor="center")



swtime_label=tk.Label(master=win,text="SW Exec time(s)",font=("Arial",25),background='yellow')
swtime_label.pack()
swtime_label.place(relx=0.1,rely=0.85,anchor="center")
swtime_box=tk.Text(height=1,width=5,font=("Arial",25),highlightthickness=4)
swtime_box.place(relx=0.2,rely=0.85,anchor="center")
swtime_box.insert(tk.END,30.8)


hwtime_label=tk.Label(master=win,text="HW Exec time(s)",font=("Arial",25),background='yellow')
hwtime_label.pack()
hwtime_label.place(relx=0.1,rely=0.95,anchor="center")
hwtime_box=tk.Text(height=1,width=5,font=("Arial",25),highlightthickness=4)
hwtime_box.place(relx=0.2,rely=0.95,anchor="center")




app=App(win)

start_button=tk.Button(master=win,command=app.loop,text="START",bg='#02fa8b',width=8,height=2,font=("Arial",25,"bold"))
start_button.pack()
start_button.place(relx=0.5,rely=0.9,anchor="center")


logo_img=ImageTk.PhotoImage((Image.open("logo.jpg")).resize((150,100)))
label_logo=tk.Label(win)
label_logo.configure(image=logo_img)
label_logo.place(relx=0.9,rely=0.05)

a2a_img=ImageTk.PhotoImage((Image.open("a2a.jpg")).resize((150,100)))
label_a2a=tk.Label(win)
label_a2a.configure(image=a2a_img)
label_a2a.place(relx=0.02,rely=0.05)



# lbl=tk.Label(text="predictions")
# lbl.grid(row=1,column=0)
# pred_text=tk.Label(win,text='loading')
# pred_text.grid(row=1,column=1)
win.mainloop()