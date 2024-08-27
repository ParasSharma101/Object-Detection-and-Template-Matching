# ELL205 Project Milestone 2
# Student1 Name: Roshan Prashant Bara
# Student2 Name: Shreyansh Singh
# Student3 Name: Rohit Janbandhu


# Importing the library
import cv2
import numpy as np


#counter for calulating the no. of similar region
c=0

# Mean Squared Error Function returns error matrix generated after sliding the object window over entire image
def mse(image_matrix, object_matrix) :

    n1 = len(image_matrix)
    m1 = len(image_matrix[0])
    n2 = len(object_matrix)
    m2 = len(object_matrix[0])
    n = n1-n2+1
    m = m1-m2+1

    error_matrix = [[0 for i in range(m)] for j in range(n)]
    total = n2*m2

    for i in range(n) :
        for j in range(m) :
            for k in range(n2):
                for l in range(m2):
                    error_matrix[i][j] = error_matrix[i][j] + (int(image_matrix[i+k][j+l])-int(object_matrix[k][l])) ** 2
            error_matrix[i][j] = error_matrix[i][j] / total

    return error_matrix

# Boundary Creater Function creates boundary around matching regions
def boundary_creater_fn(image_matrix, error_matrix, thresh_val, w, h) :
    global c

    flag = []

    for i in range(len(error_matrix)):
        for j in range(len(error_matrix[0])):

            # Using flags to store the coordinates of all regions that have mse less than or equal to thresh_val
            if(error_matrix[i][j]<=thresh_val):
                flag = flag + [(i,j)]

# We now chose the min mse value region from the cluster of matching regions inorder to avoid overlapping regions
    for i in range(len(flag)):
        for j in range(i+1,len(flag)):
            a1, b1 = flag[i]
            a2, b2 = flag[j]
            if( abs(a1-a2)<h and abs(b1-b2)<w ): 
                if(error_matrix[a1][b1] < error_matrix[a2][b2]):
                    flag[j] = (-1,-1)
                else:
                    flag[i] = (-1,-1)

# We draw rectangles around the matching regions
    for k in range(len(flag)):
        i,j = flag[k]
        if(i>=0):
            c+=1
            image_matrix= cv2.rectangle(image_matrix,(j,i),(j+w,i+h),0,1)   #using rectangle method ,thickness of 2 and colour green(0,255,0)

    return image_matrix     
    

img_file = input("Enter image filename: ")
obj_file = input("Enter object filename: ")

# Reading image in grayscale mode
img = cv2.imread(img_file, 0)
obj = cv2.imread(obj_file, 0)

#storing the height and width of the object
h = obj.shape[0]
w = obj.shape[1]


error_matrix = mse(img, obj)


# Threshold value change manually
thresh_val = 900


newimage=boundary_creater_fn(img, error_matrix, thresh_val, w, h)
cv2.imshow('Matching regions in image',newimage)
print('Number of matching objects in image: ', c)

cv2.waitKey(0)
cv2.destroyAllWindows()