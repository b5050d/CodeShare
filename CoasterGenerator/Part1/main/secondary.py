import os
import PIL
from matplotlib import pyplot as plt
import numpy as np
from math import sqrt
import math
from math import acos
import cv2
import struct


#This file will be used to define general functions that are to be used in our primary module
def s1_getborderavg(img,rows,cols):
    """This function will find the average value of that appears on the edges of an image"""
    rowct=0
    border=[]
    for row in img:
        colct=0
        if rowct==0:
            firstrow=row
        elif rowct==rows-1:
            lastrow=row
        else:
            pass
        for col in row:
            if colct==0:
                border.append(col)
            elif colct==cols-1:
                border.append(col)
            else:
                pass
            colct+=1
        rowct+=1
    for item in firstrow:
        border.append(item)
    for itme in lastrow:
        border.append(item)
    borderavg=int(sum(border)/len(border))
    return borderavg

def s2_fourlistgen(img,rowct,colct):
    """This function will look at the 4 pixels surrounding the pixel of interest and return a list of 4 with 1 representing a dark pixel, and 0 representing a light pixel"""
    fourlist=[]
    try:
        if img[rowct][colct-1]==0:
            fourlist.append(1)
        else:
            fourlist.append(0)
    except:
        fourlist.append(0)
    try:
        if img[rowct][colct+1]==0:
            fourlist.append(1)
        else:
            fourlist.append(0)
    except:
        fourlist.append(0)
    try:
        if img[rowct-1][colct]==0:
            fourlist.append(1)
        else:
            fourlist.append(0)
    except:
        fourlist.append(0)
    try:
        if img[rowct+1][colct]==0:
            fourlist.append(1)
        else:
            fourlist.append(0)
    except:
        fourlist.append(0)
    return fourlist

def s2p5_genlistofpts(boundaryimg):
    """This function will generate a list of points based on the boundary image, contains max amount of possible points, we will need to reduce this later"""
    edges=[]
    boundaryimg2=np.copy(boundaryimg)
    stopcondition1=0
    while stopcondition1==0:
        # We need to find the first point that 255 exists in the images
        flag=True
        rowct=0
        firstcol=-1
        firstrow=-1
        for row in boundaryimg2:
            colct=0
            for col in row:
                if col==255:
                    firstcol=colct
                    firstrow=rowct
                    break
                    flag=False
                colct+=1
            if flag==False:
                break
            rowct+=1
        if firstcol==-1 and firstrow==-1:
            stopcondition1=1
        else:
            edgelist=[]
            stopcondition3=0
            row1=firstrow
            col1=firstcol
            while stopcondition3==0:
                boundaryimg2[row1][col1]=0
                edgelist.append([row1,col1])
                eightlist=s3_eightlistgen(boundaryimg2,row1,col1)
                row1,col1=s4_eightlisinterpret(row1,col1,eightlist,boundaryimg2)
                if row1==-1:
                    stopcondition3=1
                    edges.append(edgelist)
                else:
                    pass
    return edges

def s3_eightlistgen(img,row,col):
    """This function will go through CW starting from the left pixel and check for high pixels"""
    eightlist=[]
    if img[row,col-1]==255: # Left
        eightlist.append(1)
    else:
        eightlist.append(0)
    if img[row-1,col-1]==255: # Upper Left
        eightlist.append(1)
    else:
        eightlist.append(0)
    if img[row-1,col]==255: # Upper
        eightlist.append(1)
    else:
        eightlist.append(0)
    if img[row-1,col+1]==255: #Upper Right
        eightlist.append(1)
    else:
        eightlist.append(0)
    if img[row,col+1]==255: # Right
        eightlist.append(1)
    else:
        eightlist.append(0)
    if img[row+1,col+1]==255: # Lower Right
        eightlist.append(1) 
    else:
        eightlist.append(0)
    if img[row+1,col]==255: # Lower
        eightlist.append(1)
    else:
        eightlist.append(0)
    if img[row+1,col-1]==255: # Lower Left
        eightlist.append(1)
    else:
        eightlist.append(0)
    return eightlist

def s4_eightlisinterpret(row1,col1,eightlist,img):
    """This function will interpret the list of 8 that is generated in the s3_eightlistgen function"""
    numones=eightlist.count(1)
    if numones==0:
        row1=-1
        col1=-1
        return row1,col1

    if numones==2:
        pos2=eightlist.index(1)
        eightlist[pos2]=0
        pos1=eightlist.index(1)
        
        # So for pos1 and pos2, find out how many path's forward there are
        trow1,tcol1=s5_return8address(row1,col1,pos1)
        trow2,tcol2=s5_return8address(row1,col1,pos2)
        eightlist1=s3_eightlistgen(img,trow1,tcol1)
        eightlist2=s3_eightlistgen(img,trow2,tcol2)
        numones1=eightlist1.count(1)
        numones2=eightlist2.count(1)
        if numones1>=numones2:
            #Choose numones2
            row1=trow2
            col1=tcol2
        elif numones2>numones1:
            row1=trow1
            col1=tcol1
        return row1,col1
    else:
        eightlist.reverse()
        lastone=eightlist.index(1)
        pos=len(eightlist)-1-lastone
        row1,col1=s5_return8address(row1,col1,pos)
        return row1,col1

def s5_return8address(row1,col1,pos1):
    """This function will take a position and caluclate what your coords should be given the CW loop"""
    if pos1==0:
        row1=row1
        col1=col1-1
    elif pos1==1:
        row1=row1-1
        col1=col1-1
    elif pos1==2:
        row1=row1-1
        col1=col1
    elif pos1==3:
        row1=row1-1
        col1=col1+1
    elif pos1==4:
        row1=row1
        col1=col1+1
    elif pos1==5:
        row1=row1+1
        col1=col1+1
    elif pos1==6:
        row1=row1+1
        col1=col1
    elif pos1==7:
        row1=row1+1
        col1=col1-1
    else:
        pass
    return row1,col1

def s6_invertvaluepair(valuelist):
    newvaluelist=[]
    for valuepair in valuelist:
        newvaluelist.append([valuepair[1],valuepair[0]])
    return newvaluelist

def s7_3pts_angle(pt1,pt2,pt3):
    """This function will return the angle between the three points if pt2 is vertex"""
    p21=s8_dist_bt_2pts(pt2,pt1)
    p23=s8_dist_bt_2pts(pt2,pt3)
    p13=s8_dist_bt_2pts(pt1,pt3)
    precos=((p21**2)+(p23**2)-(p13**2))/(2*p21*p23)
    try: #This try loop is for when the precos might ==-1.00000002
        theta=math.degrees(acos(precos))
    except:
        precos=round(precos)
        theta=math.degrees(acos(precos))
    return theta

def s8_dist_bt_2pts(pt1,pt2):
    #Simply Returns the distance between 2 points
    dist=sqrt(((pt1[0]-pt2[0])**2)+((pt1[1]-pt2[1])**2))
    return dist

def s9_checkintersect(p1,p2,p3,p4):
    """This function will determine if two line segments intersect"""
    p1x=round(p1[0],6)
    p1y=round(p1[1],6)
    p2x=round(p2[0],6)
    p2y=round(p2[1],6)
    p3x=round(p3[0],6)
    p3y=round(p3[1],6)
    p4x=round(p4[0],6)
    p4y=round(p4[1],6)
    p1=[p1x,p1y]
    p2=[p2x,p2y]
    p3=[p3x,p3y]
    p4=[p4x,p4y]
    s1,a1,t1=s10_returnline(p1,p2)
    s2,a2,t2=s10_returnline(p3,p4)
    if t1=='vert' and t2=='vert':
        if not p1[0]==p3[0]:
            return False
        elif p1[0]==p3[0]:
            y1=p3[1]
            y2=p4[1]
            if y1>y2:
                yhigh=y1
                ylow=y2
            elif y1<y2:
                yhigh=y2
                ylow=y1
            else:
                yhigh=y1
                ylow=y2
            if p1[1]<=yhigh and p1[1]>=ylow:
                # print('We have an intersection, the first segpts yvalue is between the despt yvals')
                return True
            elif p2[1]<=yhigh and p2[1]>=ylow:
                # print('We have an intersection, the first segpts yvalue is between the despt yvals')
                return True
            else:
                return False
    elif t1=='vert':
        # print('Slope of the first segment is vertical')
        tempvar1=s11_verticalintersect(p1,p2,p3,p4)
        return tempvar1
    elif t2=='vert':
        # print('Slope desired segment is Vertical')
        tempvar1=s11_verticalintersect(p3,p4,p1,p2)
        return tempvar1
    else:
        try:
            interx=(a2-a1)/(s1-s2)
            intery=(s1*interx)+a1
            xvar='no'
            yvar='no'
            if p1[0]>p2[0]:
                if p2[0]<=interx and p1[0]>=interx:
                    xvar='yes'
            elif p1[0]<p2[0]:
                if p1[0]<=interx and p2[0]>=interx:
                    xvar='yes'
            else:
                if interx==p1[0]:
                    xvar='yes'
            if p1[1]>p2[1]:
                if p2[1]<=intery and p1[1]>=intery:
                    yvar='yes'
            elif p1[1]<p2[1]:
                if p1[1]<=intery and p2[1]>=intery:
                    yvar='yes'
            else:
                if intery==p2[1]:
                    yvar='yes'
            if xvar=='yes' and yvar=='yes':
                seg1='yes'
            else:
                seg1='no'
            xvar='no'
            yvar='no'
            if p3[0]>p4[0]:
                if p4[0]<=interx and p3[0]>=interx:
                    xvar='yes'
            elif p3[0]<p4[0]:
                if p3[0]<=interx and p4[0]>=interx:
                    xvar='yes'
            else:
                if interx==p3[0]:
                    xvar='yes'
            if p3[1]>p4[1]:
                if p4[1]<=intery and p3[1]>=intery:
                    yvar='yes'
            elif p3[1]<p4[1]:
                if p3[1]<=intery and p4[1]>=intery:
                    yvar='yes'
            else:
                if intery==p4[1]:
                    yvar='yes'
            if xvar=='yes' and yvar=='yes':
                seg2='yes'
            else:
                seg2='no'
            if seg1=='yes' and seg2=='yes':
                return True
            else:
                return False
        except:
            return True #Changed this may break all things, seems to have not

def s10_returnline(p1,p2):
    """This function will take 2 pts and return the slope and y intercept"""
    try:
        s=(p2[1]-p1[1])/(p2[0]-p1[0])
        t='notvert'
        a=p1[1]-(s*p1[0])
    except:
        t='vert'
        s=0
        a=p2[0]
    return s, a, t

def s11_verticalintersect(vp1,vp2,p3,p4):
    """This is used in to determine if there is an intersect when one of the segments is vertical"""
    xline=vp1[0]
    ylim1=vp1[1]
    ylim2=vp2[1]
    ylimd1=p3[1]
    ylimd2=p4[1]
    s1,a1,t1=s10_returnline(p3,p4)
    y=(s1*xline)+a1
    if ylim1>ylim2:
        yhigh=ylim1
        ylow=ylim2
    elif ylim1<ylim2:
        yhigh=ylim2
        ylow=ylim1
    else:
        yhigh=ylim1
        ylow=ylim2
    if ylimd1>ylimd2:
        yhighd=ylimd1
        ylowd=ylimd2
    elif ylimd1<ylimd2:
        yhighd=ylimd2
        ylowd=ylimd1
    else:
        yhighd=ylimd1
        ylowd=ylimd2
    if y<=yhigh and y>=ylow: # print('The Intersect is within the vertical Segment')
        if y<=yhighd and y>=ylowd:
            return True
        else:
            return False
    else: # print('There is not an intersect within the vertical segment')
        return False

def s12_reduceparents(itemscrossed):
    """This function will eliminate repeated parents and return a new parents list with a new number of intersections"""
    uniqueparents=[]
    for parent in itemscrossed:
        if parent not in uniqueparents:
            uniqueparents.append(parent)
    return uniqueparents

def s13_generatesegments(list):
    """This function will go through all the values in a list and generate segments"""
    segments=[]
    itemct=0
    for item in list:
        if itemct==len(list)-1:
            # print('This is the final value')
            newseg=[item,list[0]]
        else:
            newseg=[item,list[itemct+1]]
        segments.append(newseg)
        itemct+=1
    return segments

# def s14_hierarchy(p1,allsegments,allidentities,listct):
#     """This function will take a single point and determine the hierarchical position of the list"""
#     itemscrossed=[]
#     segct=0
#     for seglist in allsegments:
#         if segct==listct:
#             pass
#         else:
#             for seg in seglist:
#                 a=s9_checkintersect(seg[0],seg[1],[0,0],p1)
#                 if a==True:
#                     itemscrossed.append(allidentities[segct])
#         segct+=1
#     uniqueparents,uniquenum=s12_reduceparents(itemscrossed)
#     return uniqueparents,uniquenum

def s14_familyfinder(closept,edge_id,hier):
    itemscrossed = []
    for edge in hier:
        if edge== edge_id:
            pass
        else:
            for seg in hier[edge]["Segments"]:
                ans = s9_checkintersect(seg[0],seg[1],[0,0],closept)
                if ans == True:
                    itemscrossed.append(edge)
        uniqueparents = s12_reduceparents(itemscrossed)
    return uniqueparents



def s15_findclosept(ptslist):
    distlist=[]
    for pt in ptslist:
        dist=s8_dist_bt_2pts(pt,[0,0])
        distlist.append(dist)
    mindist=min(distlist)
    minidx=distlist.index(mindist)
    closestpt=ptslist[minidx]
    return closestpt

def s16_cutinvert(p1,list):
    p1idx=list.index(p1)
    newlist=[]
    lenlist=len(list)
    indxlist=[]
    for i in range(lenlist):
        indxlist.append(p1idx-i)
    for val in indxlist:
        newlist.append(list[val])
    return newlist

def s17_generatesegmentpairs(seglist):
    """This function will take a list of segments and generate a list of segment pairs"""
    segpairlist=[]
    segct=0
    for segment in seglist:
        if segct==len(seglist)-1:
            #this is the final one
            newpair=[segment,seglist[0]]
        else:
            newpair=[segment,seglist[segct+1]]
        segpairlist.append(newpair)
        segct+=1
    return segpairlist

def s18_find_min_no_intersect_3p0(segments,pairs,angles):
    """This function will find the miniumum angle that does not produce an intersection"""
    a1=angles
    a2=set(a1)
    a3=sorted(a2)
    indexlist=[]
    for item in a3:
        p=s22_find_occ_pos(angles,item)
        for thing in p:
            indexlist.append(thing)
    iteration1=0
    sc=0
    print('indexlist:',indexlist)
    while sc==0:
        minangleidx=indexlist[iteration1]
        igval1=pairs[minangleidx][0][0]
        igval2=pairs[minangleidx][0][1]
        igval3=pairs[minangleidx][1][1]
        tempseglist=[]
        for segment in segments:
            if igval1 in segment:
                pass
            elif igval2 in segment:
                pass
            elif igval3 in segment:
                pass
            else:
                tempseglist.append(segment)
        # print('Temp Seg List:',tempseglist)
        resultlist=[]
        for segment in tempseglist:
            res1=s9_checkintersect(segment[0],segment[1],igval1,igval3) # Takes 4 points
            resultlist.append(res1)
        # print('Results:',resultlist)
        if True not in resultlist:
            # print('We found a thing with no intersections!')
            sc=1
            return minangleidx
        else:
            # print('There is an intersection :/')
            if iteration1==len(indexlist)-1:
                print('ALL AVAILABLE WERE INTERSECTED')
                sc=1
            iteration1+=1

def s19_find_occ_pos(list,item):
    positions=[]
    itemct=0
    sc=0
    while sc==0:
        try:
            itemct = list.index(item, itemct)
            positions.append(itemct)
            itemct += 1
        except: 
            sc=1
    return positions

def s20_generate_angle_list(segpairs,seglist):
    anglelist=[]
    for segpair in segpairs:
        # print('Segment Pair:',segpair)
        pt1=segpair[0][0]
        pt2=segpair[0][1]
        pt3=segpair[1][1]
        a=s21_check_interior(pt1,pt3,seglist)
        theta=s26_angle_bt_3pts(pt1,pt2,pt3)
        if a%2==0:
            # This is even
            theta=360-theta
        else:
            # This is odd
            pass
        anglelist.append(theta)
    return anglelist

def s21_check_interior(pt1,pt3,listofsegments):
    """This function will take any angle and determine if it is within the interior, convex"""
    # Find the midpoint
    midpt=s24_find_midpt(pt1,pt3)
    print('Mid Point:',midpt)
    #So we need to raytrace
    intercounts=0
    segmentcount=0
    for segment in listofsegments:
        # print('Next Segment:',segment)
        # print('Next Segment[0]:',segment[0])
        # print('Next Segment[1]:',segment[1])
        # print('determine_intersect({},{},{},{})'.format(segment[0],segment[1],[0,0],midpt))
        interval=s9_checkintersect(segment[0],segment[1],[0,0],midpt)
        if interval==True:
            intercounts+=1
        segmentcount+=1
    # print("Amount of intersections",intercounts)
    # print("Amount of segments checked",segmentcount)
    return intercounts

def s22_find_occ_pos(list,item):
    positions=[]
    itemct=0
    sc=0
    while sc==0:
        try:
            itemct = list.index(item, itemct)
            positions.append(itemct)
            itemct += 1
        except: 
            sc=1
    return positions

def s23_generate_angle_local(segpair,seglist):
    pt1=segpair[0][0]
    # print('Point1:',pt1)
    # print('Point2:',pt2)
    # print('Point3:',pt3)
    pt2=segpair[0][1]
    pt3=segpair[1][1]
    a=s21_check_interior(pt1,pt3,seglist)
    theta=s26_angle_bt_3pts(pt1,pt2,pt3)
    if a%2==0:
        # This is even
        theta=360-theta
    else:
        # This is odd
        pass
    return theta

def s24_find_midpt(pt1,pt2):
    """This function will take two points and return the midpoint between them"""
    xval=((pt2[0]-pt1[0])/2)+pt1[0]
    yval=((pt2[1]-pt1[1])/2)+pt1[1]
    midpt=[xval,yval]
    return midpt

def s25_dist_bt_2pts(pt1,pt2):
    """Simply Returns the distance between 2 points"""
    dist=sqrt(((pt1[0]-pt2[0])**2)+((pt1[1]-pt2[1])**2))
    return dist

def s26_angle_bt_3pts(pt1,pt2,pt3):
    """This function will find the angle between 3 points with pt2 as the vertex"""
    p21=s25_dist_bt_2pts(pt2,pt1)
    p23=s25_dist_bt_2pts(pt2,pt3)
    p13=s25_dist_bt_2pts(pt1,pt3)
    try:
        precos=((p21**2)+(p23**2)-(p13**2))/(2*p21*p23)
    except:
        print("Point1 : {}, Point2 : {}, Point3 : {}, ".format(pt1,pt2,pt3))
        # input('User Pause')
    try:
        theta=math.degrees(acos(precos))
    except:
        # print(precos)
        # input('User Pause')
        precos=round(precos)
        theta=math.degrees(acos(precos))
    return theta

def s27_split_to_xy(ptslist):
    x=[]
    y=[]
    for pt in ptslist:
        x.append(pt[0])
        y.append(pt[1])
    return x,y

def s28_return_ranges(ptslist):
    x,y=s27_split_to_xy(ptslist)
    xran=max(x)-min(x)
    yran=max(y)-min(y)
    return xran,yran,x,y

def s29_3pts_angle_mod(vpt1,pt2,pt3):
    """This function will return the angle between the three points if pt2 is vertex"""
    
    p21=s25_dist_bt_2pts(pt2,vpt1)
    p23=s25_dist_bt_2pts(pt2,pt3)
    p13=s25_dist_bt_2pts(vpt1,pt3)
    try:
        precos=((p21**2)+(p23**2)-(p13**2))/(2*p21*p23)
    except:
        print('Vpt1:',vpt1)
        print('pt2:',pt2)
        print('pt3:',pt3)
        print('p21',p21)
        print('p23',p23)
        print('p13',p13)
        # input('USer Pause')
    try: #This try loop is for when the precos might ==-1.00000002
        theta=math.degrees(acos(precos))
    except:
        precos=round(precos)
        theta=math.degrees(acos(precos))

    if pt3[0]<pt2[0]:
        theta=360-theta
    
    return theta

def s30_anglegenerate(list1,typetheta):
    """I want a theta for every point in the list where the point is the vertex"""
    count=0
    thetas1=[]
    thetas2=[]
    for point in list1:
        if count==len(list1)-1:
            ptbef=list1[count-1]
            ptcent=list1[count]
            ptnex=list1[0]
        else:
            ptbef=list1[count-1]
            ptcent=list1[count]
            ptnex=list1[count+1]
        count+=1
        newtheta1,newtheta2=s31_get_int_ext_angles_from_up(ptbef,ptcent,ptnex)
        thetas1.append(newtheta1)
        thetas2.append(newtheta2)
    # print('Thetas1',thetas1)
    # print('Thetas2',thetas2)
    if typetheta==0:
        if sum(thetas1)<sum(thetas2):
            typetheta=1
            thetas3=thetas1
        elif sum(thetas1)>sum(thetas2):
            typetheta=2
            thetas3=thetas2
        else:
            print('This is impossible')
            # print('Sum of Theta 1:',sum(thetas1))
            # print('Sum of Theta 2:',sum(thetas2))
        return thetas3,typetheta
    else:
        if typetheta==1:
            typetheta=1
            thetas3=thetas1
        elif typetheta==2:
            typetheta=2
            thetas3=thetas2
        else:
            print('Incorrect TypeTheta')
        return thetas3,typetheta

def s31_get_int_ext_angles_from_up(pbef,pcent,pnex):
    centerplus1=[pcent[0],pcent[1]+1]
    a1=s29_3pts_angle_mod(centerplus1,pcent,pbef)
    a2=s29_3pts_angle_mod(centerplus1,pcent,pnex)

    if a1==0:
        if pbef[1]>pcent[1]:
            a1=0
        else:
            a1=180
    if a2==0:
        if pnex[1]>pcent[1]:
            a2=0
        else:
            a2=180
    # print('Center Point:',pcent)
    # print('A1:',a1)
    # print('A2:',a2)
    side1=a1-a2
    side2=a2-a1
    if side1<0:
        side1=360-abs(side1)
    if side2<0:
        side2=360-abs(side2)
    return side1,side2

def s32_find_min_no_intersect_4p0(allpts,listpts,anglelist):
    """This function will find the miniumum angle that does not produce an intersection"""
    a1=anglelist
    a2=set(a1)
    a3=sorted(a2)
    # a3.reverse() #ADDED THIS 
    indexlist=[]
    for item in a3:
        if item>180:
            pass
        else:
            p=s22_find_occ_pos(anglelist,item)
            for thing in p:
                indexlist.append(thing)
    iteration1=0
    sc=0
    while sc==0:
        minangleidx=indexlist[iteration1]
        igval1=listpts[minangleidx-1]
        igval2=listpts[minangleidx]
        try:
            igval3=listpts[minangleidx+1]
        except:
            igval3=listpts[0]
        resultlist=[]
        for ptslist in allpts:
            ptct=0
            # print('Pointslist:',ptslist)
            if type(ptslist[0])!=float: #I Dont fully understand why this is necesssary, need to look into it later
                # input('USer Pause')
                for point in ptslist: #Changed to allptscomb instead of just listpts 8.28
                    newseg=[ptslist[ptct-1],ptslist[ptct]]
                    if igval1 in newseg:
                        pass
                    elif igval2 in newseg:
                        pass
                    elif igval3 in newseg:
                        pass
                    else:
                        # print('NewSeg0:',newseg[0])
                        # print('NewSeg1:',newseg[1])
                        result1=s9_checkintersect(newseg[0],newseg[1],igval1,igval3)
                        resultlist.append(result1)
                    ptct+=1
            else:
                pass
        if True not in resultlist:
            sc=1
            return minangleidx
        else:
            if iteration1==len(indexlist)-1:
                print('ALL AVAILABLE WERE INTERSECTED')
                sc=1
            iteration1+=1        

def s33_get_2d_centroid(pa,pb,pc):
    x=[]
    y=[]
    x.append(pa[0])
    x.append(pb[0])
    x.append(pc[0])
    y.append(pa[1])
    y.append(pb[1])
    y.append(pc[1])

    avgx=sum(x)/3
    avgy=sum(y)/3
    return [avgx,avgy]

def s34_check_interior2(p1,ptslist):
    """This function will take any pt and determine if it is within the interior of a list"""
    intercounts=0
    segmentcount=0
    seglist=s13_generatesegments(ptslist)
    for segment in seglist:
        interval=s9_checkintersect(segment[0],segment[1],[0,0],p1)
        if interval==True:
            intercounts+=1
        segmentcount+=1
    if intercounts%2==0:
        #Even intersects, its outside
        return "outside"
    else:
        return "inside"

def s35_return_normie(p1,p2,outerlist):
    """This function will take a look at one line segment, find the normal vectors, and check which one points to the internal, then it will return a normie vector list"""
    midpt=s24_find_midpt(p1,p2)
    # length=s8_dist_bt_2pts(p1,p2)
    rcomp1=p2[0]-p1[0]
    ccomp1=p2[1]-p1[1]
    nrcomp1=ccomp1
    nccomp1=rcomp1*-1
    nrcomp2=ccomp1*-1
    nccomp2=rcomp1
    checkp1=[]
    checkp1.append(midpt[0]+(nrcomp1*.1))
    checkp1.append(midpt[1]+(nccomp1*.1))
    checkp2=[]
    checkp2.append(midpt[0]+(nrcomp2*.1))
    checkp2.append(midpt[1]+(nccomp2*.1))
    location=s34_check_interior2(checkp1,outerlist)
    if location=="inside":
        return [nrcomp1,nccomp1]
    else:
        return [nrcomp2,nccomp2]

def s36_get_angle_cw_from_up(pa,pb,pc):
    centroid=s33_get_2d_centroid(pa,pb,pc)
    centroidplus1=[centroid[0],centroid[1]+1]
    a1=s26_angle_bt_3pts(centroidplus1,centroid,pa)
    a2=s26_angle_bt_3pts(centroidplus1,centroid,pb)
    a3=s26_angle_bt_3pts(centroidplus1,centroid,pc)
    if a1==0:
        if pa[1]>centroid[1]:
            a1=0
        else:
            a1=180
    if a2==0:
        if pb[1]>centroid[1]:
            a2=0
        else:
            a2=180
    if a3==0:
        if pc[1]>centroid[1]:
            a3=0
        else:
            a3=180
    if pa[0]<centroid[0]:
        a1=360-a1
    if pb[0]<centroid[0]:
        a2=360-a2
    if pc[0]<centroid[0]:
        a3=360-a3
    return a1,a2,a3

def s37_organize_pts_in_order(p1,p2,p3,a1,a2,a3,order):
    """This function will organize points in the specified order and return a newlist of pts for the triangle"""
    points=[p1,p2,p3]
    angles=[a1,a2,a3]
    newpts=[]
    newangles=[]
    if order=="cw":
        mina=min(angles)
        minaidx=angles.index(mina)
        maxa=max(angles)
        maxaidx=angles.index(maxa)
        newpts.append(points[minaidx])
        newangles.append(angles[minaidx])
        #Find the middle point
        for item in [0,1,2]:
            if item !=maxaidx and item!=minaidx:
                midaidx=item
        newpts.append(points[midaidx])
        newangles.append(angles[midaidx])
        newpts.append(points[maxaidx])
        newangles.append(angles[maxaidx])
        return newpts
    elif order=="ccw":
        mina=min(angles)
        minaidx=angles.index(mina)
        maxa=max(angles)
        maxaidx=angles.index(maxa)
        newpts.append(points[maxaidx])
        newangles.append(angles[maxaidx])
        #Find the middle point
        for item in [0,1,2]:
            if item !=maxaidx and item!=minaidx:
                midaidx=item
        newpts.append(points[midaidx])
        newangles.append(angles[midaidx])
        newpts.append(points[minaidx])
        newangles.append(angles[minaidx])
        return newpts
    else:
        print('No order selected, try cw or ccw')

def s38_reorder_triangles(trianglelist,order):
    newfulllist=[]
    for triangle in trianglelist:
        print('Individual Triangle To be rearranged:',triangle)
        p1=triangle[0]
        p2=triangle[1]
        p3=triangle[2]
        a1,a2,a3=s36_get_angle_cw_from_up(p1,p2,p3)
        # print('a1:',a1)
        # print('a2:',a2)
        # print('a3:',a3)
        newpts=s37_organize_pts_in_order(p1,p2,p3,a1,a2,a3,order)
        # print('New Generated Points:',newpts)
        # x=[]
        # y=[]
        # for item in newpts:
        #     x.append(item[0])
        #     y.append(item[1])
        # plt.scatter(x,y)
        # for i, j in zip(x, y):
        #     plt.text(i, j+0.5, '({}, {})'.format(i, j))
        # plt.show()
        newfulllist.append(newpts)
    return newfulllist

def s39_float_to_bin(num):
    # https://stackoverflow.com/questions/51179116/ieee-754-python
    bits, = struct.unpack('!I', struct.pack('!f', num))
    return "{:032b}".format(bits)

def s40_return_4_uint8s(binstr):
    a=binstr[0:8]
    b=binstr[8:16]
    c=binstr[16:24]
    d=binstr[24:32]
    a=int(a,2)
    b=int(b,2)
    c=int(c,2)
    d=int(d,2)
    return np.uint8(a),np.uint8(b),np.uint8(c),np.uint8(d)

def s41_linearsmoothing(list1,length):
    smoothed=[]
    ptct=0
    for pt in list1:
        locallist=[]
        for i in range(-1*(length),length+1):
            if ptct+i<=len(list1)-1:
                locallist.append(list1[ptct+i])
            else:
                newct=ptct+i-len(list1)
                locallist.append(list1[newct+i])
        # print(locallist)
        xran,yran,x1,y1=s28_return_ranges(locallist)
        if xran >= yran:
            a1=np.polyfit(x1,y1,1)
            xval=pt[0]
            y1=(a1[0]*xval)+(a1[1])
            pt1=[float(xval),float(y1)]
            newpt=pt1
            ptct+=1
            smoothed.append(newpt)
        else:
            a1=np.polyfit(y1,x1,1)
            yval=pt[1]
            x1=(a1[0]*yval)+(a1[1])
            pt1=[float(x1),float(yval)]
            ptct+=1
            newpt=pt1
            smoothed.append(newpt)
    return smoothed


def f42_remove_tooclose(list1,param):
    itemct=0
    dists=[]
    dists.append(0)
    for item in list1:
        if itemct==0:
            pass
        else:
            dists.append(s8_dist_bt_2pts(item,list1[itemct-1]))
        itemct+=1
    itemct=0
    newpts=[]
    carryover=0
    for item in dists:
        if itemct==0:
            newpts.append(list1[itemct])
        elif (item+carryover)<(param):
            carryover=carryover+item
        else:
            newpts.append(list1[itemct])
            carryover=0
        itemct+=1
    return newpts


def s43_refine_edgpts(edge1):
    """This function will remove any unneccesary points in an edge (just remove ones with no change in direction)"""
    #ALSO I MAY ADD A HEALTH CHECK IN HERE AND MAKE SURE THAT THERE ARE NO DUPLICATE POINTS
    edge2=edge1
    edge2.append(edge1[0])
    edge2.append(edge1[1])
    pointlist=[]
    ptct=0
    sc=0
    while sc==0:
        try:
            pt1=edge2[ptct]
            pt2=edge2[ptct+1]
            pt3=edge2[ptct+2]
            theta=s7_3pts_angle(pt1,pt2,pt3)
            if theta==180:
                del edge2[ptct+1]
            else:
                pointlist.append(pt2)
                ptct+=1
        except:
            sc=1
    return pointlist