import numpy as np
import open3d as o3d
pcd=o3d.io.read_point_cloud("rabbit.pcd")

#可视化一下
o3d.visualization.draw_geometries([pcd])
 
#下采样
downpcd = pcd.voxel_down_sample(voxel_size=0.05)
o3d.visualization.draw_geometries([downpcd])
 
#计算法向量
downpcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
o3d.visualization.draw_geometries([downpcd])
 
#原来这样获取
print("Print a normal vector of the 0th point")
print(downpcd.normals[0])
print("Print the normal vectors of the first 10 points")
print(np.asarray(downpcd.normals)[:10, :])