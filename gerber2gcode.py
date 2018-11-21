# ============================== gerber2gcode ==============================
# This application converts an RS274X gerber zip created in Labcenter Electronics Proteus
# into a G-Code to a paste dispenser modified 3D printer
# We need 3 files from the zip package: The top paste file, the bottom paste file and the READ-ME file
# > The top and bottom paste file contains (among other things) the center points (x,y) for the pads and the board edge
# > The READ-ME file contains information of the pads and its size, we will use it to calculate
#   the area of the pad and use it to calculate the quantity of paste we will need to extrude

# Import libraries:
import zipfile
import datetime
import shutil
import os
import glob
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
from PIL import Image

# Libraries that need installation via pip in case you do not have them:
import matplotlib.pyplot as plt

# Version:
CURR_VER_MAJ = 0
CURR_VER_MIN = 3

# Usually we don't need to modify these values:
extract_path = "gerber_contents"                # Folder to extract the ZIP file
picture_paste_bottom = "paste_bottom.png"       # Filename for the picture for the bottom paste layer
picture_paste_top = "paste_top.png"             # Filename for the picture for the top paste layer
gcode_bottom_filename = "bottom_layer.gcode"    # Filename for the gcode for the bottom paste layer
gcode_top_filename = "top_layer.gcode"          # Filename for the gcode for the top paste layer


# ==================================================
# ========== FUNCTIONS DEFINED AFTER HERE ==========
# ==================================================


# Converts gerber's thousand of inches (x10) to milliliters
# The gerber file shows values in th multiplied by 10 to avoid commas (decimal numbers) as they are hard to process
# The th (UK) are also known as mils (US)
# > Arguments: str
# > Returns: int
def convert_th10_to_mm(_th10_inches):
    # The correct formula is to divide with: 0.0393701 * 1000 (as we use th) * 10 (as the gerber uses th*10)
    return int(_th10_inches)/394


# Converts thousand of inches to milliliters
# The th (UK) are also known as mils (US)
# > Arguments: str
# > Returns: int
def convert_th_to_mm(_th_inches):
    # The correct formula is to divide with: 0.0393701 * 1000 (as we use th)
    return int(_th_inches)/39.4


# Gets the pad area in mm2 based on the pad ID (D15, D27, etc)
# This function will read the READ-ME gerber file and look for the pad ID, then extract the dimensions and calculate
# the area. The area calculation is calculated according to the type of pad: RECT, CIRCLE and SQUARE
# > By default the pads appear categorized as FLASH, this means the gerber processor knows they are supposed to be
#   dropped on the x,y coordinates only.
# > The type DRAW means that the object (CIRCLE, etc) is drawn from one x,y point to the next x,y one (next line),
#   this type is not relevant for our analysis.
#   For example to make a tick line, we define a circle with the thickness we want and DRAW it from x0,y0 to x1,y1.
#   Usually the board edge appears as a CIRCLE-DRAW, but we know the default board type in Proteus is D70,
#   so we ignore the thickness
# > Arguments: str, str
# > Returns: int, str
def get_pad_area(_gerber_readme_filename, _pad_id):
    _pad_area = 0

    # Check if the gerber file exists:
    if _gerber_readme_filename:
        # Read the gerber file and get its contents:
        with open(_gerber_readme_filename) as _f:
            _file_contents = _f.read().splitlines()

        # Process the file line by line:
        for _line_number in range(len(_file_contents)):
            # Get the line content:
            _line_content = _file_contents[_line_number]

            # Search for the line with the correct given pad ID (ex: D16):
            if _line_content.find(_pad_id) == 0:
                # If we found a rectangle:
                if _line_content.find("RECT") > 0:
                    # Get the index of W and th on the line, but start searching from after the word RECT (ex: W=10th)
                    _W_index = _line_content.find("W", _line_content.find("RECT") + len("RECT"))
                    _th_index = _line_content.find("th", _W_index)
                    # Get the dimension by grabbing part of the string starting at W+2 (to exclude the W and the = sign)
                    _pad_width = _line_content[(_W_index + 2):_th_index]

                    # Get the index of H and th on the line, but start searching from after the word RECT (ex: H=10th)
                    _H_index = _line_content.find("H", _line_content.find("RECT") + len("RECT"))
                    _th_index = _line_content.find("th", _H_index)
                    # Get the dimension by grabbing part of the string starting at H+2 (to exclude the H and the = sign)
                    _pad_height = _line_content[(_H_index + 2):_th_index]

                    # Calculate the pad area in mm2. The formula is: A=W*H:
                    _pad_area = convert_th_to_mm(_pad_width) * convert_th_to_mm(_pad_height)

                # If we found a square:
                if _line_content.find("SQUARE") > 0:
                    # Get the index of S and th on the line, but start searching from after the word RECT (ex: S=10th)
                    _S_index = _line_content.find("S", _line_content.find("SQUARE") + len("SQUARE"))
                    _th_index = _line_content.find("th", _S_index)
                    # Get the dimension by grabbing part of the string starting at S+2 (to exclude the S and the = sign)
                    _pad_side = _line_content[(_S_index + 2):_th_index]

                    # Calculate the pad area in mm2. The formula is: A=S^2:
                    _pad_area = convert_th_to_mm(_pad_side) * convert_th_to_mm(_pad_side)

                # If we found a circle:
                if _line_content.find("CIRCLE") > 0:
                    # Get the index of D and th on the line, but start searching from after the word RECT (ex: D=10th)
                    _D_index = _line_content.find("D", _line_content.find("CIRCLE") + len("CIRCLE"))
                    _th_index = _line_content.find("th", _D_index)
                    # Get the dimension by grabbing part of the string starting at D+2 (to exclude the D and the = sign)
                    _pad_diameter = _line_content[(_D_index + 2):_th_index]

                    # Calculate the pad area in mm2. The formula is: A=D^2 * (pi/4):
                    _pad_area = convert_th_to_mm(_pad_diameter) * convert_th_to_mm(_pad_diameter) * 0.7854
    return _pad_area


# Generates a visual representation (as PNG image) of the board and the pads to be filled with soldering paste.
# The function needs the list of x,y pairs for the board edge, the x,y pad pairs to extract coordinates and area and
# the filename where to save the image to.
# You can change the area_scale_multiplier below, which will scale the size of the points.
# > Arguments: list, list, list, list
# > Returns: -
def generate_images(_board_pairs, _pad_pairs, _picture_paste_filename):
    area_scale_multiplier = 30

    # We will need this variables:
    _board_edge_pairs_x = []
    _board_edge_pairs_y = []
    _pad_pairs_x = []
    _pad_pairs_y = []
    _pad_pairs_area = []

    # Configure the graph space and axis (sets a fixed size, hides all frames and axis and sets an equal axis):
    plt.figure(figsize=(5, 5))
    ax1 = plt.axes(frameon=False)
    ax1.set_frame_on(False)
    ax1.axes.get_xaxis().set_visible(False)
    ax1.axes.get_yaxis().set_visible(False)
    ax1.set_aspect('equal', 'datalim')

    # Get the X and Y coordinates for the board edges, then later draw them with a line:
    for value in _board_pairs:
        _board_edge_pairs_x.append(value[0])
        _board_edge_pairs_y.append(value[1])

    # Get the X and Y coordinates, the area and type for each pad, then later draw points with the appropriate size:
    for value in _pad_pairs:
        _pad_pairs_x.append(value[0])
        _pad_pairs_y.append(value[1])
        _pad_pairs_area.append(value[3] * area_scale_multiplier)

    # Generate the correct title for the image:
    if _picture_paste_filename == picture_paste_bottom:
        plt.title('Bottom paste extruding pads')
    else:
        if _picture_paste_filename == picture_paste_top:
            plt.title('Top paste extruding pads')
        else:
            plt.title('Paste extruding pads')

    # Draw the board edge lines:
    plt.plot(_board_edge_pairs_x, _board_edge_pairs_y, marker='', color='green', linewidth=2)
    # Draw the pads for paste extrusion:
    plt.scatter(_pad_pairs_x, _pad_pairs_y, marker='s', s=_pad_pairs_area, color='gray')
    # Create a path line which the paste extruder will follow:
    plt.plot(_pad_pairs_x, _pad_pairs_y, marker='.', color='blue', linewidth=0.5, markersize=3, linestyle='dashed')
    # Save the image (with a tight border):
    plt.savefig(_picture_paste_filename, bbox_inches='tight')
    return


# Displays an image on the default image viewer of the computer
# > Arguments: str
# > Returns: -
def display_image(_filename):
    # Check if the image file exists:
    if _filename:
        img = Image.open(_filename)
        img.show()
    return


# Given the location of the board in space, this function calculates the needed translation (offset) to be applied
# to all coordinates so the bottom left corner of the board is always located at 0,0.
# The x axis may be inverted on the bottom layer by setting mirror_x_axis to True, as the gerber applies no mirroring
# to the saved files. This is needed so you can flip the board and extrude solder paste correctly
# > Arguments: list, list, boolean
# > Returns: list, list
def coordinate_translation(_edge_pairs, _pad_pairs, mirror_x_axis=False):
    # Set the x coordinate multiplier if we want to mirror the x axis:
    if mirror_x_axis:
        multiplier = -1
    else:
        multiplier = 1

    # Get all x and y coordinates for the board edge (and perform x mirror if needed):
    _board_edge_pairs_x = [value[0]*multiplier for value in _edge_pairs]
    _board_edge_pairs_y = [value[1] for value in _edge_pairs]

    # Calculate the minimum, so we can know the translation (offset) needed to coordinate 0,0:
    _min_x = min(_board_edge_pairs_x)
    _min_y = min(_board_edge_pairs_y)

    # Prepare variables to store the new data:
    _new_board_edge_pairs = []
    _new_pad_layer_pairs = []

    # Go through all the coordinates of the board edge and apply the translation (offset)
    # so the bottom left corner of the board is located at 0,0, apply the x axis mirroring if needed:
    for pair in _edge_pairs:
        _new_board_edge_pairs.append(((pair[0]*multiplier)-_min_x, pair[1]-_min_y))

    # Go through all the coordinates of the pads and apply the same translation (offset) as above,
    # apply the x axis mirroring if needed and maintain the other values (pad ID and area) intact:
    for pair in _pad_pairs:
        _new_pad_layer_pairs.append(((pair[0]*multiplier)-_min_x, pair[1]-_min_y, pair[2], pair[3]))

    return _new_board_edge_pairs, _new_pad_layer_pairs


# Generates the g-code based on the board edge pairs and pad pairs for a given layer.
# The file is saved to the given filename.
# > Arguments: list, list, str, float, float, float, float
# > Returns: -
def generate_gcode(_edge_pairs, _pad_pairs, _filename):
    # Some printing settings:
    alignment_speed = 500       # The printer speed for alignment tasks
    movement_speed = 5000       # The printer speed for extruding tasks
    offset_x = 30.0             # Offset of the x axis to the 0,0 of the board
    offset_y = 30.0             # Offset of the y axis to the 0,0 of the board
    offset_z = 1.0              # Offset of the needle from the bed to the top of the board (depends on PCB thickness)
    offset_z_travel = 3.0       # Offset of the needle for traveling: how much the needle will lift from the bed to move

    make_pre_alignment = False
    make_dry_run = False

    # Ask a few questions:
    # Pre-alignment:
    if messagebox.askyesno("G-code generator - Pre-alignment",
                           "Do you want to include a pre-alignment routing on your g-code?"):
        make_pre_alignment = True

    # PCB/board offsets::
    if messagebox.askyesno("G-code generator - PCB offset",
                           "Currently your PCB offsets are:\n"
                           "  x = " + str(offset_x) + "\n"
                           "  y = " + str(offset_y) + "\n"
                           "Do you want to change them?"):
        # Ask for the new x offset (we need to add a lot of spaces as the window is very small):
        result = simpledialog.askfloat("New x offset",
                                       "Specify the new x offset:                          ",
                                       initialvalue=offset_x,
                                       minvalue=0.0)
        # If the value is not None (the user didn't close or canceled the dialog), then apply the new value
        if result is not None:
            offset_x = result

        # Ask for the new y offset (we need to add a lot of spaces as the window is very small):
        result = simpledialog.askfloat("New y offset",
                                       "Specify the new y offset:                          ",
                                       initialvalue=offset_y,
                                       minvalue=0.0)
        # If the value is not None (the user didn't close or canceled the dialog), then apply the new value
        if result is not None:
            offset_y = result

    # Dry-run:
    if messagebox.askyesno("G-code generator - Dry run",
                           "Do you want to generate a dry run g-code? (no paste extruding)"):
        make_dry_run = True

    # Get current time:
    datetime_now = datetime.datetime.now()

    # Create the g-code file and open for writing:
    gcode_file = open(_filename, "w")

    gcode_file.write("; Generated by gerber2gcode on " + datetime_now.strftime("%Y-%m-%d %H:%M") + '\n')
    gcode_file.write("; Created by: vascojdb@gmail.com, magdalena.wiktoria.szczypka@gmail.com" + '\n')
    gcode_file.write("; https://github.com/vascojdb, https://github.com/magdalenaws" + '\n')
    gcode_file.write("" + '\n')
    gcode_file.write("; BEGIN OF PRE-PREPARATIONS SECTION" + '\n')
    gcode_file.write("M107 ; fan off" + '\n')
    gcode_file.write("M117 Preparing ; display message" + '\n')
    gcode_file.write("G90 ; absolute positioning" + '\n')
    gcode_file.write("G21 ; set units to millimetres" + '\n')
    gcode_file.write("G28 ; auto home" + '\n')
    gcode_file.write("G1 Z10 F" + str(movement_speed) + " ; lift nozzle" + '\n')
    gcode_file.write("G1 F" + str(movement_speed) + " ; set movement speed" + '\n')
    gcode_file.write("; END OF PRE-PREPARATIONS SECTION" + '\n')

    if make_pre_alignment:
        gcode_file.write("" + '\n')
        gcode_file.write("; BEGIN OF ALIGNMENT SECTION" + '\n')
        gcode_file.write("M117 Aligning ; display message" + '\n')
        for pair in _edge_pairs:
            pos_x = float(pair[0]) + offset_x
            pos_y = float(pair[1]) + offset_y
            gcode_file.write("G1 X" + str("%.3f" % pos_x) + " Y" + str("%.3f" % pos_y) + " F" + str(alignment_speed) + '\n')
            gcode_file.write("G1 Z" + str("%.3f" % offset_z) + " F" + str(alignment_speed) + '\n')
            gcode_file.write("M0 Click to move to next point..." + '\n')
            gcode_file.write("G1 Z" + str("%.3f" % offset_z_travel) + " F" + str(alignment_speed) + '\n')
        gcode_file.write("; END OF ALIGNMENT SECTION" + '\n')

    gcode_file.write("" + '\n')
    gcode_file.write("; BEGIN OF PASTE EXTRUDING SECTION" + '\n')
    gcode_file.write("M75 ; start print job timer" + '\n')
    gcode_file.write("M73 P0 ; set print progress percentage" + '\n')
    gcode_file.write("M117 Applying solder paste ; display message" + '\n')

    # Variables to calculate the current job percentage:
    total_points = len(_pad_pairs)
    current_point = 0

    for pair in _pad_pairs:
        pos_x = float(pair[0]) + offset_x
        pos_y = float(pair[1]) + offset_y
        gcode_file.write("G1 X" + str("%.3f" % pos_x) + " Y" + str("%.3f" % pos_y) + '\n')
        gcode_file.write("G1 Z" + str("%.3f" % offset_z) + " F" + str(movement_speed) + '\n')
        if make_dry_run:
            gcode_file.write("; DRY RUN - Would extrude paste here" + '\n')
        else:
            # TODO: Add gcode to extrude solder paste
            gcode_file.write("; TODO" + '\n')
        gcode_file.write("G1 Z" + str("%.3f" % offset_z_travel) + " F" + str(movement_speed) + '\n')

        # Calculate percentage of job already done:
        current_point += 1
        current_percentage = (100*current_point)/total_points
        gcode_file.write("M73 P" + str("%.0f" % current_percentage) + '\n')

    gcode_file.write("M73 P100 ; set print progress percentage" + '\n')
    gcode_file.write("M77 ; stop print job timer" + '\n')
    gcode_file.write("; END OF PASTE EXTRUDING SECTION" + '\n')

    gcode_file.write("" + '\n')
    gcode_file.write("; BEGIN OF FINAL PREPARATIONS " + '\n')
    gcode_file.write("G1 X0 F10000 ; move X to position 0" + '\n')
    gcode_file.write("G1 Y150 F10000 ; move bed to the front" + '\n')
    gcode_file.write("M84 ; turn steppers off" + '\n')
    gcode_file.write("M117 Finished ; display message" + '\n')
    gcode_file.write("M300 S900 P1000; Play beep" + '\n')
    gcode_file.write("; END OF FINAL PREPARATIONS " + '\n')

    gcode_file.write("" + '\n')
    gcode_file.write("; END OF FILE " + '\n')
    gcode_file.close()
    return


# Analyses the 2 gerber files (top/bottom SMD paste and READ-ME) and extracts the coordinates of the board edge
# as well as the coordinates for all pads, their ID and their area, so later we can extrude paste depending on the area
# For Proteus, we assume the command to specify a pad ID is G54 followed by the pad ID itself
# We also assume coordinates always start with the letter X
# And finally we assume the board edge is delimited by 5 points with the D70 as pad ID
# > Arguments: str, str
# > Returns: list, list
def get_edge_and_pad_coordinates(_gerber_paste_filename, _gerber_readme_filename):
    # Initiate variables that will be needed later:
    _pad_id = None
    _pad_area = 0
    _edge_pairs = []
    _pad_pairs = []

    # Do this task if we have a top layer:
    if _gerber_paste_filename:
        # Read the top layer gerber file:
        with open(_gerber_paste_filename) as f:
            _file_contents = f.read().splitlines()

        # Process the file line by line:
        for _line_number in range(len(_file_contents)):
            # Get the line content:
            _line_content = _file_contents[_line_number]

            # Search for the command to start the coordinates of a specific pad ID (ex: G54D07*):
            if _line_content.find("G54") == 0:
                # Get the Dxx part of the string (pad ID, which starts after G54) (ex: D07*):
                _D_index = _line_content.find("D")
                _pad_id = _line_content[_D_index:]

                # Remove the '*' in the end of the line (ex: D07) to get the pad type:
                _pad_id = _pad_id.replace('*', '')
                # Get the pad area:
                _pad_area = get_pad_area(_gerber_readme_filename, _pad_id)

            # Search for coordinates (ex: X+8715Y-3543D03*), the line always starts with an X:
            if _line_content.find("X") == 0:
                # Get the location on the line where the X and Y part are located
                _X_index = _line_content.find("X")
                _Y_index = _line_content.find("Y")
                _D_index = _line_content.find("D")

                # Extract the X coordinate which is located between X+1 (+1 to ignore the letter X) and Y location
                _X_coordinate_th10 = _line_content[(_X_index + 1):_Y_index]
                _Y_coordinate_th10 = _line_content[(_Y_index + 1):_D_index]

                # Coordinates are in thousands on an inch, we need them in milliliters:
                _X_coordinate_mm = convert_th10_to_mm(_X_coordinate_th10)
                _Y_coordinate_mm = convert_th10_to_mm(_Y_coordinate_th10)

                # The D70 pad ID always refers to the board edges for Proteus:
                if _pad_id == "D70":
                    _edge_pairs.append((_X_coordinate_mm, _Y_coordinate_mm))
                else:
                    _pad_pairs.append((_X_coordinate_mm, _Y_coordinate_mm, _pad_id, _pad_area))

    return _edge_pairs, _pad_pairs


# ===========================================
# ========== MAIN CODE STARTS HERE ==========
# ===========================================

# Display welcome message:
print("Welcome to gerber2gcode v" + CURR_VER_MAJ + "." + CURR_VER_MIN)
print("Created by: vascojdb@gmail.com, magdalena.wiktoria.szczypka@gmail.com")
print("https://github.com/vascojdb, https://github.com/magdalenaws")
print("")

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


# Perform actions for the top layer:
if gerber_top_paste_filename:
    # Analyse the gerber files and extract the board edge coordinates and pad coordinates and information:
    top_edge_pairs, top_pad_pairs = get_edge_and_pad_coordinates(gerber_top_paste_filename,
                                                                 gerber_readme_filename)

    # We need to translate (offset) the coordinates so that the board origins from 0,0
    # The top layer we will not invert the x axis:
    top_edge_pairs, top_pad_pairs = coordinate_translation(top_edge_pairs,
                                                           top_pad_pairs,
                                                           False)
    
    # Generate the images/graphs with the pad locations:
    generate_images(top_edge_pairs, top_pad_pairs, picture_paste_top)

    # Display generated image:
    display_image(picture_paste_top)

    if messagebox.askyesno("Top layer solder paste G-Code generation",
                           "Do you want to generate a G-Code print file for the top solder paste layer?"):
        # Generate g-code for the top layer:
        generate_gcode(top_edge_pairs, top_pad_pairs, gcode_top_filename)
        # Open the generated file on the default text viewer for .gcode:
        os.startfile(gcode_top_filename, 'open')

# Perform actions for the bottom layer:
if gerber_bottom_paste_filename:
    # Analyse the gerber files and extract the board edge coordinates and pad coordinates and information:
    bottom_edge_pairs, bottom_pad_pairs = get_edge_and_pad_coordinates(gerber_bottom_paste_filename,
                                                                             gerber_readme_filename)

    # We need to translate (offset) the coordinates so that the board origins from 0,0
    # The bottom layer we will invert the x axis:
    bottom_edge_pairs, bottom_pad_pairs = coordinate_translation(bottom_edge_pairs,
                                                                 bottom_pad_pairs,
                                                                 True)
    
    # Generate the images/graphs with the pad locations:
    generate_images(bottom_edge_pairs, bottom_pad_pairs, picture_paste_bottom)

    # Display generated image:
    display_image(picture_paste_bottom)

    if messagebox.askyesno("Bottom layer solder paste G-Code generation",
                           "Do you want to generate a G-Code print file for the bottom solder paste layer?"):
        # Generate g-code for the top layer:
        generate_gcode(bottom_edge_pairs, bottom_pad_pairs, gcode_bottom_filename)
        # Open the generated file on the default text viewer for .gcode:
        os.startfile(gcode_bottom_filename, 'open')

print("Application concluded. Exiting...")
