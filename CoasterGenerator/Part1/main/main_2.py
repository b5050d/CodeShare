import primary as pri
import os
import json
import dev

inipath = "base.ini"
imgpath = "g.png"
currdir = os.path.dirname(__file__)
jsonpath = currdir + "\\g_hierarchy.json"
#Load our shit

coasty_edges = pri.Edges()

with open(jsonpath,"r") as newjson:
    coasty_edges.hierarchy=json.load(newjson)

#9 Group up all of our edges that are apart of the same continuous shape
coasty_edges.f14_generate_groupings()
# print(coasty_edges.groupings)

#10 Build Triangles
coasty_triangles = pri.Triangles(coasty_edges.groupings,coasty_edges.hierarchy)

#10.1 Build the Base of the Coaster
coasty_triangles.f20_generate_base()
# plotlist=[]
# plotlist.append(coasty_triangles.base_triangles)
# dev.d7_plot_3dtriangles(plotlist)

#10.2 Build the Outer Walls of the Coaster
coasty_triangles.f19_generate_outer_wall()
# plotlist=[]
# plotlist.append(coasty_triangles.outer_wall)
# dev.d7_plot_3dtriangles(plotlist)

#10.3 Build the Valleys
coasty_triangles.f21_generate_flatty("valley")
# plotlist=[]
# plotlist.append(coasty_triangles.valleys)
# dev.d7_plot_3dtriangles(plotlist)


# #10.4 Build the Walls of the Basins of the Coaster
coasty_triangles.f23_generate_interior_walls()
# for wall in coasty_triangles.inner_walls:
#     plotlist=[]
#     plotlist.append(wall)
#     dev.d7_plot_3dtriangles(plotlist)

# #10.5 Build the Face of the Coaster
coasty_triangles.f21_generate_flatty("plateau")
plotlist=[]
plotlist.append(coasty_triangles.plateaus)
dev.d7_plot_3dtriangles(plotlist)

#11 Build the STL File
#11.1 Organize the Triangles:
coasty_triangles.f40_arrange_triangles()
# print(coasty_triangles.total_triangle_list)
# print(len(coasty_triangles.total_triangle_list))
# plotlist=[]
# plotlist.append(coasty_triangles.total_triangle_list)
# dev.d7_plot_3dtriangles(coasty_triangles.total_triangle_list)

#11.2 Save the file:
imgpath_full=currdir+"\\"+imgpath[:-4]+".stl"
coasty_triangles.f23_write_triangles_to_stl(imgpath_full)