#include <iostream>

#include <boost/program_options.hpp>

#include <pcl/point_types.h>
#include <pcl/io/pcd_io.h>
#include <pcl/kdtree/kdtree_flann.h>
#include <pcl/features/normal_3d.h>
#include <pcl/surface/gp3.h>
#include <pcl/io/vtk_io.h>
#include <pcl/io/vtk_lib_io.h>
#include <pcl/visualization/cloud_viewer.h>

#include <ctime>
#include <chrono>

using namespace boost::program_options;

int triangulation(std::string filename );

std::string change_filename(std::string filename);

int
main(int argc, char** argv)
{
	std::string filename;
		for (int i = 1; i < argc; i++) {

			if (strcmp(argv[i], "--file") == 0) {
				filename = argv[i + 1];
				printf("filename: %s", filename);
				triangulation(filename);
			}
		

		}



	
}

int triangulation(std::string filename) {

	volatile int i = 0; // "volatile" is to ask compiler not to optimize the loop away.
	auto start = std::chrono::steady_clock::now();
	std::cout << filename << '\n';
	if (filename != "")
	{
		pcl::PointCloud<pcl::PointXYZ>::Ptr cloud(new pcl::PointCloud<pcl::PointXYZ>);
		pcl::PCLPointCloud2 cloud_blob;
		//"C:\\Users\\callo\\Downloads\\tosca_hires\\centaur2.pcd"
		pcl::io::loadPCDFile(filename, cloud_blob);

		pcl::fromPCLPointCloud2(cloud_blob, *cloud);
		//* the data should be available in cloud

		// Normal estimation*
		pcl::NormalEstimation<pcl::PointXYZ, pcl::Normal> n;
		pcl::PointCloud<pcl::Normal>::Ptr normals(new pcl::PointCloud<pcl::Normal>);
		pcl::search::KdTree<pcl::PointXYZ>::Ptr tree(new pcl::search::KdTree<pcl::PointXYZ>);
		tree->setInputCloud(cloud);
		n.setInputCloud(cloud);
		n.setSearchMethod(tree);
		n.setKSearch(10);
		n.compute(*normals);
		//* normals should not contain the point normals + surface curvatures

		// Concatenate the XYZ and normal fields*
		pcl::PointCloud<pcl::PointNormal>::Ptr cloud_with_normals(new pcl::PointCloud<pcl::PointNormal>);
		pcl::concatenateFields(*cloud, *normals, *cloud_with_normals);
		//* cloud_with_normals = cloud + normals

		// Create search tree*
		pcl::search::KdTree<pcl::PointNormal>::Ptr tree2(new pcl::search::KdTree<pcl::PointNormal>);
		tree2->setInputCloud(cloud_with_normals);

		// Initialize objects
		pcl::GreedyProjectionTriangulation<pcl::PointNormal> gp3;
		pcl::PolygonMesh triangles;

		// Set the maximum distance between connected points (maximum edge length)
		gp3.setSearchRadius(10);

		// Set typical values for the parameters
		gp3.setMu(2.5);
		gp3.setMaximumNearestNeighbors(50);
		gp3.setMaximumSurfaceAngle(M_PI / 4); // 45 degrees
		gp3.setMinimumAngle(M_PI / 18); // 10 degrees
		gp3.setMaximumAngle(2 * M_PI / 3); // 120 degrees
		gp3.setNormalConsistency(false);

		// Get result
		gp3.setInputCloud(cloud_with_normals);
		gp3.setSearchMethod(tree2);
		gp3.reconstruct(triangles);

		// Additional vertex information
		std::vector<int> parts = gp3.getPartIDs();
		std::vector<int> states = gp3.getPointStates();

		pcl::io::savePolygonFileSTL(change_filename(filename), triangles);

		auto end = std::chrono::steady_clock::now();
		auto elapsed = std::chrono::duration_cast<std::chrono::seconds>(end - start);
		std::cout << "It took me " << elapsed.count() << " min" << std::endl;
	}
	return (0);

}

std::string change_filename(std::string filename) {
	return  filename.replace((filename.length() - 3), 3, "stl");
}