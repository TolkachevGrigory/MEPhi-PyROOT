#!/usr/bin/env python
# coding: utf-8

# In[66]:


import ROOT
import os
import math 
from ROOT import TFile, TString
from array import array
from ROOT import RDataFrame
from ROOT import gStyle
from ROOT import gPad


# In[141]:


class Variable:
    def __init__(self,name, nbins, low , high):
        self.name = name
        self.varname = ''
        self.nbins = nbins
        self.low = low
        self.high = high
        self.command = None
        
        if 'lepmet_dphi' in self.name:
            self.command = 'if(fabs(lepmet_dphi) > 3.1415){ return double(2*3.1415 - fabs(lepmet_dphi));} else{ return double(fabs(lepmet_dphi));}'
        else:
            self.command = self.name


# In[130]:


class DataSet:
    def __init__(self, name):
    
        self.name = name
        # Latex title
        self.title = None
        # We can say if it is real Data or MC
        self.isData = False
        # list of ROOT files
        self.listOfFiles = []
        # Tree name
        self.treeName = 'NOMINAL'
        # Root color or standalone call that will keep drawing style
        self.style = None
        self.path = None
        
        
    
    def findFilesByPath(self, path = None):
        self.path = path
        self.listOfFiles = os.listdir(path)
    
    def getHistogram(self, var):
        hClone = None
        print(type(hClone))
        k = 0
        for file in self.listOfFiles:
            if self.isData == False:
                f = ROOT.TFile.Open(self.path +'/'+ str(file))
                h_8bin = f.Get('h_metadata')
                bin_8 = h_8bin.GetBinContent(8)
                kf =  11.246151648051285
                lumi2015 = 3219.56  # pb-1
                        
                df = ROOT.RDataFrame(self.treeName, self.path +'/'+ str(file))
                weight = '(weight_mc*(cross_section*filter_efficiency*kfactor))*(((((((((NOMINAL_pileup_combined_weight)*(lep_0_NOMINAL_MuEffSF_TTVA))*(lep_0_NOMINAL_MuEffSF_IsoFCTight))*(jet_NOMINAL_global_effSF_MV2c10*jet_NOMINAL_global_ineffSF_MV2c10))*(jet_NOMINAL_central_jets_global_effSF_JVT*jet_NOMINAL_central_jets_global_ineffSF_JVT))*(lep_0_NOMINAL_MuEffSF_Reco_QualMedium))*(1))*((lep_0_NOMINAL_MuEffSF_HLT_mu20_iloose_L1MU15_OR_HLT_mu50_QualMedium_IsoNone)))*(jet_NOMINAL_forward_jets_global_effSF_JVT*jet_NOMINAL_forward_jets_global_ineffSF_JVT))'      
               # oldweight = 'weight_mc*NOMINAL_pileup_combined_weight*cross_section*filter_efficiency*kfactor'
                h = df.Define('v', var.command)                      
                      .Define('w1', str(kf*lumi2015/bin_8))                     
                      .Define('w2', weight)
                      .Define('w', 'w1*w2')
                      .Histo1D(("%s"%(var.name), "%s"%(self.name), var.nbins, var.low, var.high), 'v', 'w')
                #if 'dphi' in var.varname:
                #    h = df.Define('v', 'if(fabs(lepmet_dphi) > 3.1415){ double_t dphi = 2*3.1415 - fabs(lepmet_dphi);}else{ double_t dphi  = lepmet_dphi;}return dphi;')
                    
                #else:
                #h = df.Define('v', var.name)
                
                #h = df.Histo1D(("%s"%(var.name), "%s"%(self.name), var.nbins, var.low, var.high), 'v', 'w')
                
            else:
                df = ROOT.RDataFrame(self.treeName, self.path +'/'+ str(file))
                h = df.Define('v', var.command)  
                      .Histo1D(("%s"%(var.name), "%s"%(self.name), var.nbins, var.low, var.high),'v')
                        
            if k == 0:
                hClone = h.Clone()
                hClone.SetDirectory(0)
                
                 
            else:
                
                hClone.Add(h.GetPtr())
                print(hClone)
            k+=1
        
        return hClone


# In[189]:





# In[208]:


class Plotter:
    def __init__(self, maxYaxispad1, minYaxispad2,  maxYaxispad2):
        self.minYaxispad1 = 0
        self.maxYaxispad1 = maxYaxispad1
        self.minYaxispad2 = minYaxispad2
        self.maxYaxispad2 = maxYaxispad2
        self.SetTitleX = ''
        self.SetTitleY = ''
    
    
  
    
    def painter(self, h_data, h_mc_list):
        print(type(h_mc_list[5]))
        k = 1
        while k < len(h_mc_list):
            h_sum_mc = h_mc_list[0].Clone()
            h_sum_mc.Add(h_mc_list[k])
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
        if 'lepmet_dphi' in h_mc_list[5].GetName():
            pad1.SetLogy()
            self.minYaxispad1 = 1
            
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
        
        sizemclist = len(h_mc_list)
        
        for i in reversed(range(sizemclist)):
            h_mc_list[i].SetLineColor(36)
        
        
        h_data.SetLineColor(ROOT.kBlack)
        #h_data.SetMarkerSize(1.5)

        h_data.SetLineWidth(2)
        h_data.SetMarkerStyle(15)
        
        for i in reversed(range(sizemclist)):
            h_mc_list[i].SetFillColor(7-i)
            
       

        h_data.GetYaxis().SetRangeUser(self.minYaxispad1,  self.maxYaxispad1)
        #self.h_data.GetXaxis().SetRangeUser(40, 140)
        h_data.SetLineWidth(2)
        ######################
        h_data.GetYaxis().SetTitle("#scale[2]{%s}"%self.SetTitleY)
        h_data.GetYaxis().SetLabelSize(0.05)
        #h_data.GetYaxis().SetTitleSize(0.09)
        h_data.GetYaxis().SetTitleOffset(1.53)
        
        h_data.SetTitle('')
        h_data.Draw('E0')
        
        for i in reversed(range(sizemclist)):
            h_mc_list[i].Draw('hist same')

        h_data.Draw("E0  same ")
        pt.Draw("'NDC' same")

        legend1 = ROOT.TLegend(0.70,0.88,0.52,0.60)
        legend1.SetLineColor(0)
        legend1.SetFillStyle(1)
        legend1.AddEntry( h_data ,"Data","lp")
        for i in reversed(range(sizemclist)):
            legend1.AddEntry( h_mc_list[i], str(h_mc_list[i].GetTitle()),"f")
        legend1.Draw()
        
        

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
        #h_ratio.SetMarkerSize(1.50)
        h_ratio.SetLineColor(ROOT.kBlack)
         
        #h_ratio.GetYaxis().SetLabelOffset(0.01) #сдвиг цифр
        
        #h_ratio.GetYaxis().SetLabelFont(2)
        h_ratio.GetXaxis().SetLabelSize(0.07)
        h_ratio.GetYaxis().SetTitle("#scale[2]{Data / Model  }")
        h_ratio.GetXaxis().SetTitle("#scale[2.4]{%s}"%self.SetTitleX)
        h_ratio.GetXaxis().SetLabelOffset(0.01)
        
        #####################################
        h_ratio.GetXaxis().SetTitleOffset(2.4)
        #h_ratio.GetXaxis().SetTitleSize(0.1)

        h_ratio.GetYaxis().SetRangeUser(self.minYaxispad2, self.maxYaxispad2)
       # h_ratio.GetXaxis().SetRangeUser(40, 140)
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
    
    
#NEW FUNCTION 
dirmc = '/eos/user/s/smwbr/dponomar/WTauData/v10s04/year15/filtered/SR/nom_mu'
dirdata = '/eos/user/s/smwbr/dponomar/WTauData/v10s04/year15/filtered/SR/data_mu'
listOfFilesmc = os.listdir(dirmc)
listOfFilesdata = os.listdir(dirdata)
def ghst(channel, var, dataset):
    
   
    if 'Data' in str(channel):
        listOfFiles=listOfFilesdata
        dirname = dirdata
    else:
        listOfFiles=listOfFilesmc
        dirname = dirmc
        
    dirlist = dsidDict_v9.get(channel)
    k = 0
    for dsid in dirlist:
        for directory in listOfFiles:
            if str(dsid) in directory:
                dataset.findFilesByPath(dirname +'/'+directory)

                h = dataset.getHistogram(var)
                
        if k == 0:
            hClone = h.Clone()
            hClone.SetDirectory(0)
            k+=1
            print(k)
        else:
            hClone.Add(h)
        print(k)
    return hClone 

# In[ ]:

zmumu = '/eos/user/s/smwbr/dponomar/WTauData/v10s04/year15/filtered/SR/nom_mu/user.dponomar.v10s04.mc16_13TeV.361107.PoPy8_Zmumu.M4.e3601_s3126_r9364_r9315_p3731.nom_mu_SM'
ztt = '/eos/user/s/smwbr/dponomar/WTauData/v10s04/year15/filtered/SR/nom_mu/user.dponomar.v10s04.mc16_13TeV.361108.PoPy8_Ztt.M4.e3601_s3126_r9364_r9315_p3729.nom_mu_SM'

Top = DataSet('Top')
Diboson = DataSet('Diboson')
Wmu = DataSet('W#rightarrow#mu#nu')
Tau = DataSet('W#rightarrow#tau#nu')
Data = DataSet('data')
Zmumu = DataSet('Z#rightarrow#mu#mu')
Ztt = DataSet('Z#rightarrow#tau#tau ')
Data.isData = True



Zmumu.findFilesByPath(zmumu)
Ztt.findFilesByPath(ztt)

var = Variable('lepmet_dphi', 16, 0, math.pi)


h_data = ghst('Data',var,Data)
h_top = ghst('Top',var,Top)
h_diboson = ghst('Diboson',var,Diboson)
h_wmu = ghst('Wmu',var,Wmu)
h_tau = ghst('Wt',var,Tau)

h_zmumu = Zmumu.getHistogram(var)
h_ztt = Ztt.getHistogram(var)
h_mc_list = [h_top, h_diboson, h_ztt, h_tau, h_zmumu, h_wmu]

plotdphi = Plotter(1800000000, 0.5, 1.5)
plotdphi.SetTitleX = 'd#phi(lep-MET)'
plotdphi.SetTitleY = 'Evants/0.197'
plotdphi.painter(h_data,h_mc_list)



dir_top = '/eos/user/g/gtolkach/NEWDATA/top'
dir_diboson = '/eos/user/g/gtolkach/NEWDATA/diboson'
dir_wmu = '/eos/user/g/gtolkach/NEWDATA/mu'
dir_wtau = '/eos/user/g/gtolkach/NEWDATA/tau'
data = '/eos/user/g/gtolkach/NEWDATA/Data'
zmumu = '/eos/user/g/gtolkach/NEWDATA/Zmumu'
ztt = '/eos/user/g/gtolkach/NEWDATA/Ztt'
Top = DataSet('Top')

Diboson = DataSet('Diboson')
Wmu = DataSet('W#rightarrow#mu#nu')
Tau = DataSet('W#rightarrow#tau#nu')
Data = DataSet('data')
Zmumu = DataSet('Z#rightarrow#mu#mu')
Ztt = DataSet('Z#rightarrow#tau#tau ')


Data.isData = True

Top.findFilesByPath(dir_top)
Diboson.findFilesByPath(dir_diboson)
Wmu.findFilesByPath(dir_wmu)
Tau.findFilesByPath(dir_wtau )
Data.findFilesByPath(data)
Zmumu.findFilesByPath(zmumu)
Ztt.findFilesByPath(ztt)


# In[ ]:


var = Variable('lepmet_dphi', 16, 0, math.pi)
h_top = Top.getHistogram(var)
h_diboson = Diboson.getHistogram(var)
h_wmu = Wmu.getHistogram(var)
h_tau = Tau.getHistogram(var)
h_data = Data.getHistogram(var)
h_zmumu = Zmumu.getHistogram(var)
h_ztt = Ztt.getHistogram(var)
h_mc_list = [h_top, h_diboson, h_ztt, h_tau, h_zmumu, h_wmu]


# In[211]:


# maxYaxixpad1  minYaxixpad2 
plotdphi = Plotter(1400000000, 0.6, 1.4)
plotdphi.SetTitleX = 'd#phi(lep-MET)'
plotdphi.SetTitleY = 'Evants/0.197'
plotdphi.painter(h_data,h_mc_list)


# In[203]:





# In[205]:


varPhi = Variable('met_reco_p4_fast.Phi()', 30, -math.pi - 1, math.pi+1)


# In[206]:


h_top = Top.getHistogram(varPhi)
h_diboson = Diboson.getHistogram(varPhi)
h_wmu = Wmu.getHistogram(varPhi)
h_tau = Tau.getHistogram(varPhi)
h_data = Data.getHistogram(varPhi)
h_zmumu = Zmumu.getHistogram(varPhi)
h_ztt = Ztt.getHistogram(varPhi)
h_mc_list = [h_top, h_diboson, h_ztt, h_tau, h_zmumu, h_wmu]


# In[217]:


# maxYaxixpad1  minYaxixpad2 
plotPhi = Plotter(1600000, 0.6, 1.4)
plotPhi.SetTitleX = '#phi'
plotPhi.SetTitleY = 'Evants'
plotPhi.painter(h_data,h_mc_list)


# In[218]:


varEta = Variable('lep_0_p4_fast.Eta()', 30, -3, 3)
h_top = Top.getHistogram(varEta)
h_diboson = Diboson.getHistogram(varEta)
h_wmu = Wmu.getHistogram(varEta)
h_tau = Tau.getHistogram(varEta)
h_data = Data.getHistogram(varEta)
h_zmumu = Zmumu.getHistogram(varEta)
h_ztt = Ztt.getHistogram(varEta)
h_mc_list = [h_top, h_diboson, h_ztt, h_tau, h_zmumu, h_wmu]


# In[220]:


plotEta = Plotter(1450000, 0.6, 1.4)
plotEta.SetTitleX = '#eta'
plotEta.SetTitleY = 'Evants'
plotEta.painter(h_data,h_mc_list)


# In[226]:


varMt = Variable('lepmet_mt', 30, 30, 150)
h_top = Top.getHistogram(varMt)
h_diboson = Diboson.getHistogram(varMt)
h_wmu = Wmu.getHistogram(varMt)
h_tau = Tau.getHistogram(varMt)
h_data = Data.getHistogram(varMt)
h_zmumu = Zmumu.getHistogram(varMt)
h_ztt = Ztt.getHistogram(varMt)
h_mc_list = [h_top, h_diboson, h_ztt, h_tau, h_zmumu, h_wmu]


# In[230]:


plotMt = Plotter(3450000, 0.6, 1.4)
plotMt.SetTitleX = 'M_{T}[GeV]'
plotMt.SetTitleY = 'Evants/2GeV'
plotMt.painter(h_data,h_mc_list)


# In[ ]:




