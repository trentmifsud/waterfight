import time
import numpy

def find_index_of_nearest_xy(y_array, x_array, y_point, x_point):
    distance = (y_array-y_point)**2 + (x_array-x_point)**2
    idy,idx = numpy.where(distance==distance.min())
    return idy[0],idx[0]

def do_all(y_array, x_array, points):
    store = []
    for i in xrange(points.shape[1]):
        store.append(find_index_of_nearest_xy(y_array,x_array,points[0,i],points[1,i]))
    return store


# Create some dummy data
y_array = numpy.random.random(10000).reshape(100,100)
x_array = numpy.random.random(10000).reshape(100,100)

points = numpy.random.random(10000).reshape(2,5000)

# Time how long it takes to run
start = time.time()
results = do_all(y_array, x_array, points)
end = time.time()
print ('Completed in: ' + end-start)