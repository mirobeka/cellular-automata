class TimeStep:
  def __init__(self, maxSteps):
    self.time = 0
    self.maxSteps = maxSteps

  def getTime(self):
    return self.time

  def underMaxSteps(self):
    return self.time < self.maxSteps

  def nextStep(self):
    self.time += 1
  
  def previousStep(self):
    self.time -= 1
