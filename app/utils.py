import os

def get_uploaded_images():
    rootdir = os.getcwd()
    
    images = []
    
    for subdir, _, files in os.walk(rootdir + '/uploads'):
        print(subdir)
        for file in files:
            if file != ".gitkeep":
                images.append(file) 
    return images

print(get_uploaded_images())