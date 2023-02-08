import streamlit as st
import pandas as pd
from PIL import Image
import pickle as pkle
import os.path
from io import StringIO, BytesIO
import webbrowser, os
from pathlib import Path
import face_recognition
import pickle
import cv2
import smtplib
import xlsxwriter
from datetime import datetime, timedelta
import numpy as np
from openpyxl import load_workbook, Workbook
from datetime import date
import re



# photo function
def photo_function(Path):
    
    knownEncodings = []
    knownNames = []
    # extract the person name from the image path
    name = Path.split(os.path.sep)[-2]
    # load the input image and convert it from BGR (OpenCV ordering)
    # to dlib ordering (RGB)
    image = cv2.imread(Path)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #Use Face_recognition to locate faces
    boxes = face_recognition.face_locations(rgb,model='hog')
    print(boxes)
    # compute the facial embedding for the face
    encodings = face_recognition.face_encodings(rgb, boxes)
    # loop over the encodings
    for encoding in encodings:
        knownEncodings.append(encoding)
        knownNames.append(name)
    
    return knownEncodings, knownNames



#update pickel
def update_pickel(new_st_encoding, new_st_name):
    #read_pickel
    all_student_enc = pickle.loads(open('face_enc', "rb").read())
    all_student_enc['names'].extend(new_st_name)
    all_student_enc['encodings'].extend(new_st_encoding)
    #write
    f = open("face_enc", "wb")
    f.write(pickle.dumps(all_student_enc))
    f.close()
    
    
    
# create a folder
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory.', directory)
        
        
        
# Validating the Email Address

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
def check_data(name, email):
    if(re.search(regex,email)):
        #st.success('Valid Email', icon="✅")
        #info = pd.read_csv('info.csv')
        if (email in info['email'].values) & (name in info['name'].values):
                st.error('This student already registered',icon="🚨")
                return 0
        return 1
       
    else:
        
        st.error('Invalid Email, Please write a valid Email', icon="🚨")
        return 0
    

            
            
def check_pic(picture):   
    if picture: 
        
        img = Image.open(picture)
        # To convert PIL Image to numpy array:
        img_array = np.array(img)
        rgb = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
        #Use Face_recognition to locate faces
        boxes = face_recognition.face_locations(rgb, model='hog')
  
        n_boxes = len(boxes)
        st.write(n_boxes)
        if n_boxes == 1:
            return 1
        else:
            st.error(f'This picture has {n_boxes} faces. We need only the face of the child', icon="🚨")
            return 0
    else:
        st.error('Invalid Picture, Please smile and take another one', icon="🚨")
        return 0
    
    
    
    
# load image
def load_image(picture):
    img= Image.open(picture)
    return img
        

#app      
image = Image.open('info_1.png')
st.image(image)
st.write('')

name = st.text_input('Student Name')
email = st.text_input('Parent Email')
choice_1 = st.radio( "What\'s your favorite way to take a photo", ('Upload form PC','Use webcam'))
if choice_1 == 'Upload form PC':
    picture =  st.file_uploader("Upload An Image", type =['png', 'jpg', 'jprg'])
       
else:
    picture = st.camera_input("Take a picture")

if picture:
    st.image(picture)


# add a butten to Registration
if st.button('Registration'):
    info = pd.read_csv('info.csv')
    if check_pic(picture) & check_data(name, email):
        # open the folder to save the taken photo
        path=f"C:\\Users\\anibr\\Desktop\\Images\\{name}"
        createFolder(path)
        # save a pic
        with open (path + f'\\{name}.jpg','wb') as file:
            file.write(picture.getbuffer())
    # save the Name and the Email in info.csv
        info = pd.read_csv('info.csv')
        

    # updating the column value/data
    
        row = len(info)
        info.loc[row, :] = [name, email]
        info.to_csv("info.csv", index=False)
        # calle the first function

        path = f"C:\\Users\\anibr\\Desktop\\Images\\{name}\\{name}.jpg"
        new_st_encoding, new_st_name = photo_function(path)

        #call the seconde function
        update_pickel(new_st_encoding, new_st_name)



         # Display a success message.
        st.success('The registration is a success!', icon="✅")
        
