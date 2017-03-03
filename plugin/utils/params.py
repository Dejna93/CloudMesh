import os
import  pickle
from xml.dom import minidom
from collections import OrderedDict
from plugin.utils.oso import join


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class STLParams(object):

    __metaclass__ = Singleton

    def __init__(self, *args, **kwargs):

        for key , value in kwargs.items():
            self.__dict__[key]=value

        self.load_param()
        #pickle.dump(self.__dict__, open("stl_params.pl",'wb'))


    def getParams(self):
        return self.params

    def getParamByKey(self, key):
        return self.params[key]

    def load_param(self, path):
        self.__dict__ = pickle.load(open(path, 'rb'))
        self.params = OrderedDict(sorted(self.__dict__.items()))

    def load_param(self):
        # self.__dict__ = pickle.load(open("/home/dejna/PycharmProjects/CloudMesh/plugin/utils/stl_params.pl","rb"))
        self.__dict__ = pickle.load(open(join(os.path.dirname(os.path.abspath(__file__)), "stl_params.pl"), "rb"))
        self.params = OrderedDict(sorted(self.__dict__.items()))

    def set_param(self,key, value):
        print "set_param" + key + " " + value
        self.params[key] = value
    """
    Save dict to params.ini to load in Cpp
    """
    def save_params(self,filepath):
        with open(filepath,'w') as file:
            file.write("[STLParams]\n")
            for key,value in self.params.items():
                file.write(str(key)+"="+str(value)+"\n")
        return filepath


stlParams = STLParams()

"""
stl = STLParams(visualisation=0,show_loaded=0,show_clustered=0,type_triangulation=0,savepcd=1,iterations=100,distance_threshold=0.1,scale=1.1,
cloud_multipler=1.5,
cluster_tolerance=2,
lap_max_iter=400000,
lap_convergence=0.0001,
lap_relaxation_factor=0.5,
lap_edge_smoothing=1,
lap_boundary_smoothing=1,
mls_radius=0.0,
mls_sqt_gauss=0.0,
mls_polygon_fit=1,
mls_polygon_order=2,
mls_upsampling=0,
mls_upsampling_radius=0.025,
mls_upsampling_step_size=0.015,
mls_dilation_iter=2,
mls_dilation_voxel=0.01,
mls_compute_normals=0,
cluster_type=2,
euc_cluster_tolerance=2,
euc_min_cluster_size=10,
euc_max_cluster_size=25000,
reg_radius=0.03,
reg_min_cluster=10,
reg_max_cluster=25000,
reg_num_neighbours=50,
reg_curvature=1.0,
pl_distance=2,
pl_max_iter=100,
up_search_radius=3.0,
up_sampling_radius=3.0,
up_sampling_step=20,
normal_centroid=1,
normal_radius=300,
normal_k=20,
normal_minus=0,
thread_num=4,
poisson_radius=2,
poisson_depth=9,
poisson_solver_divide=9,
poisson_iso_divide=9,
poisson_samples_per_node=2.5,
poisson_confidence=0,
greedy_radius=3.0,
greedy_mu=2.8,
greedy_maximum_neighbors=1000,
greedy_surface_angle=0.785398163,
greedy_min_angle=0.1,
greedy_max_angle=2.094395102,
cl_radius=300.0,
nr_k=50,
stddev_ml=1.0, )


"""

"""[folders]
points=/home/dejna/abaqus_plugin/CloudMesh/workspace/project/points/
stl=/home/dejna/abaqus_plugin/CloudMesh/workspace/project/stl/
[option]
show_loaded=0
show_clustered=0
type_triangulation=0
visualisation=0
savepcd=1
iterations=100
distance_threshold=0.1
scale=1.1
cloud_multipler=1.5
cluster_tolerance=2
[MLS]
mls_radius=0.0
mls_sqt_gauss=0.0
mls_polygon_fit=1
mls_polygon_order=2
mls_upsampling=0
mls_upsampling_radius=0.025
mls_upsampling_step_size=0.015
mls_dilation_iter=2
mls_dilation_voxel=0.01
mls_compute_normals=0
[clustering]
cluster_type=2
[cluster]
euc_cluster_tolerance=2
euc_min_cluster_size=10
euc_max_cluster_size=25000
[region]
reg_radius=0.03
reg_min_cluster=10
reg_max_cluster=25000
reg_num_neighbours=50
reg_curvature=1.0
pl_distance=2
pl_max_iter=100
[sampling]
up_search_radius=3.0
up_sampling_radius=3.0
up_sampling_step=20
[normals]
normal_centroid=1
normal_radius=300
normal_k=20
normal_minus=0
[poisson]
thread_num=4
poisson_radius=2
poisson_depth=9
poisson_solver_divide=9
poisson_iso_divide=9
poisson_samples_per_node=2.5
poisson_confidence=0
[greedy]
greedy_radius=3.0
greedy_mu=2.8
greedy_maximum_neighbors=1000
greedy_surface_angle=0.785398163
greedy_min_angle=0.1
greedy_max_angle=2.094395102
[normal_cluster]
cl_radius=300.0
[noise]
nr_k=50
stddev_ml=1.0"""