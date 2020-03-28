#!/usr/bin/env python
# coding: utf-8

# In[1]:


import math 
from ROOT import TMVA, TFile, TString
from array import array
import ROOT


# In[2]:


f1 = ROOT.TFile.Open('/eos/user/g/gtolkach/data/tau_mu_plusandminus.root')
f2 = ROOT.TFile.Open('/eos/user/g/gtolkach/data/data_mu.root')
f3 = ROOT.TFile.Open('/eos/user/g/gtolkach/data/mu_plusandminus.root')


# In[3]:


def rew(file, tp):
    
    tree = file.Get('NOMINAL')
    
    cutflowhisto = ROOT.TH1D("cutflow",";Cut;Event", 12, 1, 13);
    cutflowhisto.GetXaxis().SetBinLabel(1,"All")
    cutflowhisto.GetXaxis().SetBinLabel(2,"Pt > 25")
    cutflowhisto.GetXaxis().SetBinLabel(3,"E > 25")
    cutflowhisto.GetXaxis().SetBinLabel(4,"Mt > 40")
    cutflowhisto.GetXaxis().SetBinLabel(5,"|Eta| < 2.4")
    cutflowhisto.GetXaxis().SetBinLabel(6,"id tight = 1")
    cutflowhisto.GetXaxis().SetBinLabel(7,"Trigger")
    cutflowhisto.GetXaxis().SetBinLabel(8,"lep_0 = 1")
    cutflowhisto.GetXaxis().SetBinLabel(9," bjets = 0") 
    cutflowhisto.GetXaxis().SetBinLabel(10," e+mu=1 and t = 0")   
    cutflowhisto.GetXaxis().SetBinLabel(11," lep_0_iso_FCTight = 1")   
    cutflowhisto.GetXaxis().SetBinLabel(12,"run number < 284485")
    
    h = ROOT.TH1D("h","", 50,0, 120)
    print (tp.find('data'))
    
    if tp.find('data') == -1:
        h1 = file.Get('h_metadata')
        bin_8 = h1.GetBinContent(8)
        print(bin_8)
        kfactor =  11.246151648051285
        lumi2015 = 3219.56  # pb-1
        
        for i in range(0,tree.GetEntries()):
            tree.GetEntry(i)
            cutflowhisto.Fill(1)
        #cuts
            if not(tree.lep_0_p4_fast.Pt()>25):
                continue
            cutflowhisto.Fill(2)
            if not(tree.met_reco_p4_fast.E()>25):
                continue
            cutflowhisto.Fill(3)
        
            if not(tree.lepmet_mt>40):
                continue
            cutflowhisto.Fill(4)
        
            if not(math.fabs(tree.lep_0_p4_fast.Eta())<2.4):
                continue
            cutflowhisto.Fill(5)
        
            if not(tree.lep_0_id_tight==1):
                continue
            cutflowhisto.Fill(6)
        
            if not(((tree.HLT_mu20_iloose_L1MU15 and tree.muTrigMatch_0_HLT_mu20_iloose_L1MU15) or (tree.HLT_mu50 and tree.muTrigMatch_0_HLT_mu50))>0):
                continue
            cutflowhisto.Fill(7)
        
            if not(tree.lep_0 == 1):
                continue
            cutflowhisto.Fill(8)
        
            if not(tree.n_bjets == 0):
                continue
            cutflowhisto.Fill(9) 
        
            if not((tree.n_electrons+tree.n_muons)==1 and tree.n_taus==0):
                continue
            cutflowhisto.Fill(10)   
        
            if not(tree.lep_0_iso_FCTight==1):
                continue
            cutflowhisto.Fill(11) 
            if not(tree.NOMINAL_pileup_random_run_number<284485):
                continue
            cutflowhisto.Fill(12) 

            h.Fill(tree.lep_0_p4_fast.Pt(),tree.weight_mc*tree.NOMINAL_pileup_combined_weight*tree.cross_section*tree.filter_efficiency*tree.kfactor*kfactor*lumi2015/bin_8)
        
    else:
        for i in range(0,tree.GetEntries()):
            tree.GetEntry(i)
            cutflowhisto.Fill(1)
            if not(tree.lep_0_p4_fast.Pt()>25):
                continue
            cutflowhisto.Fill(2)
            if not(tree.met_reco_p4_fast.E()>25):
                continue
            cutflowhisto.Fill(3)
        
            if not(tree.lepmet_mt>40):
                continue
            cutflowhisto.Fill(4)
        
            if not(math.fabs(tree.lep_0_p4_fast.Eta())<2.4):
                continue
            cutflowhisto.Fill(5)
        
            if not(tree.lep_0_id_tight==1):
                continue
            cutflowhisto.Fill(6)
        
            if not(((tree.HLT_mu20_iloose_L1MU15 and tree.muTrigMatch_0_HLT_mu20_iloose_L1MU15) or (tree.HLT_mu50 and tree.muTrigMatch_0_HLT_mu50))>0):
                continue
            cutflowhisto.Fill(7)
        
            if not(tree.lep_0 == 1):
                continue
            cutflowhisto.Fill(8)
        
            if not(tree.n_bjets == 0):
                continue
            cutflowhisto.Fill(9) 
        
            if not((tree.n_electrons+tree.n_muons)==1 and tree.n_taus==0):
                continue
            cutflowhisto.Fill(10)   
        
            if not(tree.lep_0_iso_FCTight==1):
                continue
            cutflowhisto.Fill(11) 
            if not(tree.run_number<284485):
                continue
            cutflowhisto.Fill(12) 

            h.Fill(tree.lep_0_p4_fast.Pt())
    c1 = ROOT.TCanvas() 
    cutflowhisto.Draw()
    c1.Draw()
    c1.SaveAs('cutflow_' +str(tp) + '.pdf')
    
    return h


# In[4]:


h_pt_mc_wtau = rew(f1, 'wtau')


# In[5]:


h_pt_data = rew(f2, 'data')


# In[6]:


h_pt_mc_wmu = rew(f3, 'wmu')

c3 = ROOT.TCanvas() 
c3.Divide(1, 2)
#c1.SetLogy()
ROOT.gStyle.SetOptStat(0)
c3.cd(1)
#gPad = c1.cd(1)
#gPad.SetLogy()


h_pt_mc_wtau.SetLineColor(ROOT.kRed)
h_pt_mc_wmu.SetLineColor(ROOT.kYellow)

h_pt_mc_wmu.SetTitle("mc_wmu")
h_pt_data.SetTitle('data')
h_pt_mc_wtau.SetTitle("mc_wtau")

h_pt_data.Draw("hist ")
h_pt_mc_wtau.Draw("hist same")
h_pt_mc_wmu.Draw("hist same")


ROOT.gPad.BuildLegend(1.0,0.8,0.8,0.5,"","")
h_add = ROOT.TH1D("add","",  50,0, 120)
h_divide = ROOT.TH1D("divide","",  50,0, 120)
h_add.Add(h_pt_mc_wtau, h_pt_mc_wmu, 1, 1)
h_divide.Divide(h_pt_data, h_add, 1, 1)
c3.cd(2)
h_divide.Draw("E1")
c3.Update()

c3.Draw()


# In[13]:


c3.SaveAs('1234.pdf')


# In[ ]:




