# class to store details of user's progress

class progress:
	def __init__(self, ename,etype): # @TODO parameters for user measurements 
      self.ename = ename
      self.etype = etype
      #Employee.empCount += 1

    def getName(self):
    	return self.ename

    def getType(self):
    	return self.etype

    def setName(self,name):
    	self.name = ename 

    def setType(self,etype):
    	self.etype = etype	