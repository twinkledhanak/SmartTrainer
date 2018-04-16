# class for user
class user:
  def __init__(self, name, age , etype):
    self.name = name
    self.age = age
    self.etype = etype
      #Employee.empCount += 1

  def getName(self):
   	return self.name

  def getAge(self):
  	return self.age

  def getType(self):
   	return self.etype

  def setName(self,name):
   	self.name = name 

  def setAge(self,age):
  	self.age = age

  def setType(self,etype):
   	self.etype = etype					  