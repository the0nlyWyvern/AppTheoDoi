from PIL import Image
import streamlit as st
from glob import glob

def find_screen(date):
    name = 'Drive_folder/Screen/' + date + '.**-**-**.jpg'
    valid_screens = glob(name)
    for i in range(len(valid_screens)):
        valid_screens[i] = valid_screens[i].replace('\\','/')
    return valid_screens

def get_log(file_name)->str:
    with open(file_name, 'r') as f:
        return f.read()