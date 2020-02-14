#!/usr/bin/env python
# coding: utf-8

import ROOT
import sys

f = ROOT.TFile.Open('/eos/user/g/gtolkach/minus.1.SM_WLepton.root', 'READ')
get_ipython().run_line_magic('jsroot', 'on')
tree = f.Get("NOMINAL")


h1 = ROOT.TH1D("Pt", "lep;P_{T} [GeV];Entries",150,-50,200)
h1.SetDirectory(0)

c1 = ROOT.TCanvas()

entries = tree.GetEntries()
for i in range(0, entries):
    tree.GetEntry(i)
    h1.Fill(tree.lep_0_p4.Pt())

f.Close()
h1.Draw()
c1.Update()
c1.Draw()


# In[ ]:
