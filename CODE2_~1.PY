
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 12:40:58 2023

@author: akhtarj
"""

import os
import numpy as np
import pandas as pd
from scipy import ndimage
import cv2
import time
import matplotlib.pyplot as plt

# path of the parent folder where data folder is stored
path = r'<insert> path of the parent folder'

Edited_Image_folder_name = '\PC_Edited_PostP_Images'  # name of the folder where edited binary images are stored after runing the first code

save_folder = path + Edited_Image_folder_name
data_folder= path

IF = "tif"  # Choose image format

#--1--particle count information for all images--1--#
particle_count_table = []  # list for particle count info
particle_per_table = []  # list for particle percentage info
img_list = []  # for dataframe first column

num_img = 300 # total number of images

for k in range(1, num_img+1):
    start_img = time.time()
    # set the input filenames
    if k < 10:
        filename_in_a = f"EditedImg_000{k}A.{IF}"
        filename_in_b = f"EditedImg_000{k}B.{IF}"
    elif (k >= 10 and k <= 99):
        filename_in_a = f"EditedImg_00{k}A.{IF}"
        filename_in_b = f"EditedImg_00{k}B.{IF}"
    else:
        filename_in_a = f"EditedImg_0{k}A.{IF}"
        filename_in_b = f"EditedImg_0{k}B.{IF}"
    
    full_filename_in_a = os.path.join(save_folder, filename_in_a) # access edited image frame A from save_folder
    full_filename_in_b = os.path.join(save_folder, filename_in_b) # access edited image frame B from save_folder
    
    binary_img_a = cv2.imread(full_filename_in_a, 0) # read edited image frame A   
    binary_img_b = cv2.imread(full_filename_in_b, 0)  # read edited image frame B
    
    #--1.1--particle count information for each bin of the image--1.1--#
    particle_table_bin = []
    particle_per_table_bin = []
        
    nrow_img = binary_img_a.shape[0]
    ncolumn_img = binary_img_a.shape[1]
    bin_div_list = list(np.arange(0, ncolumn_img, int(ncolumn_img/12 + 1)))  # for dividing line positions for bins
    bin_div_list.append(ncolumn_img)  # for second bound of las bin (#12)
    
    for i in range(len(bin_div_list)-1):
        binary_img_a_bin = binary_img_a[0:nrow_img, bin_div_list[i]:bin_div_list[i+1]]  # cropped the bin from image 
        binary_img_a_bin = np.array(binary_img_a_bin)  # convert edited image frame A to array to make the image 
                                                       # frame A array writeable
        binary_img_b_bin = binary_img_b[0:nrow_img, bin_div_list[i]:bin_div_list[i+1]]  # cropped the bin from image 
        binary_img_b_bin = np.array(binary_img_b_bin)  # convert edited image frame B to array to make the image 
                                                       # frame B array writeable
                                                       
        #--1.1.1--for edited image frame A--1.1.1--#
        # Label connected regions in binary image
        labeled_img_a_bin, num_features = ndimage.label(binary_img_a_bin)

        # Count number of particles and their sizes
        particle_sizes_a_bin = ndimage.sum(binary_img_a_bin, labeled_img_a_bin, range(1, num_features+1))
        particle_count_a_bin = len(particle_sizes_a_bin)
        #--1.1.1----------------------------1.1.1--#
        
        #--1.1.2--for edited image frame B--1.1.2--#
        # Label connected regions in binary image
        labeled_img_b_bin, num_features = ndimage.label(binary_img_b_bin)

        # Count number of particles and their sizes
        particle_sizes_b_bin = ndimage.sum(binary_img_b_bin, labeled_img_b_bin, range(1, num_features+1))
        particle_count_b_bin = len(particle_sizes_b_bin)
        #--1.1.2----------------------------1.1.2--#
        
        #--1.1.3--comparision for final particle count in a bin--1.1.3--#
        if particle_count_a_bin > particle_count_b_bin:
            particle_table_bin.append(particle_count_a_bin)
        else:
            particle_table_bin.append(particle_count_b_bin)
        #--1.1.3-------------------------------------------------1.1.3--#
        
        
    str_count = f'img_{k}'
    img_list.append(str_count)
    
    # bin-wise particle count information for each set of image (frame A & B)
    particle_count_table.append(particle_table_bin)
 
    # bin-wise particle percentage information for each set of image (frame A & B)
    bin_sum = sum(particle_table_bin)
    for bin in particle_table_bin:
        bin_per = (int(bin)/bin_sum)*100
        particle_per_table_bin.append(bin_per)    
    particle_per_table.append(particle_per_table_bin)
    
    
    # time calculation to process one set of image (frame A and B)
    end_img = time.time()
    total_time_img = end_img - start_img

    print(f'Time for Img{k}: {total_time_img}')
    
    #--1.1---------------------------------------------------------1.1--#

#--1------------------------------------------------1--#
    
#--2--create dataframes for particle information--2--#
bin_list = ['bin#1', 'bin#2', 'bin#3', 'bin#4', 'bin#5', 'bin#6',
            'bin#7', 'bin#8', 'bin#9', 'bin#10', 'bin#11', 'bin#12']  # bin numbers

# dataframe for particle count (bin-wise) information for every image set (A and B)
particle_count_info = pd.DataFrame(particle_count_table, columns = bin_list) 
particle_count_overall = particle_count_info.mean().tolist()  # calculate average of all columns and store in a list
particle_count_info.insert(0, 'Img#', img_list)  # insert image count column

# dataframe for particle percentage (bin-wise) information for every image set (A and B)
particle_per_info = pd.DataFrame(particle_per_table, columns = bin_list)
particle_per_overall = particle_per_info.mean().tolist()  # calculate average of all columns and store in a list
particle_per_info.insert(0, 'Img#', img_list)  # insert image count column

# dataframe for overall particle count (bin-wise) information
particle_info_overall = pd.DataFrame()
particle_info_overall[''] = bin_list  # column for bin number
particle_info_overall['ParticleCount'] = particle_count_overall # column of particle count before mask
particle_info_overall['ParticlePercentage'] = particle_per_overall # column of particle count before mask
#--2----------------------------------------------2--#

#--3-- plotting and saving the figures--3--#   
binn = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  # create list of bin for plots

fig, ax = plt.subplots()
ax.plot(binn, particle_per_overall, linestyle='-', linewidth = 2, color= 'r', marker='^')
plt.xticks(binn)
# draw vertical grid lines at desired points
ax.axvline(x=1.5, color='grey', linestyle='-.', linewidth = 1, alpha = 0.2)
ax.axvline(x=2.5, color='grey', linestyle='-.', linewidth = 1, alpha = 0.2)
ax.axvline(x=3.5, color='grey', linestyle='-.', linewidth = 1, alpha = 0.2)
ax.axvline(x=4.5, color='grey', linestyle='-.', linewidth = 1, alpha = 0.2)
ax.axvline(x=5.5, color='grey', linestyle='-.', linewidth = 1, alpha = 0.2)
ax.axvline(x=6.5, color='grey', linestyle='-.', linewidth = 1, alpha = 0.2)
ax.axvline(x=7.5, color='grey', linestyle='-.', linewidth = 1, alpha = 0.2)
ax.axvline(x=8.5, color='grey', linestyle='-.', linewidth = 1, alpha = 0.2)
ax.axvline(x=9.5, color='grey', linestyle='-.', linewidth = 1, alpha = 0.2)
ax.axvline(x=10.5, color='grey', linestyle='-.', linewidth = 1, alpha = 0.2)
ax.axvline(x=11.5, color='grey', linestyle='-.', linewidth = 1, alpha = 0.2)

plt.xlabel("Bins")
plt.ylabel("Particle Percentage")
plt.title('Particle Distribution')
plt.savefig(f'Particle%Plot.{IF}', dpi=600)
#--3-----------------------------------3--#

print(particle_per_info)

#--4--Create a Pandas Excel writer using the save_folder as the output directory--4--#
Excel_file_name = '<action> Change the name of excel file'  # name of the excel file
writer = pd.ExcelWriter(f'{data_folder}\{Excel_file_name}.xlsx') # length of Edited_Images is 14

# Write the first dataframe to the workbook
particle_count_info.to_excel(writer, sheet_name='ParticleCount', index=False)

# Write the second dataframe to the workbook
particle_per_info.to_excel(writer, sheet_name='ParticlePercentage', index=False)

# Write the second dataframe to the workbook
particle_info_overall.to_excel(writer, sheet_name='ParticleInfoOverall', index=False)

# Save the workbook and close the Pandas Excel writer
writer.save()
#--4-----------------------------------------------------------------------------4--#

