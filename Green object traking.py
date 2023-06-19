# first lines were taken from example: https://pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/

from collections import deque
from imutils.video import VideoStream
import numpy as np
import cv2
import imutils
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
import datetime as dt

root = tk.Tk()
root.geometry('1000x600')
root.title("Lapaj drona")
frame = tk.Frame(root)
frame.configure(bg='white')
REC_color='black'
Log_color='black'
# Lay out the main container (expand to fit window)
frame.pack(fill=tk.BOTH, expand=1)

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the list of tracked points
greenLower = (45,100,100)#(29, 86, 6)
greenUpper = (80,255,255)#(64, 255, 255)
#greenLower = (29, 86, 6)
#greenUpper = (64, 255, 255)
my_width=800
mylen=10
xs = []
x1s=[]
y1s=[]
pts = deque(maxlen=mylen)

vs = VideoStream(src=0).start()

# allow the camera or video file to warm up
time.sleep(2.0)
#vframe = vs.read()

fig1,(ax1,ax2)=plt.subplots(1,2)# figure()
fig1.set_figheight(4)
fig1.set_figwidth(10)
#fig1.tight_layout(pad=5.0)

plt.subplots_adjust(left=0.075,
                    bottom=0.1,
                    right=0.925,
                    top=0.9,
                    wspace=0.4)

ax1.set_xlim([0, my_width])
ax1.set_ylim([0, my_width])
#ax2.set_xlim([0, my_width])
ax2.set_ylim([0, my_width])

ax1.grid(True)
ax2.grid(True)

ax1.set_xlabel("Pozycja x")
ax1.set_ylabel("Pozycja y")
ax1.set_title("Położenie drona")

#ax2.set_xlabel("Pozycja x")
ax2.set_ylabel("Pozycja x")
ax3 = ax2.twinx()
ax3.set_ylabel("Pozycja y")
ax3.set_ylim([0, my_width])
ax2.set_title("Położenie drona")
ax2.yaxis.label.set_color('tab:blue')
ax3.yaxis.label.set_color('tab:red')

x1, y1=0,0
point1,=ax1.plot(x1, y1, "o", color="black")

#ax2.plot(x1, -y1, "o", color="black")

""" for ax in fig1.get_axes():
    ax.label_outer() """

""" point1,ax1=plt.plot(x1, y1, "o", color="black")
point2,ax2=plt.plot(x1, -y1, "o", color="black") """

show_img=True
show_mask=False
REC=False
LOG=False
frame_width = my_width #int(vs.get(3))
frame_height = 600 #int(vs.get(4))
   
size = (frame_width, frame_height)
result = cv2.VideoWriter('dron.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, size)
canvas1 = FigureCanvasTkAgg(fig1, master=frame)
canvas_plot1 = canvas1.get_tk_widget()
def show_image():
	global show_img
	global show_mask
	show_img=not(show_img)
	show_mask=not(show_mask)

def T_log():
	global LOG
	global Log_color
	#global canvas1
	LOG=not(LOG)
	if LOG is True:
		Log_color='red'
	else:
		Log_color='black'
	#
	#	TUTAJ DOLOZYC ZAPIS DO PLIKU
	#
	print(LOG)
	print(Log_color)
	button_log.config(fg=Log_color)

def T_record():
	global REC
	global REC_color
	global size
	global result
	REC=not(REC)
	
	if REC is True:
		result = cv2.VideoWriter('dron.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, size)
		REC_color='red'
	else:
		REC_color='black'
		result.release()
	button_record.config(fg=REC_color)

def slider_def():
	H1_slider.set(45)
	S1_slider.set(100)
	V1_slider.set(100)
	H2_slider.set(80)
	S2_slider.set(255)
	V2_slider.set(255)

button_light = tk.Button(   frame,
                            text="Przelacz obraz",
                            font=12,
                            command=show_image)
button_record = tk.Button(   frame,
                            text="Record",
                            font=12,
                            command=T_record, fg=REC_color)
button_log = tk.Button(   frame,
                            text="Log",
                            font=12,
                            command=T_log, fg=Log_color)

button_quit = tk.Button(    frame,
                            text="Quit",
                            font=12,
                            command=root.destroy)
canvas_plot1.grid(	row=2,	column=0,	rowspan=5,	columnspan=10,	sticky=tk.W+tk.E+tk.N+tk.S)
button_light.grid(row=0, column=6, columnspan=1)
button_record.grid(row=0, column=7, columnspan=1)
button_log.grid(row=0, column=8, columnspan=1)
button_quit.grid(row=0, column=9, columnspan=1)

button_light = tk.Button(   frame,
                            text="slider_def",
                            font=12,
                            command=slider_def)
button_light.grid(row=1, column=6, columnspan=1)

current_value_H1 = tk.IntVar()
current_value_S1 = tk.IntVar()
current_value_V1 = tk.IntVar()
current_value_H2 = tk.IntVar()
current_value_S2 = tk.IntVar()
current_value_V2 = tk.IntVar()

def slider_changed(event):
    global greenLower
    global greenUpper
    greenLower = (current_value_H1.get(),current_value_S1.get(),current_value_V1.get())
    greenUpper = (current_value_H2.get(),current_value_S2.get(),current_value_V2.get())
    #print((current_value_H1.get(),current_value_S1.get(),current_value_V1.get()),(current_value_H2.get(),current_value_S2.get(),current_value_V2.get()))
    


# label for the slider
H1_slider_label = ttk.Label(    frame,    text='H1')
H1_slider_label.grid(    column=0,    row=0,    sticky='w')
H1_slider = ttk.Scale(    frame,    from_=255,    to=0,    orient='vertical',  command=slider_changed,    variable=current_value_H1)
H1_slider.set(45)
H1_slider.grid(     column=0,    row=1,    sticky='w')

S1_slider_label = ttk.Label(    frame,    text='S1')
S1_slider_label.grid(    column=1,    row=0,    sticky='w')
S1_slider = ttk.Scale(    frame,    from_=255,    to=0,    orient='vertical',  command=slider_changed,    variable=current_value_S1)
S1_slider.set(100)
S1_slider.grid(     column=1,    row=1,    sticky='w')

V1_slider_label = ttk.Label(    frame,    text='V1')
V1_slider_label.grid(    column=2,    row=0,    sticky='w')
V1_slider = ttk.Scale(    frame,    from_=255,    to=0,    orient='vertical',  command=slider_changed,    variable=current_value_V1)
V1_slider.set(100)
V1_slider.grid(     column=2,    row=1,    sticky='w')

H2_slider_label = ttk.Label(    frame,    text='H2')
H2_slider_label.grid(    column=3,    row=0,    sticky='w')
H2_slider = ttk.Scale(    frame,    from_=255,    to=0,    orient='vertical',  command=slider_changed,    variable=current_value_H2)
H2_slider.set(80)
H2_slider.grid(     column=3,    row=1,    sticky='w')

S2_slider_label = ttk.Label(    frame,    text='S2')
S2_slider_label.grid(    column=4,    row=0,    sticky='w')
S2_slider = ttk.Scale(    frame,    from_=255,    to=0,    orient='vertical',  command=slider_changed,    variable=current_value_S2)
S2_slider.set(255)
S2_slider.grid(     column=4,    row=1,    sticky='w')

V2_slider_label = ttk.Label(    frame,    text='V2')
V2_slider_label.grid(    column=5,    row=0,    sticky='w')
V2_slider = ttk.Scale(    frame,    from_=255,    to=0,    orient='vertical',  command=slider_changed,    variable=current_value_V2)
V2_slider.set(255)
V2_slider.grid(     column=5,    row=1,    sticky='w')



def animate(i, ax2, xs, x1s, y1s):
# keep looping
#while True:
	# grab the current frame
	vframe = vs.read()
	# resize the frame, blur it, and convert it to the HSV color space
	vframe = imutils.resize(vframe, width=my_width)
	if REC is True:
		result.write(vframe)

	blurred = cv2.GaussianBlur(vframe, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
	# construct a mask for the color "green", then perform a series of dilations and erosions to remove any small blobs left in the mask
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	if show_mask is True:
		cv2.imshow("Frame", mask)
		#show_img = False
    # find contours in the mask and initialize the current (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	#print(cnts)
	center = None
	# jesli wykryty kontury
	if len(cnts) > 0:
		# find the largest contour in the mask, then use it to compute the minimum enclosing circle and centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame, then update the list of tracked points
			cv2.circle(vframe, (int(x), int(y)), int(radius), (0, 255, 255), 2)
			cv2.circle(vframe, center, 5, (0, 0, 255), -1)
	# update the points queue
	pts.appendleft(center)
	
    # loop over the set of tracked points
	for i in range(1, len(pts)):
		# if either of the tracked points are None, ignore them
		if pts[i - 1] is None or pts[i] is None:
			continue
		# otherwise, compute the thickness of the line and draw the connecting lines
		thickness = int(np.sqrt( mylen / float(i + 1)) * 2.5)
		cv2.line(vframe, pts[i - 1], pts[i], (0, 0, 255), thickness)

	# show the frame to our screen
	if show_img is True:
		cv2.imshow("Frame", vframe)
		#show_mask = False
	#key = cv2.waitKey(1) & 0xFF
	# if the 'q' key is pressed, stop the loop
	#if key == ord("q"):
	#	break
	if center is not None:
		#print("OK", center)
		x1,b=center
		y1=my_width-b
		timestamp = mdates.date2num(dt.datetime.now())
		xs.append(timestamp)
		xs = xs[-max_elements:]
		x1s.append(x1)
		y1s.append(y1)
		x1s = x1s[-max_elements:]
		y1s = y1s[-max_elements:]
		point1.set_xdata(x1)
		point1.set_ydata(y1)
		#point2.set_xdata(x1)
		#point2.set_ydata(-y1)
		ax2.plot(xs, x1s, linewidth=1, color='tab:blue', label ="x position")
		ax3.plot(xs, y1s, linewidth=1, color='tab:red', label ="y position")
		ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
		fig1.autofmt_xdate()
	#else:
		#print(center)
max_elements=100
fargs=(ax2, xs, x1s, y1s)
anim1 = animation.FuncAnimation(fig1, animate ,fargs=fargs,frames=80, interval=100, repeat=True)

#plt.show()

root.mainloop()

vs.stop()

if REC is True:
	result.release()
# close all windows
cv2.destroyAllWindows()