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


f1 = ROOT.TFile.Open('/eos/user/g/gtolkach/NEWDATA/data_mu_6variables_forMVA.root')


# In[4]:


f2 = ROOT.TFile.Open('/eos/user/g/gtolkach/NEWDATA/Wmu_plus_6v_forMVA.root')
f3 = ROOT.TFile.Open('/eos/user/g/gtolkach/NEWDATA/Wmu_minus_6v_forMVA.root')


# In[5]:


f4 = ROOT.TFile.Open('/eos/user/g/gtolkach/NEWDATA/plus_Wtau_6v_forMVA.root')
f5 = ROOT.TFile.Open('/eos/user/g/gtolkach/NEWDATA/minus_Wtau_6v_forMVA.root')


# In[41]:


def rew(file, tp):
    
    tree = file.Get('NOMINAL')
    tree.SetBranchAddress("Pt", Pt)
    tree.SetBranchAddress("metE", MetE)
    tree.SetBranchAddress("dPhi", dPhi)
    tree.SetBranchAddress("PhiMiss", PhiMiss)
    tree.SetBranchAddress("Mt", Mt)
    tree.SetBranchAddress("Eta", Eta)
    
    h = ROOT.TH1D("h","", 30, -0.5 , 1)
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
            h.Fill(l,tree.kweight_mc*tree.NOMINAL_pileup_combined_weight*tree.cross_section*tree.filter_efficiency*kfactor*lumi2015/bin_8)
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


# In[42]:


h_data = rew(f1, 'data')


# In[43]:


h_wmu_plus = rew(f2, 'dd')
h_wmu_minus = rew(f3, 'dd')


# In[44]:


h_wtau_plus = rew(f4, 'data')
h_wtau_minus = rew(f5, 'data')


# In[75]:


c3 = ROOT.TCanvas() 

c3.Divide(1, 2)
#c1.SetLogy()
ROOT.gStyle.SetOptStat(0)
c3.cd(1)
c3.cd(1).SetMargin(0.1,0.3,0.01,1.5)
gPad = c3.cd(1)
gPad.SetLogy()

h_AddWmu = ROOT.TH1D("add1","",30, -0.5 , 1)
h_AddWmu.Add(h_wmu_plus, h_wmu_minus, 1, 1)


h_AddWtau = ROOT.TH1D("add2","",30, -0.5 , 1)
h_AddWtau.Add(h_wtau_plus,h_wtau_minus , 1, 1)


h_AddWtau.SetLineColor(36)
h_AddWmu.SetLineColor(36)
h_data.SetLineColor(ROOT.kBlack)

h_data.SetLineWidth(2)
h_data.SetMarkerStyle(15)

h_AddWmu.SetFillColor(ROOT.kRed)
h_AddWtau.SetFillColor(ROOT.kYellow)


#h_AddWmu.SetTitle("mc_wmu")
#h_data.SetTitle('data')
#h_AddWtau.SetTitle("mc_wtau")



#h_AddWmu.GetYaxis().SetRangeUser(0, 100000000)

h_AddWmu.GetXaxis().SetRangeUser(-0.5,  1)

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
h_data.Draw("P same")
h_AddWtau.Draw("hist same")

h_AddWmu.SetTitle('')

#ROOT.gPad.BuildLegend(1.0,0.8,0.8,0.5,"","")
legend1 = ROOT.TLegend(0.55,0.88,0.69,0.67)
legend1.AddEntry( h_data,"Data","lep")
legend1.AddEntry( h_AddWmu,"W#rightarrow#mu#nu ","f")
legend1.AddEntry( h_AddWtau,"W#rightarrow#tau#nu ","f")




h_add = ROOT.TH1D("add","",30, -0.5 , 1)
h_divide = ROOT.TH1D("divide","",30, -0.5 , 1)
h_add.Add(h_AddWtau, h_AddWmu, 1, 1)
h_divide.Divide(h_data, h_add, 1, 1)
c3.cd(2)



c3.cd(2).SetMargin(0.1,0.3,0.5,0.)

h_divide.SetMarkerStyle(15)
    
mc_x, mc_y = array('f'), array('f')
mc_ex, mc_ey = array('f'), array('f')

for i in range(0, 30):
    if i <=10:
        mc_x.append(0.05*i - 0.5)
        
    else:
        mc_x.append(0.05*i)
    mc_ex.append(0.025)
    mc_y.append(1)
    mc_ey.append(h_divide.GetBinError(i))
    
print(mc_x)
g = ROOT.TGraphErrors(30, mc_x, mc_y, mc_ex, mc_ey)


#h_divide.GetXaxis().SetRangeUser(-2,  1)
#g.GetYaxis().SetRangeUser(-1, 3)
legend1.AddEntry( g,"Stat.Uncert.","f")
legend1.Draw()


gr1 = ROOT.TGraph(2)
gr1.SetPoint(0, 0, 1)
gr1.SetPoint(1, 100, 1)
gr1.SetLineStyle(7)


#g.SetMarkerStyle(15)
g.SetFillColor(ROOT.kGreen -9)
g.SetLineColor(ROOT.kGreen -9)
#g.SetFillStyle( )

h_divide.GetYaxis().SetTitle("#scale[2]{Data / Model  }")
h_divide.GetXaxis().SetTitle("#scale[2]{TMVA MLP score}")

g.SetTitle('')
h_divide.SetLineColor(ROOT.kBlack)

#h_divide.GetXaxis().SetRangeUser(-0.5,  1)
g.GetXaxis().SetRangeUser(-0.5,  1)
g.GetYaxis().SetRangeUser(-1, 3)

h_divide.Draw("E")
g.Draw('A5 same')
h_divide.Draw("E same")
#gr1.Draw('Same')
gr1.Draw('same')
c3.cd(1)
legend1.Draw('same')
c3.Update()

c3.Draw()


# In[ ]:





# In[70]:


c3.SaveAs('h.pdf')


# In[ ]:




