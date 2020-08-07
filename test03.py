import open3d as o3d
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import re
import numpy as np
#读取RGBD图像
# http://redwood-data.org/
# http://www.open3d.org/docs/release/tutorial/reference.html#choi2015
# Redwood datasets数据集
def test_redwood_dataset():
    '''
    使用PinholeCameraIntrinsicParameters.PrimeSenseDefault 作为默认的相机参数，
    它的图像分辨率为640x480，焦距(fx,fy)=(525.0,525.0)，光学中心(cx,cy)=(319.5,239.5)。
    使用单位矩阵作为默认的外部参数。pcd.transform在点云上应用上下翻转实现更好的可视化的目的。'''
    print("Read Redwood dataset")
    color_raw = o3d.io.read_image("../../TestData/RGBD/color/00000.jpg")
    depth_raw = o3d.io.read_image("../../TestData/RGBD/depth/00000.png")
    #从成对的彩色图（color image）和深度图（depth image）中生成RGBDImage
    rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(color_raw, depth_raw)
    
    print(rgbd_image)
    plt.subplot(1, 2, 1)
    plt.title('Redwood grayscale image')
    plt.imshow(rgbd_image.color)
    plt.subplot(1, 2, 2)
    plt.title('Redwood depth image')
    plt.imshow(rgbd_image.depth)
    plt.show()

    # 给定一组相机参数，RGBD图像能够转换成点云。
    pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd_image,o3d.camera.PinholeCameraIntrinsic(o3d.camera.PinholeCameraIntrinsicParameters.PrimeSenseDefault))
    # Flip it, otherwise the pointcloud will be upside down
    pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
    o3d.visualization.draw_geometries([pcd], zoom=0.5)

# http://rgbd.cs.princeton.edu/
# http://www.open3d.org/docs/release/tutorial/reference.html#song2015
# SUN dataset数据集
def test_sun_dataset():
    '''
    与处理Redwood数据几乎相同。
    唯一的不同是我们使用create_rgbd_image_from_sun_format转换函数来从SUN数据集解析深度图像。
    '''
    print("Read SUN dataset")
    color_raw = o3d.io.read_image("../../TestData/RGBD/other_formats/SUN_color.jpg")
    depth_raw = o3d.io.read_image("../../TestData/RGBD/other_formats/SUN_depth.png")
    rgbd_image = o3d.geometry.RGBDImage.create_from_sun_format(color_raw, depth_raw)
    print(rgbd_image)
    plt.subplot(1, 2, 1)
    plt.title('SUN grayscale image')
    plt.imshow(rgbd_image.color)
    plt.subplot(1, 2, 2)
    plt.title('SUN depth image')
    plt.imshow(rgbd_image.depth)
    plt.show()
    pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd_image,o3d.camera.PinholeCameraIntrinsic(o3d.camera.PinholeCameraIntrinsicParameters.PrimeSenseDefault))
    # Flip it, otherwise the pointcloud will be upside down
    pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
    o3d.visualization.draw_geometries([pcd], zoom=0.5)
# http://www.open3d.org/docs/release/tutorial/reference.html#silberman2012
# https://cs.nyu.edu/~silberman/datasets/nyu_depth_v2.html
# NYU dataset数据集

# This is special function used for reading NYU pgm format
# as it is written in big endian byte order.
def read_nyu_pgm(filename, byteorder='>'):
    with open(filename, 'rb') as f:
        buffer = f.read()
    try:
        header, width, height, maxval = re.search(b"(^P5\s(?:\s*#.*[\r\n])*"b"(\d+)\s(?:\s*#.*[\r\n])*"b"(\d+)\s(?:\s*#.*[\r\n])*"b"(\d+)\s(?:\s*#.*[\r\n]\s)*)", buffer).groups()
    except AttributeError:
        raise ValueError("Not a raw PGM file: '%s'" % filename)
    img = np.frombuffer(buffer,
                        dtype=byteorder + 'u2',
                        count=int(width) * int(height),
                        offset=len(header)).reshape((int(height), int(width)))
    img_out = img.astype('u2')
    return img_out
def test_nyu_data():
    '''
    与Redwood几乎相同，只有两处不一样。首先，NYU图像不是标准的jpg或者png格式，
    因此我们需要使用 mpimg.imread来读取一个color图像为一个numpy数组，并将其转化为Open3d图像。
    还需要使用一个额外的辅助函数read_nyu_pgm来从 NYU数据集使用的特殊大端模式(special big endian) pgm格式的数据中读取深度图像。
    其次我们使用create_rgbd_image_from_nyu_format转换函数来从NYU数据集中解析深度图。
    '''
    print("Read NYU dataset")
    # Open3D does not support ppm/pgm file yet. Not using o3d.io.read_image here.
    # MathplotImage having some ISSUE with NYU pgm file. Not using imread for pgm.
    color_raw = mpimg.imread("../../TestData/RGBD/other_formats/NYU_color.ppm")
    depth_raw = read_nyu_pgm("../../TestData/RGBD/other_formats/NYU_depth.pgm")
    color = o3d.geometry.Image(color_raw)
    depth = o3d.geometry.Image(depth_raw)
    rgbd_image = o3d.geometry.RGBDImage.create_from_nyu_format(color, depth)
    print(rgbd_image)

    plt.subplot(1, 2, 1)
    plt.title('NYU grayscale image')
    plt.imshow(rgbd_image.color)
    plt.subplot(1, 2, 2)
    plt.title('NYU depth image')
    plt.imshow(rgbd_image.depth)
    plt.show()

    pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd_image,o3d.camera.PinholeCameraIntrinsic(o3d.camera.PinholeCameraIntrinsicParameters.PrimeSenseDefault))
    # Flip it, otherwise the pointcloud will be upside down
    pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
    o3d.visualization.draw_geometries([pcd], zoom=0.5)

# https://vision.in.tum.de/data/datasets/rgbd-dataset
# http://www.open3d.org/docs/release/tutorial/reference.html#strum2012
# TUM dataset数据集
def test_tum_dataset():
    '''
    和之前的Redwood数据集的介绍也几乎一样。
    只有一点不同是我们使用create_rgbd_image_from_tum_format函数去从TUM数据集中解析深度数据。
    '''
    print("Read TUM dataset")
    color_raw = o3d.io.read_image("../../TestData/RGBD/other_formats/TUM_color.png")
    depth_raw = o3d.io.read_image("../../TestData/RGBD/other_formats/TUM_depth.png")
    rgbd_image = o3d.geometry.RGBDImage.create_from_tum_format(color_raw, depth_raw)
    print(rgbd_image)
    plt.subplot(1, 2, 1)
    plt.title('TUM grayscale image')
    plt.imshow(rgbd_image.color)
    plt.subplot(1, 2, 2)
    plt.title('TUM depth image')
    plt.imshow(rgbd_image.depth)
    plt.show()
    pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd_image,o3d.camera.PinholeCameraIntrinsic(o3d.camera.PinholeCameraIntrinsicParameters.PrimeSenseDefault))
    # Flip it, otherwise the pointcloud will be upside down
    pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
    o3d.visualization.draw_geometries([pcd], zoom=0.35)