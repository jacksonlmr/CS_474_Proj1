from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from image_sampling import resize
import os

boat = Image.open("Input_Images/boat.gif").convert('L')
boat.save("Input_Images/boat.pgm")
boat = Image.open("Input_Images/boat.pgm")

f_16 = Image.open("Input_Images/f_16.gif").convert('L')
f_16.save("Input_Images/f_16.pgm")
f_16 = Image.open("Input_Images/f_16.pgm")
                  
save_file_path = "Output_Images/Equalization/"
gray_levels = 256

#create and save test image
test_img_pixels = np.array([[220, 220, 220, 220, 220], 
                            [200, 200, 200, 200, 200],
                            [190, 190, 190, 190, 190],
                            [180, 180, 180, 180, 180],
                            [170, 170, 170, 170, 170]], dtype=np.uint8)
test_img = Image.fromarray(test_img_pixels, 'L')
test_img = resize(test_img, 256, 256)
test_img.save("Input_Images/test_img.png")
test_img = Image.open("Input_Images/test_img.png")

def equalize(input_img: Image):
    output_img = Image.new(size=input_img.size, mode='L')
    width, height = input_img.size

    #get input values, create pdf for input image
    input_values, input_frequencies = get_histogram(input_img, width, height)
    input_cdf = getCDF(input_frequencies, width, height)

    input_histogram = create_histogram(input_img, input_values, input_cdf, "Input Histogram")


    #determine output value mapping
    output_values = get_output_values(width, height, gray_levels, input_cdf)

    for row in range(width):
        for col in range(height):
            input_pixel = input_img.getpixel((row, col))
            output_pixel = output_values[input_values.index(input_pixel)]
            output_img.putpixel((row, col), int(output_pixel))
    
    #get input values, create pdf for output image
    output_values, output_frequencies = get_histogram(output_img, width, height)
    output_cdf = getCDF(output_frequencies, width, height)

    output_histogram = create_histogram(input_img, output_values, output_cdf, "Output Histogram")

    return (input_histogram, output_histogram, output_img)


def get_histogram(input_img: Image, width, height):
    #get width and height of img, instantiate list of possible pixel values and dict 
    input_hist_list = list(range(0, gray_levels))
    input_hist_dict = {}

    #populate dict with 0's associated with each possible pixel value
    for value in input_hist_list:
        input_hist_dict[value] = 0
    
    #for each pixel in the image, increment the associated value in the dict
    for row in range(width):
        for col in range(height):
            input_pixel = input_img.getpixel((row, col))
            input_hist_dict[input_pixel] += 1

    #convert dict to 2 arrays
    input_pixel_value = list(input_hist_dict.keys())
    input_pixel_frequency = list(input_hist_dict.values())

    return (input_pixel_value, input_pixel_frequency)

def getCDF(input_frequencies, width, height):
    pdf = []
    #calculate pdf
    for frequency in input_frequencies:
        pdf.append(frequency/(width*height))

    return pdf

def create_histogram(in_img, in_values, in_cdf, histogram_label):
    input_histogram, ax1 = plt.subplots()
    ax1.bar(in_values, in_cdf)
    ax1.set_xlabel("Pixel Value")
    ax1.set_ylabel("CDF")
    input_file_name = os.path.basename(in_img.filename)
    input_file_name = os.path.splitext(input_file_name)[0].capitalize()
    ax1.set_title(f"{input_file_name} {histogram_label}")

    return input_histogram    

def get_output_values(w, h, gray_levels, in_cdf):
    output_values = []
    for i in range(w*h):
        denorm_cum_cdf = round(sum(in_cdf[:i])*(gray_levels-1))
        output_values.append(denorm_cum_cdf)

    return output_values

test_input_hist, test_output_hist, equalized_test = equalize(test_img)
equalized_test.save(f"{save_file_path}equalized_test.gif")
test_input_hist.savefig(f"{save_file_path}test_input_hist.png")
test_output_hist.savefig(f"{save_file_path}test_output_hist.png")

boat_input_hist, boat_output_hist, equalized_boat = equalize(boat)
equalized_boat.save(f"{save_file_path}equalized_boat.gif")
boat_input_hist.savefig(f"{save_file_path}boat_input_hist.png")
boat_output_hist.savefig(f"{save_file_path}boat_output_hist.png")

f_16_input_hist, f_16_output_hist, equalized_f_16 = equalize(f_16)
equalized_f_16.save(f"{save_file_path}equalized_f_16.gif")
f_16_input_hist.savefig(f"{save_file_path}f_16_input_hist.png")
f_16_output_hist.savefig(f"{save_file_path}f_16_output_hist.png")