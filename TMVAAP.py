#!/usr/bin/env python
# coding: utf-8

# In[1]:



import math 
from ROOT import gPad
from ROOT import TMVA, TFile, TString
from array import array
import ROOT
import os


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


# In[36]:


#f1 = ROOT.TFile.Open('/eos/user/g/gtolkach/NEWDATA/data_mu_6variables_forMVA.root')


# In[37]:


#f2 = ROOT.TFile.Open('/eos/user/g/gtolkach/NEWDATA/Wmu_plus_6v_forMVA.root')
#f3 = ROOT.TFile.Open('/eos/user/g/gtolkach/NEWDATA/Wmu_minus_6v_forMVA.root')


# In[38]:


#f4 = ROOT.TFile.Open('/eos/user/g/gtolkach/NEWDATA/plus_Wtau_6v_forMVA.root')
#f5 = ROOT.TFile.Open('/eos/user/g/gtolkach/NEWDATA/minus_Wtau_6v_forMVA.root')


# In[39]:


#f1 = ROOT.TFile.Open('/eos/user/g/gtolkach/NEWDATA/Data/data_mu.root')
#f2 = ROOT.TFile.Open('/eos/user/g/gtolkach/NEWDATA/Wmu_plus_6v_forMVA.root')
#f3 = ROOT.TFile.Open('/eos/user/g/gtolkach/NEWDATA/mu/Wmu_minus.root')
#f4 = ROOT.TFile.Open('/eos/user/g/gtolkach/NEWDATA/tau/plus_wtau.root')
#f5 = ROOT.TFile.Open('/eos/user/g/gtolkach/NEWDATA/tau/minus_Wtau.root')


#f1 ='/eos/user/g/gtolkach/NEWDATA/Data/data_mu.root'
#f2 = '/eos/user/g/gtolkach/NEWDATA/mu/Wmu_plus.root'
#f3 ='/eos/user/g/gtolkach/NEWDATA/mu/Wmu_minus.root'
#f4 = '/eos/user/g/gtolkach/NEWDATA/tau/plus_wtau.root'
#f5 = '/eos/user/g/gtolkach/NEWDATA/tau/minus_Wtau.root'


# In[3]:


def rew(filename, tp):
    
    #f1 = ROOT.TFile.Open(filename)
    #tree = f1.Get('NOMINAL')
   
    
    h = ROOT.TH1D("h","", 30, -0.5, 1.2 )
    h.SetDirectory(0)
    print(type(h))
    print (tp.find('data'))
    tree = ROOT.TChain('NOMINAL')
    tree.Add(filename + '/*.root' )
    if tp.find('data') == -1:
        bin_8 = 0 
        for file in os.listdir(filename):
            f = ROOT.TFile.Open(filename+'/'+ file)
            h_8bin = f.Get('h_metadata')
            bin_8+= h_8bin.GetBinContent(8)
    
        print(bin_8)
        kfactor =  11.246151648051285
        lumi2015 = 3219.56  # pb-1
        for i in range(0,int(tree.GetEntries())):
            tree.GetEntry(i)
            if not(tree.lep_0==1):
                continue
            if not(tree.met_reco_p4_fast.E()>25):
                continue
            if not(tree.lep_0_p4_fast.Pt()>27):
                continue    
            if not(tree.lepmet_mt>40):
                continue
            if not(math.fabs(tree.lep_0_p4_fast.Eta())<2.4):
                continue
            if not(((tree.HLT_mu20_iloose_L1MU15 and tree.muTrigMatch_0_HLT_mu20_iloose_L1MU15) or (tree.HLT_mu50 and tree.muTrigMatch_0_HLT_mu50))>0):
                continue
            if not(tree.n_bjets == 0):
                continue
            if not(tree.lep_0_id_tight==1):
                continue
            if not((tree.lep_0_iso_ptcone20_TightTTVA_pt1000/(tree.lep_0_p4_fast.Pt()*1000))<0.06):
                continue
            if not((tree.n_electrons+tree.n_muons)==1 and tree.n_taus==0):
                continue
            if not(tree.lep_0_iso_FCTight==1):
                continue
            if not(tree.NOMINAL_pileup_random_run_number<284485):
                continue
            Pt[0] = tree.lep_0_p4_fast.Pt()
            MetE[0] = tree.met_reco_p4.E()
            if math.fabs(tree.lepmet_dphi)> math.pi:
                dPhi[0] = 2*math.pi-math.fabs(tree.lepmet_dphi)
            else:
                dPhi[0] = math.fabs(tree.lepmet_dphi)
                
            Mt[0] = tree.lepmet_mt
            Eta[0] = tree.lep_0_p4_fast.Eta()
            PhiMiss[0] = tree.met_reco_p4.Phi()
            
            l = reader.EvaluateMVA("MLP")
            #weight = tree.weight_mc*tree.cross_section*tree.filter_efficiency*tree.kfactor*tree.NOMINAL_pileup_combined_weight*tree.lep_0_NOMINAL_MuEffSF_TTVA*tree.jet_NOMINAL_global_effSF_MV2c10*tree.jet_NOMINAL_global_ineffSF_MV2c10*tree.jet_NOMINAL_central_jets_global_effSF_JVT*tree.jet_NOMINAL_central_jets_global_ineffSF_JVT*tree.lep_0_NOMINAL_MuEffSF_Reco_QualMedium*tree.lep_0_NOMINAL_MuEffSF_IsoFCLoose*tree.lep_0_NOMINAL_MuEffSF_HLT_mu20_iloose_L1MU15_OR_HLT_mu50_QualMedium_IsoNone*tree.jet_NOMINAL_forward_jets_global_effSF_JVT*tree.jet_NOMINAL_forward_jets_global_ineffSF_JVT*kfactor*lumi2015/bin_8
            weight = (tree.weight_mc*(tree.cross_section*tree.filter_efficiency*tree.kfactor))*(((((((((tree.NOMINAL_pileup_combined_weight)*(tree.lep_0_NOMINAL_MuEffSF_TTVA))*(tree.lep_0_NOMINAL_MuEffSF_IsoFCTight))*(tree.jet_NOMINAL_global_effSF_MV2c10*tree.jet_NOMINAL_global_ineffSF_MV2c10))*(tree.jet_NOMINAL_central_jets_global_effSF_JVT*tree.jet_NOMINAL_central_jets_global_ineffSF_JVT))*(tree.lep_0_NOMINAL_MuEffSF_Reco_QualMedium))*(1))*((tree.lep_0_NOMINAL_MuEffSF_HLT_mu20_iloose_L1MU15_OR_HLT_mu50_QualMedium_IsoNone)))*(tree.jet_NOMINAL_forward_jets_global_effSF_JVT*tree.jet_NOMINAL_forward_jets_global_ineffSF_JVT))*kfactor*lumi2015/bin_8
            #weight1 = tree.weight_mc*tree.NOMINAL_pileup_combined_weight*tree.cross_section*tree.filter_efficiency*kfactor*lumi2015/bin_8
            h.Fill(l,weight)
            #print(tree.NOMINAL_pileup_combined_weight*tree.cross_section*tree.filter_efficiency*tree.kfactor/bin_8)
    else:
        for i in range(0,int(tree.GetEntries())):
            tree.GetEntry(i)
            if not(tree.lep_0==1):
                continue
            if not(tree.met_reco_p4_fast.E()>25):
                continue
            if not(tree.lep_0_p4_fast.Pt()>27):
                continue    
            if not(tree.lepmet_mt>40):
                continue
            if not(math.fabs(tree.lep_0_p4_fast.Eta())<2.4):
                continue
            if not(((tree.HLT_mu20_iloose_L1MU15 and tree.muTrigMatch_0_HLT_mu20_iloose_L1MU15) or (tree.HLT_mu50 and tree.muTrigMatch_0_HLT_mu50))>0):
                continue
            if not(tree.n_bjets == 0):
                continue
            if not(tree.lep_0_id_tight==1):
                continue
            if not((tree.lep_0_iso_ptcone20_TightTTVA_pt1000/(tree.lep_0_p4_fast.Pt()*1000))<0.06):
                continue
            if not((tree.n_electrons+tree.n_muons)==1 and tree.n_taus==0):
                continue
            if not(tree.lep_0_iso_FCTight==1):
                continue
            if not(tree.run_number<284485):
                continue

            Pt[0] = tree.lep_0_p4_fast.Pt()
            MetE[0] = tree.met_reco_p4.E()
            if math.fabs(tree.lepmet_dphi)> math.pi:
                dPhi[0] = 2*math.pi-math.fabs(tree.lepmet_dphi)
            else:
                dPhi[0] = math.fabs(tree.lepmet_dphi)
            
            Mt[0] = tree.lepmet_mt
            Eta[0] = tree.lep_0_p4_fast.Eta()
            PhiMiss[0] = tree.met_reco_p4.Phi()
            
        
            l = reader.EvaluateMVA("MLP")
            h.Fill(l)
    return h


# In[4]:


dir_top1 = '/eos/user/s/smwbr/dponomar/WTauData/v10s04/year15/filtered/SR/nom_mu/user.dponomar.v10s04.mc16_13TeV.410013.PoPy_P2012_Wt_incl_top.M4.e3753_s3126_r9364_r9315_p3729.nom_mu_SM'
dir_top2 = '/eos/user/s/smwbr/dponomar/WTauData/v10s04/year15/filtered/SR/nom_mu/user.dponomar.v10s04.mc16_13TeV.410014.PoPy_P2012_Wt_incl_atop.M4.e3753_s3126_r9364_r9315_p3729.nom_mu_SM'
dir_top3 = '/eos/user/s/smwbr/dponomar/WTauData/v10s04/year15/filtered/SR/nom_mu/user.dponomar.v10s04.mc16_13TeV.410470.PhPy8_A14_ttb_nonallh.M4.e6337_e5984_s3126_r9364_r9315_p3729.nom_mu_SM'
dir_top4 = '/eos/user/s/smwbr/dponomar/WTauData/v10s04/year15/filtered/SR/nom_mu/user.dponomar.v10s04.mc16_13TeV.410644.PoPy8_A14_st_schan_lept_top.M4.e6527_e5984_s3126_r9364_r9315_p3729.nom_mu_SM'
dir_top5 = '/eos/user/s/smwbr/dponomar/WTauData/v10s04/year15/filtered/SR/nom_mu/user.dponomar.v10s04.mc16_13TeV.410645.PoPy8_A14_st_schan_lept_atop.M4.e6527_e5984_s3126_r9364_r9315_p3729.nom_mu_SM'
dir_top6 = '/eos/user/s/smwbr/dponomar/WTauData/v10s04/year15/filtered/SR/nom_mu/user.dponomar.v10s04.mc16_13TeV.410646.PoPy8_A14_Wt_DR_inclusive_top.M4.e6552_e5984_s3126_r9364_r9315_p3729.nom_mu_SM'
#[410013, 410014, 410470] + [410644, 410645, 410646],

dir_diboson1 = '/eos/user/s/smwbr/dponomar/WTauData/v10s04/year15/filtered/SR/nom_mu/user.dponomar.v10s04.mc16_13TeV.363356.Sh221_PDF30_ZqqZll.M4.e5525_s3126_r9364_r9315_p3729.nom_mu_SM'
dir_diboson2 = '/eos/user/s/smwbr/dponomar/WTauData/v10s04/year15/filtered/SR/nom_mu/user.dponomar.v10s04.mc16_13TeV.363358.Sh221_PDF30_WqqZll.M4.e5525_s3126_r9364_r9315_p3729.nom_mu_SM'
dir_diboson3 = '/eos/user/s/smwbr/dponomar/WTauData/v10s04/year15/filtered/SR/nom_mu/user.dponomar.v10s04.mc16_13TeV.363359.Sh221_PDF30_WpqqWmlv.M4.e5583_s3126_r9364_r9315_p3729.nom_mu_SM'
dir_diboson4 = '/eos/user/s/smwbr/dponomar/WTauData/v10s04/year15/filtered/SR/nom_mu/user.dponomar.v10s04.mc16_13TeV.363360.Sh221_PDF30_WplvWmqq.M4.e5983_s3126_r9364_r9315_p3729.nom_mu_SM'
dir_diboson5 = '/eos/user/s/smwbr/dponomar/WTauData/v10s04/year15/filtered/SR/nom_mu/user.dponomar.v10s04.mc16_13TeV.363489.Sh221_PDF30_WlvZqq.M4.e5525_s3126_r9364_r9315_p3729.nom_mu_SM'
dir_diboson6 = '/eos/user/s/smwbr/dponomar/WTauData/v10s04/year15/filtered/SR/nom_mu/user.dponomar.v10s04.mc16_13TeV.364250.Sh222_PDF30_llll.M4.e5894_s3126_r9364_r9315_p3729.nom_mu_SM'
dir_diboson7 = '/eos/user/s/smwbr/dponomar/WTauData/v10s04/year15/filtered/SR/nom_mu/user.dponomar.v10s04.mc16_13TeV.364253.Sh222_PDF30_lllv.M4.e5916_s3126_r9364_r9315_p3729.nom_mu_SM'
dir_diboson8 = '/eos/user/s/smwbr/dponomar/WTauData/v10s04/year15/filtered/SR/nom_mu/user.dponomar.v10s04.mc16_13TeV.364254.Sh222_PDF30_llvv.M4.e5916_s3126_r9364_r9315_p3729.nom_mu_SM'
dir_diboson9 = '/eos/user/s/smwbr/dponomar/WTauData/v10s04/year15/filtered/SR/nom_mu/user.dponomar.v10s04.mc16_13TeV.364255.Sh222_PDF30_lvvv.M4.e5916_s3126_r9364_r9315_p3729.nom_mu_SM'
#[363356, 363358, 363359, 363360, 363489] + [364250, 364253, 364254, 364255],


dir_wmu1 = '/eos/user/s/smwbr/dponomar/WTauData/v10s04/year15/filtered/SR/nom_mu/user.dponomar.v10s04.mc16_13TeV.361101.PoPy8_Wplusmunu.M4.e3601_s3126_r9364_r9315_p3731.nom_mu_SM'
dir_wmu2 = '/eos/user/s/smwbr/dponomar/WTauData/v10s04/year15/filtered/SR/nom_mu/user.dponomar.v10s04.mc16_13TeV.361104.PoPy8_Wminusmunu.M4.e3601_s3126_r9364_r9315_p3731.nom_mu_SM'
#[361101, 361104],

dir_wtau1 = '/eos/user/s/smwbr/dponomar/WTauData/v10s04/year15/filtered/SR/nom_mu/user.dponomar.v10s04.mc16_13TeV.361102.PoPy8_Wplustaunu.M4.e3601_s3126_r9364_r9315_p3729.nom_mu_SM'
dir_wtau2 = '/eos/user/s/smwbr/dponomar/WTauData/v10s04/year15/filtered/SR/nom_mu/user.dponomar.v10s04.mc16_13TeV.361105.PoPy8_Wminustaunu.M4.e3601_s3126_r9364_r9315_p3729.nom_mu_SM'
#[361102, 361105],

data1 = '/eos/user/s/smwbr/dponomar/WTauData/v10s04/year15/filtered/SR/data_mu/user.dponomar.v10s04.data15_13TeV.periodD.physics_Main.M4.grp23_v01_p3781.nom_mu_SM'
data2 = '/eos/user/s/smwbr/dponomar/WTauData/v10s04/year15/filtered/SR/data_mu/user.dponomar.v10s04.data15_13TeV.periodE.physics_Main.M4.grp23_v01_p3781.nom_mu_SM'
data3 = '/eos/user/s/smwbr/dponomar/WTauData/v10s04/year15/filtered/SR/data_mu/user.dponomar.v10s04.data15_13TeV.periodF.physics_Main.M4.grp23_v01_p3781.nom_mu_SM'
data4 = '/eos/user/s/smwbr/dponomar/WTauData/v10s04/year15/filtered/SR/data_mu/user.dponomar.v10s04.data15_13TeV.periodG.physics_Main.M4.grp23_v01_p3781.nom_mu_SM'
data5 = '/eos/user/s/smwbr/dponomar/WTauData/v10s04/year15/filtered/SR/data_mu/user.dponomar.v10s04.data15_13TeV.periodH.physics_Main.M4.grp23_v01_p3781.nom_mu_SM'
data6 = '/eos/user/s/smwbr/dponomar/WTauData/v10s04/year15/filtered/SR/data_mu/user.dponomar.v10s04.data15_13TeV.periodJ.physics_Main.M4.grp23_v01_p3781.nom_mu_SM'


Zmumu = '/eos/user/s/smwbr/dponomar/WTauData/v10s04/year15/filtered/SR/nom_mu/user.dponomar.v10s04.mc16_13TeV.361107.PoPy8_Zmumu.M4.e3601_s3126_r9364_r9315_p3731.nom_mu_SM'
#[361107],
Ztt = '/eos/user/s/smwbr/dponomar/WTauData/v10s04/year15/filtered/SR/nom_mu/user.dponomar.v10s04.mc16_13TeV.361108.PoPy8_Ztt.M4.e3601_s3126_r9364_r9315_p3729.nom_mu_SM'
#[361108],


# In[5]:


h_top1 = rew(dir_top1, 'top')
h_top2 = rew(dir_top2, 'top')
h_top3 = rew(dir_top3, 'top')
h_top4 = rew(dir_top4, 'top')
h_top5 = rew(dir_top5, 'top')
h_top6 = rew(dir_top6, 'top')
h_top = h_top1.Clone()
h_top.Add(h_top2)
h_top.Add(h_top3)
h_top.Add(h_top4)
h_top.Add(h_top5)
h_top.Add(h_top6)


# In[6]:


h_diboson1 = rew(dir_diboson1, 'top')
h_diboson2 = rew(dir_diboson2, 'top')
h_diboson3 = rew(dir_diboson3, 'top')
h_diboson4 = rew(dir_diboson4, 'top')
h_diboson5 = rew(dir_diboson5, 'top')
h_diboson6 = rew(dir_diboson6, 'top')
h_diboson7 = rew(dir_diboson7, 'top')
h_diboson8 = rew(dir_diboson8, 'top')
h_diboson9 = rew(dir_diboson9, 'top')
h_diboson = h_diboson1.Clone()
h_diboson.Add(h_diboson2)
h_diboson.Add(h_diboson3)
h_diboson.Add(h_diboson4)
h_diboson.Add(h_diboson5)
h_diboson.Add(h_diboson6)
h_diboson.Add(h_diboson7)
h_diboson.Add(h_diboson8)
h_diboson.Add(h_diboson9)


# In[7]:


h_wmu1 = rew(dir_wmu1, 'top')
h_wmu2 = rew(dir_wmu2, 'top')
h_wmu = h_wmu1.Clone()
h_wmu.Add(h_wmu2)


# In[8]:


h_wtau1 = rew(dir_wtau1, 'top')
h_wtau2 = rew(dir_wtau2, 'top')
h_wtau = h_wmu1.Clone()
h_wtau.Add(h_wtau2)


# In[87]:


#def poolhisto(dirname, tp):
#    files = os.listdir(dirname)
#    h_list = []
#    for i in range(len(files)):
#        h = rew(dirname +'/'+ str(files[i]), tp)
#        h_list.append(h)
#    k = 1
#    print(h_list)
#    if len(h_list) > 1:
#        while k < len(h_list):
#            hClone = h_list[0].Clone()
#            hClone.Add(h_list[k])
#            k+=1
#    else:
#        hClone = h_list[0].Clone()
#    return hClone


# In[9]:


h_data1 = rew(data1, 'data')
h_data2 = rew(data2, 'data')
h_data3 = rew(data3, 'data')
h_data4 = rew(data4, 'data')
h_data5 = rew(data5, 'data')
h_data6 = rew(data6, 'data')
h_data = h_data1.Clone()
h_data.Add(h_data2)
h_data.Add(h_data3)
h_data.Add(h_data4)
h_data.Add(h_data5)
h_data.Add(h_data6)


# In[10]:


h_zmumu = rew(Zmumu, 'ss')
h_ztt = rew(Ztt, 'ss')


# In[ ]:


#h_top = poolhisto(dir_top, 'dd')
#h_diboson = poolhisto(dir_diboson, 'dd')
#h_wmu = poolhisto(dir_wmu, 'dd')
#h_wtau = poolhisto(dir_wtau, 'dd')
#h_ztt = poolhisto(Ztt, 'dd')
#h_zmumu = poolhisto(Zmumu, 'dd')


# In[ ]:


#data = '/eos/user/g/gtolkach/NEWDATA/Data'
#h_data = poolhisto(data, 'data')


# In[11]:


from ROOT import gPad
h_mc = [h_top, h_diboson, h_ztt, h_zmumu, h_wtau , h_wmu]

k = 1
while k < len(h_mc):
    h_sum_mc = h_mc[0].Clone()
    h_sum_mc.Add(h_mc[k])
    k+=1
h_ratio = h_data.Clone()
h_ratio.Divide(h_sum_mc)
    
mcSumHistWithoutErrors = h_sum_mc.Clone()
h_sum_mc.Sumw2()
mcSumRatioHist = h_sum_mc.Clone()
mcSumRatioHist.Divide(mcSumHistWithoutErrors)


# In[29]:


print(h_mc[0].Integral())
print(h_mc[1].Integral())
print(h_mc[2].Integral())
print(h_mc[3].Integral())
print(h_mc[4].Integral())
print(h_mc[5].Integral())


# In[41]:


c3 = ROOT.TCanvas ("c3", "ph_et in",600,600)
ROOT.gStyle.SetOptStat(0)
hs131 =  ROOT.THStack("hs","")
pad1 = ROOT.TPad("pad1","This is pad1",0.01,0.40,1,1.0)
pad2 = ROOT.TPad("pad2","This is pad2",0.01,0.01,1,0.39)
pad1.SetBorderSize(0)
pad1.SetBottomMargin(0.0);
pad1.Draw()
pad2.SetBorderSize(0)
pad2.SetTopMargin(0.)
pad2.SetBottomMargin(0.40)
pad2.Draw()
pad1.cd(0)
#pad1.SetLogy()

pt =  ROOT.TPaveText(0.13,0.65,0.6,0.88,"NDC")

pt.SetFillColor(0)
#pt.SetFillStyle(1)
pt.SetTextAlign(12)
#pt.SetLineStyle(0)

pt.AddText('#it{ATLAS} #bf{#bf{Work in Progress}}')
pt.AddText('#bf{#bf{3.22fb^{-1}, #sqrt{S}=13 TeV}}')
pt.AddText('#bf{#bf{SR}}')
pt.AddText('#bf{#bf{2015}}')

for i in range(len(h_mc)):
    h_mc[i].SetLineColor(36)

h_data.SetLineColor(ROOT.kBlack)
h_data.SetMarkerSize(1)

h_data.SetLineWidth(2)
h_data.SetMarkerStyle(15)


h_mc[0].SetFillColor(ROOT.kMagenta+2)
h_mc[1].SetFillColor(ROOT.kCyan-3)
h_mc[2].SetFillColor(ROOT.kBlue-3)
h_mc[3].SetFillColor(ROOT.kRed-3)
h_mc[4].SetFillColor(ROOT.kYellow-7)
h_mc[5].SetFillColor(ROOT.kOrange + 8)

hs131.Add(h_mc[0])
hs131.Add(h_mc[1])
hs131.Add(h_mc[2])
hs131.Add(h_mc[3])
hs131.Add(h_mc[4])
hs131.Add(h_mc[5])


h_data.GetYaxis().SetRangeUser(10,  10400000)
h_data.GetXaxis().SetRangeUser(-0.1,  0.85)
h_data.SetLineWidth(2)

h_data.GetYaxis().SetTitle("#scale[2]{Events/0.057}")
h_data.GetYaxis().SetLabelSize(0.05)
h_data.Draw(" E0  ")
hs131.Draw('hist same')
h_data.Draw("E0  same ")
pt.Draw("'NDC' same")
#####################
legend1 = ROOT.TLegend(0.70,0.88,0.55,0.6)
legend1.SetLineColor(0)
legend1.SetFillStyle(1)
legend1.AddEntry( h_data,"Data","lp")
legend1.AddEntry( h_mc[5],"W#rightarrow#mu#nu ","f")
legend1.AddEntry( h_mc[4],"W#rightarrow#tau#nu ","f")
legend1.AddEntry( h_mc[3],"Z#rightarrow#mu#mu","f")
legend1.AddEntry( h_mc[2],"Z#rightarrow#tau#tau ","f")
legend1.AddEntry( h_mc[1],"Diboson","f")
legend1.AddEntry( h_mc[0],"Top","f")
legend1.Draw()

gr1 = ROOT.TGraph(2)
gr1.SetPoint(0, -1, 1)
gr1.SetPoint(1, 100, 1)
gr1.SetLineStyle(7)

gPad.RedrawAxis()
c3.Update()

#mc_x, mc_y = array('f'), array('f')
#mc_ex, mc_ey = array('f'), array('f')

#for i in range(0, h_sum_mc.GetNbinsX()):
#    mc_x.append(0.05*i)
#    mc_ex.append(0.025)
#    mc_y.append(1)
#    mc_ey.append(h_ratio.GetBinError(i))
    
#g = ROOT.TGraphErrors(h_sum_mc.GetNbinsX(), mc_x, mc_y, mc_ex, mc_ey)



mcSumRatioHist.SetFillColor(ROOT.kGreen -9)
#mcSumRatioHist.SetLineColor(ROOT.kGreen -9)
mcSumRatioHist.SetTitle('')

pad2.cd(0)


h_ratio.SetMarkerStyle(15)
h_ratio.SetLineColor(ROOT.kBlack)
 
#h_ratio.GetYaxis().SetLabelOffset(0.01) #сдвиг цифр
h_ratio.GetYaxis().SetLabelSize(0.07)
#h_ratio.GetYaxis().SetLabelFont(2)
h_ratio.GetXaxis().SetLabelSize(0.07)
h_ratio.GetYaxis().SetTitle("#scale[3]{Data / Model  }")
h_ratio.GetXaxis().SetTitle("#scale[2]{TMVA MLP score}")
h_ratio.GetXaxis().SetLabelOffset(0.01)

h_ratio.GetXaxis().SetTitleOffset(1.5)
h_ratio.GetXaxis().SetTitleSize(0.05)

h_ratio.GetXaxis().SetRangeUser(-0.1,  0.85)
h_ratio.GetYaxis().SetRangeUser(0.2, 1.8)
h_ratio.Draw("E")
mcSumRatioHist.Draw(' E2 same')
h_ratio.Draw("same E")
gr1.Draw('same')

gPad.RedrawAxis()

legend1.AddEntry( mcSumRatioHist,"Stat.Uncert.","f")

c3.cd(1)
#legend1.Draw('same')


pad1.Update()
pad2.Update()
c3.Update()
c3.Draw()


# In[ ]:





# In[37]:


c3.SaveAs('h.pdf')


# In[ ]:




