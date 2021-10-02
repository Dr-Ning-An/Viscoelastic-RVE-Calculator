# -*- coding: mbcs -*-
from abaqus import *
from abaqusConstants import *

Mdb()

import sys
sys.path.insert(8, r'c:/SIMULIA/CAE/plugins/2020/abaqus_plugins/createRVE')
import createRVE
createRVE.createRVE(model_lib_item='Hexagonal Array', partName='Part-1', 
    fiber_vof=0.1, RVE_length=1, Edge_seeds=10)

mdb.models['RVE_Hexagonal'].Material(name='Material-Fiber')
mdb.models['RVE_Hexagonal'].materials['Material-Fiber'].Elastic(
    type=ENGINEERING_CONSTANTS, table=((303.0, 15.2, 15.2, 0.2, 0.2, 
    0.2, 9.65, 9.65, 15.2/2.0/(1.0+0.2)), ))
mdb.models['RVE_Hexagonal'].parts['Part-1'].MaterialOrientation(
    region=mdb.models['RVE_Hexagonal'].parts['Part-1'].sets['Set-Fiber'], 
    orientationType=GLOBAL, axis=AXIS_1, additionalRotationType=ROTATION_NONE, 
    localCsys=None, fieldName='', stackDirection=STACK_3)

mdb.models['RVE_Hexagonal'].Material(name='Material-Matrix')
mdb.models['RVE_Hexagonal'].materials['Material-Matrix'].Elastic(table=((3.31, 0.35), ))
sys.path.insert(9, r'c:/SIMULIA/CAE/plugins/2020/abaqus_plugins/editMaterials')
import editMaterials
editMaterials.editMaterials(modelName_fiber='RVE_Hexagonal', 
    materialName_fiber='Material-Fiber', modelName_matrix='RVE_Hexagonal', 
    materialName_matrix='Material-Matrix')

sys.path.insert(10, r'c:/SIMULIA/CAE/plugins/2020/abaqus_plugins/easyPBC')
import easypbc
easypbc.feasypbc(modelName='RVE_Hexagonal', partName='Part-1', meshsens=1E-07, 
    CPU=12, Stiff_mat_E=True, Stiff_mat_V=False, relaxationTime=10E10, 
    minNumInc=200, umatName='')
