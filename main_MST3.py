# ELL205 Project Milestone 2
# Student1 Name: Roshan Prashant Bara
# Student2 Name: Shreyansh Singh
# Student3 Name: Rohit Janbandhu


# Importing the library
import cv2


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

# Returns list of tuples containing positions and error ans dimensions of matchings(Note these aren't the final matchings) 
def getflag(image_matrix, object_matrix, threshval) :
    error_matrix = mse(image_matrix, object_matrix)

    flag = []

    h = object_matrix.shape[0]
    w = object_matrix.shape[1]

    for i in range(len(error_matrix)):
        for j in range(len(error_matrix[0])):

            # Using flag to store the coordinates of all regions that have mse less than or equal to thresh_val
            if(error_matrix[i][j]<=threshval):
                flag = flag + [(i,j, error_matrix[i][j], w, h)]

    return flag


# Boundary Creater Function creates boundary around matching regions
def boundary_creater_fn(image_matrix, flag) :
    global c

# We draw rectangles around the matching regions
    for k in range(len(flag)):
        i,j,v,w,h = flag[k]
        if(i>=0):
            c+=1
            image_matrix= cv2.rectangle(image_matrix,(j,i),(j+w,i+h),0,1)   #using rectangle method ,thickness of 1 and black colour

    return image_matrix

def remove_duplicate(flag):  #flag tuple of 5

    for i in range(len(flag)):
        for j in range(i+1,len(flag)):
            x1, y1, err1, w1, h1 = flag[i]
            x2, y2, err2, w2, h2 = flag[j]
            if(x1 == -1 or x2 == -1): continue
            if((x1>=x2 and x1-x2< h2) or (x1<=x2 and x2-x1< h1)):
                if((y1>=y2 and y1-y2< w2) or (y1<=y2 and y2-y1< w1)):
                    if(err1<err2):
                        flag[j] = (-1, -1, 999, -1, -1)
                    else:
                        flag[i] = (-1, -1, 999, -1, -1)

    
    return flag
    
def main() :
    img_file = input("Enter image filename: ")
    obj_file = input("Enter object filename: ")

    # Reading image in grayscale mode
    img = cv2.imread(img_file, 0)
    obj = cv2.imread(obj_file, 0)
    

    #storing the height and width of the object
    h = obj.shape[0]
    w = obj.shape[1]

    
    threshval = 2500

    flag = []

    flag = flag + getflag(img, cv2.pyrDown(cv2.pyrDown(obj)), threshval)
    flag = flag + getflag(img, cv2.pyrDown(obj), threshval)
    flag = flag + getflag(img, obj, threshval)
    flag = flag + getflag(img, cv2.pyrUp(obj), threshval*2)
    flag = flag + getflag(img, cv2.pyrUp(cv2.pyrUp(obj)), threshval*2)

    final_flag = remove_duplicate(flag)
    

    newimage=boundary_creater_fn(img, final_flag)
    cv2.imshow('Matching regions in image',newimage)
    print('Number of matching objects in image: ', c)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

main()
