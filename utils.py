import numpy as np
import cv2

def seam_carve(input, new_h, new_w):
    in_im = cv2.imread(input).astype(np.float64)
    h, w = in_im.shape[:2]

    assert new_w <= w and new_w > 0 and new_h <= h and new_h > 0, 'Please enter dimensions that are smaller than the original image and are positive.'

    out_im = np.copy(in_im)

    e_kernel_x = np.array([[0, 0, 0],
                           [-1, 0, 1],
                           [0, 0, 0]], dtype=np.float64)
    e_kernel_y_l = np.array([[0, 0, 0],
                             [0, 0, 1],
                             [0, -1, 0]], dtype=np.float64)
    e_kernel_y_r = np.array([[0, 0, 0],
                             [1, 0, 0],
                             [0, -1, 0]], dtype=np.float64)
    
    num_rows, num_cols = int(h - new_h), int(w - new_w)

    remove_seam(out_im, num_cols)