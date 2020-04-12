#!/usr/bin/env python
# coding: utf-8

# In[1]:


import ROOT
from ROOT import TMVA, TFile, TTree, TCut, TString


# In[2]:


outputFile = TFile( "TMVA.root", 'RECREATE' )
ROOT.TMVA.Tools.Instance()

factory = TMVA.Factory('TMVAClassification', outputFile,
                       '!V:!Silent:Color:DrawProgressBar:Transformations=G:AnalysisType=Classification')


# In[3]:


loader = TMVA.DataLoader("dataset_cv")
loader.AddVariable( "Pt","P_{T}","GeV", 'D' )
loader.AddVariable( "metE","E^{miss}_{T}","GeV",'D' )
loader.AddVariable( "dPhi","d#phi", 'D' )
loader.AddVariable( "Mt","M_{T}","GeV", 'D' )


# In[4]:


f1 = ROOT.TFile.Open('/eos/user/g/gtolkach/signal_event_with_cuts_plus.root')
f2 = ROOT.TFile.Open('/eos/user/g/gtolkach/beackground_event_with_cuts_plus.root')

signal = f1.Get('NOMINAL')
background = f2.Get('NOMINAL')


# In[5]:


loader.AddSignalTree    ( signal, 1.0 );
loader.AddBackgroundTree( background, 1.0);
loader.PrepareTrainingAndTestTree(TCut(""),
        "nTrain_Signal=86203 :nTrain_Background=412573 :SplitMode=Random:NormMode=NumEvents:!V")


# In[6]:


cv = TMVA.CrossValidation("TMVACrossValidation",loader,outputFile,"!V:!Silent:ModelPersistence:AnalysisType=Classification:NumFolds=3:SplitExpr=")


# In[7]:


cv.BookMethod(TMVA.Types.kMLP, "MLP", 
                   "H:!V:NeuronType=tanh:VarTransform=N:NCycles=600:HiddenLayers=N+1:TestRate=5:!UseRegulator")


# In[8]:


cv.Evaluate();


# In[9]:


resultsCV = cv.GetResults()


# In[10]:


print(cv.GetMethods()[0].GetValue("MethodName"))


# In[13]:


meth=0
for res_f in resultsCV:
    res_f
    print("mehtod = ",cv.GetMethods()[meth].GetValue("MethodName"),", average= ",res_f.GetROCAverage())
    meth=+1
    for iFold in range(cv.GetNumFolds()):
        print("    Fold ",iFold," ROC-integ= ",res_f.GetROCValues()[iFold],"BkgEff@SigEff=0.3: ",res_f.GetEff30Values()[iFold])


# In[14]:


resultsCV[0].GetROCAverage()


# In[15]:


outputFile.Close()


# In[16]:


get_ipython().run_line_magic('jsroot', 'on')


# In[17]:


resultsCV[0].Draw()


# In[ ]:




