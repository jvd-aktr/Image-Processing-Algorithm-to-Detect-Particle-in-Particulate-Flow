# Problem Statement:
Two Python-based codes were developed to process the raw images to detect, identify and count the particles and upload the data to a spreadsheet.

# Motivation:
The number of GitHub repositories dedicated to image processing algorithms is limited, and even fewer of them address the challenging task of detecting particles from raw images with significant background noise. To support our fellow researchers across various fields, who often encounter the need to process and analyze raw image data, we have decided to share an image processing algorithm that effectively removes background noise from raw images and accurately detects and counts particles within the image.

# Background:
This image processing algorithm has been specifically tailored for the investigation of particulate flow in wavy channels. The algorithm involves custom Python-based codes to process the raw images and estimate the particle distribution across the channel width. Two Python codes were developed for this purpose: The first code is responsible for eliminating noise from the raw image, thereby generating a noise-free binary image (a black and white image containing only particles). The second code processes the noise-free binary image to assess the particle distribution profile across the channel width. 
To facilitate these image processing tasks, Python harnesses various libraries, including Pandas, NumPy, SciPy, and cv2. For a more in-depth understanding of the algorithm, you can find a comprehensive discussion in the "Image Processing Algorithm" PDF file. the PDF file consists the flow chart of the image processing algorithm along with some sample images.
# Step to Run Codes:
## To Run the First Code:
