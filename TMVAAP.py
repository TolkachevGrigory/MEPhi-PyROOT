#!/usr/bin/env python
# coding: utf-8

# In[1]:



import math 
from ROOT import TMVA, TFile, TString
from array import array
import ROOT


# In[2]:


get_ipython().run_line_magic('jsroot', 'on')


# In[3]:



f1 = ROOT.TFile.Open('/eos/user/g/gtolkach/data/tau_mu_plusandminus_6variables.root')
f2 = ROOT.TFile.Open('/eos/user/g/gtolkach/data/mu_plusandminus_6variables.root')
f3 = ROOT.TFile.Open('/eos/user/g/gtolkach/data/data_mu_6variables.root')

tree1 = f1.Get('NOMINAL')
tree2 = f2.Get('NOMINAL')
tree3 = f3.Get('NOMINAL')


# In[4]:


TMVA.Tools.Instance()
TMVA.PyMethodBase.PyInitialize()
reader = TMVA.Reader( "!Color:!Silent" )


# In[5]:


Pt = array('f',[0])
MetE = array('f',[0])
dPhi = array('f',[0])
PhiMiss = array('f',[0])
Mt = array('f',[0])
Eta = array('f',[0])

reader.AddVariable( "Pt", Pt)
tree1.SetBranchAddress("Pt", Pt)
tree2.SetBranchAddress("Pt", Pt)
tree3.SetBranchAddress("Pt", Pt)

reader.AddVariable( "metE",MetE)
tree1.SetBranchAddress("metE", MetE)
tree2.SetBranchAddress("metE", MetE)
tree3.SetBranchAddress("metE", MetE)

reader.AddVariable( "dPhi",dPhi)
tree1.SetBranchAddress("dPhi", dPhi)
tree2.SetBranchAddress("dPhi", dPhi)
tree3.SetBranchAddress("dPhi", dPhi)

reader.AddVariable( "PhiMiss",PhiMiss)
tree1.SetBranchAddress("PhiMiss", PhiMiss)
tree2.SetBranchAddress("PhiMiss", PhiMiss)
tree3.SetBranchAddress("PhiMiss", PhiMiss)

reader.AddVariable( "Mt", Mt)
tree1.SetBranchAddress("Mt", Mt)
tree2.SetBranchAddress("Mt", Mt)
tree3.SetBranchAddress("Mt", Mt)

reader.AddVariable( "Eta",Eta)
tree1.SetBranchAddress("Eta", Eta)
tree2.SetBranchAddress("Eta", Eta)
tree3.SetBranchAddress("Eta", Eta)


# In[6]:



reader.BookMVA("MLP",ROOT.TString("/eos/user/g/gtolkach/SWAN_projects/testpy/datasetV6newBDT/weights/TMVAClassification_MLP.weights.xml"))


# In[7]:


h1 = ROOT.TH1D("output_s","Blue=Signal, Red=Background;EvaluateMVA;Probability", 100,-0.5, 1.1)
h2 = ROOT.TH1D("output_b","", 100, -0.4, 1.1)
h3 = ROOT.TH1D("output_b","", 100, -0.4, 1.1)


# In[8]:


for i in range(0,tree1.GetEntries()):
    tree1.GetEntry(i)
    Pt[0] = tree1.Pt
    MetE[0] = tree1.metE
    dPhi[0] = tree1.dPhi
    Mt[0] = tree1.Mt
    Eta[0] = tree1.Eta
    PhiMiss[0] = tree1.PhiMiss
    l = reader.EvaluateMVA("MLP")
    h1.Fill(l)


# In[9]:


for i in range(0, tree2.GetEntries()):
    tree2.GetEntry(i)
    Pt[0] = tree2.Pt
    MetE[0] = tree2.metE
    dPhi[0] = tree2.dPhi
    Mt[0] = tree2.Mt
    Eta[0] = tree2.Eta
    PhiMiss[0] = tree2.PhiMiss
    k = reader.EvaluateMVA("MLP")
    h2.Fill(k)


# In[10]:


for i in range(0, tree3.GetEntries()):
    tree3.GetEntry(i)
    Pt[0] = tree3.Pt
    MetE[0] = tree3.metE
    dPhi[0] = tree3.dPhi
    Mt[0] = tree3.Mt
    Eta[0] = tree3.Eta
    PhiMiss[0] = tree3.PhiMiss
    k = reader.EvaluateMVA("MLP")
    h3.Fill(k)


# In[11]:



#h1.Scale(1./h1.Integral())
#h2.Scale(1./h2.Integral())
#h3.Scale(1./h3.Integral())


# In[12]:


c1 = ROOT.TCanvas() 
c1.SetLogy()
c1.cd()

h1.SetLineColor(ROOT.kRed)
h2.SetLineColor(ROOT.kYellow)
h3.Draw("hist")
h2.Draw("hist same")
h1.Draw("hist same")

c1.Draw()


# In[ ]:




