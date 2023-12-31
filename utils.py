""" 
Utils
"""

import random
import matplotlib.pyplot as plt
import numpy as np

def save_frame(im, seam, is_vertical_seam, index):
    file_name = f'images/frame_by_frame_outputs/{"vertical" if is_vertical_seam else "horizontal"}_{index}_seam_removed.png'
    curr = np.copy(im)
    num_rows, num_cols = np.shape(np.sum(curr,axis=2).astype(np.uint8))
    
    curr[range(num_rows),seam,:] = [255,0,0]

    plt.figure(figsize=(5,5))
    plt.axis("off")
    plt.imshow(curr if is_vertical_seam else np.rot90(curr, 3))
    plt.savefig(file_name)
    
    return

def findseam(im):
    """
    Find a seam running from top to bottom of image or from right to left (once image is rotated ccw)
    """
    g_im = np.sum(im,axis=2) if len(np.shape(im)) == 3 else im
    g_im = g_im.astype(np.uint8)
        
    h, w = np.shape(g_im)

    # find energy map
    e_map = np.copy(g_im)
    mid = g_im[1:-1,1:-1]
    
    e_map[1:-1,1:-1] = (abs(mid - g_im[:-2,1:-1]) + abs(mid - g_im[2:,1:-1]) +
                     abs(mid - g_im[1:-1,:-2]) + abs(mid - g_im[1:-1,2:]))

    e_map[:,0] = (abs(g_im[:,0] - g_im[:,1]) + abs(g_im[:,0] - g_im[:,-1]))
    e_map[:,-1] = (abs(g_im[:,-1] - g_im[:,-2]) + abs(g_im[:,-1] - g_im[:,0]))

    e_map[:,1:-1] = (abs(g_im[:,1:-1]-g_im[:,:-2]) + abs(g_im[:,1:-1]-g_im[:,2:]))

    # columns
    e_map_y = np.copy(g_im)
    e_map_y[0,:] = (abs(g_im[0,:] - g_im[1,:]) + abs(g_im[0,:] - g_im[-1,:]))
    e_map_y[1,:] = (abs(g_im[-1,:] - g_im[-2,:]) + abs(g_im[-1,:] - g_im[0,:]))

    e_map_y[1:-1,:] = (abs(g_im[1:-1,:] - g_im[1:-1,:]) + abs(g_im[1:-1,:] - g_im[1:-1,:]))
    e_map += e_map_y

    
    # calculate energy paths
    e_paths = np.zeros([h, w])
    e_paths[0,:] = e_map[0,:]

    for row in np.arange(1, h):
        e_paths[row,0] = e_map[row,0]+min(e_paths[row-1,:2])
        e_paths[row, w-1] = e_map[row, w-1] + np.min(e_paths[row-1, w-2:])
        
        channels = np.zeros([w-2,3])
        channels[:,0] = e_paths[row-1, :w-2]
        channels[:,1] = e_paths[row-1, 1:w-1]
        channels[:,2] = e_paths[row-1, 2:]
        e_paths[row, 1:w-1] = e_map[row, 1:w-1] + np.min(channels, axis=1)       
    
    # construct the seam from lowest e_path
    seam = np.zeros(h).astype(int)
    seam[-1] = random.choice(np.where(e_paths[-1, :] == e_paths[-1, :].min())[0])

    for row in np.arange(h-2, -1, -1):
        prev = seam[row+1]
        seam[row] = assign_seam(row, prev, w, e_paths)
    
    return seam, e_paths


def removeseam(im, seam):
    if len(np.shape(im)) < 3:
        s_rows, s_cols = np.shape(im)
        bin_mask = np.ones(np.shape(im[:,:]), dtype=bool)
    else:
        s_rows, s_cols, colors = np.shape(im)
        bin_mask = np.ones(np.shape(im[:,:,0]), dtype=bool)
    
    for row in range(s_rows):
        bin_mask[row, seam[row]]=False
    carved = im[bin_mask]
    
    if len(np.shape(im)) < 3:
        carved = carved.reshape(s_rows, s_cols - 1)
    else:
        carved = carved.reshape(s_rows, s_cols - 1, colors)

    return carved

def assign_seam(row, prev, w, e_paths):
    out = -1
    if prev == 0:
        out = prev if e_paths[row, prev] <= e_paths[row, prev + 1] else prev + 1

    if prev != 0 and prev != w-1:
        if e_paths[row, prev - 1] < e_paths[row, prev] and e_paths[row, prev - 1] < e_paths[row, prev + 1]:
            out = prev - 1
        elif e_paths[row, prev + 1] < e_paths[row, prev - 1] and e_paths[row, prev + 1] < e_paths[row, prev]:
            out = prev + 1
        else:
            out = prev  

    if prev == w-1:
        out = prev if e_paths[row, prev]<=e_paths[row, prev - 1] else prev - 1
    
    return out
        
