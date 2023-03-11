#This script is to assist with selecting valid gear combinations given some design constraints for the pedals
#Written by 50-50 1/22/23

#Define the constants that we will be using
big_diameters = [120,121,122,123,124,125,126,127,128,129,130]
little_diameters = [10,11,12,13,14,15,16,17]
modules = [1, 1.125, 1.25, 1.375, 1.5, 1.75, 2]

deg_move = 22.5 #This is the degrees of movement that the main pedal can move
smallest_mod = 1.25 #This is our smallest acceptable mod due to printing constraints
smallest_teeth = 10 # this is the smallest acceptable number of teeth we would like on the small gear

#So we need to find every combo of big_diameters and litte_diameters that will produce an even number of teeth
def num_teeth(dia,module):
    teeth = dia/module
    tmodulus = dia%module
    return teeth,tmodulus

for i in range(10):
    print("\n")

for bigd in big_diameters:
    for lild in little_diameters:
        for mod in modules:
            bigteeth,bmodulus = num_teeth(bigd,mod)
            lilteeth,lmodulus = num_teeth(lild,mod)
            if bmodulus == 0 and lmodulus == 0:
                if mod>smallest_mod:
                    if lilteeth>=smallest_teeth:
                        print('Valid combo: BigDia = {} with {} teeth, LittleDia = {} with {} teeth, Module = {}'.format(bigd,bigteeth,lild,lilteeth,mod))
                        potmove = deg_move* bigteeth/lilteeth
                        print(" -The above would produce {} degrees of potentiometer movement".format(potmove))
                        print(" -The above would require {} mm separation between the 2 gear axes".format((bigd+lild)/2))
                        print("\n")

for i in range(10):
        print("\n")