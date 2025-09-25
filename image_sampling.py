from PIL import Image
from IPython.display import display

lenna = Image.open("Input_Images/lenna.gif")
peppers = Image.open("Input_Images/peppers.gif")
save_file_path = "Output_Images/Sampling/"

def subsample(input_img: Image, factor: int):
    width, height = input_img.size

    #Calculate output image size
    output_width = width//factor
    output_height = height//factor
    output_size = (output_width, output_height)

    output_img = Image.new(size=output_size, mode='L')

    for row in range(width):
        for col in range(height):

            current_input_pixel = input_img.getpixel((row, col))

            #check if current location is a pixel to be sampled, if it is, map value to output
            if (row-1)%factor == 0 and (col-1)%factor == 0: 
                output_img_row = row//factor
                output_img_col = col//factor
                output_img.putpixel((output_img_row, output_img_col), current_input_pixel)
    
    return resize(output_img, width, height)

def resize(input_img: Image, width: int, height: int):
    input_width, input_height = input_img.size
    factor = width/input_width

    output_size = (width, height)
    output_img = Image.new(size=output_size, mode='L')

    for row in range(width):
        for col in range(height):
            input_pixel = input_img.getpixel((int(row/factor), int(col/factor)))
            output_img.putpixel((row, col), input_pixel)

    return output_img

# factor 2
sub_sampled_lenna = subsample(lenna, 2)
sub_sampled_lenna.save(f"{save_file_path}sub_sampled_lenna_2.gif")

sub_sampled_peppers = subsample(peppers, 2)
sub_sampled_peppers.save(f"{save_file_path}sub_sampled_peppers_2.gif")

# factor 4
sub_sampled_lenna = subsample(lenna, 4)
sub_sampled_lenna.save(f"{save_file_path}sub_sampled_lenna_4.gif")

sub_sampled_peppers = subsample(peppers, 4)
sub_sampled_peppers.save(f"{save_file_path}sub_sampled_peppers_4.gif")

# factor 8
sub_sampled_lenna = subsample(lenna, 8)
sub_sampled_lenna.save(f"{save_file_path}sub_sampled_lenna_8.gif")

sub_sampled_peppers = subsample(peppers, 8)
sub_sampled_peppers.save(f"{save_file_path}sub_sampled_peppers_8.gif")

