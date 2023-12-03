""" 
Utils
"""

import random
import numpy as np


def find_seam(im):
    """
    Choose a competent seam to eventually remove
    """

    gray = np.sum(im,axis=2) if len(np.shape(im)) != 2 else im
    gray = gray.astype(np.uint8)
        
    r,c = np.shape(gray)

    #create energy map through calculating differences
    energy = np.copy(gray)
    
    mid = gray[1:-1,1:-1]
    energy[1:-1,1:-1] = (abs(mid-gray[:-2,1:-1]) + abs(mid-gray[2:,1:-1]) + abs(mid-gray[1:-1,:-2]) + abs(mid-gray[1:-1,2:]))

    #differences by row
    energy[:,0] = (abs(gray[:,0]-gray[:,1]) + abs(gray[:,0]-gray[:,-1]))
    energy[:,-1] = (abs(gray[:,-1]-gray[:,-2]) + abs(gray[:,-1]-gray[:,0]))
    energy[:,1:-1] = (abs(gray[:,1:-1]-gray[:,:-2]) + abs(gray[:,1:-1]-gray[:,2:]))

    #differences by column
    energy_col = np.copy(gray)
    energy_col[0,:] = (abs(gray[0,:]-gray[1,:]) + abs(gray[0,:]-gray[-1,:]))
    energy_col[1,:] = (abs(gray[-1,:]-gray[-2,:]) + abs(gray[-1,:]-gray[0,:]))
    energy_col[1:-1,:] = (abs(gray[1:-1,:]-gray[1:-1,:]) + abs(gray[1:-1,:]-gray[1:-1,:]))
    energy += energy_col

    #calculate energy paths
    energypaths = np.zeros([r,c])
    energypaths[0,:] = energy[0,:]

    for row in np.arange(1,r):
        energypaths[row,0] = energy[row,0] + min(energypaths[row-1,:2])
        energypaths[row,c-1] = energy[row,c-1] + min(energypaths[row-1,c-2:])
        
        #left, center, or right
        min_ = np.zeros([c-2,3])
        for i in range(3):
            min_[:,i] = energypaths[row-1,i:c-2+i]
        energypaths[row,1:c-1] = energy[row,1:c-1]+np.min(min_,axis=1)       
    
    #4: pick out the lowest energy path and construct the seam from it
    seam = np.zeros(r).astype(int)
    minimums = np.where(energypaths[-1,:]==energypaths[-1,:].min())[0]
    seam[-1] = random.choice(minimums)

    for row in np.arange(r-2,-1,-1):
        prevcol = seam[row+1]
        if prevcol!=0 and prevcol!=c-1:
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
        if prevcol==c-1:
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