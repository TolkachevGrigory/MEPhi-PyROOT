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


h_e_pt = ROOT.TH1F("e_pt", "e^{#minus} ;P_{T} [GeV];Normalized Units", 50, 20, 120)
h_e_phi_minus = ROOT.TH1F("e_phi", "e^{#minus};d#varphi (l-E^{miss}_{T}) ;Normalized Units", 50, 0, 4)
h_emet_energy = ROOT.TH1F("e_energy", "#bar{#nu}_{e};E [GeV];Normalized Units", 50, 20, 120)
h_enu_mt = ROOT.TH1F("e_mt", "W^{#minus} #rightarrow e^{#minus} #plus #bar{#nu}_{e};m_{T} [GeV];Normalized Units", 50, 30, 170); 
h_e_eta = ROOT.TH1F("e_eta", "e^{#minus};#eta ;Normalized Units", 100, -3,3)
h_e_phi = ROOT.TH1F("phi", "e^{#minus};#varphi ;Normalized Units", 100, -4, 4)
h_emet_phi = ROOT.TH1F("emet_phi", " #bar{#nu}_{e};#varphi ;Normalized Units", 100, -4, 4)
  
h_mu_pt = ROOT.TH1F("mu_pt", "#mu^{#minus} ;P_{T} [GeV];Normalized Units", 50, 20, 120)
h_mu_phi_minus = ROOT.TH1F("mu_phi", "#mu^{#minus};d#varphi (l-E^{miss}_{T}) ;Normalized Units", 50, 0, 4)
h_mumet_energy = ROOT.TH1F("met_energy", "#bar{#nu}_{#mu};E [GeV];Normalized Units", 50, 20, 120)
h_munu_mt = ROOT.TH1F("mu_mt", "W^{#minus} #rightarrow #mu^{#minus} #plus #bar{#nu}_{#mu};m_{T} [GeV];Normalized Units", 50, 30, 170)
h_mu_eta = ROOT.TH1F("mu_eta", "#mu^{#minus};#eta ;Normalized Units", 100, -3, 3)
h_mu_phi = ROOT.TH1F("phi", "#mu^{#minus};#varphi ;Normalized Units", 100, -4, 4)
h_mumet_phi = ROOT.TH1F("mu_metphi", "#bar{#nu}_{#mu};#varphi ;Normalized Units", 100, -4, 4)

h_e_pt.SetDirectory(0)
h_e_eta.SetDirectory(0)
h_e_phi_minus.SetDirectory(0)
h_e_phi.SetDirectory(0)
h_emet_phi.SetDirectory(0)
h_emet_energy.SetDirectory(0)
h_enu_mt.SetDirectory(0)

h_mu_pt.SetDirectory(0) 
h_mu_eta.SetDirectory(0)
h_mu_phi.SetDirectory(0)
h_mu_phi_minus.SetDirectory(0)
h_mumet_phi.SetDirectory(0)
h_mumet_energy.SetDirectory(0)
h_munu_mt.SetDirectory(0)


# In[5]:


N = tree_Signal.GetEntries()
for i in range(0, N):
    tree_Signal.GetEntry(i)
    Mt_S = (2*tree_Signal.lep_0_p4.Pt()*tree_Signal.met_reco_p4.Pt()*(1-math.cos(tree_Signal.lep_0_p4.Phi() - tree_Signal.met_reco_p4.Phi())))**(0.5)
    if not(((tree_Signal.n_electrons + tree_Signal.n_muons) == 1 and tree_Signal.n_taus == 0)):
        continue
    if not((math.fabs(tree_Signal.lep_0_p4.Eta()) < 1.37 or math.fabs(tree_Signal.lep_0_p4.Eta()) > 1.52) and math.fabs(tree_Signal.lep_0_p4.Eta()) < 2.47):
        continue
        
    # Cut for QCD
    if  not(tree_Signal.lep_0_p4.Pt() > 25):
        continue
    if  not(tree_Signal.lep_0_p4.E() > 25):
        continue
    if  not(Mt_S) > 40:
        continue
    if  not(tree_Signal.lep_0_id_medium == 1):
        continue
    if  not(tree_Signal.lep_0_iso_FCTight == 1):
        continue
    if  not(tree_Signal.n_bjets == 0):
        continue
        
    h_e_pt.Fill(tree_Signal.lep_0_p4.Pt())
    h_e_eta.Fill(tree_Signal.lep_0_p4.Eta())
    h_e_phi.Fill(tree_Signal.lep_0_p4.Phi())
       
      
    h_emet_phi.Fill(tree_Signal.met_reco_p4.Phi())
    h_emet_energy.Fill(tree_Signal.met_reco_p4.E());
    h_enu_mt.Fill(Mt_S);
    
    phi_e = (tree_Signal.lep_0_p4.Phi()-tree_Signal.met_reco_p4.Phi())
    if math.fabs(phi_e) > 3.14159:
        phi_e = 2*3.14159 - phi_e
        h_e_phi_minus.Fill(phi_e)
    else:
        h_e_phi_minus.Fill(phi_e)


# In[6]:


K = tree_Beack.GetEntries()
for i in range(0, K):
    tree_Beack.GetEntry(i)
    Mt_B = (2*tree_Beack.lep_0_p4.Pt()*tree_Beack.met_reco_p4.Pt()*(1-math.cos(tree_Beack.lep_0_p4.Phi() - tree_Beack.met_reco_p4.Phi())))**(0.5)
    if not(((tree_Beack.n_electrons + tree_Beack.n_muons) == 1 and tree_Beack.n_taus == 0)):
        continue
    if not((math.fabs(tree_Beack.lep_0_p4.Eta()) < 1.37 or math.fabs(tree_Beack.lep_0_p4.Eta()) > 1.52) and math.fabs(tree_Beack.lep_0_p4.Eta()) < 2.47):
        continue
        
    # Cut for QCD
    if  not(tree_Beack.lep_0_p4.Pt() > 25):
        continue
    if  not(tree_Beack.lep_0_p4.E() > 25):
        continue
    if  not(Mt_B) > 40:
        continue
    if  not(tree_Beack.lep_0_id_medium == 1):
        continue
    if  not(tree_Beack.lep_0_iso_FCTight == 1):
        continue
    if  not(tree_Beack.n_bjets == 0):
        continue
        
    h_mu_pt.Fill(tree_Beack.lep_0_p4.Pt())
    h_mu_eta.Fill(tree_Beack.lep_0_p4.Eta())
    h_mu_phi.Fill(tree_Beack.lep_0_p4.Phi())
       
      
    h_mumet_phi.Fill(tree_Beack.met_reco_p4.Phi())
    h_mumet_energy.Fill(tree_Beack.met_reco_p4.E());
    h_munu_mt.Fill(Mt_B);
    
    phi_mu = (tree_Beack.lep_0_p4.Phi()-tree_Beack.met_reco_p4.Phi())
    if math.fabs(phi_mu) > 3.14159:
        phi_mu = 2*3.14159 - phi_mu
        h_mu_phi_minus.Fill(phi_mu)
    else:
        h_mu_phi_minus.Fill(phi_mu)


# In[24]:


c1 = ROOT.TCanvas()
c2 = ROOT.TCanvas()




f1.Close()
f2.Close()


# In[28]:


norm = 1

h_e_pt.Scale(norm/h_e_pt.Integral(), "width")
h_mu_pt.Scale(norm/h_mu_pt.Integral(), "width")

h_mu_pt.SetLineColor(57)
h_mu_pt.SetMarkerStyle (21)
h_mu_pt.SetMarkerSize (0.2)
h_mu_pt.SetFillStyle(4050)
h_mu_pt.SetFillColor(64)
h_mu_pt.Draw("HIST")
h_mu_pt.GetYaxis().SetRangeUser(0., 0.08);
h_mu_pt.Draw("E same")

h_e_pt.SetLineColor(102)
     #  h_mu_pt->Sumw2()
h_e_pt.SetMarkerStyle (21)
h_e_pt.SetMarkerSize (0.2)
h_e_pt.SetFillColor(2)
h_e_pt.SetFillStyle(3354)
h_e_pt.Draw("HIST  E same")

c1.Update()
c1.Draw()


h_e_phi_minus.Scale(norm/h_e_phi_minus.Integral(), "width")
h_mu_phi_minus.Scale(norm/h_mu_phi_minus.Integral(), "width")

h_mu_phi_minus.SetLineColor(57)
h_mu_phi_minus.Sumw2()
h_mu_phi_minus.SetMarkerStyle (21) 
h_mu_phi_minus.SetMarkerSize (0.2)
h_mu_phi_minus.SetFillStyle(4050)
h_mu_phi_minus.SetFillColor(64)
h_mu_phi_minus.Draw("HIST")
h_mu_phi_minus.GetYaxis().SetRangeUser(0., 4.0);
h_mu_phi_minus.Draw("E same ")

h_e_phi_minus.SetLineColor(102)
# h_e_phi_minus->Sumw2()
h_e_phi_minus.SetMarkerStyle (21)
h_e_phi_minus.SetMarkerSize (0.2)
h_e_phi_minus.SetFillColor(2)
h_e_phi_minus.SetFillStyle(3354)
h_e_phi_minus.Draw("HIST E same ")

c2.Update()
c2.Draw()



# In[ ]:




