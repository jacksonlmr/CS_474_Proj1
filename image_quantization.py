from PIL import Image
from IPython.display import display
from math import ceil

lenna = Image.open("Input_Images/lenna.gif").convert('L')
peppers = Image.open("Input_Images/peppers.gif").convert('L')
save_file_path = "Output_Images/Quantization/"

def quantize(input_img: Image, gray_levels: int):
    width, height = input_img.size

    output_img = Image.new(size=input_img.size, mode='L')

    slope =  (gray_levels)/256

    for row in range(width):
        for col in range(height):
            input_pixel = input_img.getpixel((row, col))
            output_pixel = int(slope*input_pixel) * 1/slope
            output_img.putpixel((row, col), int(output_pixel))
    
    return output_img

# gray level 2
quantized_lenna = quantize(lenna, 2)
quantized_lenna.save(f"{save_file_path}quantized_lenna_2.gif")

quantized_peppers = quantize(peppers, 2)
quantized_peppers.save(f"{save_file_path}quantized_peppers_2.gif")

# gray level 8
quantized_lenna = quantize(lenna, 8)
quantized_lenna.save(f"{save_file_path}quantized_lenna_8.gif")

quantized_peppers = quantize(peppers, 8)
quantized_peppers.save(f"{save_file_path}quantized_peppers_8.gif")

# gray level 32
quantized_lenna = quantize(lenna, 32)
quantized_lenna.save(f"{save_file_path}quantized_lenna_32.gif")

quantized_peppers = quantize(peppers, 32)
quantized_peppers.save(f"{save_file_path}quantized_peppers_32.gif")

# gray level 128
quantized_lenna = quantize(lenna, 128)
quantized_lenna.save(f"{save_file_path}quantized_lenna_128.gif")

quantized_peppers = quantize(peppers, 128)
quantized_peppers.save(f"{save_file_path}quantized_peppers_128.gif")