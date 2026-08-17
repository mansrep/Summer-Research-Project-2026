import math

print("Please enter length of moire pattern:")
length = float(input())
print("Please enter width of moire pattern:")
width = float(input())
print

y = math.degrees(math.acos(width/length))
x = 90 - y
print(f"Tilted with: {x} degrees")
print("Enter measured length of segment you want to calculate real length of:")
false_length = float(input())
real_length = false_length/math.cos(math.radians(x))
print(f"Real length of segment is {real_length} nm")
print(f"Difference in length: {real_length-false_length} nm")

##EVERYTHING IS TRIANGLES!