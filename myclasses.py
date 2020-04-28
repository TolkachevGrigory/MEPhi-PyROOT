#!/usr/bin/env python
# coding: utf-8

# In[3]:


import ROOT
import os
import math 
from ROOT import TFile, TString
from array import array
from ROOT import RDataFrame
from ROOT import gStyle
from ROOT import gPad


# In[4]:


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


# In[30]:


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
        self.listchanneldsid = []
        self.listforgethisto = []
        self.path = ''
    
    def findFilesByPath(self, listchanneldsid, path):
    
        self.path = path
        self.listdsid = os.listdir(self.path)
        self.listchanneldsid = listchanneldsid
        print(listchanneldsid)
        
        for  channeldsid in self.listchanneldsid:
            for dsid in self.listdsid:
                if str(channeldsid) in dsid:
                    self.listforgethisto.append(self.path +'/'+dsid)
    
    def getHistogram(self, var):
    
        hClone = None
        k = 0
        for dirpath in self.listforgethisto:
            #print(dirpath)
            
            if self.isData == False:
                kf =  11.246151648051285
                lumi2015 = 3219.56  # pb-1
                bin_8 = 0 
                
               
                for filename in os.listdir(dirpath):
                    f = ROOT.TFile.Open(dirpath+'/'+ filename)
                    h_8bin = f.Get('h_metadata')
                    bin_8+= h_8bin.GetBinContent(8)
                print(bin_8)
                        
                df = ROOT.RDataFrame(self.treeName, dirpath+'/*.root')
               # weight1 = '(weight_mc*(cross_section*filter_efficiency*kfactor))*((((((((((NOMINAL_pileup_random_run_number<284490)*NOMINAL_pileup_combined_weight)*(lep_0_NOMINAL_MuEffSF_TTVA))*(jet_NOMINAL_global_effSF_MV2c10*jet_NOMINAL_global_ineffSF_MV2c10))*(jet_NOMINAL_central_jets_global_effSF_JVT*jet_NOMINAL_central_jets_global_ineffSF_JVT))*(lep_0_NOMINAL_MuEffSF_Reco_QualMedium))*(lep_0_NOMINAL_MuEffSF_IsoFCLoose))*(1))*((NOMINAL_pileup_random_run_number<284490)*(lep_0_NOMINAL_MuEffSF_HLT_mu20_iloose_L1MU15_OR_HLT_mu50_QualMedium_IsoNone)+(NOMINAL_pileup_random_run_number>=284490)*(lep_0_NOMINAL_MuEffSF_HLT_mu26_ivarmedium_OR_HLT_mu50_QualMedium_IsoNone)))*(jet_NOMINAL_forward_jets_global_effSF_JVT*jet_NOMINAL_forward_jets_global_ineffSF_JVT))"
                #weight = '(weight_mc*(cross_section*filter_efficiency*kfactor))*((((((((((1)*(lep_0_NOMINAL_MuEffSF_HLT_mu20_iloose_L1MU15_OR_HLT_mu50_QualMedium_IsoNone))*(lep_0_NOMINAL_MuEffSF_TTVA))*(lep_0_NOMINAL_MuEffSF_IsoFCTight))*(jet_NOMINAL_global_effSF_MV2c10*jet_NOMINAL_global_ineffSF_MV2c10))*((NOMINAL_pileup_random_run_number<284490)*NOMINAL_pileup_combined_weight))*(jet_NOMINAL_central_jets_global_effSF_JVT*jet_NOMINAL_central_jets_global_ineffSF_JVT))*(lep_0_NOMINAL_MuEffSF_Reco_QualMedium))*(1))*(jet_NOMINAL_forward_jets_global_effSF_JVT*jet_NOMINAL_forward_jets_global_ineffSF_JVT))'
               # weight = 'weight_mc*cross_section*filter_efficiency*kfactor*NOMINAL_pileup_combined_weight*lep_0_NOMINAL_MuEffSF_TTVA*jet_NOMINAL_global_effSF_MV2c10*jet_NOMINAL_global_ineffSF_MV2c10*jet_NOMINAL_central_jets_global_effSF_JVT*jet_NOMINAL_central_jets_global_ineffSF_JVT*lep_0_NOMINAL_MuEffSF_Reco_QualMedium*lep_0_NOMINAL_MuEffSF_IsoFCLoose*lep_0_NOMINAL_MuEffSF_HLT_mu20_iloose_L1MU15_OR_HLT_mu50_QualMedium_IsoNone'
                weight = '(weight_mc*(cross_section*filter_efficiency*kfactor))*(((((((((NOMINAL_pileup_combined_weight)*(lep_0_NOMINAL_MuEffSF_TTVA))*(lep_0_NOMINAL_MuEffSF_IsoFCTight))*(jet_NOMINAL_global_effSF_MV2c10*jet_NOMINAL_global_ineffSF_MV2c10))*(jet_NOMINAL_central_jets_global_effSF_JVT*jet_NOMINAL_central_jets_global_ineffSF_JVT))*(lep_0_NOMINAL_MuEffSF_Reco_QualMedium))*(1))*((lep_0_NOMINAL_MuEffSF_HLT_mu20_iloose_L1MU15_OR_HLT_mu50_QualMedium_IsoNone)))*(jet_NOMINAL_forward_jets_global_effSF_JVT*jet_NOMINAL_forward_jets_global_ineffSF_JVT))'
                #weight = 'weight_mc*NOMINAL_pileup_combined_weight*cross_section*filter_efficiency*kfactor'
                h = df.Filter('((HLT_mu20_iloose_L1MU15 && muTrigMatch_0_HLT_mu20_iloose_L1MU15)||(HLT_mu50 && muTrigMatch_0_HLT_mu50))>0')
                      .Filter('NOMINAL_pileup_random_run_number<284485')
                      .Filter('lep_0==1')
                      .Filter('(n_electrons+n_muons)==1')
                      .Filter('n_taus==0')
                      .Filter('lep_0_id_tight==1')
                      .Filter('lep_0_iso_FCTight==1')
                      .Filter('lep_0_id_tight==1')
                      .Filter('fabs(lep_0_p4_fast.Eta())<2.4')
                      .Filter('lep_0_p4_fast.Pt()>27')
                      .Filter('met_reco_p4_fast.Et()>25')
                      .Filter('lepmet_mt>40')
                      .Filter('(lep_0_iso_ptcone20_TightTTVA_pt1000/(lep_0_p4_fast.Pt()*1000))<0.06')
                      .Define('v', var.command)
                      .Define('w1', str(kf*lumi2015/bin_8))
                      .Define('w2', weight)
                      .Define('w', 'w1*w2')
                      .Histo1D(("%s"%(var.name), "%s"%(self.name), var.nbins, var.low, var.high), 'v', 'w')
            else:
                df = ROOT.RDataFrame(self.treeName, dirpath+'/*.root')
                h = df.Filter('((HLT_mu20_iloose_L1MU15 && muTrigMatch_0_HLT_mu20_iloose_L1MU15)||(HLT_mu50 && muTrigMatch_0_HLT_mu50))>0')
                      .Filter('run_number<284485')
                      .Filter('lep_0==1')
                      .Filter('(n_electrons+n_muons)==1')
                      .Filter('n_taus==0')
                      .Filter('lep_0_id_tight==1')
                      .Filter('lep_0_iso_FCTight==1')
                      .Filter('lep_0_id_tight==1')
                      .Filter('fabs(lep_0_p4_fast.Eta())<2.4')
                      .Filter('lep_0_p4_fast.Pt()>27')
                      .Filter('met_reco_p4_fast.Et()>25')
                      .Filter('lepmet_mt>40')
                      .Filter('(lep_0_iso_ptcone20_TightTTVA_pt1000/(lep_0_p4_fast.Pt()*1000))<0.06')
                      .Define('v', var.command)
                      .Histo1D(("%s"%(var.name), "%s"%(self.name), var.nbins, var.low, var.high),'v')                   
            if k == 0:
                hClone = h.Clone()
                hClone.SetDirectory(0)
                
                 
            else:
                hClone.Add(h.GetPtr())
            k+=1
        return hClone
    
    


# In[42]:


class Plotter:
    def __init__(self, maxYaxispad1, minYaxispad2,  maxYaxispad2):
        self.minYaxispad1 = 0
        self.maxYaxispad1 = maxYaxispad1
        self.minYaxispad2 = minYaxispad2
        self.maxYaxispad2 = maxYaxispad2
        self.SetTitleX = ''
        self.SetTitleY = ''
    
    
  
    
    def painter(self, h_data, h_mc_list):
        #print(type(h_mc_list[5]))
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
        if 'lepmet_dphi' in h_mc_list[0].GetName():
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

        legend1 = ROOT.TLegend(0.70,0.88,0.52,0.7)
        legend1.SetLineColor(0)
        legend1.SetFillStyle(1)
        legend2 = ROOT.TLegend(0.88,0.88,0.70,0.7)
        legend2.SetLineColor(0)
        legend2.SetFillStyle(1)
        
        legend1.AddEntry( h_data ,"Data","lp")
        
        for i in reversed(range(int(sizemclist/2),sizemclist)):
            legend1.AddEntry( h_mc_list[i], str(h_mc_list[i].GetTitle()),"f")
        legend1.Draw()
        
        for i in reversed(range(0,int(sizemclist/2))):
            legend2.AddEntry( h_mc_list[i], str(h_mc_list[i].GetTitle()),"f")
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
        #h_ratio.SetMarkerSize(1.50)
        h_ratio.SetLineColor(ROOT.kBlack)
         
        #h_ratio.GetYaxis().SetLabelOffset(0.01) #сдвиг цифр
        
        #h_ratio.GetYaxis().SetLabelFont(2)
        h_ratio.GetXaxis().SetLabelSize(0.07)
        h_ratio.GetYaxis().SetTitle("#scale[2.4]{Data / Model  }")
        h_ratio.GetXaxis().SetTitle("#scale[2.4]{%s}"%self.SetTitleX)
        h_ratio.GetXaxis().SetLabelOffset(0.01)
        h_ratio.GetYaxis().SetTitleOffset(1.4)
        #####################################
        h_ratio.GetXaxis().SetTitleOffset(2.4)
        #h_ratio.GetXaxis().SetTitleSize(0.1)

       
       # h_ratio.GetXaxis().SetRangeUser(40, 140)
        h_ratio.SetLineWidth(2)
        h_ratio.Draw("E")
        mcSumRatioHist.Draw(' E2 same')
        h_ratio.Draw("E same")
        gr1.Draw('same')
        h_ratio.GetYaxis().SetRangeUser(self.minYaxispad2, self.maxYaxispad2)
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


# In[32]:


dsidDict_v9 = {
    # PowhegPythia8EvtGen
    'Wmu': [361101, 361104],
    'We': [361100, 361103],
    'Wt': [361102, 361105],
    'DYee': [361106],
    'DYmm': [361107],
    'DYtt': [361108],
    'Top': [410013, 410014, 410470] + [410644, 410645, 410646],  # [410025]+[410647], is not in DBs
    'Diboson': [363356, 363358, 363359, 363360, 363489] + [364250, 364253, 364254, 364255],
    'QCD': [],
    'Data': ['periodD','periodE','periodF','periodG','periodH','periodJ' ],
}


# In[ ]:





# In[33]:



Top = DataSet('Top')
Diboson = DataSet('Diboson')
Wmu = DataSet('W#rightarrow#mu#nu')
Tau = DataSet('W#rightarrow#tau#nu')
Data = DataSet('data')
Zmumu = DataSet('Z#rightarrow#mu#mu')
Ztt = DataSet('Z#rightarrow#tau#tau ')
Data.isData = True


Top.findFilesByPath(dsidDict_v9.get('Top'),'/eos/user/s/smwbr/dponomar/WTauData/v10s04/year15/filtered/SR/nom_mu')
Diboson.findFilesByPath(dsidDict_v9.get('Diboson'),'/eos/user/s/smwbr/dponomar/WTauData/v10s04/year15/filtered/SR/nom_mu')
Wmu.findFilesByPath(dsidDict_v9.get('Wmu'),'/eos/user/s/smwbr/dponomar/WTauData/v10s04/year15/filtered/SR/nom_mu')
Tau.findFilesByPath(dsidDict_v9.get('Wt'),'/eos/user/s/smwbr/dponomar/WTauData/v10s04/year15/filtered/SR/nom_mu')
Data.findFilesByPath(dsidDict_v9.get('Data'),'/eos/user/s/smwbr/dponomar/WTauData/v10s04/year15/filtered/SR/data_mu')
Zmumu.findFilesByPath(dsidDict_v9.get('DYmm'),'/eos/user/s/smwbr/dponomar/WTauData/v10s04/year15/filtered/SR/nom_mu')
Ztt.findFilesByPath(dsidDict_v9.get('DYtt'),'/eos/user/s/smwbr/dponomar/WTauData/v10s04/year15/filtered/SR/nom_mu')


# In[50]:


var = Variable('lepmet_dphi', 16, 0, math.pi)
h_top = Top.getHistogram(var)
h_diboson = Diboson.getHistogram(var)
h_wmu = Wmu.getHistogram(var)
h_tau = Tau.getHistogram(var)
h_data = Data.getHistogram(var)
h_zmumu = Zmumu.getHistogram(var)
h_ztt = Ztt.getHistogram(var)
h_mc_list = [h_top, h_diboson, h_ztt, h_tau, h_zmumu, h_wmu]


# In[98]:


# maxYaxixpad1  minYaxixpad2 
plotdphi = Plotter(1800000000, 0.3, 1.7)
plotdphi.SetTitleX = 'd#phi(lep-MET)'
plotdphi.SetTitleY = 'Evants/0.197'
plotdphi.painter(h_data,h_mc_list)


# In[99]:


varPhi = Variable('met_reco_p4_fast.Phi()', 32, -math.pi, math.pi)


# In[100]:


h_top = Top.getHistogram(varPhi)
h_diboson = Diboson.getHistogram(varPhi)
h_wmu = Wmu.getHistogram(varPhi)
h_tau = Tau.getHistogram(varPhi)
h_data = Data.getHistogram(varPhi)
h_zmumu = Zmumu.getHistogram(varPhi)
h_ztt = Ztt.getHistogram(varPhi)
h_mc_list = [h_top, h_diboson, h_ztt, h_tau, h_zmumu, h_wmu]


# In[109]:


# maxYaxixpad1  minYaxixpad2 
plotPhi = Plotter(770000, 0.8, 1.2)
plotPhi.minYaxispad1 = 130000
plotPhi.SetTitleX = '#phi_{ MET}'
plotPhi.SetTitleY = 'Evants/0.197'
plotPhi.painter(h_data,h_mc_list)


# In[110]:


varPhilep = Variable('lep_0_p4_fast.Phi()', 32, -math.pi, math.pi)


# In[111]:


h_top = Top.getHistogram(varPhilep)
h_diboson = Diboson.getHistogram(varPhilep)
h_wmu = Wmu.getHistogram(varPhilep)
h_tau = Tau.getHistogram(varPhilep)
h_data = Data.getHistogram(varPhilep)
h_zmumu = Zmumu.getHistogram(varPhilep)
h_ztt = Ztt.getHistogram(varPhilep)
h_mc_list = [h_top, h_diboson, h_ztt, h_tau, h_zmumu, h_wmu]


# In[119]:


# maxYaxixpad1  minYaxixpad2 
plotPhilep = Plotter(790000, 0.8, 1.2)
plotPhilep.minYaxispad1 = 130000
plotPhilep.SetTitleX = 'lep #phi'
plotPhilep.SetTitleY = 'Evants/0.197'
plotPhilep.painter(h_data,h_mc_list)


# 

# In[120]:


varEta = Variable('lep_0_p4_fast.Eta()', 30, -2.5, 2.5)
h_top = Top.getHistogram(varEta)
h_diboson = Diboson.getHistogram(varEta)
h_wmu = Wmu.getHistogram(varEta)
h_tau = Tau.getHistogram(varEta)
h_data = Data.getHistogram(varEta)
h_zmumu = Zmumu.getHistogram(varEta)
h_ztt = Ztt.getHistogram(varEta)
h_mc_list = [h_top, h_diboson, h_ztt, h_tau, h_zmumu, h_wmu]


# In[125]:


plotEta = Plotter(1000000, 0.6, 1.4)
plotEta.SetTitleX = 'lep #eta'
plotEta.SetTitleY = 'Evants/0.167'
plotEta.painter(h_data,h_mc_list)


# In[79]:


varMt = Variable('lepmet_mt', 60, 40, 160)
h_top = Top.getHistogram(varMt)
h_diboson = Diboson.getHistogram(varMt)
h_wmu = Wmu.getHistogram(varMt)
h_tau = Tau.getHistogram(varMt)
h_data = Data.getHistogram(varMt)
h_zmumu = Zmumu.getHistogram(varMt)
h_ztt = Ztt.getHistogram(varMt)
h_mc_list = [h_top, h_diboson, h_ztt, h_tau, h_zmumu, h_wmu]


# In[80]:


h_top.Integral()


# In[81]:


h_diboson.Integral()


# In[82]:


h_wmu.Integral()


# In[83]:


h_tau.Integral()


# In[84]:


h_data.Integral()


# In[85]:


h_zmumu.Integral()


# In[86]:


h_ztt.Integral()


# In[94]:


plotM2 = Plotter(1700000, 0.2, 1.8)
plotM2.SetTitleX = 'M_{T}[GeV]'
plotM2.SetTitleY = 'Evants/2GeV'
plotM2.painter(h_data,h_mc_list)


# In[126]:


varPt = Variable('lep_0_p4_fast.Pt()', 40, 20, 100)
h_top = Top.getHistogram(varPt)
h_diboson = Diboson.getHistogram(varPt)
h_wmu = Wmu.getHistogram(varPt)
h_tau = Tau.getHistogram(varPt)
h_data = Data.getHistogram(varPt)
h_zmumu = Zmumu.getHistogram(varPt)
h_ztt = Ztt.getHistogram(varPt)
h_mc_list = [h_top, h_diboson, h_ztt, h_tau, h_zmumu, h_wmu]


# In[132]:


plotPt = Plotter(2850000, 0.6, 1.4)
plotPt.SetTitleX = 'P_{T}[GeV]'
plotPt.SetTitleY = 'Evants/2GeV'
plotPt.painter(h_data,h_mc_list)


# In[133]:


varE = Variable('met_reco_p4_fast.E()', 45, 20, 110)
h_top = Top.getHistogram(varE)
h_diboson = Diboson.getHistogram(varE)
h_wmu = Wmu.getHistogram(varE)
h_tau = Tau.getHistogram(varE)
h_data = Data.getHistogram(varE)
h_zmumu = Zmumu.getHistogram(varE)
h_ztt = Ztt.getHistogram(varE)
h_mc_list = [h_top, h_diboson, h_ztt, h_tau, h_zmumu, h_wmu]


# In[137]:


plotE = Plotter(2450000, 0.6, 1.4)
plotE.SetTitleX = 'E_{MET}[GeV]'
plotE.SetTitleY = 'Evants/2GeV'
plotE.painter(h_data,h_mc_list)


# In[ ]:




