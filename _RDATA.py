#!/usr/bin/env python
# coding: utf-8

# In[102]:


import ROOT
import os
import math 
from ROOT import TFile, TString
from array import array
from ROOT import RDataFrame
from ROOT import gStyle
from ROOT import gPad

#from ROOT.ROOT import RDataFrame


# In[123]:


get_ipython().run_line_magic('jsroot', 'on')


# In[59]:


def rdhisto(filename, variable):
    if filename.find('data') == -1:
        f1 = ROOT.TFile.Open(filename)
        h1 = f1.Get('h_metadata')
        bin_8 = h1.GetBinContent(8)
        
        kf =  11.246151648051285
        lumi2015 = 3219.56  # pb-1
        
        df = ROOT.RDataFrame('NOMINAL', filename) 
        h = df.Define("fPt", variable)              .Define('w1', str(kf*lumi2015/bin_8))              .Define("w2", "weight_mc*NOMINAL_pileup_combined_weight*cross_section*filter_efficiency*kfactor")              .Define('w', 'w1*w2')              .Histo1D(("h_s", "h_s", 50, 0, 140), "fPt", 'w') 
    else: 
        df = ROOT.RDataFrame('NOMINAL', filename) 
        h = df.Define("fPt", variable)              .Histo1D(("h_s", "h_s", 50, 0, 140), "fPt") 
    return h


# In[35]:


h1 = rdhisto('/eos/user/g/gtolkach/NEWDATA/mu/Wmu_plus.root', 'lep_0_p4_fast.Pt()')
h2 = rdhisto('/eos/user/g/gtolkach/NEWDATA/mu/Wmu_minus.root', 'lep_0_p4_fast.Pt()')


# In[78]:


dir_top = '/eos/user/g/gtolkach/NEWDATA/top'
dir_diboson = '/eos/user/g/gtolkach/NEWDATA/diboson'
dir_wmu = '/eos/user/g/gtolkach/NEWDATA/mu'
dir_wtau = '/eos/user/g/gtolkach/NEWDATA/tau'
data = '/eos/user/g/gtolkach/data/data_mu.root'
Zmumu = '/eos/user/g/gtolkach/NEWDATA/Zmumu'
Ztt = '/eos/user/g/gtolkach/NEWDATA/Ztt'


# In[81]:


def poolhisto(dirname, variable):
    files = os.listdir(dirname)
    h_list = []
    for i in range(len(files)):
        h = rdhisto(dirname +'/'+ str(files[i]), variable)
        h_list.append(h)
    k = 1
    print(h_list)
    if len(h_list) > 1:
        while k < len(h_list):
            hClone = h_list[0].Clone()
            hClone.Add(h_list[k].GetPtr())
            k+=1
    else:
        hClone = h_list[0].Clone()
    return hClone


# In[54]:


h = poolhisto('/eos/user/g/gtolkach/NEWDATA/tau', 'lep_0_p4_fast.Pt()')


# In[173]:


var = 'lepmet_mt'
h_top = poolhisto(dir_top, var)
h_diboson = poolhisto(dir_diboson, var)
h_wmu = poolhisto(dir_wmu, var)
h_wtau = poolhisto(dir_wtau, var)
h_ztt = poolhisto(Ztt, var)
h_zmumu = poolhisto(Zmumu, var)


# In[174]:



h_data = rdhisto(data, var)


# In[175]:


h_mc = [h_top, h_diboson, h_ztt, h_wtau, h_zmumu, h_wmu]


# In[184]:


def painter(h_data, h_mc):
    
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
    #pad1.SetLogy()

    pt =  ROOT.TPaveText(0.13,0.65,0.6,0.88,"NDC")
   
#    pt.SetFillStyle(1)
    pt.SetFillColor(0)
    #pt.SetFillStyle(1)
    pt.SetTextAlign(12)
#    pt.SetLineStyle(0)

    pt.AddText('#it{ATLAS} #bf{#bf{Work in Progress}}')
    pt.AddText('#bf{#bf{3.22fb^{-1}, #sqrt{S}=13 TeV}}')
    pt.AddText('#bf{#bf{SR}}')
    pt.AddText('#bf{#bf{2015}}')


    h_mc[5].SetLineColor(36)
    h_mc[4].SetLineColor(36)
    h_mc[3].SetLineColor(36)
    h_mc[2].SetLineColor(36)
    h_mc[1].SetLineColor(36)
    h_mc[0].SetLineColor(36)
    
    h_data.SetLineColor(ROOT.kBlack)
    h_data.SetMarkerSize(1.54)

    h_data.SetLineWidth(2)
    h_data.SetMarkerStyle(15)
    
    h_mc[0].SetFillColor(ROOT.kBlue-6)
    h_mc[1].SetFillColor(ROOT.kOrange+3)
    h_mc[2].SetFillColor(ROOT.kBlue)
    h_mc[3].SetFillColor(ROOT.kYellow)
    h_mc[4].SetFillColor(ROOT.kTeal)
    h_mc[5].SetFillColor(ROOT.kRed)
   

    h_data.GetYaxis().SetRangeUser(0,  2500000)
    h_data.GetXaxis().SetRangeUser(40, 140)
    h_data.SetLineWidth(2)

    h_data.GetYaxis().SetTitle("#scale[2]{Events/2Gev}")
    h_data.GetYaxis().SetLabelSize(0.05)
    h_data.GetYaxis().SetTitleOffset(1.5)
    
    h_data.SetTitle('')
    h_data.Draw('E0')
    h_mc[5].Draw('hist same')
    h_mc[4].Draw('hist same')
    h_mc[3].Draw('hist same')
    h_mc[2].Draw('hist same')
    h_mc[1].Draw('hist same')
    h_mc[0].Draw('hist same')
    h_data.Draw("E0  same ")
    pt.Draw("'NDC' same")

    legend1 = ROOT.TLegend(0.70,0.88,0.52,0.67)
    legend1.SetLineColor(0)
    legend1.SetFillStyle(1)
    legend1.AddEntry( h_data.GetPtr() ,"Data","lp")
    legend1.AddEntry( h_mc[5],"W#rightarrow#mu#nu ","f")
    legend1.AddEntry( h_mc[4],"Z#rightarrow#mu#mu ","f")
    legend1.AddEntry( h_mc[3],"W#rightarrow#tau#nu ","f")
    legend1.Draw()
    
    legend2 = ROOT.TLegend(0.88,0.88,0.70,0.67)
    legend2.SetLineColor(0)
    legend2.SetFillStyle(1)
    legend2.AddEntry( h_mc[2],"Z#rightarrow#tau#tau ","f")
    legend2.AddEntry( h_mc[1],"Diboson","f")
    legend2.AddEntry( h_mc[0],"Top","f")
    legend2.Draw()

    gr1 = ROOT.TGraph(2)
    gr1.SetPoint(0, -1, 1)
    gr1.SetPoint(1, 100, 1)
    gr1.SetLineStyle(7)

    gPad.RedrawAxis()
    c3.Update()

    mcSumRatioHist.SetFillColor(ROOT.kGreen -9)
    #mcSumRatioHist.SetLineColor(ROOT.kGreen -9)
    h_ratio.SetTitle('')

    pad2.cd(0)


    h_ratio.SetMarkerStyle(15)
    h_ratio.SetMarkerSize(1.54)
    h_ratio.SetLineColor(ROOT.kBlack)
     
    #h_ratio.GetYaxis().SetLabelOffset(0.01) #сдвиг цифр
    h_ratio.GetYaxis().SetLabelSize(0.07)
    #h_ratio.GetYaxis().SetLabelFont(2)
    h_ratio.GetXaxis().SetLabelSize(0.07)
    h_ratio.GetYaxis().SetTitle("#scale[3]{Data / Model  }")
    h_ratio.GetXaxis().SetTitle("#scale[2]{M_{T}[GeV]}")
    h_ratio.GetXaxis().SetLabelOffset(0.01)

    h_ratio.GetXaxis().SetTitleOffset(1.8)
    h_ratio.GetXaxis().SetTitleSize(0.05)

    h_ratio.GetYaxis().SetRangeUser(0.8,  1.2)
    h_ratio.GetXaxis().SetRangeUser(40, 140)
    h_ratio.SetLineWidth(2)
    h_ratio.Draw("E")
    mcSumRatioHist.Draw(' E2 same')
    h_ratio.Draw("E same")
    gr1.Draw('same')

    gPad.RedrawAxis()

    legend2.AddEntry( mcSumRatioHist,"Stat.Uncert.","f")

   # c3.cd(1)
   # legend1.Draw('same')


    pad1.Update()
    pad2.Update()
    c3.Update()
    c3.SaveAs('fff.pdf')
    c3.Draw()
    return c3


# In[185]:


painter(h_data, h_mc)


# In[ ]:




