from Math.Vector import Vector
a = Vector(1, 2, 3)
b = Vector(4, 5, 6)
c = a + b * 2
print(c.serialize())
c = c  * 20
print(c.serialize())