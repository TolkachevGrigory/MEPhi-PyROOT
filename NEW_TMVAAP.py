#!/usr/bin/env python
# coding: utf-8

# In[5]:



import math 
from ROOT import gPad
from ROOT import TMVA, TFile, TString
from array import array
import ROOT
import os


# In[6]:


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


# In[67]:


#f1 = ROOT.TFile.Open('/eos/user/g/gtolkach/NEWDATA/data_mu_6variables_forMVA.root')


# In[68]:


#f2 = ROOT.TFile.Open('/eos/user/g/gtolkach/NEWDATA/Wmu_plus_6v_forMVA.root')
#f3 = ROOT.TFile.Open('/eos/user/g/gtolkach/NEWDATA/Wmu_minus_6v_forMVA.root')


# In[69]:


#f4 = ROOT.TFile.Open('/eos/user/g/gtolkach/NEWDATA/plus_Wtau_6v_forMVA.root')
#f5 = ROOT.TFile.Open('/eos/user/g/gtolkach/NEWDATA/minus_Wtau_6v_forMVA.root')


# In[99]:


#f1 = ROOT.TFile.Open('/eos/user/g/gtolkach/NEWDATA/Data/data_mu.root')
#f2 = ROOT.TFile.Open('/eos/user/g/gtolkach/NEWDATA/Wmu_plus_6v_forMVA.root')
#f3 = ROOT.TFile.Open('/eos/user/g/gtolkach/NEWDATA/mu/Wmu_minus.root')
#f4 = ROOT.TFile.Open('/eos/user/g/gtolkach/NEWDATA/tau/plus_wtau.root')
#f5 = ROOT.TFile.Open('/eos/user/g/gtolkach/NEWDATA/tau/minus_Wtau.root')


f1 ='/eos/user/g/gtolkach/NEWDATA/Data/data_mu.root'
f2 = '/eos/user/g/gtolkach/NEWDATA/mu/Wmu_plus.root'
f3 ='/eos/user/g/gtolkach/NEWDATA/mu/Wmu_minus.root'
f4 = '/eos/user/g/gtolkach/NEWDATA/tau/plus_wtau.root'
f5 = '/eos/user/g/gtolkach/NEWDATA/tau/minus_Wtau.root'


# In[7]:


def rew(filename, tp):
    
    f1 = ROOT.TFile.Open(filename)
    tree = f1.Get('NOMINAL')
   # tree.SetBranchAddress("lep_0_p4_fast.Pt()", Pt)
   # tree.SetBranchAddress("met_reco_p4.E()", MetE)
   # tree.SetBranchAddress("lepmet_dphi", dPhi)
   # tree.SetBranchAddress("met_reco_p4.Phi()", PhiMiss)
   # tree.SetBranchAddress("lepmet_mt", Mt)
   # tree.SetBranchAddress("lep_0_p4_fast.Eta()", Eta)
    
    h = ROOT.TH1D("h","", 40, -0.5, 1.2 )
    h.SetDirectory(0)
    print(type(h))
    print (tp.find('data'))
    if tp.find('data') == -1:
        h1 = f1.Get('h_metadata')
        bin_8 = h1.GetBinContent(8)
        print(bin_8)
        kfactor =  11.246151648051285
        lumi2015 = 3219.56  # pb-1
        for i in range(0,int(tree.GetEntries())):
            tree.GetEntry(i)
            Pt[0] = tree.lep_0_p4_fast.Pt()
            MetE[0] = tree.met_reco_p4.E()
            dPhi[0] = tree.lepmet_dphi
            Mt[0] = tree.lepmet_mt
            Eta[0] = tree.lep_0_p4_fast.Eta()
            PhiMiss[0] = tree.met_reco_p4.Phi()
            
            l = reader.EvaluateMVA("MLP")
            h.Fill(l,tree.weight_mc*tree.NOMINAL_pileup_combined_weight*tree.cross_section*tree.filter_efficiency*kfactor*lumi2015/bin_8)
            #print(tree.NOMINAL_pileup_combined_weight*tree.cross_section*tree.filter_efficiency*tree.kfactor/bin_8)
    else:
        for i in range(0,int(tree.GetEntries())):
            tree.GetEntry(i)
            Pt[0] = tree.lep_0_p4_fast.Pt()
            MetE[0] = tree.met_reco_p4.E()
            dPhi[0] = tree.lepmet_dphi
            Mt[0] = tree.lepmet_mt
            Eta[0] = tree.lep_0_p4_fast.Eta()
            PhiMiss[0] = tree.met_reco_p4.Phi()
            
        
            l = reader.EvaluateMVA("MLP")
            h.Fill(l)
    return h


# In[105]:


h_data = rew(f1, 'data')


# In[106]:


h_wmu_plus = rew(f2, 'dd')
h_wmu_minus = rew(f3, 'dd')


# In[107]:


h_wtau_plus = rew(f4, 'data')
h_wtau_minus = rew(f5, 'data')


# In[108]:


print(h_wtau_plus)


# In[109]:


h_sum_wmu = h_wmu_plus.Clone()
h_sum_wmu.Add(h_wmu_minus)


# In[110]:


h_sum_wtau = h_wtau_plus.Clone()
h_sum_wtau.Add(h_wtau_minus)


# In[111]:


h_sum_mc = h_sum_wmu.Clone()
h_sum_mc.Add(h_sum_wtau)

h_ratio = h_data.Clone()
h_ratio.Divide(h_sum_mc)



# In[112]:


h_sum_mc.GetNbinsX()


# In[113]:


mcSumHistWithoutErrors = h_sum_mc.Clone()
h_sum_mc.Sumw2() 
mcSumRatioHist = h_sum_mc.Clone()
mcSumRatioHist.Divide(mcSumHistWithoutErrors)


# In[8]:


dir_top = '/eos/user/g/gtolkach/NEWDATA/top'
dir_diboson = '/eos/user/g/gtolkach/NEWDATA/diboson'
dir_wmu = '/eos/user/g/gtolkach/NEWDATA/mu'
dir_wtau = '/eos/user/g/gtolkach/NEWDATA/tau'
data = '/eos/user/g/gtolkach/data/data_mu.root'
Zmumu = '/eos/user/g/gtolkach/NEWDATA/Zmumu'
Ztt = '/eos/user/g/gtolkach/NEWDATA/Ztt'


# In[9]:


def poolhisto(dirname, tp):
    files = os.listdir(dirname)
    h_list = []
    for i in range(len(files)):
        h = rew(dirname +'/'+ str(files[i]), tp)
        h_list.append(h)
    k = 1
    print(h_list)
    if len(h_list) > 1:
        while k < len(h_list):
            hClone = h_list[0].Clone()
            hClone.Add(h_list[k])
            k+=1
    else:
        hClone = h_list[0].Clone()
    return hClone


# In[10]:


h_top = poolhisto(dir_top, 'dd')
h_diboson = poolhisto(dir_diboson, 'dd')
h_wmu = poolhisto(dir_wmu, 'dd')
h_wtau = poolhisto(dir_wtau, 'dd')
h_ztt = poolhisto(Ztt, 'dd')
h_zmumu = poolhisto(Zmumu, 'dd')


# In[11]:


data = '/eos/user/g/gtolkach/NEWDATA/Data'
h_data = poolhisto(data, 'data')


# In[12]:


from ROOT import gPad
h_mc = [h_top, h_diboson, h_ztt, h_wtau, h_zmumu, h_wmu]

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


# In[20]:


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
pad1.SetLogy()

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
hs131.Add(h_mc[0])

h_mc[1].SetFillColor(ROOT.kCyan-3)
hs131.Add(h_mc[1])

h_mc[2].SetFillColor(ROOT.kBlue-3)
hs131.Add(h_mc[2])

h_mc[3].SetFillColor(ROOT.kRed-3)
hs131.Add(h_mc[3])

h_mc[4].SetFillColor(ROOT.kYellow-7)
hs131.Add(h_mc[4])

h_mc[5].SetFillColor(ROOT.kOrange + 8)
hs131.Add(h_mc[5])


h_data.GetYaxis().SetRangeUser(1,  1500000000)
h_data.GetXaxis().SetRangeUser(-0.1,  1)
h_data.SetLineWidth(2)

h_data.GetYaxis().SetTitle("#scale[2]{Events/2GeV}")
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
legend1.AddEntry( h_mc[4],"Z#rightarrow#mu#mu","f")
legend1.AddEntry( h_mc[3],"W#rightarrow#tau#nu ","f")
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

h_ratio.GetXaxis().SetRangeUser(-0.1,  1)
h_ratio.GetYaxis().SetRangeUser(0, 2)
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





# In[21]:


c3.SaveAs('h.pdf')


# In[ ]:




