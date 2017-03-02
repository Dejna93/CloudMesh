from plugin.config import storage
from plugin.utils.oso import join
import sys
import os

if storage.DEBUG == False:
    from abaqus import *
    from abaqusConstants import *

    import __main__


    def stl_to_abaqus(filename, modelname, mergeNodesTolerance):
        import section
        import regionToolset
        import displayGroupMdbToolset as dgm
        import part
        import material
        import assembly
        import step
        import interaction
        import load
        import mesh
        import optimization
        import job
        import sketch
        import visualization
        import xyPlot
        import displayGroupOdbToolset as dgo
        import connectorBehavior
        sys.path.insert(11, add_to_path())
        print "Creating model from STL"
        import stl2inp
        stl2inp.STL2inp(
            stlfile=filename,
            modelName=modelname, mergeNodesTolerance=1E-006)


    def add_to_path():
        path = join(os.path.split(os.__file__)[0], 'abaqus_plugins/stlImport')
        print path
        if os.path.exists(path):
            return path



    def make_solid(modelName,meshPartName,geoPartName,solid=True):
        import section
        import regionToolset
        import displayGroupMdbToolset as dgm
        import part
        import material
        import assembly
        import step
        import interaction
        import load
        import mesh
        import optimization
        import job
        import sketch
        import visualization
        import xyPlot
        import displayGroupOdbToolset as dgo
        import connectorBehavior
        sys.path.insert(12,
                        r'c:/Users/callo/abaqus_plugins/3DMesh_to_Geometry_Plugin614')
        import mesh_geo
        mesh_geo.Run(modelName='10', meshPartName='PART-1', geoPartName='', solid=True)