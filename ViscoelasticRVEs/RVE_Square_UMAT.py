# -*- coding: mbcs -*-
from abaqus import *
from abaqusConstants import *

Mdb()

import sys
sys.path.insert(8, r'c:/SIMULIA/CAE/plugins/2020/abaqus_plugins/createRVE')
import createRVE
createRVE.createRVE(model_lib_item='Square Array', partName='Part-1', 
    fiber_vof=0.2, RVE_length=1, Edge_seeds=10)

mdb.models['RVE_Square'].Material(name='Material-1')
mdb.models['RVE_Square'].materials['Material-1'].UserMaterial(
    mechanicalConstants=(32.38, 8.03, 13.20, 6.37, 21.56, 10.38, 13.40, 6.48, 3.71, 1.81, 4.00, 1.92, 30.0))
mdb.models['RVE_Square'].parts['Part-1'].MaterialOrientation(
    additionalRotationType=ROTATION_NONE, axis=AXIS_1, fieldName='', localCsys=
    None, orientationType=GLOBAL, 
    region=mdb.models['RVE_Square'].parts['Part-1'].sets['Set-Fiber'], stackDirection=STACK_3)
mdb.models['RVE_Square'].parts['Part-1'].MaterialOrientation(
    additionalRotationType=ROTATION_NONE, axis=AXIS_1, fieldName='', localCsys=
    None, orientationType=GLOBAL, 
    region=mdb.models['RVE_Square'].parts['Part-1'].sets['Set-Matrix'], stackDirection=STACK_3)

sys.path.insert(9, r'c:/SIMULIA/CAE/plugins/2020/abaqus_plugins/editMaterials')
import editMaterials
editMaterials.editMaterials(modelName_fiber='RVE_Square', 
    materialName_fiber='Material-1', modelName_matrix='RVE_Square', 
    materialName_matrix='Material-1')

mdb.models['RVE_Square'].rootAssembly.regenerate()

sys.path.insert(10, r'c:/SIMULIA/CAE/plugins/2020/abaqus_plugins/easyPBC')

import easypbc
import os
curr_dir = os.getcwd()
easypbc.feasypbc(modelName='RVE_Square', partName='Part-1', meshsens=1E-07, 
    CPU=12, Stiff_mat_E=False, Stiff_mat_V=True, relaxationTime=200, 
    minNumInc=100, umatName=curr_dir + '/umat3dorthotropic_viscoelastic.for')
