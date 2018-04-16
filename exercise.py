# class for exercise, contains parameters, values to be hardcoded elsewhere

# ename: Mountain - pose
# etype: front / side 
# ASSUME: LEGS = BLUE , HANDS = GREEN , NECK = BLUE / GREEN , HIP = BLUE / GREEN
# right = 1 , left = 2 (for actual human)
# we need different objects for each colour and band

class exercise:
	def __init__(self, ename,etype): # @TODO parameters for exercise pmeasurements 
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