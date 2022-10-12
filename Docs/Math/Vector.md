# Documentation
## 1. Math Package
1.1. The Vector Class
Vector class implements vector calculation in R^3. Vector calculation is done by creating Vector instance. 
Initialize a vector takes three arguments, x component, y component, and z component. Below is a triival example:
```python
from Math.Vector import Vector
# creating vector with component[1, 2, 3]
a = Vector(1, 2, 3)
# creating vector with component[3, 4, 5]
b = Vector(3, 2, 4)
```

Vector class has four public property, that is:
1. x : float = the component of the vector in x
2. y : float = the compoenent of the vector in y
3. z : float = the component of the vector in z
4. mag : float = the length of the vector 

Basic operation on vector can be done using basic operator on python such as '+', '-', '*', '/'. 
```python
a = Vector[1, 2, 3]
b = Vector[3, 4, 5]
c = a + b # add vector [4, 6, 5]
d = a - b # substract a with b [-2, -2, -2]
e = a * 2 # multiply a with scalar k [2, 4, 6]
f = a / 2 # multiply a with scalar 0.5 [0.5, 1, 1.5]
```

For multiplication or division, scalar must be placed after the vector else *TypeError* exception will be raised. 
```python
c = 20 * a # will raise exception
c = 1 / a # will raise exception
```

1.1.1. serialize
Serialize a vector into a list of float. the value in the list is the component of the vector. 
```python
c = Vector[1, 2, 3]
print(c.serialize()) # [1, 2, 3]
```
If needed angle information, use serializeAngle instead. 

1.1.2 serializeAngle
Serialize a vector into a list of float, where the value is the angle the vector make with x axis, y axis, and z axis. Serialize takes degrees flag as parameter to determine the angle type. If degrees is True, then angle in degrees else in radians. (Default value is False) 

```python
a = Vector(1, 2, 3) 
print(a.serializeAngle())
# [1.3002465638163236, 1.0068536854342678, 0.6405223126794245]
print(a.serializeAngle(True)) 
# [74.498640433063, 57.688466762576155, 36.69922520048988]
```

1.1.3 magnitude
Return the magnitude of a vector

1.1.4 crossProduct
Calculate the result of cross product a x b. The return value will be a Vector instance. Calculation is done using equation below:
```python
a = Vector(1, 2, 3)
b = Vector(3, 4, 5)
c = a.crossProduct(b)
# c.serialize() = [-2, 4, -2]
```

1.1.5 dotProduct
Calculate the result of a dot product a.b. 
```python
a = Vector(1, 2, 3)
b = Vector(3, 4, 5)
dot = a.dotProduct(b)
# 123
```

1.1.6 distance
Calculate the distance between vector a with vector b. 
```python 
d = a.distance(b)
```

1.1.7 angle
Calculate the angle between two vector(in radians). 
```python
angle = a.angle(b)
```

1.1.8 normalized
Return the normalized vector or unit vector of self.

1.1.10 changeBasis
Change the basis of the vector from ax, ay, az into user specified basis v1, v2, v3. 
