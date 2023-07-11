import primary as pri
import os
import json
import dev

inipath = "base.ini"
imgpath = "g.png"
currdir = os.path.dirname(__file__)
jsonpath = currdir + "\\g_hierarchy.json"

coasty_image = pri.CoasterImg(imgpath,inipath)

#Step 1 : Open the image
coasty_image.f1_openimg()
# dev.d1_show(coasty_image.og_img_matrix)

# #Step 2 : Add A Square Border
coasty_image.f2_addsquareborder()
# dev.d1_show(coasty_image.sq_img)

#Step 3 : Create a Binary Image
coasty_image.f3_findcutoff(114)
# print(coasty_image.binary_cutoff)
coasty_image.f4_performcutoff()
# dev.d1_show(coasty_image.binary_img)

#Step 4: Find and mark the edges around the binary image
coasty_image.f5_markboundaries()
# dev.d1_show(coasty_image.boundaryimg)

# Step 5: Generate a list of points for the boundary
coasty_edges = pri.Edges(coasty_image.boundaryimg)

# # Step 6: Scale the Coaster Accordingly
coasty_edges.f7_placeoutercircle()
coasty_edges.f8_genoutercircle()

# Step 7: Refine Edge points
#7.1 Scale to 90
coasty_edges.f12_scale_to_90()

#7.2 Perform Linear Smoothing

coasty_edges.f13_linearsmoothing()

#7.3 Remove Points that are too close together
coasty_edges.f17_remove_tooclose()

#7.4 Remove Points that are redundant
# coasty_edges.f9_refine_edgepoints()

#Consider - > adding a random tiny adjustment to every edge to avoid bug with floating point nums

#8 Generate a Hierarchy of edges
coasty_edges.f10_hierarchy_build()
coasty_edges.f11_levelidentities()

#9 Group up all of our edges that are apart of the same continuous shape

#Save Out dict into a json file to avoid re-doing the stuff
jsonobj = json.dumps(coasty_edges.hierarchy,indent = 4)
with open(jsonpath,"w") as newjson:
    newjson.write(jsonobj)
     
#10 Build Triangles

#10.1 Build the Base of the Coaster

#10.2 Build the Walls of the Coaster

#10.3 Build the Basins of the Coaster

#10.4 Build the Walls of the Basins of the Coaster

#10.5 Build the Face of the Coaster

#11 Build the STL File