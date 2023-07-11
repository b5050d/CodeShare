import primary as pri
import os
import json
import dev

inipath = "base.ini"
imgpath = "spiral.png"
currdir = os.path.dirname(__file__)

coasty_image = pri.CoasterImg(imgpath,inipath)

#Step 1 : Open the image
coasty_image.f1_openimg()
# dev.d1_show(coasty_image.og_img_matrix)

# #Step 2 : Add A Square Border
coasty_image.f2_addsquareborder()
# dev.d1_show(coasty_image.sq_img)

# #Step 3 : Create a Binary Image
coasty_image.f3_findcutoff(103)
# coasty_image.f3_findcutoff()
coasty_image.f4_performcutoff()
# dev.d1_show(coasty_image.binary_img)

#Step 4: Find and mark the edges around the binary image
coasty_image.f5_markboundaries()
# dev.d1_show(coasty_image.boundaryimg)

# # # Step 5: Generate a list of points for the boundary
coasty_edges = pri.Edges(coasty_image.boundaryimg)

# # # Step 6: Place the Outer Boundary Circle
coasty_edges.f7_placeoutercircle()
coasty_edges.f8_genoutercircle()

# # # Step 7: Refine Edge points
# # #7.1 Scale to 90
# dev.d2p5_scat_all(coasty_edges.edges)
coasty_edges.f12_scale_to_90()
# dev.d2p5_scat_all(coasty_edges.edges)

# #7.2 Perform Linear Smoothing
# dev.d2p5_scat_all(coasty_edges.edges)
coasty_edges.f13_linearsmoothing()
# dev.d2p5_scat_all(coasty_edges.edges)

# #7.3 Remove Points that are too close together
# dev.d2p5_scat_all(coasty_edges.edges)
coasty_edges.f17_remove_tooclose()
# dev.d2p5_scat_all(coasty_edges.edges)

# #7.4 Remove Points that are redundant
# coasty_edges.f9_refine_edgepoints()

# #Consider - > adding a random tiny adjustment to every edge to avoid bug with floating point nums

#8 Generate a Hierarchy of edges
coasty_edges.f10_hierarchy_build()
coasty_edges.f11_levelidentities()

#9 Group up all of our edges that are apart of the same continuous shape
coasty_edges.f14_generate_groupings()
# print(coasty_edges.groupings)

#10 Build Triangles
coasty_triangles = pri.Triangles(coasty_edges.groupings,coasty_edges.hierarchy)

# #10.1 Build the Base of the Coaster
coasty_triangles.f20_generate_base()

# #10.2 Build the Outer Walls of the Coaster
coasty_triangles.f19_generate_outer_wall()
plotlist=[]
plotlist.append(coasty_triangles.outer_wall)
dev.d7_plot_3dtriangles(plotlist)

# #10.3 Build the Valleys
coasty_triangles.f21_generate_flatty("valley")

# # #10.4 Build the Walls of the Basins of the Coaster
coasty_triangles.f23_generate_interior_walls()
plotlist=[]
plotlist.append(coasty_triangles.inner_walls)
dev.d7_plot_3dtriangles(plotlist)

# # #10.5 Build the Face of the Coaster
coasty_triangles.f21_generate_flatty("plateau")

# #11 Build the STL File
# #11.1 Organize the Triangles:
coasty_triangles.f40_arrange_triangles()
# # print(coasty_triangles.total_triangle_list)
# # print(len(coasty_triangles.total_triangle_list))
# # plotlist=[]
# # plotlist.append(coasty_triangles.total_triangle_list)
# # dev.d7_plot_3dtriangles(coasty_triangles.total_triangle_list)

# #11.2 Save the file:
imgpath_full=currdir+"\\"+imgpath[:-4]+".stl"
coasty_triangles.f23_write_triangles_to_stl(imgpath_full)