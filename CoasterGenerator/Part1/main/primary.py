import secondary as sec
import os
from matplotlib import pyplot as plt
import PIL
import numpy as np
from math import sqrt
import cv2
import dev

class CoasterImg:
    def __init__(self,imgname, ininame):
        currdir = os.path.dirname(__file__)
        self.inipath = currdir + "\\inis\\" + ininame
        self.imgpath = currdir + "\\imgs\\" + imgname
        self.og_img_matrix = []
        self.cols = []
        self.rows = []

    def f1_openimg(self):
        """This function  opens our image find the rows and columns"""
        with PIL.Image.open(self.imgpath) as newim:
            newim=PIL.ImageOps.grayscale(newim)
            imsize=newim.size
            self.cols=imsize[0]
            self.rows=imsize[1]
        self.og_img_matrix=np.asarray(newim)

    def f2_addsquareborder(self):
        """Adds empty space around the border of the image in a square"""
        if self.rows>self.cols:
            self.sq_rows=int(self.rows*1.4)
            self.sq_cols=self.sq_rows
        else:
            self.sq_cols=int(self.cols*1.4)
            self.sq_rows=self.sq_cols
        self.sq_img=np.zeros((self.sq_cols,self.sq_rows))
        rowct=0
        borderavg=sec.s1_getborderavg(self.og_img_matrix,self.rows,self.cols)
        for row in self.sq_img:
            colct=0
            for px in row:
                self.sq_img[rowct][colct]=np.uint8(borderavg)
                colct+=1
            rowct+=1
        rowoff=int((self.sq_rows-self.rows)/2)
        coloff=int((self.sq_cols-self.cols)/2)
        rowct=0
        for row in self.og_img_matrix:
            colct=0
            for col in row:
                self.sq_img[rowct+rowoff][colct+coloff]=np.uint8(col)
                colct+=1
            rowct+=1

    def f3_findcutoff(self,provided=None):
        """This function will prompt the user to determine the point at which to cut-off white and black"""
        if provided==None:
            flatimg=self.sq_img.flatten()
            maxval=int(max(flatimg))
            def on_change(val):
                cutoff=val
                binflat=[]
                for item in flatimg:
                    if item<cutoff:
                        binflat.append(np.uint8(0))
                    else:
                        binflat.append(np.uint8(255))
                binsquare=np.reshape(binflat,(self.sq_rows,self.sq_cols))
                img2disp2=cv2.resize(binsquare,(500,500))
                cv2.imshow(windowName,img2disp2)
                global cutoff2
                cutoff2=cutoff
            windowName='Choose Cutoff'
            img2disp1=cv2.resize(self.sq_img,(500,500))
            cv2.imshow(windowName,img2disp1)
            cv2.createTrackbar('slider',windowName,0,maxval,on_change)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            self.binary_cutoff = cutoff2
        else:
            self.binary_cutoff=provided

    def f4_performcutoff(self):
        """This function will just perform the cutting off, now that we have a cutoff value"""
        flatimg=self.sq_img.flatten()
        binflat=[]
        for item in flatimg:
            if item<self.binary_cutoff:
                binflat.append(np.uint8(0))
            else:
                binflat.append(np.uint8(255))
        self.binary_img=np.reshape(binflat,(self.sq_rows,self.sq_cols))

    def f5_markboundaries(self):
        """This function will trace all the edges of dark shapes"""
        rowct=0
        self.bin_rows = len(self.binary_img)
        self.bin_cols = len(self.binary_img[0])
        #We will start by filtering out undesirable edges
        for row in self.binary_img:
            colct=0
            for col in row:
                if col==255:
                    fourlist=sec.s2_fourlistgen(self.binary_img,rowct,colct)
                    numones=fourlist.count(1)
                    if numones>2:
                        self.binary_img[rowct][colct]=0
                colct+=1
            rowct+=1    
        self.boundaryimg=np.zeros([self.bin_rows,self.bin_cols],dtype=np.uint8)
        rowct=0
        for row in self.binary_img:
            colct=0
            for col in row:
                if col==0:
                    pass
                else:
                    try:
                        collist=sec.s2_fourlistgen(self.binary_img,rowct,colct)                   
                        numones=collist.count(1)
                        if numones<1 or numones>2:
                            pass
                        else:
                            self.boundaryimg[rowct][colct]=255
                    except:
                        pass
                colct+=1
            rowct+=1

class Edges:
    def __init__(self,boundary_image=False):

        self.edges = []
        if type(boundary_image) != type(False):
            self.boundary_img = boundary_image
            self.rows = len(self.boundary_img)
            self.cols = len(self.boundary_img[0])
            self.f6_genlistofpts(boundary_image)
        self.hierarchy = {}
        self.groupings = {}

    def f6_genlistofpts(self,boundaryimg):
        self.edges = sec.s2p5_genlistofpts(boundaryimg)

    def f7_placeoutercircle(self):
        import patternplacement as pp
        self.rad,self.xc,self.yc=pp.gencirc(self.boundary_img,self.rows,self.cols)

    def f8_genoutercircle(self):
        """This function will return the list of points for the outer circle"""
        mat=np.zeros((self.rows,self.cols))
        avec=np.linspace(start=-self.rad,stop=self.rad,num=self.rad*2+1)
        resvalhigh=[]
        resvallow=[]
        for x in avec:
            x=int(x)
            y1=-1*sqrt(self.rad**2-x**2)
            y2=1*sqrt(self.rad**2-x**2)
            resvalhigh.append([x,round(y1)])
            resvallow.append([x,round(y2)])
        resvalinvhigh=sec.s6_invertvaluepair(resvalhigh)
        resvalinvlow=sec.s6_invertvaluepair(resvallow)
        totvallist=[]
        totvallist.append(resvalhigh)
        totvallist.append(resvallow)
        totvallist.append(resvalinvhigh)
        totvallist.append(resvalinvlow)
        totvallist2=[]
        for list in totvallist:
            for valuepair in list:
                rval=int(valuepair[0]+self.yc)
                cval=int(valuepair[1]+self.xc)
                mat[rval][cval]=255
                templist1=[rval,cval]
                if templist1 not in totvallist2:
                    totvallist2.append(templist1)
        totvallist2=sec.s2p5_genlistofpts(mat)

        #Alright now we need to place the outer edge as the first of the edgelist 
        newedges = []
        newedges.append(totvallist2[0])
        for edge in self.edges:
            newedges.append(edge)

        self.edges = []
        self.edges = newedges

    def f12_scale_to_90(self):
        """This function will scale all of our edges to 90mm"""
        #Start by finding the min and max rows, min and max columns of the outerlists
        
        rowlist,collist=sec.s27_split_to_xy(self.edges[0])
        minrow=min(rowlist)
        maxrow=max(rowlist)
        span=maxrow-minrow
        scaling=span/90
        newedges=[]
        for edge in self.edges:
            newedge=[]
            for pt in edge:
                newpt=[float(pt[0]/scaling),float(pt[1]/scaling)]
                newedge.append(newpt)
            newedges.append(newedge)
        self.edges = []
        self.edges = newedges

    def f13_linearsmoothing(self):
        newedges=[]
        for edge in self.edges:
            newedge=sec.s41_linearsmoothing(edge,2)
            newedges.append(newedge)
        self.edges = []
        self.edges = newedges

    def f17_remove_tooclose(self):
        newedges = []
        for edge in self.edges:
            newedge=sec.f42_remove_tooclose(edge,1)
            newedges.append(newedge)
        self.edges = []
        self.edges = newedges

    def f9_refine_edgepoints(self):
        newedges = []
        for edge in self.edges:
            newedge=sec.s43_refine_edgpts(edge)
            newedges.append(newedge)
        self.edges = []
        self.edges = newedges

    def f10_hierarchy_build(self):
        itemct = 1
        for edge in self.edges:
            identifier = "Edge_"+str(itemct)
            self.hierarchy[identifier]={}
            self.hierarchy[identifier]["Points"] = edge
            self.hierarchy[identifier]["Segments"] = sec.s13_generatesegments(edge)
            itemct+=1
        
        for edge in self.hierarchy:
            closestpt = sec.s15_findclosept(self.hierarchy[edge]["Points"])
            self.hierarchy[edge]["Parents"]= sec.s14_familyfinder(closestpt, edge, self.hierarchy)
            
    def f11_levelidentities(self):
        """This function will take all identities and all parents and find the level of the items as well as the children of the items"""
        for edge1 in self.hierarchy:
            children = []
            for edge2 in self.hierarchy:
                if edge1 == edge2:
                    pass
                else:
                    if edge1 in self.hierarchy[edge2]["Parents"]:
                        children.append(edge2)
            self.hierarchy[edge1]["Children"]=children
            
        for edge1 in self.hierarchy:
            level=0
            for edge2 in self.hierarchy:
                suspects = self.hierarchy[edge2]["Children"]
                if edge1 in suspects:
                    level+=1
            self.hierarchy[edge1]["Level"]= level

    def f14_generate_groupings(self):
        groupiter = 0
        for edge in self.hierarchy:
            direct_child_lvl = self.hierarchy[edge]["Level"]+1
            childlist = self.hierarchy[edge]["Children"]
            groupstring = "Group_"+str(groupiter)
            self.groupings[groupstring] = {}
            self.groupings[groupstring]["Outer"]=edge
            self.groupings[groupstring]["Inners"]=[]
            if self.hierarchy[edge]["Level"]%2 == 0:
                self.groupings[groupstring]["Valley?"]=False
            else:
                self.groupings[groupstring]["Valley?"]=True
            for child in childlist:
                if self.hierarchy[child]["Level"]==direct_child_lvl:
                    self.groupings[groupstring]["Inners"].append(child)
            groupiter+=1

class Triangles:
    def __init__(self,groupings,hierarchy):
        self.groupings = groupings
        self.hierarchy = hierarchy
        self.base_triangles = []
        self.outer_wall = []
        self.inner_walls = []
        self.valleys = []
        self.plateaus = []
        self.total_triangle_list=[]
        self.depth1=3
        self.depth2=6

    #Generate Walls of Coaster
    def f25_wall_generate(self,list1,type):
        if type == "outest":
            dep1 = 0
            dep2 = self.depth2
        elif type == "outer" or type == "inner":
            dep1 = self.depth1
            dep2 = self.depth2
        else:
            raise "Error, incorrect type"
        toplist=list1
        bottomlist=list1
        bottomtriangles=[]
        itemct=0
        for item in toplist:
            newtri=[]
            newtri.append(item)
            if type == 'inner':
                if itemct==len(toplist)-1:
                    newtri.append(bottomlist[itemct])
                    newtri.append(bottomlist[0])
                else: 
                    newtri.append(bottomlist[itemct])
                    newtri.append(bottomlist[itemct+1])
            elif type== 'outer' or type == "outest":
                if itemct==len(toplist)-1:
                    newtri.append(bottomlist[0])
                    newtri.append(bottomlist[itemct])
                else: 
                    newtri.append(bottomlist[itemct+1])
                    newtri.append(bottomlist[itemct])
            itemct+=1
            newfulltri=[]
            #Lets start by finding both normal vectors to the upper segment, finding a point just off on each side, and checking whether it is internal or external to the shape
            normie=sec.s35_return_normie(newtri[1],newtri[2],bottomlist)
            fullnormie=[]
            fullnormie.append(normie[0])
            fullnormie.append(normie[1])
            fullnormie.append(0)
            newfulltri.append(fullnormie)
            pt1=[item[0],item[1],dep2]
            pt2=[newtri[1][0],newtri[1][1],dep1]
            pt3=[newtri[2][0],newtri[2][1],dep1]
            newfulltri.append(pt1)
            newfulltri.append(pt2)
            newfulltri.append(pt3)
            bottomtriangles.append(newfulltri)

        uppertriangles=[]
        itemct=0
        for item in toplist:
            newtri=[]
            newtri.append(item)
            if itemct==len(toplist)-1:
                newtri.append(bottomlist[0])
                newtri.append(toplist[0])
            else:
                newtri.append(bottomlist[itemct+1]) 
                newtri.append(toplist[itemct+1])
            itemct+=1
            newfulltri=[]
            #Lets start by finding both normal vectors to the upper segment, finding a point just off on each side, and checking whether it is internal or external to the shape
            normie=sec.s35_return_normie(newtri[0],newtri[1],toplist)
            fullnormie=[]
            fullnormie.append(normie[0])
            fullnormie.append(normie[1])
            fullnormie.append(0)
            newfulltri.append(fullnormie)
            pt1=[item[0],item[1],dep2]
            pt2=[newtri[1][0],newtri[1][1],dep2]
            pt3=[newtri[2][0],newtri[2][1],dep1]
            if type == "inner":
                newfulltri.append(pt1)
                newfulltri.append(pt3)# Switched pt3 and pt2 to get it in counter clockwise order
                newfulltri.append(pt2)
            elif type == "outer" or "outest":
                newfulltri.append(pt1)
                newfulltri.append(pt2)
                newfulltri.append(pt3)
            else:
                raise "Error - Incorrect 'type' provided"
            uppertriangles.append(newfulltri)
        allwalltriangles=[]
        for item in bottomtriangles:
            allwalltriangles.append(item)
        for item in uppertriangles:
            allwalltriangles.append(item)
        return allwalltriangles

    def f19_generate_outer_wall(self):
        toplist=self.hierarchy["Edge_1"]["Points"]
        self.outer_wall=self.f25_wall_generate(toplist,"outest")

    def f23_generate_interior_walls(self):
        inner_walls = []
        for group in self.groupings: 
            if self.groupings[group]["Valley?"]==False:
                pass
            else:
                if self.groupings[group]["Inners"]==[]:
                    outer_id = self.groupings[group]["Outer"]
                    valley_points = self.hierarchy[outer_id]["Points"]
                    newwalls=self.f25_wall_generate(valley_points,"inner")
                    for tri in newwalls:
                        inner_walls.append(tri)
                else:
                    outer_id = self.groupings[group]["Outer"]
                    outerpts=self.hierarchy[outer_id]["Points"]
                    innerpts_list=[]
                    innerpts_ids = self.groupings[group]["Inners"]
                    for inner in innerpts_ids:
                        innerpts= self.hierarchy[inner]["Points"]
                        innerpts_list.append(innerpts)
                    newwalls=self.f25_wall_generate(outerpts,"inner")
                    for tri in newwalls:
                        inner_walls.append(tri)
                    for inner in innerpts_list:
                        newwalls = self.f25_wall_generate(inner,"inner")
                        for tri in newwalls:
                            inner_walls.append(tri)
        self.inner_walls = inner_walls
 
    #Generate Flat Surfaces of Coaster

    def f15_generate_triangles(self,list1):
        list2=[] #Making a copy so we can continue to make sure that new segments do not cross points that have long been eliminated with triangles drawn there
        list3=[]
        for item in list1:
            list2.append(item)
            list3.append(item)
        trianglelist=[]
        typetheta=1 #HARD CODED THIS TO 1 8/29 MAY BE A MISTAKE, 
        counter=0
        while len(list3)>=4:
            if len(list3)>4:
                anglelist,typetheta=sec.s30_anglegenerate(list3,typetheta)
                combinedlists=[]
                combinedlists.append(list3)
                for item in trianglelist:
                    trilist=[item[0],item[1],item[2],item[0]]
                    combinedlists.append(trilist)
                
                minidx=sec.s32_find_min_no_intersect_4p0(combinedlists,list3,anglelist)
                a_vertex=list3[minidx-1]
                b_vertex=list3[minidx]
                counter+=1
                print('Counter:',counter)
                try:
                    c_vertex=list3[minidx+1]
                except:
                    c_vertex=list3[0]
                newcoords=[a_vertex,b_vertex,c_vertex]
                trianglelist.append(newcoords)
                del list3[minidx]
                # if counter>95:
                #     dev.d6_plot2D(trianglelist)
                #     dev.d5_plotsegments(list3)
                
            else:
                anglelist,typetheta=sec.s30_anglegenerate(list3,typetheta)
                minidx=sec.s32_find_min_no_intersect_4p0(list2,list3,anglelist)
                a_vertex=list3[minidx-1]
                b_vertex=list3[minidx]
                try:
                    c_vertex=list3[minidx+1]
                except:
                    c_vertex=list3[0]
                newcoords=[a_vertex,b_vertex,c_vertex]
                trianglelist.append(newcoords)
                # d2_plot2D(trianglelist)
                    # d1_plotsegments(list1)
                # d2_plot2D(trianglelist)
                for point in list3:
                    if point in newcoords:
                        pass
                    else:
                        d_vertex=point
                newcoords=[a_vertex,d_vertex,c_vertex]
                del list3[0]
                trianglelist.append(newcoords)
        return trianglelist

    def f20_generate_base(self):
        """This function will generate the triangles Base of the Triangle"""
        templist = self.hierarchy["Edge_1"]["Points"]
        base_triangles=self.f15_generate_triangles(templist)
        # dev.d3_plottrianglelist(base_triangles)
        self.base_triangles=self.f30_flat_triangle_rearrange(base_triangles,'base')
        
    def f21_generate_flatty(self,type):
        if type == "valley":
            valley_bool = True
        elif type == "plateau":
            valley_bool = False
        else:
            raise "Error - Incorrect Type provided"
        flatty = []
        for group in self.groupings: 
            if self.groupings[group]["Valley?"]!=valley_bool:
                pass
            else:
                if self.groupings[group]["Inners"]==[]:
                    shape_id = self.groupings[group]["Outer"]
                    shape_points = self.hierarchy[shape_id]["Points"]
                    trivert=self.f15_generate_triangles(shape_points)
                    for item in trivert:
                        flatty.append(item)
                else:
                    outer_id = self.groupings[group]["Outer"]
                    inner_ids = self.groupings[group]["Inners"]
                    outerpts = self.hierarchy[outer_id]["Points"]
                    innerpts = []
                    for id in inner_ids:
                        newpts = self.hierarchy[id]["Points"]
                        innerpts.append(newpts)
                    combinedlist=self.f16_combine_outerinners(outerpts,innerpts)
                    trivert=self.f15_generate_triangles(combinedlist)
                    for item in trivert:
                        flatty.append(item)
        # dev.d3_plottrianglelist(flatty)
        val1 = self.f30_flat_triangle_rearrange(flatty,type)
        
        if type == "valley":
            for val in val1:
                self.valleys.append(val)
        else:
            for val in val1:
                self.plateaus.append(val)

    def f16_combine_outerinners(self,outerlist,innerlists): #NEED TO PROBABLY ADD A METHOD TO CHECK FOR INTERSECTIONS
        """This function will just connect a single outer list to all the inner lists inside it """
        #Every outerlist needs to be combined with every inner list
        #Find a thing that does not result in any intersections between the outer and inner lists, 
        leninlist=len(innerlists)
        print('There are {} inner lists we need to combine with the outer list:',leninlist)
        inlistct=0
        for inlist in innerlists:
            flag=False
            for point1 in inlist:
                if flag==True:
                    break
                for point2 in outerlist:
                    if flag==True:
                        break
                    # s5_dist_bt_2pts(point1,point2)
                    proposedseg=[point1,point2]
                    outerct=0
                    outerresults=[]
                    for pt3 in outerlist:
                        if point2==pt3:
                            pass
                        elif point2==outerlist[outerct-1]:
                            pass
                        else:
                            newres=sec.s9_checkintersect(point1,point2,pt3,outerlist[outerct-1])#Takes 4 points
                            outerresults.append(newres)
                        outerct+=1
                    innerresults=[]
                    for inlist2 in innerlists:
                        inct=0
                        for pt4 in inlist2:
                            if point1==pt4:
                                pass
                            elif point1==inlist2[inct-1]:
                                pass
                            else:
                                newres=sec.s9_checkintersect(point1,point2,pt4,inlist2[inct-1])
                                innerresults.append(newres)
                            inct+=1
                    if True not in outerresults:
                        print('Does not intersect with exterior')
                        if True not in innerresults:
                            print('Does not intersect with Any inner Lists')
                            chosenseg=proposedseg
                            flag=True
                            print('Chosen Segment:',chosenseg)
                print('Chosen Segment:',chosenseg)
                insideoutinnerlist=sec.s16_cutinvert(chosenseg[0],inlist)
                newouterlist=[]
                singleflag=False
                for point in outerlist:
                    if point in chosenseg:
                        if singleflag==False:
                            singleflag=True
                            newouterlist.append(chosenseg[1])
                            for item in insideoutinnerlist:
                                newouterlist.append(item)
                            newouterlist.append(chosenseg[0])
                            newouterlist.append(chosenseg[1])
                        else:
                            newouterlist.append(point)
                    else:
                        newouterlist.append(point)
                outerlist=newouterlist
        return newouterlist

    def f30_flat_triangle_rearrange(self,triangles,type):
        """This function adds CCW orientation + 3D element + normal vector"""
        if type=='valley':
            depth=self.depth1
            order = "ccw"
            norms=[0,0,1]
        elif type=='plateau':
            depth=self.depth2
            order = "ccw"
            norms=[0,0,1]
        elif type == 'base':
            depth = 0 
            order = "cw"
            norms=[0,0,-1]
        else:
            raise "Error - incorrect or no 'type' provided to this function"
        triangles1=sec.s38_reorder_triangles(triangles,order)
        flatlist1=[]
        for tri1 in triangles1:
            tri2=[]
            tri2.append(norms)
            p1=[]
            p1.append(tri1[0][0])
            p1.append(tri1[0][1])
            p1.append(depth)
            tri2.append(p1)
            p3=[]
            p3.append(tri1[1][0])
            p3.append(tri1[1][1])
            p3.append(depth)
            tri2.append(p3)
            p2=[]
            p2.append(tri1[2][0])
            p2.append(tri1[2][1])
            p2.append(depth)
            tri2.append(p2)
            flatlist1.append(tri2)
        return flatlist1

    #Generate STL File

    def f40_arrange_triangles(self):
        """This is to arrange the triangles in a list so that we can build our stl"""
        total_triangle_list=[]
        total_triangle_list.append(self.base_triangles)
        # print(len(self.base_triangles))
        total_triangle_list.append(self.outer_wall)
        # print(len(self.outer_wall))
        total_triangle_list.append(self.valleys)
        # print(len(self.valleys))
        total_triangle_list.append(self.inner_walls)
        # print(len(self.inner_walls))
        total_triangle_list.append(self.plateaus)
        # print(len(self.plateaus))
        # input("User Pause 78")
        total_triangle_list1=[]
        for list1 in total_triangle_list:
            print('List1:',list1)
            # input('Pausing for user')
            for item in list1:
                total_triangle_list1.append(item)
        self.total_triangle_list = total_triangle_list1

    def f23_write_triangles_to_stl(self,filepath):
        alltriangles = self.total_triangle_list
        with open(filepath,'wb') as stlpath:
            #Write the header
            for i in range(80):
                stlpath.write(np.uint8(0))
            numtri=len(alltriangles)
            #Write the uint 32 number of triangles
            print('number of triangles:',numtri)
            stlpath.write(np.uint32(numtri))

            #write each triangle 
            for triangle in alltriangles:
                for item in triangle:
                    for value in item:
                        binstr=sec.s39_float_to_bin(value)
                        a,b,c,d=sec.s40_return_4_uint8s(binstr)
                        stlpath.write(d)
                        stlpath.write(c)
                        stlpath.write(b)
                        stlpath.write(a)
                stlpath.write(np.uint16(0))