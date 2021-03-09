from PIL import Image
import os
from statistics import mode
import webbrowser

file = 'wavy'
os.chdir(r"C:\Folder\where\Gif\is\located")

num_key_frames = 60

with Image.open(file+'.gif') as im:
    if im.n_frames < num_key_frames:
        num_key_frames = im.n_frames
    for i in range(num_key_frames):
        im.seek(im.n_frames // num_key_frames * i)
        im.save('{}.png'.format(i))

#Height of your neopixel display
width = 16
height = 16

#Crops from the center of the gif
zoom = 500//2
(left,upper,right,lower) = (int(im.width//2-zoom),int( im.height-zoom),int( im.width//2+zoom),int( im.height))


print("\n** Analysing image **\n")

# Display image format, size, colour mode
print("Format:", im.format, "\nWidth:", im.width, "\nHeight:", im.height, "\nMode:", im.mode)


# Check if GIF is animated

print("Number of frames: " + str(im.n_frames))

# Iterate through frames and pixels, top row first

listA = []
#Finds the pixel color that could be background of a gif and remove it
with Image.open('0.png') as img:
    rgb_img= img.convert('RGB')
    for y in range(img.height):
        for x in range(img.width): 
            data = rgb_img.getpixel((x, y))
            listA.append(data)

remove = mode(listA)
print("Pixel removed:", remove)

# Opens Arduino File
os.chdir(r"C:\Users\Jacob\Desktop\Projects\Gifmaker\code")
with open("Intro.txt") as f:
    with open("code.ino", "w") as f1:
        for line in f:
            f1.write(line) 
f = open('code.ino','a')
for z in range(0,num_key_frames):

    # Go to frame
    os.chdir(r"C:\Users\Jacob\Desktop\Projects\Gifmaker")
    im = Image.open(str(z)+'.png')
    #im = im.crop((left,upper,right,lower)) #(left, upper, right, lower) origin is at top left corner
    im = im.resize((width,height))
    im = im.rotate(270)
    rgb_im = im.convert('RGB')
    os.chdir(r"C:\Users\Jacob\Desktop\Projects\Gifmaker\code")
    for y in range(width):
        for x in range(height):
            
            # Get RGB values of each pixel
            data = rgb_im.getpixel((x, y))
            # Builds code in a txt file for Neopixel display
            
            if y == 0 and x == 0:
               f.write('\nif(currentMillis - previousMillis >= fps && frame == %d) {\n' % z)
               f.write('   previousMillis = currentMillis;\n')
              
            if y == width-1 and x == height-1 and z != num_key_frames-1:
                f.write('   FastLED.show();\n   frame = frame+1;\n  clearLEDs();\n}\n ')
               
            elif y == width-1 and x == height-1 and z == num_key_frames-1:
                f.write('   leds[%d][%d] = ' % (y,x))
                f.write('   CRGB(%s,%s,%s);\n' % data)
                f.write('   FastLED.show();\n   frame = 0;\n    clearLEDs();\n}\n ')
                f.write('}\nvoid clearLEDs(){\nfor(int j = 0; j < 16; j++){\nfor(int k = 0; k < 16; k++){\nleds[j][k] = CRGB(0,0,0); \n }}}')
                
           
            if data ==(0,0,0) or z == num_key_frames-1:
                continue
            f.write('   leds[%d][%d] = ' % (y,x))
            f.write('   CRGB(%s,%s,%s);\n' % data)
os.chdir(r"C:\Users\Jacob\Desktop\Projects\Gifmaker")
f1 = open(path+'1.txt','w')
for z in range(0,num_key_frames):

    # Go to frame
    os.chdir(r"C:\Users\Jacob\Desktop\Projects\Gifmaker")
    im = Image.open(str(z)+'.png')
    #im = im.crop((left,upper,right,lower)) #(left, upper, right, lower) origin is at top left corner
    im = im.resize((width,height))
    im = im.rotate(270)
    rgb_im = im.convert('RGB')
    for y in range(width):
        for x in range(height):
            
            # Get RGB values of each pixel
            data = rgb_im.getpixel((x, y))
            # Builds code in a txt file for Neopixel display
            
            if y == 0 and x == 0:
               f1.write('\nif(currentMillis - previousMillis >= fps && frame == %d) {\n' % z)
               f1.write('   previousMillis = currentMillis;\n')
              
            if y == width-1 and x == height-1 and z != num_key_frames-1:
                f1.write('   FastLED.show();\n   frame = frame+1;\n  clearLEDs();\n}\n ')
               
            elif y == width-1 and x == height-1 and z == num_key_frames-1:
                f1.write('   FastLED.show();\n   frame = 0;\n    clearLEDs();\n}\n ')
                f1.write('}\nvoid clearLEDs(){\nfor(int j = 0; j < 16; j++){\nfor(int k = 0; k < 16; k++){\nleds[j][k] = CRGB(0,0,0); \n }}}')
                
           
            if data ==(0,0,0) or data == remove:
                continue
            f1.write('   leds[%d][%d] = ' % (y,x))
            f1.write('   CRGB(%s,%s,%s);\n' % data)
os.chdir(r"C:\Users\Jacob\Desktop\Projects\Gifmaker\code")
webbrowser.open('code.ino')



