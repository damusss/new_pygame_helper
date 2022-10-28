import math
from typing import Tuple

# MATH UTILS FUNCTIONS
def det(a,b):
	"""
	I have no idea but the code is just: "return a[0]*b[1]-a[1]*b[0]".
	"""
	return a[0]*b[1]-a[1]*b[0]

def in_range(a,b,c):
	"""
	Check if a number is in the range of two others.
	"""
	return c>=min(a, b) and c<=max(a,b)

def dist(p1,p2):
	"""
	Calculate distance between two points.
	"""
	return math.sqrt((p2[0]-p1[0])**2+(p2[1]-p1[1])**2)

def tuple_slope(tuplee:Tuple[Tuple[float,float],Tuple[float,float]])->float:
	"""
	Find the slope of a line that is made of tuples.
	"""
	if (tuplee[1][0]-tuplee[0][0]) == 0:
		return None
	return (tuplee[1][1]-tuplee[0][1])/(tuplee[1][0]-tuplee[0][0])