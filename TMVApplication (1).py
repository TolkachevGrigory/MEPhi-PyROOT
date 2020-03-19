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


f1 = ROOT.TFile.Open('/eos/user/g/gtolkach/data/mu_plusandminus_6variables.root')
oldtree = f1.Get('NOMINAL')


# In[4]:


#ULong64_t event
#N = background.GetEntries()
#EvaluateMVAB = array('f',N*[0.])
#event = array('i',[0])

#f11 = ROOT.TFile("EvaluateMVATest.root","recreate")
#EvMva = ROOT.TTree("EvMva","Simple Tree")
#EvMva.Branch("EventBranch", event, "EventBranch/I")
#EvMva.Branch("EvaluateMVAB", EvaluateMVAB, "EvaluateMVAB[EventBranch]/F")


# In[5]:


from ROOT import TFile, TTree
from ROOT import gROOT, AddressOf

gROOT.ProcessLine(
"struct MyStruct {\
   Int_t     fEvent;\
   Double_t    fEvMva;\
};" );
 
from ROOT import MyStruct
mystruct = MyStruct()
 
f2 = TFile( '/eos/user/g/gtolkach/data/treeEvMVA_for_mu_plusandminus_6V.root', 'RECREATE' )
tree = TTree( 'EvMvatree', 'Just A Tree' )
tree.Branch( 'event', mystruct, 'fEvent/I' )
tree.Branch( 'EvMva', AddressOf( mystruct, 'fEvMva' ), 'EvMva/F' )


# In[6]:


TMVA.Tools.Instance()
TMVA.PyMethodBase.PyInitialize()
reader = TMVA.Reader( "!Color:!Silent" )


# In[7]:



#branches = {}
#for branch in signal.GetListOfBranches():
#    branchName = branch.GetName()
#    branches[branchName] = array('f', [-999])
#    signal.SetBranchAddress(branchName, branches[branchName])
#    background.SetBranchAddress(branchName, branches[branchName])
#    if branchName != 'EventBranch':
#        reader.AddVariable(branchName, branches[branchName])


# In[8]:


Pt = array('f',[0])
metE = array('f',[0])
dPhi = array('f',[0])
PhiMiss = array('f',[0])
Mt = array('f',[0])
Eta = array('f',[0])
n = oldtree.GetEntries()

#for i in range(0,n):
#	oldtree.GetEntry(i)
#	PT = oldtree.GetLeaf("lep_0_pr.Pt()")


# In[9]:


reader.AddVariable( "Pt", Pt)
oldtree.SetBranchAddress("Pt", Pt )

reader.AddVariable( "metE ",metE)
oldtree.SetBranchAddress("metE", metE )

reader.AddVariable( "dPhi ",dPhi)
oldtree.SetBranchAddress("dPhi", dPhi )

reader.AddVariable( "PhiMiss ",PhiMiss)
oldtree.SetBranchAddress("PhiMiss", PhiMiss )

reader.AddVariable( "Mt", Mt)
oldtree.SetBranchAddress("Mt", Mt )

reader.AddVariable( "Eta",Eta)
oldtree.SetBranchAddress("Eta", Eta )


# In[10]:


reader.BookMVA("MLP",ROOT.TString("/eos/user/g/gtolkach/SWAN_projects/testpy/datasetV6newBDT/weights/TMVAClassification_MLP.weights.xml"))


# In[11]:


#h = ROOT.TH1D("output_s","Blue=Signal, Red=Background;EvaluateMVA;Probability", 20,0, 1.1)


# In[12]:


for i in range(0,n):
    oldtree.GetEntry(i)
    Pt[0] = oldtree.Pt
    metE[0] = oldtree.metE
    dPhi[0] = oldtree.dPhi
    Mt[0] = oldtree.Mt
    Eta[0] = oldtree.Eta
    PhiMiss[0] = oldtree.PhiMiss
#    l = reader.EvaluateMVA("MLP")
#    h.Fill(l)
 #   for write tree
    mystruct.fEvent = i
    mystruct.fEvMva = reader.EvaluateMVA("MLP")
    tree.Fill()


# In[ ]:


f2.Write()


# In[ ]:


#c1 = ROOT.TCanvas() 
#c1.cd()
#h.Draw("hist ")
#c1.Draw()


# In[ ]:


f1.Close()
f2.Close


# In[ ]:


#f2 = ROOT.TFile.Open('/eos/user/g/gtolkach/background_event_with_cuts_plus_1.root')
#f2 = ROOT.TFile.Open('/eos/user/g/gtolkach/background_event_with_cuts_plus_1.root','UPDATE')
#tree = f2.Get('NOMINAL')
#tree.AddFriend("EvMvatree","treefriend.root")
#f2.Write


# In[ ]:


#df = ROOT.ROOT.Experimental.TDataFrame("tree", "treefriend.root");
#df.Snapshot("EvMVA", "/eos/user/g/gtolkach/background_event_with_cuts_plus_1.root", {"EvMva"})


# In[ ]:


#new tree
import ROOT
f1 = ROOT.TFile.Open('/eos/user/g/gtolkach/data/mu_plusandminus_6variables.root')
f2 = ROOT.TFile.Open('/eos/user/g/gtolkach/data/treeEvMVA_for_mu_plusandminus_6V.root')
oldtree1 = f1.Get('NOMINAL')
oldtree2 = f2.Get('EvMvatree')


# In[ ]:


f = ROOT.TFile( '/eos/user/g/gtolkach/data/mu_6variables_and_EvMVAtree.root', 'RECREATE')
oldtree1.CloneTree().Write()
oldtree2.CloneTree().Write()
f.Close()


# In[ ]:


f1.Close()
f2.Close()


# In[ ]:


#oldtree.AddFriend(newtree)
#oldtree.AddFriend('EvMvatree','/eos/user/g/gtolkach/SWAN_projects/testpy/treefriend.root');


# In[ ]:


#oldtree.Write()


# In[ ]:




