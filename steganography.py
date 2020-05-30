from PIL import Image

class stegano_img(object):

    @staticmethod
    def int_to_bin(rgb):
        r,g,b = rgb
        return ('{0:08b}'.format(r),
                '{0:08b}'.format(g),
                '{0:08b}'.format(b))

    @staticmethod
    def bin_to_int(rgb):
        r, g, b = rgb
        return (int(r, 2),
                int(g, 2),
                int(b, 2))

    @staticmethod
    def merge_rgb(rgb1, rgb2):
        r1, g1, b1 = rgb1
        r2, g2, b2 = rgb2
        rgb = (r1[:4] + r2[:2] + r2[7] + r2[2],
               g1[:4] + g2[:2] + g2[7] + g2[2],
               b1[:4] + b2[:2] + b2[7] + b2[2])
        return rgb

    @staticmethod
    def merge(img1, img2):
        # Check the images dimensions
        if img2.size[0] > img1.size[0] or img2.size[1] > img1.size[1]:
            raise ValueError('Image 2 should not be larger than Image 1!')

        # Get the pixel map of the two images
        pixel_map1 = img1.load()
        pixel_map2 = img2.load()

        # Create a new image that will be outputted
        new_image = Image.new(img1.mode, img1.size)
        pixels_new = new_image.load()

        for i in range(img1.size[0]):
            for j in range(img1.size[1]):
                rgb1 = stegano_img.int_to_bin(pixel_map1[i, j])

                # Use a black pixel as default
                rgb2 = stegano_img.int_to_bin((0, 0, 0))

                # Check if the pixel map position is valid for the second image
                if i < img2.size[0] and j < img2.size[1]:
                    rgb2 = stegano_img.int_to_bin(pixel_map2[i, j])

                # Merge the two pixels and convert it to a integer tuple
                rgb = stegano_img.merge_rgb(rgb1, rgb2)

                pixels_new[i, j] = stegano_img.bin_to_int(rgb)

        return new_image

    @staticmethod
    def unmerge(img):
        # Load the pixel map
        pixel_map = img.load()

        # Create the new image and load the pixel map
        new_image = Image.new(img.mode, img.size)
        pixels_new = new_image.load()

        # Tuple used to store the image original size
        original_size = img.size

        for i in range(img.size[0]):
            for j in range(img.size[1]):
                # Get the RGB (as a string tuple) from the current pixel
                r, g, b = stegano_img.int_to_bin(pixel_map[i, j])

                # Exracting information regarding the hidden image
                rgb = (r[4:6] + r[7] + '0000' + r[6],
                       g[4:6] + g[7] + '0000' + g[6],
                       b[4:6] + b[7] + '0000' + b[6])

                # Convert it to an integer tuple
                pixels_new[i, j] = stegano_img.bin_to_int(rgb)

                # If this is a valid position, store it as the last valid position
                if pixels_new[i, j] != (0, 0, 0):
                    original_size = (i + 1, j + 1)

        # Crop the image based on the valid pixels
        new_image = new_image.crop((0, 0, original_size[0], original_size[1]))

        return new_image

class stegano_txt(object):
    # Convert encoding data into 8-bit binary form using ASCII value of characters 
    @staticmethod
    def genData(data): 
              
            # list of binary codes of given data 
            newd = []  
              
            for i in data: 
                newd.append(format(ord(i), '08b')) 
            return newd 
              
    # Pixels are modified according to the 8-bit binary data and finally returned 
    @staticmethod
    def modPix(pix, data): 
          
        datalist = stegano_txt.genData(data) 
        lendata = len(datalist) 
        imdata = iter(pix) 
      
        for i in range(lendata): 
              
            # Extracting 3 pixels at a time 
            pix = [value for value in imdata.__next__()[:3] +
                                      imdata.__next__()[:3] +
                                      imdata.__next__()[:3]] 
                                          
            # Pixel value should be made odd for 1 and even for 0 
            for j in range(0, 8): 
                if (datalist[i][j]=='0') and (pix[j]% 2 != 0): 
                      
                    if (pix[j]% 2 != 0): 
                        pix[j] -= 1
                          
                elif (datalist[i][j] == '1') and (pix[j] % 2 == 0): 
                    pix[j] -= 1
                      
            # Eighth pixel of every set tells whether to stop or to read further. 
            # 0 means keep reading; 1 means the message is over. 
            if (i == lendata - 1): 
                if (pix[-1] % 2 == 0): 
                    pix[-1] -= 1
            else: 
                if (pix[-1] % 2 != 0): 
                    pix[-1] -= 1
      
            pix = tuple(pix) 
            yield pix[0:3] 
            yield pix[3:6] 
            yield pix[6:9] 
      
    @staticmethod
    def encode_enc(newimg, data): 
        w = newimg.size[0] 
        (x, y) = (0, 0) 
          
        for pixel in stegano_txt.modPix(newimg.getdata(), data): 
              
            # Putting modified pixels in the new image 
            newimg.putpixel((x, y), pixel) 
            if (x == w - 1): 
                x = 0
                y += 1
            else: 
                x += 1
                  
     
    @staticmethod
    def encode(): 
        img = input("Enter image name(with extension): ") 
        image = Image.open(img, 'r') 
          
        data = input("Enter data to be encoded : ") 
        if (len(data) == 0): 
            raise ValueError('Data is empty') 
              
        newimg = image.copy() 
        stegano_txt.encode_enc(newimg, data) 
          
        new_img_name = input("Enter the name of new image(with extension): ") 
        newimg.save(new_img_name, str(new_img_name.split(".")[1].upper())) 

    @staticmethod
    def decode(): 
        img = input("Enter image name(with extension) :") 
        image = Image.open(img, 'r') 
          
        data = '' 
        imgdata = iter(image.getdata()) 
          
        while (True): 
            pixels = [value for value in imgdata.__next__()[:3] +
                                      imgdata.__next__()[:3] +
                                      imgdata.__next__()[:3]] 
            # string of binary data 
            binstr = '' 

            for i in pixels[:8]: 
                if (i % 2 == 0): 
                    binstr += '0'
                else: 
                    binstr += '1'
                      
            data += chr(int(binstr, 2)) 
            if (pixels[-1] % 2 != 0): 
                return data 
                
def txt_img(): 
    a = int(input("Choose the operations to be performed :\n"
                        "1. Encode the Text into Image\n2. Decode the Text from Image \n")) 
    if (a == 1): 
        stegano_txt.encode() 
          
    elif (a == 2): 
        print("Decoded Data- " + stegano_txt.decode()) 
    else: 
        raise Exception("Enter correct input") 

def img_img(): 
    a = int(input("Choose the operations to be performed :\n"
                        "1. Merge the two Images\n2. Unmerge the Images\n")) 
    if (a == 1):
        img1 = input("Enter larger Image in which smaller Image is to be hidden (with extension): ")
        img2 = input("Enter the Image in which data has been encoded (with extension): ")
        output = input("Enter the name for final Image (with extension): ")
        merged_image = stegano_img.merge(Image.open(img1), Image.open(img2))
        merged_image.save(output)
         
    elif (a == 2): 
        img = input("Enter Image that needs to be decoded (with extension): ")
        output = input("Enter the name for decoded Image (with extension): ")
        unmerged_image = stegano_img.unmerge(Image.open(img))
        unmerged_image.save(output)
    else: 
        raise Exception("Enter correct input") 

def main():
    b = int(input("Welcome to Steganography\n"
                    "Choose the combination on which the operation is to be performed: \n"
                        "1. Text and Image \n2. Image and Image\n"))
    if (b == 1): 
        txt_img() 
          
    elif (b == 2): 
        img_img() 
    else: 
        raise Exception("Enter correct input")  

if __name__ == '__main__' :  
    main()
