# Python default libraries:
import zipfile
import shutil
import os
import glob
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image

# Libraries that need installation:
import matplotlib.pyplot as plt

# This application converts an RS274X gerber zip created in Labcenter Electronics Proteus
# into a G-Code to a paste dispenser modified 3D printer
# We need 3 files: The top paste file, the bottom paste file and the READ-ME file
# > The top and bottom paste file contains (among other things) the center points (x,y) for the pads
# > The READ-ME file contains information of the pads and its size, we will use it to calculate
#   the area of the pad and use it to calculate the quantity of paste we will need to drop

# Define the folder to extract the ZIP file, usually nobody needs to change these values:
extract_path = "gerber_contents"
picture_paste_bottom = "paste_bottom.png"
picture_paste_top = "paste_top.png"
gcode_bottom_filename = "bottom_layer.gcode"
gcode_top_filename = "top_layer.gcode"

# ============================================
# ========== FUNCTIONS DEFINED HERE ==========
# ============================================


# Converts thousand of inches (x10) to milliliters (the gerber file shows values in th*10 to avoid commas)
# The th (UK) are also known as mils (US)
def convert_th10_to_mm(_th10_inches):
    # The correct formula is to divide with: 0.0393701 * 1000 (as we use th) * 10 (as the gerber uses th*10)
    return int(_th10_inches)/394


# Converts thousand of inches to milliliters
# The th (UK) are also known as mils (US)
def convert_th_to_mm(_th_inches):
    # The correct formula is to divide with: 0.0393701 * 1000 (as we use th)
    return int(_th_inches)/39.4


# Gets the pad area in mm2, based on the pad type (D15, D27, etc)
# This function will read the READ-ME gerber file and look for the pad type, extract the dimensions and calculate
# the areas. The area calculation is made for RECT, CIRCLE and SQUARE
# > By default the pads appear as FLASH, meaning they will just appear once in one place
# > The type DRAW means that the object (CIRCLE, etc) is drawn from one point to the next one
#   (for example to make a tick line), this is not relevant for our tool.
# Usually the board edge appears as a CIRCLE-DRAW, but we usually know the board type is D70 (default), so we don't care
# about thickness.
def get_pad_area(_gerber_readme_filename, _pad_type):
    _pad_area = 0
    if _gerber_readme_filename:
        # Read the gerber file:
        with open(_gerber_readme_filename) as _f:
            _file_contents = _f.read().splitlines()

        # Process the file line by line:
        for _line_number in range(len(_file_contents)):
            # Get the line content:
            _line_content = _file_contents[_line_number]

            # Search for the line with the correct pad type (ex: D16):
            if _line_content.find(_pad_type) == 0:
                # If we have a rectangle:
                if _line_content.find("RECT") > 0:
                    # Get the location of W and th, as in W=10th
                    _W_location = _line_content.find("W", _line_content.find("RECT") + len("RECT"))
                    _th_location = _line_content.find("th", _W_location)
                    # Get the dimension by grabbing part of the string starting at W+2 (to exclude the W and the = sign)
                    _pad_width = _line_content[(_W_location + 2):_th_location]

                    # Get the location of H and th, as in H=10th
                    _H_location = _line_content.find("H", _line_content.find("RECT") + len("RECT"))
                    _th_location = _line_content.find("th", _H_location)
                    # Get the dimension by grabbing part of the string starting at H+2 (to exclude the H and the = sign)
                    _pad_height = _line_content[(_H_location + 2):_th_location]

                    # Calculate the pad area in mm2:
                    # Formula is: A=W*H
                    _pad_area = convert_th_to_mm(_pad_width) * convert_th_to_mm(_pad_height)

                # If we have a square:
                if _line_content.find("SQUARE") > 0:
                    # Get the location of S and th, as in S=10th
                    _S_location = _line_content.find("S", _line_content.find("SQUARE") + len("SQUARE"))
                    _th_location = _line_content.find("th", _S_location)
                    # Get the dimension by grabbing part of the string starting at S+2 (to exclude the S and the = sign)
                    _pad_side = _line_content[(_S_location + 2):_th_location]

                    # Calculate the pad area in mm2:
                    # Formula is: A=S^2
                    _pad_area = convert_th_to_mm(_pad_side) * convert_th_to_mm(_pad_side)

                # If we have a circle:
                if _line_content.find("CIRCLE") > 0:
                    # Get the location of D and th, as in D=10th, start after the word CIRCLE (start + length):
                    _D_location = _line_content.find("D", _line_content.find("CIRCLE") + len("CIRCLE"))
                    _th_location = _line_content.find("th", _D_location)
                    # Get the dimension by grabbing part of the string starting at D+2 (to exclude the D and the = sign)
                    _pad_diameter = _line_content[(_D_location + 2):_th_location]

                    # Calculate the pad area in mm2:
                    # Formula is: A=D^2 * (pi/4)
                    _pad_area = convert_th_to_mm(_pad_diameter) * convert_th_to_mm(_pad_diameter) * 0.7854
    return _pad_area


# Saves an image (graph) which will include the board limits, then the top and the bottom layer paste points
# The size of the points will relate directly to their real area/size, in order to keep a better viewing accuracy
# you can change the area_scale_multiplier below, which will scale the size of the points.
def generate_images(_top_board_edge_pairs, _bottom_board_edge_pairs, _top_layer_pairs, _bottom_layer_pairs):
    area_scale_multiplier = 30

    # Configure the graph space and axis:
    plt.figure(figsize=(5, 5))
    ax1 = plt.axes(frameon=False)
    ax1.set_frame_on(False)
    ax1.axes.get_xaxis().set_visible(False)
    ax1.axes.get_yaxis().set_visible(False)
    ax1.set_aspect('equal', 'datalim')

    # Get the X and Y coordinates for the board edges, then later draw them with a line:
    # We need the *_inv value because the bottom layer is inverted on the horizontal axis:
    _top_board_edge_pairs_x = [value[0] for value in _top_board_edge_pairs]
    _top_board_edge_pairs_y = [value[1] for value in _top_board_edge_pairs]
    _botton_board_edge_pairs_x = [value[0] for value in _bottom_board_edge_pairs]
    _botton_board_edge_pairs_y = [value[1] for value in _bottom_board_edge_pairs]

    # Get the X and Y coordinates and the area for each pad, then later draw points with the appropriate size:
    # We need the *_inv value because the bottom layer is inverted on the horizontal axis:
    _bottom_layer_pairs_x = [value[0] for value in _bottom_layer_pairs]
    _bottom_layer_pairs_y = [value[1] for value in _bottom_layer_pairs]
    _bottom_layer_pairs_area = [value[3]*area_scale_multiplier for value in _bottom_layer_pairs]

    # Get the X and Y coordinates and the area for each pad, then later draw points with the appropriate size:
    _top_layer_pairs_x = [value[0] for value in _top_layer_pairs]
    _top_layer_pairs_y = [value[1] for value in _top_layer_pairs]
    _top_layer_pairs_area = [value[3] * area_scale_multiplier for value in _top_layer_pairs]

    # Save the picture only with bottom points, then clean the graph:
    plt.title('Bottom solder paste locations')
    plt.plot(_botton_board_edge_pairs_x, _botton_board_edge_pairs_y, marker='', color='green')
    plt.scatter(_bottom_layer_pairs_x, _bottom_layer_pairs_y, marker='s', s=_bottom_layer_pairs_area, color='gray')
    plt.savefig(picture_paste_bottom, bbox_inches='tight')
    plt.cla()

    # Save the picture only with top points, then clean the graph:
    plt.title('Top solder paste locations')
    plt.plot(_top_board_edge_pairs_x, _top_board_edge_pairs_y, marker='', color='green')
    plt.scatter(_top_layer_pairs_x, _top_layer_pairs_y, marker='s', s=_top_layer_pairs_area, color='gray')
    plt.savefig(picture_paste_top, bbox_inches='tight')
    plt.cla()
    return


# This function is used to display an image. It will open the default picture viewer on the computer
def display_image(_filename):
    img = Image.open(_filename)
    img.show()


# This function looks for the minimum X and Y coordinates of the board, calculates the offset to 0,0
# and moves the whole coordinates setting the board origin at 0,0
def correct_layer_coordinates(_board_edge_pairs, _pad_layer_pairs, invert_x_axis=False):
    if invert_x_axis:
        multiplier = -1
    else:
        multiplier = 1

    _board_edge_pairs_x = [value[0]*multiplier for value in _board_edge_pairs]
    _board_edge_pairs_y = [value[1] for value in _board_edge_pairs]

    _min_x = min(_board_edge_pairs_x)
    _min_y = min(_board_edge_pairs_y)

    _new_board_edge_pairs = []
    _new_pad_layer_pairs = []

    for pair in _board_edge_pairs:
        _new_board_edge_pairs.append(((pair[0]*multiplier)-_min_x, pair[1]-_min_y))

    for pair in _pad_layer_pairs:
        _new_pad_layer_pairs.append(((pair[0]*multiplier)-_min_x, pair[1]-_min_y, pair[2], pair[3]))

    return _new_board_edge_pairs, _new_pad_layer_pairs


def generate_gcode(_edge_pairs, _pad_pairs, _filename):
    # Offset values in mm:
    offset_x = 50
    offset_y = 50
    offset_z = 1
    offset_z_travel = 3

    gcode_file = open(_filename, "w")

    gcode_file.write("; Generated by gerber2gcode" + '\n')
    gcode_file.write("; Coded by: vascojdb@gmail.com, magdalena.wiktoria.szczypka@gmail.com" + '\n')
    gcode_file.write("" + '\n')
    gcode_file.write("M107 ; fan off" + '\n')
    gcode_file.write("M117 Preparing ; display message" + '\n')
    gcode_file.write("G90 ; absolute positioning" + '\n')
    gcode_file.write("G21 ; set units to millimeters" + '\n')
    gcode_file.write("G28 ; auto home" + '\n')
    gcode_file.write("G1 Z10 F5000 ; lift nozzle" + '\n')
    gcode_file.write("G1 F5000 ; set movement speed" + '\n')
    gcode_file.write("M75 ; start print job timer" + '\n')
    gcode_file.write("M73 P0 ; set print progress" + '\n')

    gcode_file.write("" + '\n')
    gcode_file.write("M117 Aligning ; display message" + '\n')
    for pair in _edge_pairs:
        pos_x = float(pair[0]) + offset_x
        pos_y = float(pair[1]) + offset_y
        gcode_file.write("G1 X" + str("%.3f" % pos_x) + " Y" + str("%.3f" % pos_y) + '\n')
        gcode_file.write("G1 Z" + str("%.3f" % offset_z) + " F5000" + '\n')
        gcode_file.write("G1 Z" + str("%.3f" % offset_z_travel) + " F5000" + '\n')

    gcode_file.write("" + '\n')
    gcode_file.write("M117 Printing ; display message" + '\n')
    for pair in _pad_pairs:
        pos_x = float(pair[0]) + offset_x
        pos_y = float(pair[1]) + offset_y
        gcode_file.write("G1 X" + str("%.3f" % pos_x) + " Y" + str("%.3f" % pos_y) + '\n')
        gcode_file.write("G1 Z" + str("%.3f" % offset_z) + " F5000" + '\n')
        # Add gcode here to push solder paste
        gcode_file.write("G1 Z" + str("%.3f" % offset_z_travel) + " F5000" + '\n')

    gcode_file.write("" + '\n')
    gcode_file.write("G1 X0 F10000 ; move X to position 0" + '\n')
    gcode_file.write("G1 Y150 F10000 ; move bed to the front" + '\n')
    gcode_file.write("M84 ; turn steppers off" + '\n')
    gcode_file.write("M73 P100 ; set print progress" + '\n')
    gcode_file.write("M77 ; stop print job timer" + '\n')
    gcode_file.write("M117 Finished ; display message" + '\n')
    gcode_file.write("M300 S900 P1000; Play beep" + '\n')

    gcode_file.close()
    return

# ===========================================
# ========== MAIN CODE STARTS HERE ==========
# ===========================================

# Create the window manager and hide it as we don't need a main window:
root = tk.Tk()
root.withdraw()

# Check if a previous folder already exists, if yes, just deletes it (and its contents):
try:
    if os.path.isdir(extract_path):
        shutil.rmtree(extract_path)
# Catch the exception thrown by rmtree in case the folder is in use by the user, display an error and exit:
except PermissionError:
    messagebox.showerror("Directory in use",
                         "Impossible to clean the environment as the directory " + extract_path + " is in use.\n"
                         "Close all files you may have open on this directory and try again!")
    exit(-1)

# Open the file dialog to open the gerber ZIP file:
zip_path = filedialog.askopenfilename(title="Select gerber ZIP file",
                                      filetypes=[("Gerber ZIP file", "*.ZIP")])

# If the user did not select any ZIP file (pressed the Cancel or the X button to close the dialog), then exit:
if not zip_path:
    messagebox.showinfo("No file selected",
                        "Nothing to process.\nGoodbye!")
    exit(0)

# Open zip file, then extract contents and close it (mandatory):
zip_ref = zipfile.ZipFile(zip_path, 'r')
zip_ref.extractall(extract_path)
zip_ref.close()
# We don't need the ZIP file anymore after this point.

# Search here for the needed file names:
# Start with empty filenames:
gerber_top_paste_filename = None
gerber_bottom_paste_filename = None
gerber_readme_filename = None

# Change directory to get inside the extracted folder:
os.chdir(extract_path)

# Look for each file real name (as in includes also the project name)
for gerber_top_paste_filename in glob.glob("*Top SMT Paste Mask*"):
    print("Found file for top SMD mask: " + gerber_top_paste_filename)
for gerber_bottom_paste_filename in glob.glob("*Bottom SMT Paste Mask*"):
    print("Found file for bottom SMD mask: " + gerber_bottom_paste_filename)
for gerber_readme_filename in glob.glob("*READ-ME*"):
    print("Found file with pad information: " + gerber_readme_filename)

# Display message boxes in case files are missing:
# If we can't find the 3 needed files, then probably this is not a correct zip file, display error and exit.
if not gerber_top_paste_filename and not gerber_bottom_paste_filename and gerber_readme_filename:
    messagebox.showerror("Unrecognized gerber ZIP file",
                         "The selected ZIP file is not a valida gerber package\nCan't continue!")
    exit(-1)
# If we cant find the top paste file, then we ask if we want to proceed or not (we may only need the bottom layer)
if not gerber_top_paste_filename:
    if not messagebox.askyesno("Missing top layer file",
                               "No gerber file found for the top layer\nContinue?"):
        exit(0)
# If we cant find the bottom paste file, then we ask if we want to proceed or not (we may only need the top layer)
if not gerber_bottom_paste_filename:
    # But before anything, if we don't have bottom layer but we also don't have top layer, we cant do anything, so exit:
    if not gerber_top_paste_filename:
        messagebox.showerror("Missing top and bottom layer file",
                             "No gerber file found for any later\nCan't continue!")
        exit(-1)
    if not messagebox.askyesno("Missing bottom layer file",
                               "No gerber file found for the bottom layer\nContinue?"):
        exit(0)
if not gerber_readme_filename:
    messagebox.showerror("Missing pad information file",
                         "No gerber file found for the pad size information\nCan't continue!")
    exit(0)

# Initiate variables that will be needed later:
pad_type = None
top_layer_pairs = []
top_board_edge_pairs = []
bottom_layer_pairs = []
bottom_board_edge_pairs = []
bottom_layer_pairs_inv = []
bottom_board_edge_pairs_inv = []

# Do this task if we have a top layer:
if gerber_top_paste_filename:
    # Read the top layer gerber file:
    with open(gerber_top_paste_filename) as f:
        file_contents = f.read().splitlines()

    # Process the file line by line:
    for line_number in range(len(file_contents)):
        # Get the line content:
        line_content = file_contents[line_number]

        # Search for the command to start the coordinates of a specific pad size (ex: G54D07*):
        if line_content.find("G54") == 0:
            # Get the Dxx part of the string (which starts after G54, so position 3) (ex: D07*):
            pad_type = line_content[3:]
            # Remove the '*' in the end of the line (ex: D07) to get the pad type:
            pad_type = pad_type.replace('*', '')
            # Get the pad area:
            pad_area = get_pad_area(gerber_readme_filename, pad_type)
            #print("Pad type: " + pad_type + " (area: " + str(pad_area) + ")")

        # Search for coordinates (ex: X+8715Y-3543D03*), the line always starts with an X:
        if line_content.find("X") == 0:
            # Get the location on the line where the X and Y part are located
            X_location = line_content.find("X")
            Y_location = line_content.find("Y")
            D_location = line_content.find("D")

            # Extract the X coordinate which is located between X+1 (+1 to ignore the letter X) and Y location
            X_coordinate_th10 = line_content[(X_location + 1):Y_location]
            Y_coordinate_th10 = line_content[(Y_location + 1):D_location]

            # Coordinates are in thousands on an inch, we need them in milliliters:
            X_coordinate_mm = convert_th10_to_mm(X_coordinate_th10)
            Y_coordinate_mm = convert_th10_to_mm(Y_coordinate_th10)

            # The D70 type always refers to the board edges for Proteus:
            if pad_type == "D70":
                top_board_edge_pairs.append((X_coordinate_mm, Y_coordinate_mm))
            else:
                top_layer_pairs.append((X_coordinate_mm, Y_coordinate_mm, pad_type, pad_area))

# Do this task if we have a bottom layer:
if gerber_bottom_paste_filename:
    # Read the bottom layer gerber file:
    with open(gerber_bottom_paste_filename) as f:
        file_contents = f.read().splitlines()

    # Process the file line by line:
    for line_number in range(len(file_contents)):
        # Get the line content:
        line_content = file_contents[line_number]

        # Search for the command to start the coordinates of a specific pad size (ex: G54D07*):
        if line_content.find("G54") == 0:
            # Get the Dxx part of the string (which starts after G54, so position 3) (ex: D07*):
            pad_type = line_content[3:]
            # Remove the '*' in the end of the line (ex: D07) to get the pad type:
            pad_type = pad_type.replace('*', '')
            # Get the pad area:
            pad_area = get_pad_area(gerber_readme_filename, pad_type)
            #print("Pad type: " + pad_type + " (area: " + str(pad_area) + ")")

        # Search for coordinates (ex: X+8715Y-3543D03*), the line always starts with an X:
        if line_content.find("X") == 0:
            # Get the location on the line where the X and Y part are located
            X_location = line_content.find("X")
            Y_location = line_content.find("Y")
            D_location = line_content.find("D")

            # Extract the X coordinate which is located between X+1 (+1 to ignore the letter X) and Y location
            X_coordinate_th10 = line_content[(X_location + 1):Y_location]
            Y_coordinate_th10 = line_content[(Y_location + 1):D_location]

            # Coordinates are in thousands on an inch, we need them in milliliters:
            X_coordinate_mm = convert_th10_to_mm(X_coordinate_th10)
            Y_coordinate_mm = convert_th10_to_mm(Y_coordinate_th10)

            # The D70 type always refers to the board edges for Proteus:
            if pad_type == "D70":
                bottom_board_edge_pairs.append((X_coordinate_mm, Y_coordinate_mm))
            else:
                bottom_layer_pairs.append((X_coordinate_mm, Y_coordinate_mm, pad_type, pad_area))


# We need to offset and correct the coordinates and mirror the bottom layer,
# as usually the board is far away from 0,0 and the bottom layer is not inverted.
if gerber_top_paste_filename:
    top_board_edge_pairs, top_layer_pairs = correct_layer_coordinates(top_board_edge_pairs,
                                                                      top_layer_pairs,
                                                                      False)
if gerber_bottom_paste_filename:
    bottom_board_edge_pairs_inv, bottom_layer_pairs_inv = correct_layer_coordinates(bottom_board_edge_pairs,
                                                                                    bottom_layer_pairs,
                                                                                    True)

#print("Board edges:")
#print(top_board_edge_pairs)
#print(bottom_board_edge_pairs_inv)
#print("Top layer pads:")
#print(top_layer_pairs)
#print("Bottom layer pads:")
#print(bottom_layer_pairs_inv)

# Generate the images/graphs with the pad locations, and then display the result:
generate_images(top_board_edge_pairs, bottom_board_edge_pairs_inv, top_layer_pairs, bottom_layer_pairs_inv)

# Display generated images:
display_image(picture_paste_top)
display_image(picture_paste_bottom)

# Ask here if we want to do something with the top layer:
if gerber_top_paste_filename:
    if messagebox.askyesno("Top layer solder paste G-Code generation",
                           "Do you want to generate a G-Code print file for the top solder paste layer?"):
        generate_gcode(top_board_edge_pairs, top_layer_pairs, gcode_top_filename)

# Ask here if we want to do something with the bottom layer:
if gerber_bottom_paste_filename:
    if messagebox.askyesno("Bottom layer solder paste G-Code generation",
                           "Do you want to generate a G-Code print file for the bottom solder paste layer?"):
        generate_gcode(bottom_board_edge_pairs_inv, bottom_layer_pairs_inv, gcode_bottom_filename)

print("END")
