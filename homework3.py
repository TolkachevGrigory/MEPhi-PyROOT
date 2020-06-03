#!/usr/bin/env python
# coding: utf-8

# In[45]:


import random

class Particle:
    def __init__(self, particle):
        self.particle = particle
        
    def decay(self):
        if 'W' in self.particle:
            return random.choices(['W->e+nu_e', 'W->mu+nu_mu','W->tau+nu_tau', 'W->hadrons ','Другое'], weights=[10.5, 10,11,67,1])[0]
        if 'Z' in self.particle:
            return random.choices(['Z->e+e', 'Z->mu+mu','Z->tau+tau', 'Z->hadrons ','Другое'], weights=[3.4,3.4,3.4,70,19.2])[0]
        if 'K+' in self.particle:
            return random.choices(['K+->mu+nu_mu', 'K+->pi0+e+nu_e','K+->pi0+mu+nu_mu', 'K+->pi_minus+pi_plus+e+nu_e','Другое'], weights=[63,5,3,4.5,24.5])[0]
        
    def particlesdecay(self, number):
        dictionary = {} 
        for i in range(number):
            mode = self.decay()
            dictionary[mode] = dictionary.get(mode,0)+1
    
        for mode in dictionary:
            print( mode,': ' + str(dictionary[mode]))


# In[49]:


#Реалицизия класса Particle
W = Particle('W')
W.particlesdecay(100)


# In[50]:


Z = Particle('Z')
Z.particlesdecay(100)


# In[51]:


K = Particle('K+')
K.particlesdecay(100)


# In[ ]:




