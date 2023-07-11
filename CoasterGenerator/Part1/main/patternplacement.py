import PIL
import os
import numpy as np
# import coaster_generator_0p1 as cg
from math import sqrt
from matplotlib import pyplot as plt

def gencirc(boundaryimg,rows,cols):  
    def invert_valuepair(valuelist):
        newvaluelist=[]
        for valuepair in valuelist:
            newvaluelist.append([valuepair[1],valuepair[0]])
        return newvaluelist

    def circle_gen(rad,mat,xcent,ycent):
        matcopy=mat
        avec=np.linspace(start=-rad,stop=rad,num=rad*2+1)
        resvalhigh=[]
        resvallow=[]
        for x in avec:
            # print('X:',x)
            # print('Type X:',type(x))
            x=int(x)
            y1=-1*sqrt(rad**2-x**2)
            y2=1*sqrt(rad**2-x**2)
            resvalhigh.append([x,round(y1)])
            resvallow.append([x,round(y2)])
        resvalinvhigh=invert_valuepair(resvalhigh)
        resvalinvlow=invert_valuepair(resvallow)
        totvallist=[]
        totvallist.append(resvalhigh)
        totvallist.append(resvallow)
        totvallist.append(resvalinvhigh)
        totvallist.append(resvalinvlow)
        totvallist2=[]
        for list in totvallist:
            for valuepair in list:
                rval=int(valuepair[0]+ycent)
                cval=int(valuepair[1]+xcent)
                matcopy[rval][cval]=255
                templist1=[rval,cval]
                if templist1 not in totvallist2:
                    totvallist2.append(templist1)

        # totvallist2=gen_list_of_pts(matcopy)
        return matcopy#,totvallist2

    startrad=int((cols/2)*.8)
    startxc=int(cols/2)
    startyc=int(rows/2)

    import tkinter as tk

    win1=tk.Tk()

    rad_lab=tk.Label(text='Radius').grid()
    rad_ent=tk.Entry()
    rad_ent.grid()

    xc_lab=tk.Label(text='X Center').grid()
    xc_ent=tk.Entry()
    xc_ent.grid()

    yc_lab=tk.Label(text='Y Center').grid()
    yc_ent=tk.Entry()
    yc_ent.grid()

    rad_ent.delete('0',tk.END)
    rad_ent.insert('0',startrad)
    xc_ent.delete('0',tk.END)
    xc_ent.insert('0',startxc)
    yc_ent.delete('0',tk.END)
    yc_ent.insert('0',startyc)



    def genfn():
        rad=int(rad_ent.get())
        xc=int(xc_ent.get())
        yc=int(yc_ent.get())
        newimcopy=np.copy(boundaryimg)
        modim=circle_gen(rad,newimcopy,xc,yc)
        plt.imshow(modim)
        plt.show()

    def closefn():
        global rad, xc, yc
        rad=int(rad_ent.get())
        xc=int(xc_ent.get())
        yc=int(yc_ent.get())
        win1.destroy()

    gen_butt=tk.Button(text='Generate',command=genfn).grid()
    close_butt=tk.Button(text='Save and Close',command=closefn).grid()
    win1.mainloop()
    # os.remove(imgpath)
    return rad,xc,yc