#!/usr/bin/env python
# coding: utf-8

# In[1]:


import ROOT
import sys
import math
get_ipython().run_line_magic('jsroot', 'on')


# In[2]:


f1 = ROOT.TFile.Open('/eos/user/g/gtolkach/minus.1.SM_WLepton.root', 'READ')
f2 = ROOT.TFile.Open('/eos/user/g/gtolkach/minus.6.SM_WLepton.root', 'READ')


# In[3]:


tree_Signal = f1.Get("NOMINAL")
tree_Beack = f2.Get("NOMINAL")


# In[4]:


h1 = ROOT.TH1F("enu", "W #rightarrow e #nu_{e};m_{T} [GeV];Normalized Units", 150, 0, 200);
h2 = ROOT.TH1F("munu", "W #rightarrow #mu #nu_{#mu};m_{T} [GeV];Normalized Units", 150, 0, 200);
h1.SetDirectory(0)
h2.SetDirectory(0)


# In[5]:


N = tree_Signal.GetEntries()
for i in range(0, N):
    tree_Signal.GetEntry(i)
    Mt_S = (2*tree_Signal.lep_0_p4.Pt()*tree_Signal.met_reco_p4.Pt()*(1-math.cos(tree_Signal.lep_0_p4.Phi() - tree_Signal.met_reco_p4.Phi())))**(0.5)
    h1.Fill(Mt_S)


# In[6]:


K = tree_Beack.GetEntries()
for i in range(0, K):
    tree_Beack.GetEntry(i)
    Mt_B = (2*tree_Beack.lep_0_p4.Pt()*tree_Beack.met_reco_p4.Pt()*(1-math.cos(tree_Beack.lep_0_p4.Phi() - tree_Beack.met_reco_p4.Phi())))**(0.5)
    h2.Fill(Mt_B)


# In[21]:


c1 = ROOT.TCanvas()
ROOT.gStyle.SetOptTitle(False)
ROOT.gStyle.SetOptStat(False)
f1.Close()
f2.Close()


# In[25]:


norm = 1
h1.Scale(norm/h1.Integral(), "width")
h2.Scale(norm/h2.Integral(), "width")
h1.SetLineColor(2)
h2.Draw("HIST")
h1.Draw("HIST SAME")
c1.Update()
c1.Draw()
ROOT.gPad.BuildLegend(1.0,0.8,0.8,0.5,"","")


# In[ ]:


