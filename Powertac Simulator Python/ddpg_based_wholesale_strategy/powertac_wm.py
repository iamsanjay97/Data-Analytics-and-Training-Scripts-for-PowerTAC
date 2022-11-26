import gym
import collections as col
import numpy as np

class PowerTAC_WM(object):

  def __init__(self,proximity=None, quantity=None, mean_market_price=None):

    proximity_ohe = np.zeros(24)

    if(proximity != 0):
        proximity_ohe[proximity-1] = 1

    self.proximity = proximity_ohe           # One-Hot Encoded Proximity
    self.quantity = quantity
    self.mean_market_price = mean_market_price

  def form_network_input(self):

     state = list()
     state.extend(self.proximity)
     state.append(self.quantity)
     state.append(self.mean_market_price)

     return state


  def step(self, action):
      pass

  def reset(self):

      self.proximity = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]           # One-Hot Encoded Proximity
      self.quantity = 0.0
      self.mean_market_price = 0.0
      self.observation = self.make_observaton()
      return self.observation


  def make_observaton(self):

      names = ['proximity', 'quantity', 'mean_market_price']
      Observation = col.namedtuple('Observaion', names)
      return Observation(proximity=self.proximity, quantity=self.quantity, mean_market_price=self.mean_market_price)


  def render(self, mode='human', close=False):

      print('Proximity : ', self.proximity)
      print('Required Quantity : ', self.quantity)
      print('Mean Market Price: ', self.mean_market_price)

  def __str__(self):

      return "<" + str(self.proximity) + \
             "," + str(self.quantity) + \
             "," + str(self.mean_market_price) + ">"
