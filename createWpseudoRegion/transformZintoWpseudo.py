#!/usr/bin/env python
# coding: utf-8

# In[1]:


import ROOT
import shutil
import random
from array import array
from ROOT import gDirectory
import uuid
import os


# In[4]:


def createPseudo(input_path):
    listPath = input_path.split('/')
    
    outputfinalfilename  = listPath[len(listPath) - 1 ]
    
    nameGUID = str(uuid.uuid4().hex)
    output_dir_path = '/eos/user/g/gtolkach/pseudo/'
    outputfinaldir = output_dir_path+'/'+listPath[len(listPath) - 3 ]
    branch_file_path = output_dir_path+nameGUID +  '_branch_tree.root'
    clone_tree_file = output_dir_path +nameGUID + '_clone_tree.root'
    
    
    result_file = outputfinaldir +'/'+ outputfinalfilename
    if not os.path.exists(outputfinaldir):
        os.makedirs(outputfinaldir)
    
    print('Output branch file: %s'%branch_file_path)
    print('Output clone tree file: %s'%clone_tree_file)
    print('Output result file: %s'%result_file)
    f = ROOT.TFile.Open(input_path)
    input_tree = f.Get('MicroTree/microtree')
    branch_file = ROOT.TFile.Open(branch_file_path,"RECREATE")
    branch_tree = ROOT.TTree("microtree","Simple Tree")
    lep_0_p4 = ROOT.TLorentzVector(0,0,0,0)
    met_reco_p4 = ROOT.TLorentzVector(0,0,0,0)
    b1 = branch_tree.Branch('lep_0_p4','TLorentzVector',lep_0_p4,)
    b2 = branch_tree.Branch('met_reco_p4','TLorentzVector',met_reco_p4)
    
    print('Recreate branch file with %s event '% input_tree.GetEntries())
    for i in range(input_tree.GetEntries()):
        input_tree.GetEntry(i)
        rand = random.choices([0, 1], weights=[50, 50 ])[0]
    
        if rand:
            lep_0_p4.SetPtEtaPhiE(input_tree.lep_0_p4.Pt(),input_tree.lep_0_p4.Eta(),input_tree.lep_0_p4.Phi(),input_tree.lep_0_p4.E())
            metPt = input_tree.met_reco_p4.Pt() + input_tree.lep_1_p4.Pt()
            metEta = input_tree.met_reco_p4.Eta()+ input_tree.lep_1_p4.Eta()
            metPhi = input_tree.met_reco_p4.Phi()+ input_tree.lep_1_p4.Phi()
            metE = input_tree.met_reco_p4.E()+ input_tree.lep_1_p4.E()
            met_reco_p4.SetPtEtaPhiE(metPt,metEta,metPhi,metE)
        else:
            lep_0_p4.SetPtEtaPhiE(input_tree.lep_1_p4.Pt(),input_tree.lep_1_p4.Eta(),input_tree.lep_1_p4.Phi(),input_tree.lep_1_p4.E())
            metPt = input_tree.met_reco_p4.Pt() + input_tree.lep_0_p4.Pt()
            metEta = input_tree.met_reco_p4.Eta() + input_tree.lep_0_p4.Eta()
            metPhi = input_tree.met_reco_p4.Phi()+ input_tree.lep_0_p4.Phi()
            metE = input_tree.met_reco_p4.E()+ input_tree.lep_0_p4.E()
            met_reco_p4.SetPtEtaPhiE(metPt,metEta,metPhi,metE)
        branch_tree.Fill()
    branch_file.Write('', ROOT.TObject.kOverwrite)
    branch_file.Close()
    del branch_tree 
    del input_tree
    f.Close()
    
    
    f = ROOT.TFile.Open(input_path)
    treeForClone = f.Get('MicroTree/microtree')
    treeForClone.SetBranchStatus("lep_0_p4", 0)
    treeForClone.SetBranchStatus("met_reco_p4", 0)
    clonetree_file = ROOT.TFile.Open(clone_tree_file,"RECREATE")
    print('Clone new tree')
    cloneTree = treeForClone.CloneTree()
    clonetree_file.Write('', ROOT.TObject.kOverwrite)
    clonetree_file.Close()
    f.Close()
    del treeForClone
    del cloneTree
    
    branch_file = ROOT.TFile.Open(branch_file_path,"OPEN")
    branch_tree = branch_file.Get('microtree')
    branch_tree.AddFriend('microtree',clone_tree_file)
    print('AddFriend clone file to branch file and Snapshot')
    df = ROOT.RDataFrame(branch_tree)
    df.Snapshot('MicroTree/microtree',result_file)
    
    branch_file.Close()
    del branch_tree
    
    if 'MC' in listPath[len(listPath) - 3 ]:
        f = ROOT.TFile.Open(input_path) 
        h_metadata = f.Get('MicroTree/h_metadata')
        print("Write %s in resultfile"%h_metadata)
        outputfile = ROOT.TFile.Open(result_file,"UPDATE")
        outputfile.cd('MicroTree')
        h_metadata.Write()
        outputfile.Close()
        f.Close()
      
    if os.path.isfile(branch_file_path):
        os.remove(branch_file_path)
    if os.path.isfile(clone_tree_file):
        os.remove(clone_tree_file)


# In[17]:


data_files = '/eos/user/s/smwbr/LowMu/histograms/v20200821_dponomar_prod_LUZanalysis/LUZanalysis_MicroTree_zmumu_DATA_13TeV/Nominal/'
data_file_list = os.listdir(data_files)
#createPseudo(data_files)


# In[2]:


mc_files = '/eos/user/s/smwbr/LowMu/histograms/v20200821_dponomar_prod_LUZanalysis/LUZanalysis_MicroTree_zmumu_MC_13TeV/Nominal/'
mc_file_list = os.listdir(mc_files)


# In[ ]:


for i in data_file_list:
    print('createPseudo(): addfile %s'%(data_files + i))
    createPseudo(data_files + i)


# In[6]:


k = 0
for i in mc_file_list:
    if not 'sys' in i:
        if k >=260:  
            print('createPseudo(): addfile %s'%(mc_files + i))
            createPseudo(mc_files + i)
        k+=1
print(k)


# In[30]:


len(mc_file_list)


# In[ ]:




