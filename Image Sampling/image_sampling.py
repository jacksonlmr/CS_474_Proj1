# Write a program to change the spatial resolution from 256 x 256 to 128 x 128, 64 x 64, and 32 x
# 32 pixels using sub-sampling by a factor of 2, 4, and 8 correspondingly. For comparison
# purposes, resize the sub-sampled images back to the original size 256 x 256 (as shown in the
# lecture). Show your results using the “lenna” and “peppers” images from the image gallery. The
# example below shows how to sub-sample and resize an image assuming a factor of 2. Use the
# same idea for factors 4 and 8.

from PIL import Image
from IPython.display import display

lenna = Image.open("Image Sampling/lenna.gif")
peppers = Image.open("Image Sampling/peppers.gif")

def subsample(input_img: Image, factor: int):
    width, height = input_img.size

    output_width = width//factor
    output_height = height//factor
    output_size = (output_width, output_height)

    output_img = Image.new(size=output_size, mode='L')

    for row in range(width):
        for col in range(height):
            output_img_row = row//factor
            output_img_col = col//factor

            current_input_pixel = input_img.getpixel((row, col))

            if (row-1)%factor == 0 and (col-1)%factor == 0: #check if current location is a pixel to be sampled
                output_img.putpixel((output_img_row, output_img_col), current_input_pixel)
    
    return resize(output_img, width, height)

def resize(input_img: Image, width: int, height: int):
    input_width, input_height = input_img.size
    factor = width/input_width

    output_size = (width, height)
    output_img = Image.new(size=output_size, mode='L')

    for row in range(width):
        for col in range(height):
            input_pixel = input_img.getpixel((round(row/factor)-1, round(col/factor)-1))
            output_img.putpixel((row, col), input_pixel)

    return output_img

# factor 2
sub_sampled_lenna = subsample(lenna, 2)
sub_sampled_lenna.save("sub_sampled_lenna_2.gif")

sub_sampled_peppers = subsample(peppers, 2)
sub_sampled_peppers.save("sub_sampled_peppers_2.gif")

# factor 4
sub_sampled_lenna = subsample(lenna, 4)
sub_sampled_lenna.save("sub_sampled_lenna_4.gif")

sub_sampled_peppers = subsample(peppers, 4)
sub_sampled_peppers.save("sub_sampled_peppers_4.gif")

# factor 8
sub_sampled_lenna = subsample(lenna, 8)
sub_sampled_lenna.save("sub_sampled_lenna_8.gif")

sub_sampled_peppers = subsample(peppers, 8)
sub_sampled_peppers.save("sub_sampled_peppers_8.gif")

