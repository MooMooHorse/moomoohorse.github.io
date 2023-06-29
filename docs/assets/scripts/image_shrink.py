# Helper scripts that resize all images in the post to 50% of the original size
# @version : 1.0
# @author : Hao Ren (haor2@illinois.edu)
# Please redistribute this file freely

import sys
import os
import shutil
from PIL import Image
# configurations
# please overwrite this if your directory structure is not
# docs
# | - _posts
# | - assets
#     | - scripts
#         | - image_shrink.py
curFilePath = os.path.dirname(os.path.realpath(__file__))
docPath = os.path.dirname(os.path.dirname(curFilePath))
postPath = os.path.join(docPath, "_posts")

def resize(input_image_path, output_image_path, percentage, auto=False):
    """
    if auto is False : resize the image to the given percentage
    if auto is True : resize the image so that it fits the website.
    The website needs an image whose width is 850px to 1000 px.
    """
    image = Image.open(input_image_path)
    width, height = image.size
    if auto:
        new_width = 1000
        new_height = int(height * new_width / width)
    else:
        new_width = int(width * percentage / 100)
        new_height = int(height * percentage / 100)
    new_image = image.resize((new_width, new_height))
    print("Image resized from {}x{} to {}x{}".format(width, height, new_width, new_height))
    print("Saving image to {}".format(output_image_path))
    new_image.save(output_image_path)

def filename2date(filename):
    date = filename[:10]
    return date

def handle_flags():
    """
    -new: get the date of latest post and process all images in the post
    -date=<date1>,<date2>,... : get the post of the date and process all images in the post
    """
    global curFilePath, docPath, postPath
    dateproc = []
    ifRecover = False
    for arg in sys.argv[1:]:
        if arg.startswith("-date="):
            dateproc = arg[6:].split(",")
        elif arg.startswith("-new"):
            for filename in os.listdir(postPath):
                if filename.endswith(".md"):
                    dateproc.append(filename2date(filename))
            # sort 
            dateproc.sort()
            # get the latest date
            dateproc = dateproc[-1:]
        elif arg.startswith("-recover"):
            ifRecover = True
        else:
            print("Error: invalid flag")
            return None
        
    return dateproc, ifRecover

def proc_post(fpath):
    """
    Process all the links to images in the post
    All images should have format :
    ![something](<image_path>)
    <image_path> is relative to the post
    """
    # scan the post
    write_lines = []
    with open(fpath, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            import re
            newline = None
            m = re.search(r"!\[.*\]\((.*)\)", line)
            if m:
                imgpath = m.group(1)
                # replace / with \
                imgpath = imgpath.replace("/", "\\")
                # check if the image exists
                originalImgPath = os.path.join(os.path.dirname(fpath), imgpath)
                if not os.path.exists(originalImgPath):
                    print("Error: image not found {}".format(originalImgPath))
                    return
                # shrink the image
                imgname = os.path.basename(originalImgPath)
                imgname = "shrink_" + imgname
                imgpath = os.path.join(os.path.dirname(originalImgPath), imgname)
                print(f"Shrinking image {originalImgPath} to {imgpath}")
                resize(originalImgPath, imgpath, 50, auto=True)
                # # replace the image path (only replace the basename)
                newline = line.replace(os.path.basename(originalImgPath), imgname)
                print("Replacing {} with {}".format(line, newline))
            if newline is None:
                newline = line
            write_lines.append(newline)
    with open(fpath, "w", encoding="utf-8") as f:
        f.writelines(write_lines)

def recover_post(fpath):
    """
    Revert the effect done by proc_post.
    We should find all the image basename, and remove the shrink_ prefix.
    """
    write_lines = []
    with open(fpath, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            import re
            newline = None
            m = re.search(r"!\[.*\]\((.*)\)", line)
            if m:
                imgpath = m.group(1)
                # replace / with \
                imgpath = imgpath.replace("/", "\\")
                # check if the image exists
                originalImgPath = os.path.join(os.path.dirname(fpath), imgpath)
                if not os.path.exists(originalImgPath):
                    print("Error: image not found {}".format(originalImgPath))
                    return
                # shrink the image
                imgname = os.path.basename(originalImgPath)
                # if the image is not shrinked, skip
                if not imgname.startswith("shrink_"):
                    continue
                imgname = imgname[7:] # remove the shrink_ prefix
                newline = line.replace(os.path.basename(originalImgPath), imgname)
                print("Replacing {} with {}".format(line, newline))
            if newline is None:
                newline = line
            write_lines.append(newline)
    with open(fpath, "w", encoding="utf-8") as f:
        f.writelines(write_lines)

def main():
    dateproc, ifRecover = handle_flags()
    if not os.path.exists(postPath):
        print("Error: post path not found")
        return
    for filename in os.listdir(postPath):
        if filename.endswith(".md"):
            date = filename2date(filename)
            if date in dateproc:
                fpath = os.path.join(postPath, filename)
                print("Processing {}".format(fpath))
                if ifRecover:
                    recover_post(fpath)
                else:
                    proc_post(fpath)

if __name__ == "__main__":
    main()