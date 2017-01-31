from plugin.config import global_vars
import sys
sys.path.append('G:\SIMULIA\Abaqus\6.13-1\code\python\lib\abaqus_plugins')
if global_vars.DEBUG == False:
    from abaqus import *
    from abaqusConstants import *
    #from stlImport import *
    print sys.path

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
        #import stl2inp
        #stl2inp.STL2inp(stlfile=filename,
                   #     modelName=modelname, mergeNodesTolerance=mergeNodesTolerance)


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