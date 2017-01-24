# Embedded file name: SMAPyaModules\SMAPyaPluginsPy.m\src\abaqus_plugins\stlImport\stl2inp.py
import struct
from abaqus import *
from abaqusConstants import *
from caeModules import *
import i18n
from stl_Constants import *
import os, sys
from fromstl import *


def generateJobName(stlFileName):
    jobName = stlFileName[:-4]
    return jobName


def modelFromInp(stlinp, modelName, mergeNodesTolerance):
    try:
        mdb.ModelFromInputFile(name=modelName, inputFileName=stlinp)
        p = mdb.models[modelName].parts['PART-1']
        nodes = p.nodes
        p.mergeNodes(nodes=nodes, tolerance=mergeNodesTolerance)
        session.viewports['Viewport: 1'].setValues(displayedObject=p)
    except:
        raise ValueError, i18n.tr("Failed to create model from '%s'") % stlinp


def STL2inp(stlfile, modelName, mergeNodesTolerance):
    jobName = generateJobName(stlfile)
    args = ('-job',
            jobName,
            '-input',
            jobName,
            '-verbose',
            '1')
    print args
    app = fromstlApplication(args)
    status = app.run()
    if status:
        raise ValueError, i18n.tr('Error: conversion failed.')
    else:
        inpFileName = jobName + '.inp'
        inpFileName = os.path.abspath(inpFileName)
        if os.path.isfile(inpFileName) == FALSE:
            raise ValueError, i18n.tr('Error: conversion failed.')
        else:
            modelFromInp(inpFileName, modelName, mergeNodesTolerance)
