import pandas as pd
import data_loader as dl
import matplotlib as mp

df_images = dl.load_data('_annotations.coco.json', 'images')
df_info = dl.load_data('_annotations.coco.json', 'info')
df_licenses = dl.load_data('_annotations.coco.json', 'licenses')
df_cat = dl.load_data('_annotations.coco.json', 'categories')
df_annot = dl.load_data('_annotations.coco.json', 'annotations')

def data_count(df):
    
    df_explore = dl.load_data(df)
    return df_explore.count()

def data_shape(df):
    
    df_explore = dl.load_data(df)
    return df_explore.shape()

def data_info(df):
    
    df_explore = dl.load_data(df)
    return df_explore.info()

def data_graph(df):
    
    df_explore = dl.load_data(df)
    return df_explore.describe()