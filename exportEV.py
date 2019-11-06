"""
This module provides a function to export Eigenvalue text files
"""

def exportEV(d,outfile):
    """
    Save EV file
    
    usage: exportEV(data,outfile)

    """

    # imports
    import numpy as np

    # open file
    try:
        f = open(outfile,'w')
    except IOError:
        print("[File "+outfile+" not writable]")
        return

    # check data structure
    if not 'Eigenvalues' in d:
        print("ERROR: no Eigenvalues specified")
        exit(1)

    # ...

    #
    if 'Creator' in d: f.write(' Creator: '+d['Creator']+'\n')
    if 'File' in d: f.write(' File: '+d['File']+'\n')
    if 'User' in d: f.write(' User: '+d['User']+'\n')
    if 'Refine' in d: f.write(' Refine: '+str(d['Refine'])+'\n')
    if 'Degree' in d: f.write(' Degree: '+str(d['Degree'])+'\n')
    if 'Dimension' in d: f.write(' Dimension: '+str(d['Dimension'])+'\n')
    if 'Elements' in d: f.write(' Elements: '+str(d['Elements'])+'\n')
    if 'DoF' in d: f.write(' DoF: '+str(d['DoF'])+'\n')
    if 'NumEW' in d: f.write(' NumEW: '+str(d['NumEW'])+'\n')
    f.write('\n')
    if 'Area' in d: f.write(' Area: '+str(d['Area'])+'\n')    
    if 'Volume' in d: f.write(' Volume: '+str(d['Volume'])+'\n')
    if 'BLength' in d: f.write(' BLength: '+str(d['BLength'])+'\n')
    if 'EulerChar' in d: f.write(' EulerChar: '+str(d['EulerChar'])+'\n')
    f.write('\n')
    if 'TimePre' in d: f.write(' Time(Pre) : '+str(d['TimePre'])+'\n')
    if 'TimeCalcAB' in d: f.write(' Time(calcAB) : '+str(d['TimeCalcAB'])+'\n')
    if 'TimeCalcEW' in d: f.write(' Time(calcEW) : '+str(d['TimeCalcEW'])+'\n')
    if 'TimePre' in d and 'TimeCalcAB' in d and 'TimeCalcEW' in d:
        f.write(' Time(total ) : '+str(d['TimePre']+d['TimeCalcAB']+d['TimeCalcEW'])+'\n')

    f.write('\n')
    f.write('Eigenvalues:\n')
    f.write('{ '+' ; '.join(map(str,d['Eigenvalues']))+' }\n') # consider precision
    f.write('\n')
    
    if 'Eigenvectors' in d:
        f.write('Eigenvectors:\n')
        #f.write('sizes: '+' '.join(map(str,d['EigenvectorsSize']))+'\n')
	# better compute real sizes from eigenvector array?
        f.write('sizes: '+' '.join(map(str,d['Eigenvectors'].shape))+'\n')
        f.write('\n')
        f.write('{ ')
        for i in range(np.shape(d['Eigenvectors'])[1]-1):
            f.write('(')
            f.write(','.join(map(str,d['Eigenvectors'][:,i])))
            f.write(') ;\n')
        f.write('(')
        f.write(','.join(map(str,d['Eigenvectors'][:,np.shape(d['Eigenvectors'])[1]-1])))
        f.write(') }\n')

    # close file
    f.close()
