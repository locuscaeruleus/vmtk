#!/usr/bin/env python

## Program:   VMTK
## Module:    $RCSfile: vmtkicpregistration.py,v $
## Language:  Python
## Date:      $Date: 2005/09/14 09:49:59 $
## Version:   $Revision: 1.7 $

##   Copyright (c) Luca Antiga, David Steinman. All rights reserved.
##   See LICENCE file for details.

##      This software is distributed WITHOUT ANY WARRANTY; without even 
##      the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
##      PURPOSE.  See the above copyright notices for more information.


import vtk
import vtkvmtk
import sys

import pypes

vmtkicpregistration = 'vmtkICPRegistration'

class vmtkICPRegistration(pypes.pypeScript):

    def __init__(self):

        pypes.pypeScript.__init__(self)
        
        self.ReferenceSurface = None
        self.Surface = None
        self.DistanceArrayName = ''
        self.SignedDistanceArrayName = ''
        self.Level = 0.0

        self.FlipNormals = 0

        self.SetScriptName('vmtkicpregistration')
        self.SetScriptDoc('register a surface to a reference surface using the ICP algorithm')
        self.SetInputMembers([
            ['Surface','i','vtkPolyData',1,'','the input surface','vmtksurfacereader'],
            ['ReferenceSurface','r','vtkPolyData',1,'','the reference surface','vmtksurfacereader'],
            ['DistanceArrayName','distancearray','str',1,'','name of the array where the distance of the input surface to the reference surface has to be stored'],
            ['SignedDistanceArrayName','signeddistancearray','str',1,'','name of the array where the signed distance of the input surface to the reference surface is stored; distance is positive if distance vector and normal to the reference surface have negative dot product, i.e. if the input surface is outer with respect to the reference surface'],
            ['FlipNormals','flipnormals','bool',1,'','flip normals to the reference surface after computing them']
            ])
        self.SetOutputMembers([
            ['Surface','o','vtkPolyData',1,'','the output surface','vmtksurfacewriter']
            ])

    def Execute(self):

        if self.Surface == None:
            self.PrintError('Error: No Surface.')

        if self.ReferenceSurface == None:
            self.PrintError('Error: No ReferenceSurface.')

##         if (self.SignedDistanceArrayName != '') & (self.ReferenceSurface.GetPointData().GetNormals() == None):
        if (self.SignedDistanceArrayName != ''):
            normalsFilter = vtk.vtkPolyDataNormals()
            normalsFilter.SetInput(self.ReferenceSurface)
            normalsFilter.AutoOrientNormalsOn()
            normalsFilter.ConsistencyOn()
            normalsFilter.SplittingOff()
            normalsFilter.SetFlipNormals(self.FlipNormals)
            normalsFilter.Update()
            self.ReferenceSurface.GetPointData().SetNormals(normalsFilter.GetOutput().GetPointData().GetNormals())

        self.PrintLog('Computing ICP transform.')

        icpTransform = vtk.vtkIterativeClosestPointTransform()
        icpTransform.SetSource(self.Surface)
        icpTransform.SetTarget(self.ReferenceSurface)
        icpTransform.GetLandmarkTransform().SetModeToRigidBody()
        icpTransform.StartByMatchingCentroidsOn()
        icpTransform.SetMaximumNumberOfLandmarks(1000)
        icpTransform.SetMaximumNumberOfIterations(1000)
        icpTransform.SetMaximumMeanDistance(1E-2)

        transformFilter = vtk.vtkTransformPolyDataFilter()
        transformFilter.SetInput(self.Surface)
        transformFilter.SetTransform(icpTransform)
        transformFilter.Update()

        self.PrintLog('Mean distance: '+str(icpTransform.GetMeanDistance()))

        self.Surface = transformFilter.GetOutput()

        if (self.DistanceArrayName != '') | (self.SignedDistanceArrayName != ''):
            self.PrintLog('Computing distance.')
            surfaceDistance = vtkvmtk.vtkvmtkSurfaceDistance()
            surfaceDistance.SetInput(self.Surface)
            surfaceDistance.SetReferenceSurface(self.ReferenceSurface)
            if (self.DistanceArrayName != ''):
                surfaceDistance.SetDistanceArrayName(self.DistanceArrayName)
            if (self.SignedDistanceArrayName != ''):
                surfaceDistance.SetSignedDistanceArrayName(self.SignedDistanceArrayName)
            surfaceDistance.Update()
            self.Surface = surfaceDistance.GetOutput()


if __name__=='__main__':
    main = pypes.pypeMain()
    main.Arguments = sys.argv
    main.Execute()