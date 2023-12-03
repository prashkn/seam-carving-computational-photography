""" 
Utils
"""

import random
import numpy as np


def findseam(im):
    """
    Find a seam running from top to bottom of image or from left to right (once image is rotated)
    """

    if len(np.shape(im)) == 2:
        gray = im.astype(np.uint8)
    else:
        gray = np.sum(im,axis=2).astype(np.uint8)
    num_rows, num_cols = np.shape(gray)


    # find energy map
    e_map = np.copy(gray)
    
    e_map[1:-1,1:-1] = (abs(gray[1:-1,1:-1] - gray[:-2,1:-1]) + abs(gray[1:-1,1:-1] - gray[2:,1:-1]) +
                     abs(gray[1:-1,1:-1] - gray[1:-1,:-2]) + abs(gray[1:-1,1:-1] - gray[1:-1,2:]))

    e_map[:,0] = (abs(gray[:,0] - gray[:,1]) + abs(gray[:,0] - gray[:,-1]))
    e_map[:,-1] = (abs(gray[:,-1] - gray[:,-2]) + abs(gray[:,-1] - gray[:,0]))

    e_map[:,1:-1] = (abs(gray[:,1:-1]-gray[:,:-2]) + abs(gray[:,1:-1]-gray[:,2:]))

    # differences along columns
    e_map2 = np.copy(gray)
    e_map2[0,:] = (abs(gray[0,:] - gray[1,:]) + abs(gray[0,:] - gray[-1,:]))
    e_map2[1,:] = (abs(gray[-1,:] - gray[-2,:]) + abs(gray[-1,:] - gray[0,:]))

    e_map2[1:-1,:] = (abs(gray[1:-1,:] - gray[1:-1,:]) + abs(gray[1:-1,:] - gray[1:-1,:]))
    e_map += e_map2


    # calculate energy paths
    e_paths = np.zeros([num_rows, num_cols])
    e_paths[0,:] = energy[0,:]

    for row in np.arange(1,num_rows):
        e_paths[row,0] = energy[row,0]+min(e_paths[row-1,:2])
        e_paths[row, num_cols-1] = energy[row, num_cols-1] + np.min(e_paths[row-1, num_cols-2:])
        
        channels = np.zeros([num_cols-2,3])
        channels[:,0] = e_paths[row-1, :num_cols-2]
        channels[:,1] = e_paths[row-1, 1:num_cols-1]
        channels[:,2] = e_paths[row-1, 2:]
        e_paths[row, 1:num_cols-1] = e_map[row, 1:num_cols-1] + np.min(channels, axis=1)       
    
    #4: construct the seam from lowest e_path
    seam = np.zeros(num_rows).astype(int)
    mins = np.where(e_paths[-1, :] == e_paths[-1, :].min())[0]
    seam[-1] = random.choice(mins)

    for row in np.arange(num_rows-2, -1, -1):
        prev = seam[row+1]
        if prev != 0 and prev != num_cols-1:
            if e_paths[row, prev - 1] < e_paths[row, prev] and e_paths[row, prev - 1] < e_paths[row, prev + 1]:
                seam[row] = prev - 1
            elif e_paths[row, prev + 1] < e_paths[row, prev - 1] and e_paths[row, prev + 1] < e_paths[row, prev]:
                seam[row] = prev + 1
            else:
                seam[row] = prev  
        if prev == 0:
            if e_paths[row, prev]<=e_paths[row, prev + 1]:
                seam[row] = prev    
            else:
                seam[row] = prev + 1
        if prev == num_cols-1:
            if e_paths[row, prev]<=e_paths[row, prev - 1]:
                seam[row] = prev    
            else:
                seam[row] = prev - 1
    
    return seam, e_paths


def removeseam(im,seam):
    """ 
    Removes given seam from an image
    """
    
    if len(np.shape(im)) == 2:
        s_rows, s_cols = np.shape(im)
        bin_mask = np.ones(np.shape(im[:,:]), dtype=bool)
    else:
        s_rows, s_cols, colors = np.shape(im)
        bin_mask = np.ones(np.shape(im[:,:,0]), dtype=bool)
    
    for row in range(s_rows):
        bin_mask[row, seam[row]]=False
    keep = im[bin_mask]
    
    if len(np.shape(im)) == 2:
        keep = keep.reshape(s_rows, s_cols - 1)
    else:
        keep = keep.reshape(s_rows, s_cols - 1, colors)

    return keep

def rotate_im(im, num_rots):
    # rotate once and then 3 more times to rotate back to normal
    out = np.rot90(im, num_rots)
    return out
    