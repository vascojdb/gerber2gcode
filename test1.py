import zipfile

zip_path = "sample_gerber.ZIP"
extract_path = "bananas"

print("Reading file: " + zip_path)

# Open zip file
zip_ref = zipfile.ZipFile(zip_path, 'r')
# Extract files:
zip_ref.extractall(extract_path)
# Finally, close the file (mandatory)
zip_ref.close()

# read the file
import glob, os
os.chdir(extract_path)
for top_paste_filename in glob.glob("*Top SMT Paste Mask*"):
    print(top_paste_filename)

    with open(top_paste_filename) as f:
        whole_text = f.read().splitlines()

    print(whole_text)

    for line_number in range(len(whole_text)):
        print(whole_text[line_number])
