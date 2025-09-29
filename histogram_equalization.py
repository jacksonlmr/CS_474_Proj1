from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from image_sampling import resize
import os

boat = Image.open("Input_Images/boat.gif")
f_16 = Image.open("Input_Images/f_16.gif")
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
    input_values, input_frequencies = get_histogram(input_img, width, height)

    #create bar graph to represent histogram
    input_pdf = getPDF(input_frequencies, width, height)

    input_histogram, ax1 = plt.subplots()
    ax1.bar(input_values, input_pdf)
    ax1.set_title(f"{os.path.splitext(os.path.basename(input_img.filename))[0].capitalize()} Input Histogram")


    #determine output value mapping
    output_values = []
    for i in range(width*height):
        denorm_cum_pdf = round(sum(input_pdf[:i])*(gray_levels-1))
        output_values.append(denorm_cum_pdf)

    for row in range(width):
        for col in range(height):
            input_pixel = input_img.getpixel((row, col))
            output_pixel = output_values[input_values.index(input_pixel)]
            output_img.putpixel((row, col), int(output_pixel))
    
    output_values, output_frequencies = get_histogram(output_img, width, height)
    output_pdf = getPDF(output_frequencies, width, height)
    output_histogram, ax2 = plt.subplots()
    ax2.bar(output_values, output_pdf)
    ax2.set_title(f"{os.path.splitext(os.path.basename(input_img.filename))[0].capitalize()} Output Histogram")

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
    
def getPDF(input_frequencies, width, height):
    pdf = []
    #calculate pdf
    for frequency in input_frequencies:
        pdf.append(frequency/(width*height))

    return pdf

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