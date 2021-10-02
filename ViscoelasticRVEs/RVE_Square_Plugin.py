# -*- coding: mbcs -*-
from abaqus import *
from abaqusConstants import *

Mdb()

import sys
sys.path.insert(8, r'c:/SIMULIA/CAE/plugins/2020/abaqus_plugins/createRVE')
import createRVE
createRVE.createRVE(model_lib_item='Square Array', partName='Part-1', 
    fiber_vof=0.2, RVE_length=1, Edge_seeds=10)

mdb.models['RVE_Square'].Material(name='Material-Fiber')
mdb.models['RVE_Square'].materials['Material-Fiber'].Elastic(table=((80.0, 0.3), 
    ))
mdb.models['RVE_Square'].Material(name='Material-Matrix')
mdb.models['RVE_Square'].materials['Material-Matrix'].Viscoelastic(domain=TIME, 
    time=PRONY, table=((0.5, 0.5, 30.0), ))
mdb.models['RVE_Square'].materials['Material-Matrix'].Elastic(moduli=INSTANTANEOUS, 
    table=((8.0, 0.4), ))
sys.path.insert(9, r'c:/SIMULIA/CAE/plugins/2020/abaqus_plugins/editMaterials')
import editMaterials
editMaterials.editMaterials(modelName_fiber='RVE_Square', 
    materialName_fiber='Material-Fiber', modelName_matrix='RVE_Square', 
    materialName_matrix='Material-Matrix')

mdb.models['RVE_Square'].rootAssembly.regenerate()

sys.path.insert(10, r'c:/SIMULIA/CAE/plugins/2020/abaqus_plugins/easyPBC')

import easypbc
easypbc.feasypbc(modelName='RVE_Square', partName='Part-1', meshsens=1E-07, 
    CPU=12, Stiff_mat_E=False, Stiff_mat_V=True, relaxationTime=200, 
    minNumInc=100, umatName='')
