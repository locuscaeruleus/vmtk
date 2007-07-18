#!/usr/bin/env python

## Program:   VMTK
## Module:    $RCSfile: vmtkimagecompose.py,v $
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

vmtkimagecompose = 'vmtkImageCompose'

class vmtkImageCompose(pypes.pypeScript):

    def __init__(self):

        pypes.pypeScript.__init__(self)
        
        self.Image = None
        self.Image2 = None
        self.Operation = 'min'

        self.SetScriptName('vmtkimagecompose')
        self.SetScriptDoc('compose an image based on user-specified parameters or on a reference image')
        self.SetInputMembers([
            ['Image','i','vtkImageData',1,'','the input image','vmtkimagereader'],
            ['Image2','i2','vtkImageData',1,'','the second input image','vmtkimagereader'],
            ['Operation','operation','str',1,'["min","max"]','the operation used to compose images']
            ])
        self.SetOutputMembers([
            ['Image','o','vtkImageData',1,'','the output image','vmtkimagewriter']
            ])

    def Execute(self):

        if self.Image == None:
            self.PrintError('Error: No input image.')

        if self.Image2 == None:
            self.PrintError('Error: No input image2.')

        composeFilter = vtk.vtkImageMathematics()
        composeFilter.SetInput1(self.Image)
        composeFilter.SetInput2(self.Image2)
        if self.Operation == 'min':
            composeFilter.SetOperationToMin()
        elif self.Operation == 'max':
            composeFilter.SetOperationToMax()
        else:
            self.PrintError('Error: Unsupported operation')
        composeFilter.Update()

        self.Image = composeFilter.GetOutput()


if __name__=='__main__':

    main = pypes.pypeMain()
    main.Arguments = sys.argv
    main.Execute()