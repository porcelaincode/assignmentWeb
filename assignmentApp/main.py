from PIL import Image, ImageDraw, ImageFont
import os
import random
import shelve
import time
import sys
import threading


def make_assignment(fileData, date, font_to_use, page_type):

    images_formed = []

    shelfFile = shelve.open("assignmentApp/extras/PageDim")
    
    #Opening the blank page
    if page_type == "ruled":
        page_path = "page.jpeg"
    else:
        page_path = "white.jpg"
    
    page = Image.open(f"assignmentApp/page_templates/{page_path}")

    def convert_to_pixels(cm, multiplicative_factor):
        return cm*multiplicative_factor

    #Getting the pixel width and height of the page
    width, height = page.size

    try:
        page_hor, page_ver, page_lmar, page_tmar, page_bmar, page_line_space = shelfFile["pagedimensions"]
    except:
        print("Enter The following dimensions of the page in cm")
        print("Enter Horizontal Length of the Page")
        page_hor = round(float(input()))
        print("Enter Vertical Length of the Page")
        page_ver = round(float(input()))
        #Converting cm values to pixels
        horizontal_factor = width/page_hor
        vertical_factor = height/page_ver
        page_hor = width
        page_ver = height
        print("Enter Left Margin Length of the Page")
        page_lmar = float(input())
        page_lmar = round(convert_to_pixels(page_lmar, horizontal_factor))
        print("Enter Top Margin Length of the Page")
        page_tmar = float(input())
        page_tmar = round(convert_to_pixels(page_tmar, vertical_factor))
        print("Enter Bottom Margin Length of the Page")
        page_bmar = float(input())
        page_bmar = round(convert_to_pixels(page_bmar,vertical_factor))
        print("Enter Distance Between two horizontal lines on the page (rules)")
        page_line_space = float(input())
        page_line_space = round(convert_to_pixels(page_line_space, vertical_factor))

        #Page Size is stored in the format Page Horizontal, Page Vertical, Page Left Margin, Page Top Margin, Page Bottom Margin, Page Line Space
        shelfFile["pagedimensions"] = [page_hor, page_ver, page_lmar, page_tmar, page_bmar, page_line_space]

    #Making a copy of the blank page
    copy = page.copy()

    #Making ImageDraw object to add text to it
    draw = ImageDraw.Draw(copy)

    #Making ImageFont object of users font

    
    if font_to_use == "Snake":
        font_path = "Snake.ttf"
    elif font_to_use == "Qournatte":
        font_path = "Qournatte.ttf"
    elif font_to_use == "Mumsies":
        font_path = "Mumsies.ttf"
    else:
        font_path = "Sour Dough.ttf"

    myfont = ImageFont.truetype(f"assignmentApp/fonts/{font_path}", 105)

    # Open custom text document
    text = fileData

    page_no = 1

    lwidth = 0

    # page_hor, page_ver, page_lmar, page_tmar, page_bmar, page_line_space

    page_lmar += 10
    page_line_space -= 2.5
    #page_line_space += 10
    image_list = []
    page_lmar += 2
    page_tmar -= 15

    twidth = page_tmar

    for index, letter in enumerate(text):
        
        try:
            if(letter == " "):
                nlflag = 0
                for i in range(index+1, len(text)):
                    if(text[i] == " "):
                        nlflag = 1
                        break
                if(nlflag == 1):
                    temp_width = draw.textsize(text[index:i], myfont)[0]
                    if((lwidth+temp_width) >= (page_hor-page_lmar-100)):
                        twidth = twidth + page_line_space
                        lwidth = 0
                        continue

            if((twidth+page_line_space >= page_ver - page_bmar + 50)):
                temp_copy = copy.convert("RGB")
                if(page_no == 1):
                    first_image = temp_copy
                    file_name = f"text{page_no}.png"
                    images_formed.append(file_name)
                else:
                    image_list.append(temp_copy)
                copy.save(f'staticfiles/assignmentApp/text{page_no}.png')
                print(f"Saved page {page_no}.")
                copy = page.copy()
                draw = ImageDraw.Draw(copy)
                lwidth = 0
                twidth = page_tmar
                page_no+=1
                file_name = f"text{page_no}.png"
                images_formed.append(file_name)

            if((letter == "\n") or (lwidth >= (page_hor-page_lmar-100))):
                #If there is no space to write characters
                #start_index = index
                lwidth = 0
                twidth += page_line_space
            human = random.randint(0,5)
            add_sub = random.randint(0,1)
            if(add_sub == 0):
                draw.text((page_lmar+lwidth,twidth+human), letter, fill = (0,15,85,255), font = myfont)
            else:
                draw.text((page_lmar+lwidth,twidth-human), letter, fill = (0,15,85,255), font = myfont)
            lwidth += draw.textsize(letter, myfont)[0]
        except Exception as e:
            print(f"Error Occured: {e}")


    copy.save(f'staticfiles/assignmentApp/text{page_no}.png')
    copy.convert("RGB")
    image_list.append(copy)

    try:
        os.mkdir("assignmentApp/documents")
    except FileExistsError:
        pass

    first_image.save(r"assignmentApp\documents\assignment.pdf", save_all=True, append_images=image_list)

    print("DONE!", end = "\r")
    return images_formed
