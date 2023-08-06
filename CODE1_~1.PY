# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 17:15:27 2023

@author: akhtarj
"""

import cv2
import os
import numpy as np
import time


# path of the parent folder where data folder, python codes, PC_Edited_images folder are stored
folder = r'<insert> path of the parent folder'  

IF = "tif"  # Choose image format

##------------------Image_Clean_Section-------------------##
#----------------------------------------------------------#

path1 = folder + '\Particle Count'  # Particle Count folder in parent folder

# <Action> create an empty folder named "PC_Edited_Images" in parent folder before hand
save_folder = folder + '\Python_ImgProcessing_circularity' + '\PC_Edited_PostP_Images'

channel_frame_file_in = os.path.join(folder, f'Channel_frame.{IF}')                             
channel_frame = cv2.imread(channel_frame_file_in, 0)  # load channel frame

# Check that channel_fram image was loaded successfully
assert channel_frame is not None, 'Error: Failed to load channel_frame image'


#*****loop over the input images (both frame A & B)*****# 

frame_name_dict = {'A': 1.06, 'B': 1.055}  # create a dict for both frame with luminosity multiplying factor
# frame_name_dict = {'B': 1.07} 
img_start = 1  # starting image number
img_end = 300 # ending image number

# Define minimum and maximum area (in pixels) of particles to keep
min_area = 10
max_area = 60
particle_circularity = 0.35

start_all = time.time()
for frame, lum_mf in frame_name_dict.items():
        
    # loop over one frame (A or B) input/output images
    
    for k in range(img_start, img_end+1): 
        start_img1 = time.time()
        #---set the input and output filenames---#
        if k < 10:
            filename_in = f"test1_000{k}{frame}.{IF}"
            filename_out = f"EditedImg_000{k}{frame}.{IF}"
        elif (k >= 10 and k <= 99):
            filename_in = f"test1_00{k}{frame}.{IF}"
            filename_out = f"EditedImg_00{k}{frame}.{IF}"
        else:
            filename_in = f"test1_0{k}{frame}.{IF}"
            filename_out = f"EditedImg_0{k}{frame}.{IF}"
        
        full_filename_in = os.path.join(path1, filename_in)
        full_filename_out = os.path.join(save_folder, filename_out)
        #----------------------------------------#

        # read the input images
        image = cv2.imread(full_filename_in, 0)
        nrow_img = image.shape[0]
        ncolumn_img = image.shape[1]
        
        # Merge the two images horizontally
        merge_image = cv2.add(image, channel_frame)
        
        #---image processing based on local average pixel thresold---#
        x_len = int(ncolumn_img/87)  # length of local croped image (in 1392 direction)
        y_len = int(nrow_img/64)  # hight of local croped image (in 1024 direction)
    
        bin_x_list = list(np.arange(0, ncolumn_img, x_len))  # list for dividing line positions for local croped image
                                                             # in x-direction (1392 direction)
        bin_x_list.append(ncolumn_img)  # for second bound of local image in x-direction (1392 direction)
        
        bin_y_list = list(np.arange(0, nrow_img, y_len))  # list for dividing line positions for local croped image
                                                             # in y-direction (1024 direction)
        bin_y_list.append(nrow_img)  # for second bound of local image in y-direction (1024 direction)
        
        ############################################################################################################
        # 1. create local images using loop in x and y                                                             #
        # 2. calculate the average pixel value for thresold of the local image                                     #
        # 3. compare each pixel of local image with local thresold to remove noise and create                      #
        #    an array of noise free local image                                                                    #
        # 4. concatenate the local image arrays in y-direction (1024 direction) to make img_col arrays             #
        #    (img_row array length will be 1024 x x_len)                                                           #
        # 5. concatenate img_col arrays in x-direction (1392 direction) to generate img_entire (entire image)      #
        ############################################################################################################
        
        img_x = []
        for x in range(len(bin_x_list)-1):  # x+1 is used as index
            img_y = []
            for y in range(len(bin_y_list)-1):  # y+1 is used as index
                # cropped the local image from the image 
                image_local = image[bin_y_list[y]:bin_y_list[y+1], bin_x_list[x]:bin_x_list[x+1]]
                
                local_pxl_thrld = lum_mf*np.mean(np.array(image_local))  # local thresold value for image_local
                img_local = np.zeros_like(image_local)  # create an array for image_local to make noise free local image
                for i in range(image_local.shape[0]):  # loop for rows in image_local
                    for j in range(image_local.shape[1]):  # loop for rows in image_local
                        if image_local[i,j] == 255:  # to avoid the bight edge of image_local in the whole figure
                            img_local[i,j] = 0
                        if image_local[i,j] > local_pxl_thrld:  # comparing with thresold value to remove noise
                            img_local[i,j] = image_local[i,j]  # updating img_local array 
                        else:
                            img_local[i,j] = 0  # updating img_local array
                            
                img_y.append(img_local)  # creating a list of img_local array in y-direction
            
            img_col = np.concatenate(img_y, axis=0)  # concatenating to generate img_col array
            
            img_x.append(img_col)  # creating a list of img_col arrays in x-direction
            
        img_entire = np.concatenate(img_x, axis=1)  #concatenating to generate img_entire (entire image)
            
        #----------------------------------------------------------#               

        #---covert noise less image to a binary image and divide image into 12 bins---#
        binary_img = np.zeros_like(img_entire)
        div_line_arr = np.arange(0, ncolumn_img, int(ncolumn_img/12))  # for dividing line positions
        for i in range(nrow_img):
            for j in range(ncolumn_img):
                if j in div_line_arr:
                    binary_img[i,j] = 0  # diving image into 12 parts
                elif channel_frame[i,j] >= 50:
                    binary_img[i,j] = 0  # eliminating the wall pixels
                elif img_entire[i,j] > 50:
                    binary_img[i,j] = 255
                else:
                    binary_img[i,j] = 0
        
        #--------------------------------------------------------------------#
             
        #---removing particles baed on size---#
        
        # find contours of particles
        contours, hierarchy = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Create a new binary image for selected particles
        binary_img = np.zeros_like(binary_img)
        
        # filter particles based on size for frame A
        for cnt in contours:
            area = cv2.contourArea(cnt)
            perimeter = cv2.arcLength(cnt, True)
            if perimeter ==0:
                perimeter = 1
            circularity = 4*np.pi*(area/(perimeter**2))
            if area >= min_area and area <= max_area and circularity > particle_circularity:
                cv2.drawContours(binary_img, [cnt], 0, 255, -1)
        
        #----------------------------------------------#
        
        #---convert noise normalized pic to binary image---#
        
        
        #--------------------------------------------------#
                     
        # save the output images
        cv2.imwrite(full_filename_out, binary_img)
        
        end_img1 = time.time()
        total_time_img1 = end_img1 - start_img1
        
        print(f'Time taken for img_{k}{frame}: {total_time_img1}')
        
#*********************************************************#
end_all = time.time()
total_time = end_all - start_all

print(f'Total time for processing {img_end - img_start + 1} images (both frame A & B): {total_time}')