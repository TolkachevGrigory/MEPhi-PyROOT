#!/usr/bin/env python
# coding: utf-8

# In[1]:



import math 
from ROOT import TMVA, TFile, TString
from array import array
import ROOT


# In[2]:


TMVA.Tools.Instance()
TMVA.PyMethodBase.PyInitialize()
reader = TMVA.Reader( "!Color:!Silent" )

Pt = array('f',[0])
MetE = array('f',[0])
dPhi = array('f',[0])
PhiMiss = array('f',[0])
Mt = array('f',[0])
Eta = array('f',[0])

reader.AddVariable( "Pt", Pt)
reader.AddVariable( "metE",MetE)
reader.AddVariable( "dPhi",dPhi)
reader.AddVariable( "PhiMiss",PhiMiss)
reader.AddVariable( "Mt", Mt)
reader.AddVariable( "Eta",Eta)
reader.BookMVA("MLP",ROOT.TString("/eos/user/g/gtolkach/SWAN_projects/testpy/datasetV6newBDT/weights/TMVAClassification_MLP.weights.xml"))


# In[3]:


f1 = ROOT.TFile.Open('/eos/user/g/gtolkach/data/tau_mu_plusandminus_6variables_and_luminosity.root')
f2 = ROOT.TFile.Open('/eos/user/g/gtolkach/data/data_mu_6variables_and_charge_minus.root')
f3 = ROOT.TFile.Open('/eos/user/g/gtolkach/data/mu_plusandminus_6variables_and_luminosity.root')


# In[40]:


def rew(file, tp):
    
    tree = file.Get('NOMINAL')
    tree.SetBranchAddress("Pt", Pt)
    tree.SetBranchAddress("metE", MetE)
    tree.SetBranchAddress("dPhi", dPhi)
    tree.SetBranchAddress("PhiMiss", PhiMiss)
    tree.SetBranchAddress("Mt", Mt)
    tree.SetBranchAddress("Eta", Eta)
    
    h = ROOT.TH1D("h","", 20,-0.1, 1.1)
    print(type(h))
    print (tp.find('data'))
    if tp.find('data') == -1:
        h1 = file.Get('h_metadata')
        bin_8 = h1.GetBinContent(8)
        print(bin_8)
        kfactor =  11.246151648051285
        lumi2015 = 3219.56  # pb-1
        for i in range(0,tree.GetEntries()):
            tree.GetEntry(i)
            Pt[0] = tree.Pt
            MetE[0] = tree.metE
            dPhi[0] = tree.dPhi
            Mt[0] = tree.Mt
            Eta[0] = tree.Eta
            PhiMiss[0] = tree.PhiMiss
            l = reader.EvaluateMVA("MLP")
            h.Fill(l,tree.NOMINAL_pileup_combined_weight*tree.cross_section*tree.filter_efficiency*kfactor*lumi2015/bin_8)
            #print(tree.NOMINAL_pileup_combined_weight*tree.cross_section*tree.filter_efficiency*tree.kfactor/bin_8)
    else:
        for i in range(0,tree.GetEntries()):
            tree.GetEntry(i)
            Pt[0] = tree.Pt
            MetE[0] = tree.metE
            dPhi[0] = tree.dPhi
            Mt[0] = tree.Mt
            Eta[0] = tree.Eta
            PhiMiss[0] = tree.PhiMiss
            l = reader.EvaluateMVA("MLP")
            h.Fill(l)
    return h


# In[41]:


h_mc_wtau = rew(f1, 'dd')


# In[33]:


h_data = rew(f2, 'data')


# In[42]:


h_mc_wmu = rew(f3, 'dd')


# In[8]:


#c1 = ROOT.TCanvas() 
#c1.SetLogy()
#c1.cd()
#h_mc_wmu.SetLineColor(ROOT.kRed)
#h_mc_wtau.SetLineColor(ROOT.kYellow)
#h_data.Draw('hist')
#h_mc_wmu.Draw('hist ')
#h_mc_wtau.Draw('hist same')
#c1.Draw()


# In[43]:


c1 = ROOT.TCanvas() 
c1.Divide(1, 2)
c1.SetLogy()
ROOT.gStyle.SetOptStat(0)
c1.cd()
gPad = c1.cd(1)
gPad.SetLogy()


h_mc_wtau.SetLineColor(ROOT.kRed)
h_mc_wmu.SetLineColor(ROOT.kYellow)

h_mc_wmu.SetTitle("mc_wmu")
h_data.SetTitle('data')
h_mc_wtau.SetTitle("mc_wtau")

h_data.Draw("hist ")
h_mc_wtau.Draw("hist same")
h_mc_wmu.Draw("hist same")



ROOT.gPad.BuildLegend(1.0,0.8,0.8,0.5,"","")
h_add = ROOT.TH1D("add","", 20, -0.1, 1.1)
h_divide = ROOT.TH1D("divide","", 20, -0.1, 1.1)
h_add.Add(h_mc_wtau, h_mc_wmu, 1, 1)
h_divide.Divide(h_data, h_add, 1, 1)
c1.cd(2)
h_divide.Draw("E1")
c1.Update()
c1.Draw()
h_add.Add(h_mc_wtau, h_mc_wmu, 1, 1)
h_divide.Divide(h_data, h_add, 1, 1)
c1.cd(2)
h_divide.Draw("E1")
c1.Update()
c1.Draw()


# In[ ]:




