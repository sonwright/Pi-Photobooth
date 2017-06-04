# Adapted from some original code by bennuttall and waveform80
# ------------------------------------------------------------- 
 
from PIL import Image
from PIL import ImageOps
from itertools import cycle

# EDIT THESE VALUES ------------------------
overlays_dir = "/home/pi/Pi-Photobooth/overlays"
overlays = ['bald_head','bunny1','bunny2','dog','monster','unicorn','mouth','ears','dog_face','eyes','girl', 'cowboy', 'top', 'pink', 'glassesnose', 'wings', 'moustache', 'angel','sunglasses', 'elvis', 'emo', 'blackhat_sm', 'emo2', 'baseball_sm', 'flowers', 'santa_sm', 'alps_sm', 'mop', 'glasses',""]
# ------------------------------------------

overlay = overlays[0] # Starting value

def _get_overlay_image(overlay):
    
    # Open the overlay as an Image object
    return Image.open(overlays_dir + "/" + overlay + ".png")

def _pad(resolution, width=32, height=16):
    # Pads the specified resolution
    # up to the nearest multiple of *width* and *height*; this is
    # needed because overlays require padding to the camera's
    # block size (32x16)
    return (
        ((resolution[0] + (width - 1)) // width) * width,
        ((resolution[1] + (height - 1)) // height) * height,
    )

def remove_overlays(camera):
    
    # Remove all overlays from the camera preview
    for o in camera.overlays:
        camera.remove_overlay(o) 


def preview_overlay(camera=None, overlay=None):

    # Remove all overlays
    remove_overlays(camera)

    # Get an Image object of the chosen overlay
    overlay_img = _get_overlay_image(overlay)

    # Pad it to the right resolution
    pad = Image.new('RGB', _pad(camera.resolution))
    pad.paste(overlay_img, (0, 0),overlay_img)

    # Add the overlay
    camera.add_overlay(pad.tobytes(),alpha=150, layer=3)

def output_overlay(output=None, overlay=None):

    
	# Take an overlay Image
    overlay_img = _get_overlay_image(overlay)
    background = Image.open(output)
    # ...and a captured photo
    #output_img = Image.open(output).convert('RGBA')
    overlay_img = ImageOps.mirror(overlay_img)
    # Combine the two and save the image as output
    background.paste(overlay_img,(0,0),overlay_img)
    background.save(output)


def output_no_overlay(output=None):
    background = Image.open(output)
    background.save(output)

all_overlays = cycle(overlays)
