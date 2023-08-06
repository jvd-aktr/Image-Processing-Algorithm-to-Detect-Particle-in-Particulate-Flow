# Problem Statement:
Two Python-based codes were developed to process the raw images to detect, identify and count the particles and upload the data to a spreadsheet.

# Motivation:
The number of GitHub repositories dedicated to image processing algorithms is limited, and even fewer of them address the challenging task of detecting particles from raw images with significant background noise. To support our fellow researchers across various fields, who often encounter the need to process and analyze raw image data, we have decided to share an image processing algorithm that effectively removes background noise from raw images and accurately detects and counts particles within the image.

# Background:
This image processing algorithm has been specifically tailored for the investigation of particulate flow in wavy channels. The algorithm involves custom Python-based codes to process the raw images and estimate the particle distribution across the channel width. Two Python codes were developed for this purpose: The first code is responsible for eliminating noise from the raw image, thereby generating a noise-free binary image (a black and white image containing only particles). The second code processes the noise-free binary image to assess the particle distribution profile across the channel width. 
To facilitate these image processing tasks, Python harnesses various libraries, including Pandas, NumPy, SciPy, and cv2. For a more in-depth understanding of the algorithm, you can find a comprehensive discussion in the "Image Processing Algorithm" PDF file. the PDF file consists the flow chart of the image processing algorithm along with some sample images.

# Step to Run Codes:
1. Rename the raw image folder to " Particle Count" and put it in a parent folder where both first and second codes are stored.
2. The raw images should be named in certain manner. A sample set of images are uploaded.
3. Create a empty folder name "PC_Edited_PostP_Images" in the parent folder to store the generated binary image from Code1.

## To Run the First Code "Code1_Noise_Removal_Generate_Binary_Images.py":
1. Add the path of the parent folder in line 15 (folder = r'.......').
2. Change the intensity multiplying factors according to requirement (line 36 >> frame_name_dict = {'A': ---, 'B': ---}).
3. Change "img_start" and "end_image" based on number of image you want to process from raw image folder " Particle Count" (line 38, 39).
4. Change "min_area", "max_area" and "particle_circularity" values based requirment (line 42, 43, 44).
5. Run the code.

## To Run the Second Code "Code2_Evaluate_Particle_Distribution.py":
1. Add the path of the parent folder in line 18 (path = r'.......').
2. Change "num_img" based on number of image in "PC_Edited_PostP_Images" folder (line 32).
3. Change the name of the excel file based on your choice (line 169 >> Excel_file_name = '-----').
4. Run the code.

