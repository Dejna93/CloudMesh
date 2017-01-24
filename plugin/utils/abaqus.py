from plugin.config import global_vars
import sys
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
        # sys.path.append(r'G:\SIMULIA\Abaqus\6.13-1\code\python\lib\abaqus_plugins')
        # print sys.path
        # import imp
        # f , filename , desc  = imp.find_module('stl2inp',[r'G:\SIMULIA\Abaqus\6.13-1\code\python\lib\abaqus_plugins\stlImport'])
        # try:
        #     stl2inp = imp.load_module('stl2inp', f , filename, desc)
        #     f, filename, desc = imp.find_module('stl_Constants',
        #                                         [r'G:\SIMULIA\Abaqus\6.13-1\code\python\lib\abaqus_plugins\stlImport'])
        #     stl_Constants = imp.load_module('stl_Constants', f , filename, desc)
        # finally:
        #     print "end"
        from plugin.stl_import import stl2inp, stl_Constants
        filename = r'C:/Users/callo/abaqus_plugins/CloudMesh/plugin/workspace/project/stl/data'
        modelname = 'data'
        stl2inp.STL2inp(stlfile=filename,
                        modelName=modelname, mergeNodesTolerance='1E-006')


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

        import mesh_geo
        mesh_geo.Run(modelName='10', meshPartName='PART-1', geoPartName='', solid=True)