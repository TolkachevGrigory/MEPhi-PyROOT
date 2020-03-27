#!/usr/bin/env python
# coding: utf-8

# In[1]:


import ROOT
from ROOT import TFile, TTree
from ROOT import gROOT, AddressOf
import math 


# In[2]:


def rewrite_tree(oldfile, newname):
    f = ROOT.TFile.Open(oldfile)
    oldtree = f.Get('NOMINAL')
    gROOT.ProcessLine(
    "struct MyStruct {\
       Int_t     fEvent;\
       Double_t    fNOMINAL_pileup_combined_weight;\
       Double_t    fcross_section;\
       Double_t    ffilter_efficiency;\
       Double_t    fkfactor;\
       Double_t    fweight_mc;\
       Double_t    fPt;\
       Double_t    fmetE;\
       Double_t    fdPhi;\
       Double_t    fPhiMiss;\
       Double_t    fMt;\
       Double_t    fEta;\
    };" );
    from ROOT import MyStruct
    mystruct = MyStruct()
    f1 = TFile( '/eos/user/g/gtolkach/data/' + newname , 'RECREATE' )
    tree = TTree( 'NOMINAL', 'Just A Tree' )
    tree.Branch( 'event', mystruct, 'fEvent/I' )
    
    if oldfile.find('data_mu') == -1:
        tree.Branch( 'NOMINAL_pileup_combined_weight', AddressOf( mystruct, 'fNOMINAL_pileup_combined_weight' ), 'fNOMINAL_pileup_combined_weight/D' )
        tree.Branch( 'cross_section', AddressOf( mystruct, 'fcross_section' ), 'fcross_section/D' )
        tree.Branch( 'filter_efficiency', AddressOf( mystruct, 'ffilter_efficiency' ), 'ffilter_efficiency/D' )
        tree.Branch( 'kfactor', AddressOf( mystruct, 'fkfactor' ), 'fkfactor/D' )
        tree.Branch( 'kweight_mc', AddressOf( mystruct, 'fweight_mc' ), 'fweight_mc/D' )
        
    tree.Branch( 'Pt', AddressOf( mystruct, 'fPt' ), 'fPt/D' )
    tree.Branch( 'metE', AddressOf( mystruct, 'fmetE' ), 'fmetE/D' )
    tree.Branch( 'dPhi', AddressOf( mystruct, 'fdPhi' ), 'fdPhi/D' )
    tree.Branch( 'PhiMiss', AddressOf( mystruct, 'fPhiMiss' ), 'fPhiMiss/D' )
    tree.Branch( 'Mt', AddressOf( mystruct, 'fMt' ), 'fMt/D' )
    tree.Branch( 'Eta', AddressOf( mystruct, 'fEta' ), 'fEta/D' )
    
    cutflowhisto = ROOT.TH1D("cutflow",";Cut;Event", 5, 1, 6 );
    cutflowhisto.GetXaxis().SetBinLabel(1,"All");
    cutflowhisto.GetXaxis().SetBinLabel(2,"charge");
    cutflowhisto.GetXaxis().SetBinLabel(3,"medium ");
    cutflowhisto.GetXaxis().SetBinLabel(4,"isoTight");
    cutflowhisto.GetXaxis().SetBinLabel(5,"n_bjets");
    

    
   
    
        
    for i in range(0, oldtree.GetEntries()):
#    for i in range(0, 60000):    
        oldtree.GetEntry(i)
        mystruct.fEvent = i
        cutflowhisto.Fill(1)
        #cuts
        if not(oldtree.lep_0_q == -1):
            continue
        cutflowhisto.Fill(2)
        if not(oldtree.lep_0_id_medium == 1):
            continue
        cutflowhisto.Fill(3)
        
        if not(oldtree.lep_0_iso_FCTight == 1):
            continue
            
        cutflowhisto.Fill(4)
        if not(oldtree.n_bjets == 0):
            continue
        cutflowhisto.Fill(5)
        
        
        
#        if oldfile.find('data_mu') != -1:
#            if not(oldtree.lep_0_q == -1):
#                continue
#            print(oldtree.lep_0_q)
#            mystruct.fPt = oldtree.lep_0_p4_fast.Pt()
#            mystruct.fmetE = oldtree.met_reco_p4_fast.E()
#            if math.fabs(oldtree.lepmet_dphi) > 3.14159:
#                 mystruct.fdPhi = 2*3.14159 - math.fabs(oldtree.lepmet_dphi)
#            else:
#                mystruct.fdPhi = math.fabs(oldtree.lepmet_dphi)
#            mystruct.fPhiMiss = oldtree.met_reco_p4_fast.Phi()
#            mystruct.fMt = oldtree.lepmet_mt
#            mystruct.fEta = oldtree.lep_0_p4_fast.Eta()
#            
#        if oldfile.find('data_mu') == -1:         
#        mystruct.fNOMINAL_pileup_combined_weight = oldtree.NOMINAL_pileup_combined_weight
#        mystruct.fcross_section = oldtree.cross_section
#        mystruct.ffilter_efficiency = oldtree.filter_efficiency
#        mystruct.fkfactor = oldtree.kfactor
#        mystruct.fweight_mc = oldtree.weight_mc
        mystruct.fPt = oldtree.lep_0_p4_fast.Pt()
        mystruct.fmetE = oldtree.met_reco_p4_fast.E()
        if math.fabs(oldtree.lepmet_dphi) > 3.14159:
            mystruct.fdPhi = 2*3.14159 - math.fabs(oldtree.lepmet_dphi)
        else:
            mystruct.fdPhi = math.fabs(oldtree.lepmet_dphi)
        mystruct.fPhiMiss = oldtree.met_reco_p4_fast.Phi()
        mystruct.fMt = oldtree.lepmet_mt
        mystruct.fEta = oldtree.lep_0_p4_fast.Eta()
        
        tree.Fill()
    if oldfile.find('data_mu') == -1:
        h_metadata = f.Get('h_metadata')
        h_metadata.Write()
    c1 = ROOT.TCanvas() 
    cutflowhisto.Draw()
    c1.Draw()
    c1.SaveAs('hist.pdf')
    
    f1.Write()
    f.Close()
    f1.Close()


# In[ ]:





# In[3]:


#rewrite_tree('/eos/user/g/gtolkach/data/tau_mu_plusandminus.root', 'tau_mu_plusandminus_6variables_and_luminosity_cuts.root')


# In[4]:


#rewrite_tree('/eos/user/g/gtolkach/data/mu_plusandminus.root', 'mu_plusandminus_6variables_and_luminosity_CUTS.root')


# In[5]:


rewrite_tree('/eos/user/g/gtolkach/data/data_mu.root', 'data_mu_6variables_and_charge_minus_cuts.root')


# In[ ]:




