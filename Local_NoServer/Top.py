#Used for debugging, when not in iPython
import sys
import os

os.chdir('..\\WebProject')
sys.path.append('app\\')

import Alignment2D
(kp1Matches, kp2Matches) = Alignment2D.SetupTheStuff()
Alignment2D.LinearLeastSquare ( kp1Matches, kp2Matches ) 
#Alignment2D.Levenberg(kp1Matches, kp2Matches) 