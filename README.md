# open3dTest
三维点云数据运行操作

pip install open3d
conda isntall -c open3d-admin open3d
python -c "import open3d as o3d"

点云格式：
xyz，xyzn，xyzrgb，pts，ply，pcd

网格格式：
ply,stl,obj,off,gltf

读取图像格式


Redwood dataset
Redwood格式数据将深度存储在16-bit单通道图像中。整数值表示深度，以毫米为单位。它是Open3d解析深度图像的默认格式。

SUN dataset

NYU dataset
NYU图像不是标准的jpg或者png格式，因此我们需要使用 mpimg.imread来读取一个color图像为一个numpy数组