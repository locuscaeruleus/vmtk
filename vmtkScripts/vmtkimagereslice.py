#!/usr/bin/env python

## Program:   VMTK
## Module:    $RCSfile: vmtkimagereslice.py,v $
## Language:  Python
## Date:      $Date: 2006/07/17 09:53:14 $
## Version:   $Revision: 1.8 $

##   Copyright (c) Luca Antiga, David Steinman. All rights reserved.
##   See LICENCE file for details.

##      This software is distributed WITHOUT ANY WARRANTY; without even 
##      the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
##      PURPOSE.  See the above copyright notices for more information.


import vtk
import sys

import pypes

vmtkimagereslice = 'vmtkImageReslice'

class vmtkImageReslice(pypes.pypeScript):

    def __init__(self):

        pypes.pypeScript.__init__(self)
        
        self.Image = None
        self.ReferenceImage = None

        self.OutputSpacing = []
        self.OutputOrigin = []
        self.OutputExtent = []

        self.Interpolation = 'linear'
        self.Cast = 1

        self.BackgroundLevel = 0.0

        self.SetScriptName('vmtkimagereslice')
        self.SetScriptDoc('reslice an image based on user-specified parameters or on a reference image')
        self.SetInputMembers([
            ['Image','i','vtkImageData',1,'','the input image','vmtkimagereader'],
            ['ReferenceImage','r','vtkImageData',1,'','the reference image','vmtkimagereader'],
            ['OutputSpacing','spacing','float',3,'','the output spacing'],
            ['OutputOrigin','origin','float',3,'','the output origin'],
            ['OutputExtent','extent','int',6,'','the output extent'],
            ['Interpolation','interpolation','str',1,'["nearestneighbor","linear","cubic"]','interpolation during reslice'],
            ['Cast','cast','bool',1,'','toggle cast image to float type'],
            ['BackgroundLevel','background','float',1,'','the output image background']
            ])
        self.SetOutputMembers([
            ['Image','o','vtkImageData',1,'','the output image','vmtkimagewriter']
            ])

    def Execute(self):

        if self.Image == None:
            self.PrintError('Error: No input image.')

        if self.Cast:
            cast = vtk.vtkImageCast()
            cast.SetInput(self.Image)
            cast.SetOutputScalarTypeToFloat()
            cast.Update()
            self.Image = cast.GetOutput()

        resliceFilter = vtk.vtkImageReslice()
        resliceFilter.SetInput(self.Image)
        if self.ReferenceImage:
            resliceFilter.SetInformationInput(self.ReferenceImage)
        else:
            if self.OutputSpacing:
                resliceFilter.SetOutputSpacing(self.OutputSpacing)
            if self.OutputOrigin:
                resliceFilter.SetOutputOrigin(self.OutputOrigin)
            if self.OutputExtent:
                resliceFilter.SetOutputExtent(self.OutputExtent)
        if self.Interpolation == 'nearestneighbor':
            resliceFilter.SetInterpolationModeToNearestNeighbor()
        elif self.Interpolation == 'linear':
            resliceFilter.SetInterpolationModeToLinear()
        elif self.Interpolation == 'cubic':
            resliceFilter.SetInterpolationModeToCubic()
        else:
            self.PrintError('Error: unsupported interpolation mode')
        resliceFilter.SetBackgroundLevel(self.BackgroundLevel)
        resliceFilter.Update()

        self.Image = resliceFilter.GetOutput()


if __name__=='__main__':

    main = pypes.pypeMain()
    main.Arguments = sys.argv
    main.Execute()