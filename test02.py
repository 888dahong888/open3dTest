#控件变换操作
import open3d as o3d
import numpy as np
#平移操作
def test_translate(mesh,copy):
    mesh=o3d.geometry.TriangleMesh.create_coordinate_frame()
    mesh_tx=copy.deepcopy(mesh).translate((1.3,0.0))
    mesh_ty=copy.deepcopy(mesh).translate((0.0,1.3))
    print("center of mesh: ",mesh.get_center())
    print(f'Center of mesh tx: {mesh_tx.get_center()}')
    print(f'Center of mesh ty: {mesh_ty.get_center()}')
    o3d.visualization.draw_geometries([mesh, mesh_tx, mesh_ty])
    mesh_mv = copy.deepcopy(mesh).translate((2,2,2), relative=False)        #移动中心点
    print(f'Center of mesh: {mesh.get_center()}')
    print(f'Center of translated mesh: {mesh_mv.get_center()}')
    o3d.visualization.draw_geometries([mesh, mesh_mv])

#旋转操作
def test_rotate(mesh,copy):
    mesh = o3d.geometry.TriangleMesh.create_coordinate_frame()
    mesh_r = copy.deepcopy(mesh)
    R = mesh.get_rotation_matrix_from_xyz((np.pi/2,0,np.pi/4))
    mesh_r.rotate(R, center=(0,0,0))
    o3d.visualization.draw_geometries([mesh, mesh_r])
    mesh = o3d.geometry.TriangleMesh.create_coordinate_frame()
    mesh_r = copy.deepcopy(mesh).translate((2,0,0))
    mesh_r.rotate(mesh.get_rotation_matrix_from_xyz((np.pi/2,0,np.pi/4)), center=(0,0,0))
    o3d.visualization.draw_geometries([mesh, mesh_r])

#缩放操作
def test_scale(mesh,copy):
    mesh = o3d.geometry.TriangleMesh.create_coordinate_frame()
    mesh_s = copy.deepcopy(mesh).translate((2,0,0))
    mesh_s.scale(0.5, center=mesh_s.get_center())
    o3d.visualization.draw_geometries([mesh, mesh_s])
    mesh = o3d.geometry.TriangleMesh.create_coordinate_frame()
    mesh_s = copy.deepcopy(mesh).translate((2,1,0))
    mesh_s.scale(0.5, center=(0,0,0))
    o3d.visualization.draw_geometries([mesh, mesh_s])

#通用装换操作
def test_transform(mesh,copy):
    mesh = o3d.geometry.TriangleMesh.create_coordinate_frame()
    T = np.eye(4)
    T[:3,:3] = mesh.get_rotation_matrix_from_xyz((0,np.pi/3, np.pi/2))
    T[0,3] = 1
    T[1,3] = 1.3
    print(T)
    mesh_t = copy.deepcopy(mesh).transform(T)
    o3d.visualization.draw_geometries([mesh, mesh_t])