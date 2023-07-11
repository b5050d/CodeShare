from matplotlib import pyplot as plt
#Alright we need to do the following:

#Save out an image from a Matrix
def d1_show(img):
    """A dev function to quickly do an imshow"""
    plt.imshow(img)
    plt.show()

def d2_scat(list):
    """A dev function to quickly plot scatter lists"""
    x=[]
    y=[]
    for item in list:
        x.append(item[0])
        y.append(item[1])
    plt.scatter(x,y)
    plt.show()

def d2p5_scat_all(lists):
    x=[]
    y=[]
    for list in lists:
        for item in list:
            x.append(item[0])
            y.append(item[1])
    plt.scatter(x,y)
    plt.show()

def d3_plottrianglelist(listoftriangles):
    for triangle in listoftriangles:
        x1=[]
        y1=[]
        x1.append(triangle[0][0])
        y1.append(triangle[0][1])
        x1.append(triangle[1][0])
        y1.append(triangle[1][1])
        x1.append(triangle[2][0])
        y1.append(triangle[2][1])
        x1.append(triangle[0][0])
        y1.append(triangle[0][1])
        # print(x1)
        # print(y1)
        # input('userpause')
        plt.plot(x1,y1,linestyle="-")
    plt.show()

def d4_ptype(list):
    pt1=list[0]
    print('Type of List: ',type(pt1[0]))

def d5_plotsegments(list1):
    count=0
    for item in list1:
        x1=[]
        y1=[]
        x1.append(list1[count-1][0])
        y1.append(list1[count-1][1])
        x1.append(list1[count][0])
        y1.append(list1[count][1])
        plt.plot(x1,y1,linestyle='-')
        count+=1
    plt.show()

def d6_plot2D(listoftriangles):
    for triangle in listoftriangles:
        x1=[]
        y1=[]
        x1.append(triangle[0][0])
        y1.append(triangle[0][1])
        x1.append(triangle[1][0])
        y1.append(triangle[1][1])
        x1.append(triangle[2][0])
        y1.append(triangle[2][1])
        x1.append(triangle[0][0])
        y1.append(triangle[0][1])
        plt.plot(x1,y1,'o',linestyle="-")
    plt.show()

def d7_plot_3dtriangles(listoflists):
    fig=plt.figure()
    ax=fig.add_subplot(111,projection='3d')
    for list1 in listoflists:
        for item in list1:
            x1=[]
            y1=[]
            z1=[]
            x1.append(item[1][0])
            y1.append(item[1][1])
            z1.append(item[1][2])
            x1.append(item[2][0])
            y1.append(item[2][1])
            z1.append(item[2][2])
            x1.append(item[3][0])
            y1.append(item[3][1])
            z1.append(item[3][2])
            x1.append(item[1][0])
            y1.append(item[1][1])
            z1.append(item[1][2])
            ax.plot(x1,y1,z1,color='b',marker='o')
    plt.show()

def d8_save_list_to_txt(input_list,pngname,listvar):
    """This function will save the list into a text file so we can quickly mess around with it later"""
    currdir = os.path.dirname(__file__)
    name = os.path.basename(pngname)
    name = name[:-4]
    name = name + "_"+str(listvar)+".txt"
    txtname = currdir + "\\" + name
    with open(txtname,"w") as newtxt:
        for item in input_list:
            newtxt.write(str(item)+"\n")