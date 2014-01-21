################################################################
# Module #
# Imports Blob libraries,identifies blobs and Resizes into 20X20
################################################################

def resize(binary_image):
	from cv import *
	#from opencv.highgui import *

	#from blobs.Blob import *
	#from blobs.BlobResult import *

	#from Blob import *
	#from BlobResult import *

	frame_size = cvGetSize (binary_image)
	blo = cvCreateImage(frame_size, 8, 1)
	resize=cvCreateMat(20,20,blo.type)
	mask = cvCreateImage (frame_size, 8, 1)
	cvSet(mask, 255)
	myblobs = CBlobResult(binary_image, mask, 0, True)
	myblobs.filter_blobs(700,9000)
	blob_count = myblobs.GetNumBlobs()
	print blob_count
	for i in range(blob_count):
        	cvSet(resize,0)
      		cvSet(blo,0)
		my_enum_blob = myblobs.GetBlob(i)
		my_enum_blob.FillBlob(blo,CV_RGB(255,0,255),0,0)
		f=open("ab.txt","w")
		for rowitem in range(blo.rows):
		    for colitem in range(blo.cols):
		       if blo[rowitem,colitem]!=0:
		          f.write(str(rowitem)+" " + str(colitem)+" "+str(blo[rowitem,colitem]))
		          f.write("\n")
		                                
		f.close()          
		value=[]
		rowval=[]
		colval=[]
		for line in open("ab.txt"):
		    attr=line.split()
		    rowval.append(attr[0])
		    colval.append(attr[1])
		    value.append(attr[2])
		
		rowmin=int(rowval[0])
		rowedit=[]
		for item in rowval:
		    rowedit.append(int(item)-rowmin)
	
		coledit=[]
		colsort=[]
		for item in colval:
		    colsort.append(int(item))
		
		colsort.sort()
		colmin=colsort[0]
		for item in colval:
		    coledit.append(int(item)-colmin)
	
		rowmax=int(rowedit[-1])
		colmax=int(colsort[-1]-colmin)
		moved=cvCreateMat(rowmax+1,colmax+1,blo.type)
		cvSet(moved,0)
		
		for i in range(len(rowval)):
		    moved[int(rowedit[i]),int(coledit[i])]=int(value[i])
		
        	cvResize(moved,resize,1)
		cvSaveImage("pic"+ str(i)+".JPG",resize)       
