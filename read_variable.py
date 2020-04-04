#!/usr/bin/env python
# coding: utf-8

# In[351]:


import math 
from ROOT import TMVA, TFile, TString
from array import array
import ROOT


# In[352]:


#f1 = ROOT.TFile.Open('/eos/user/g/gtolkach/data/tau_mu_plusandminus.root')
#f2 = ROOT.TFile.Open('/eos/user/g/gtolkach/data/data_mu.root')
#f3 = ROOT.TFile.Open('/eos/user/g/gtolkach/new_WMU.root')
#f4 = ROOT.TFile.Open('/eos/user/g/gtolkach/new_WMU_minus.root')
#f5 = ROOT.TFile.Open('/eos/user/g/gtolkach/plus_wtau.root')
#f6 = ROOT.TFile.Open('/eos/user/g/gtolkach/minus_Wtau.root')


# In[353]:


f1 = ROOT.TFile.Open('/eos/user/g/gtolkach/NEWDATA/data_mu_6variables_forMVA.root')
f2 = ROOT.TFile.Open('/eos/user/g/gtolkach/NEWDATA/Wmu_plus_6v_forMVA.root')
f3 = ROOT.TFile.Open('/eos/user/g/gtolkach/NEWDATA/Wmu_minus_6v_forMVA.root')
f4 = ROOT.TFile.Open('/eos/user/g/gtolkach/NEWDATA/plus_Wtau_6v_forMVA.root')
f5 = ROOT.TFile.Open('/eos/user/g/gtolkach/NEWDATA/minus_Wtau_6v_forMVA.root')


# In[356]:


def rew(file, tp): 
    tree = file.Get('NOMINAL')
    
    h = ROOT.TH1D("h","", 50,-math.pi, math.pi)
  

    if tp.find('data') == -1:
        h1 = file.Get('h_metadata')
        bin_8 = h1.GetBinContent(8)
        print(bin_8)
        kfactor =  11.246151648051285
        lumi2015 = 3219.56  # pb-1
        print(tree.GetEntries())
        for i in range(0,tree.GetEntries()):
            tree.GetEntry(i)
            
            #if not(tree.lep_0_id_tight==1):
            #    continue

           # weight = (tree.weight_mc*(tree.cross_section*tree.filter_efficiency*tree.kfactor))*((((((((((1)*(tree.lep_0_NOMINAL_MuEffSF_HLT_mu20_iloose_L1MU15_OR_HLT_mu50_QualMedium_IsoNone))*(tree.lep_0_NOMINAL_MuEffSF_TTVA))*(tree.lep_0_NOMINAL_MuEffSF_IsoFCTight))*(tree.jet_NOMINAL_global_effSF_MV2c10*tree.jet_NOMINAL_global_ineffSF_MV2c10))*((tree.NOMINAL_pileup_random_run_number<284490)*tree.NOMINAL_pileup_combined_weight))*(tree.jet_NOMINAL_central_jets_global_effSF_JVT*tree.jet_NOMINAL_central_jets_global_ineffSF_JVT))*(tree.lep_0_NOMINAL_MuEffSF_Reco_QualMedium))*(1))*(tree.jet_NOMINAL_forward_jets_global_effSF_JVT*tree.jet_NOMINAL_forward_jets_global_ineffSF_JVT))*kfactor*lumi2015
            weight1 = tree.kweight_mc*tree.NOMINAL_pileup_combined_weight*tree.cross_section*tree.filter_efficiency*tree.kfactor*kfactor*lumi2015
        
            h.Fill(tree.PhiMiss, weight1/bin_8)
        
    else:
        for i in range(0,tree.GetEntries()):
            tree.GetEntry(i)
            #if not(tree.lep_0_id_tight==1):
            #    continue
            
            h.Fill(tree.PhiMiss)
    
        print(tree.GetEntries())
    return h


# In[357]:


h_data = rew(f1, 'data')


# In[358]:


h_wmu_plus = rew(f2, 'wmu')
h_wmu_minus = rew(f3, 'wmu')


# In[359]:


h_wtau_plus = rew(f4, 'wmu')
h_wtau_minus = rew(f5, 'wmu')


# In[ ]:


h_mc = []
h_mc.append(h_wmu_plus)
h_mc.append(h_wmu_minus)
h_mc.append(h_wtau_plus)
h_mc.append(h_wtau_minus)


# In[ ]:


h_sum_wmu = h_mc[0].Clone()
h_sum_wmu.Add(h_mc[1])
h_sum_wmu.SetDirectory(0)
h_sum_wtau = h_mc[2].Clone()
h_sum_wtau.Add(h_mc[3])

h_sum_mc = h_sum_wmu.Clone()
h_sum_mc.Add(h_sum_wtau)

h_ratio = h_data.Clone()
h_ratio.Divide(h_sum_mc)
    
mcSumHistWithoutErrors = h_sum_mc.Clone()
h_sum_mc.Sumw2()
mcSumRatioHist = h_sum_mc.Clone()
mcSumRatioHist.Divide(mcSumHistWithoutErrors)


# In[117]:


print(int(h_data.GetMaximum()))
maxv = h_data.GetMaximum()


# In[360]:


def painter(h_data, h_sum_wmu, h_sum_wtau, h_ratio, mcSumRatioHist):
    

    c3 = ROOT.TCanvas ("c3", "ph_et in",600,600)
    gStyle.SetOptStat(0)
    
    pad1 = ROOT.TPad("pad1","This is pad1",0.01,0.40,1,1.0)
    pad2 = ROOT.TPad("pad2","This is pad2",0.01,0.01,1,0.39)
    pad1.SetBorderSize(0)
    pad1.SetBottomMargin(0.0)
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


    h_sum_wtau.SetLineColor(36)
    h_sum_wmu.SetLineColor(36)
    h_data.SetLineColor(ROOT.kBlack)
    h_data.SetMarkerSize(1.24)

    h_data.SetLineWidth(2)
    h_data.SetMarkerStyle(15)
    

    h_sum_wtau.SetFillColor(ROOT.kYellow)

    h_sum_wmu.SetFillColor(ROOT.kOrange+10)
   

#    h_data.GetYaxis().SetRangeUser(1,  170000000)
#    h_data.GetXaxis().SetRangeUser(0, 400)
    h_data.SetLineWidth(2)

    h_data.GetYaxis().SetTitle("#scale[2]{Events/2Gev}")
    h_data.GetYaxis().SetLabelSize(0.05)
    h_data.GetYaxis().SetTitleOffset(1.5)
    
    h_data.Draw('E0')
    h_sum_wmu.Draw('hist same')
    h_sum_wtau.Draw('hist same')
    h_data.Draw("E0  same ")
    pt.Draw("'NDC' same")

    legend1 = ROOT.TLegend(0.88,0.88,0.70,0.67)
    legend1.AddEntry( h_data,"Data","lp")
    legend1.AddEntry( h_sum_wmu,"W#rightarrow#mu#nu ","f")
    legend1.AddEntry( h_sum_wtau,"W#rightarrow#tau#nu ","f")
    legend1.Draw()

    gr1 = ROOT.TGraph(2)
    gr1.SetPoint(0, -1, 1)
    gr1.SetPoint(1, 100, 1)
    gr1.SetLineStyle(7)

    gPad.RedrawAxis()
    c3.Update()

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
    h_ratio.GetXaxis().SetTitle("#scale[2]{#phi_{MET}")
    h_ratio.GetXaxis().SetLabelOffset(0.01)

    h_ratio.GetXaxis().SetTitleOffset(1.8)
    h_ratio.GetXaxis().SetTitleSize(0.05)

   # h_ratio.GetYaxis().SetRangeUser(0.7,  1.3)
    #h_ratio.GetYaxis().SetRangeUser(0, 2)
    h_ratio.SetLineWidth(2)
    h_ratio.Draw("E")
    mcSumRatioHist.Draw(' E2 same')
    h_ratio.Draw("E same")
    gr1.Draw('same')

    gPad.RedrawAxis()

    legend1.AddEntry( mcSumRatioHist,"Stat.Uncert.","f")

   # c3.cd(1)
   # legend1.Draw('same')


    pad1.Update()
    pad2.Update()
    c3.Update()
    c3.SaveAs('fff.pdf')
    c3.Draw()
    return c3


# In[361]:


painter(h_data, h_sum_wmu, h_sum_wtau, h_ratio, mcSumRatioHist)


# In[284]:


c.Draw()


# In[1]:


c3 = ROOT.TCanvas() 

c3.Divide(1, 2)
#c1.SetLogy(
ROOT.gStyle.SetOptStat(0)
c3.cd(1)
c3.cd(1).SetMargin(0.1,0.3,0.01,1.5)


#gPad = c3.cd(1)
#gPad.SetLogy()
h_AddWmu = ROOT.TH1D("add1","",  50,0, 120)
h_AddWmu.Add(h_pt_mc_wmu_minus, h_pt_mc_wmu, 1, 1)

h_AddWtau = ROOT.TH1D("add1","",  50,0, 120)
h_AddWtau.Add(h_pt_mc_wtau_plus, h_pt_mc_wtau_minus, 1, 1)

h_AddWtau.SetLineColor(36)
h_AddWmu.SetLineColor(36)
h_pt_data.SetLineColor(ROOT.kBlack)

h_pt_data.SetLineWidth(2)

h_AddWmu.SetFillColor(ROOT.kRed)
h_AddWtau.SetFillColor(ROOT.kYellow)

h_AddWmu.SetTitle("mc_wmu")
h_pt_data.SetTitle('data')
h_AddWtau.SetTitle("mc_wtau")
h_pt_data.SetMarkerStyle(15)
h_AddWmu.GetXaxis().SetRangeUser(0, 90)
h_AddWmu.GetYaxis().SetRangeUser(0, 2900000)


pt =  ROOT.TPaveText(0.12,0.6,0.3,0.88,"NDC")

pt.SetFillColor(0)
#pt.SetFillStyle(1)
pt.SetTextAlign(12)
#pt.SetLineStyle(0)

pt.AddText('#it{ATLAS} #bf{#bf{Work in Progress}}')
pt.AddText('#bf{#bf{3.22fb^{-1}, #sqrt{S}=13 TeV}}')
pt.AddText('#bf{#bf{SR}}')
pt.AddText('#bf{#bf{2015}}')


h_AddWmu.GetYaxis().SetTitle("#scale[2]{Events/2GeV}")
h_AddWmu.Draw("hist")
pt.Draw("'NDC' same")
h_AddWmu.Draw("hist same")
h_pt_data.Draw("P same")
h_AddWtau.Draw("hist same")

h_AddWmu.SetTitle('')

#ROOT.gPad.BuildLegend(1.0,0.8,0.8,0.5,"","")
legend1 = ROOT.TLegend(0.55,0.88,0.69,0.67)
legend1.AddEntry( h_pt_data,"Data","lep")
legend1.AddEntry( h_AddWmu,"W#rightarrow#mu#nu ","f")
legend1.AddEntry( h_AddWtau,"W#rightarrow#tau#nu ","f")




h_add = ROOT.TH1D("add","",  50,0, 120)
h_divide = ROOT.TH1D("divide","",  50,0, 120)
h_add.Add(h_AddWtau, h_AddWmu, 1, 1)
h_divide.Divide(h_pt_data, h_add, 1, 1)
c3.cd(2)
#c3.cd(2).SetLeftMargin(



gr1 = ROOT.TGraph(2)
gr1.SetPoint(0, 0, 1)
gr1.SetPoint(1, 100, 1)
gr1.SetLineStyle(7)
c3.cd(2).SetMargin(0.1,0.3,0.5,0.)


h_divide.SetMarkerStyle(15)






#for i in range(0, 50):
#    g.SetPoint(i, 1 ,i)
#    g.SetPointError(i,h_divide.GetBinError(i))
    
mc_x, mc_y = array('f'), array('f')
mc_ex, mc_ey = array('f'), array('f')

for i in range(0, 55):
    mc_x.append(2*i)
    mc_ex.append(1)
    mc_y.append(1)
    mc_ey.append(h_divide.GetBinError(i))
   


g  = ROOT.TGraphErrors(50, mc_x, mc_y, mc_ex, mc_ey)

g.GetXaxis().SetRangeUser(0, 90)
g.GetYaxis().SetRangeUser(0.9, 1.1)
legend1.AddEntry( g,"Stat.Uncert.","f")
legend1.Draw()

#for i in range(0,50,2):
#    g.SetPoint(i,i+1,1)
#    g.SetPointError(i,mc_x[i],mc_y[i])



#g.SetMarkerStyle(15)
g.SetFillColor(ROOT.kGreen -9)
g.SetLineColor(ROOT.kGreen -9)
#g.SetFillStyle( )

g.GetYaxis().SetTitle("#scale[2]{Data / Model  }")
g.GetXaxis().SetTitle("#scale[2]{P_{T}[GeV]}")

g.SetTitle('')
h_divide.SetLineColor(ROOT.kBlack)

g.Draw('A5')
h_divide.Draw("E same")
gr1.Draw('Same')

c3.cd(1)
legend1.Draw('same')
c3.Update()

c3.Draw()


# In[276]:


c3.SaveAs('12311114.pdf')


# In[272]:


c6 = ROOT.TCanvas("c6", "ph_et in",600,600)
pad_ph_et_21 = ROOT.TPad("pad_ph_et_21","This is pad_ph_et_1",0.01,0.31,1,1.0)
pad_ph_et_22 = ROOT.TPad("pad_ph_et_22","This is pad_ph_et_2",0.01,0.01,1,0.3)
pad_ph_et_21.SetBorderSize(0)
pad_ph_et_21.SetBottomMargin(0.02)
pad_ph_et_21.Draw()
pad_ph_et_22.SetBorderSize(0)
pad_ph_et_22.SetBottomMargin(0.40)
pad_ph_et_22.Draw()
pad_ph_et_21.cd(0)
#pad_ph_et_21.SetLogy()
h_pt_data.Draw("P")

h_AddWtau.Draw("hist same")
h_AddWmu.Draw("hist same")
#gPad.RedrawAxis()
c6.Update()
pad_ph_et_22.cd(0)
h_divide.Draw("E2")
#gPad.RedrawAxis();
c6.Draw()


# In[ ]:




