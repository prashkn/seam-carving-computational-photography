""" 
Utils
"""

import random
import numpy as np


def findseam(image):
    """
    Find a seam running from top to bottom of image
    """

    #1: convert to grayscale if necessary
    grayscale = len(np.shape(image))==2
    if grayscale:
        gray = image.astype(np.uint8)
    else:
        gray = np.sum(image,axis=2).astype(np.uint8)
    num_rows, num_cols = np.shape(gray)


    #2: find the energy, or amount of interest in the image
    # define energy based on pixel difference along a row

    #assume edges wrap
    #differences along rows
    energy = np.copy(gray)
    
    energy[1:-1,1:-1] = (abs(gray[1:-1,1:-1]-gray[:-2,1:-1])+
                     abs(gray[1:-1,1:-1]-gray[2:,1:-1])+
                     abs(gray[1:-1,1:-1]-gray[1:-1,:-2])+
                     abs(gray[1:-1,1:-1]-gray[1:-1,2:]))

    energy[:,0] = (abs(gray[:,0]-gray[:,1])+
                   abs(gray[:,0]-gray[:,-1]))
    energy[:,-1] = (abs(gray[:,-1]-gray[:,-2])+
                   abs(gray[:,-1]-gray[:,0]))

    energy[:,1:-1] = (abs(gray[:,1:-1]-gray[:,:-2])+
                         abs(gray[:,1:-1]-gray[:,2:]))

    #differences along columns
    energy2 = np.copy(gray)
    energy2[0,:] = (abs(gray[0,:]-gray[1,:])+
                   abs(gray[0,:]-gray[-1,:]))
    energy2[1,:] = (abs(gray[-1,:]-gray[-2,:])+
                   abs(gray[-1,:]-gray[0,:]))

    energy2[1:-1,:] = (abs(gray[1:-1,:]-gray[1:-1,:])+
                         abs(gray[1:-1,:]-gray[1:-1,:]))
    energy+=energy2


    #3: calculate energy paths
    energypaths = np.zeros([num_rows,num_cols])
    energypaths[0,:] = energy[0,:]

    for row in np.arange(1,num_rows):
        energypaths[row,0] = energy[row,0]+min(energypaths[row-1,:2])
        energypaths[row,num_cols-1] = energy[row,num_cols-1]+min(energypaths[row-1,num_cols-2:])
        
        #left, center, or right
        triples = np.zeros([num_cols-2,3])
        triples[:,0] = energypaths[row-1,:num_cols-2]
        triples[:,1] = energypaths[row-1,1:num_cols-1]
        triples[:,2] = energypaths[row-1,2:]
        energypaths[row,1:num_cols-1] = energy[row,1:num_cols-1]+np.min(triples,axis=1)       
    
    #4: pick out the lowest energy path and construct the seam from it
    seam = np.zeros(num_rows).astype(int)
    minimums = np.where(energypaths[-1,:]==energypaths[-1,:].min())[0]
    seam[-1] = random.choice(minimums)

    for row in np.arange(num_rows-2,-1,-1):
        prevcol = seam[row+1]
        if prevcol!=0 and prevcol!=num_cols-1:
            if energypaths[row,prevcol-1]<energypaths[row,prevcol] and energypaths[row,prevcol-1]<energypaths[row,prevcol+1]:
                seam[row] = prevcol-1
            elif energypaths[row,prevcol+1]<energypaths[row,prevcol-1] and energypaths[row,prevcol+1]<energypaths[row,prevcol]:
                seam[row] = prevcol+1
            else:
                seam[row] = prevcol  
        if prevcol==0:
            if energypaths[row,prevcol]<=energypaths[row,prevcol+1]:
                seam[row] = prevcol    
            else:
                seam[row] = prevcol+1
        if prevcol==num_cols-1:
            if energypaths[row,prevcol]<=energypaths[row,prevcol-1]:
                seam[row] = prevcol    
            else:
                seam[row] = prevcol-1
    
    return seam, energypaths


def removeseam(image,seam):
    """ 
    Removes one seam from an image
    """
    grayscale = len(np.shape(image))==2
    
    if grayscale:
        startrows, startcols = np.shape(image)
        binarymask = np.ones(np.shape(image[:,:]),dtype=bool)
    else:
        startrows, startcols, colors = np.shape(image)
        binarymask = np.ones(np.shape(image[:,:,0]),dtype=bool)
    
    for row in range(startrows):
        binarymask[row,seam[row]]=False
    keep = image[binarymask]
    
    if grayscale:
        keep = keep.reshape(startrows,startcols-1)
    else:
        keep = keep.reshape(startrows,startcols-1,colors)

    return keep