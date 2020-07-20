    def createHistogramFromTree(self, tree, title='', weightExpression=None, drawOption='', style=None, nEntries=-1,
                                firstEntry=0):
        if not tree:
            return
        if not nEntries or nEntries < 0:
            from ROOT import TTree
            nEntries = TTree.kMaxEntries
        cut = weightExpression if weightExpression else Cut()
        cut *= self.defaultCut
        opt = drawOption + 'goff'
        # create an empty histogram
        h = self.createHistogram(title)
        # no range set, need to determine from values
        from ROOT import RDataFrame, ROOT
        from ROOT.ROOT import EnableImplicitMT
        EnableImplicitMT()
        df = RDataFrame(tree)
        EnableImplicitMT()

        if self.binning.low is None or self.binning.high is None:
            self.logger.debug( 'createHistogramFromTree(): missing range from binning - determining range automatically.' )
            tree.Draw( '%s >> temp(%d)' % ( self.command, 1000 ), cut.cut, opt )
            hTemp = tree.GetHistogram()
            if hTemp:
                low = max(hTemp.GetXaxis().GetXmin(), hTemp.GetMean()-3*hTemp.GetStdDev()) if self.binning.low is None else self.binning.low
                up = min(hTemp.GetXaxis().GetXmax(), hTemp.GetMean()+3*hTemp.GetStdDev()) if self.binning.high is None else self.binning.high

            if h:
                low = max(h.GetXaxis().GetXmin(), h.GetMean()-3*hTemp.GetStdDev()) if self.binning.low is None else self.binning.low
                up = min(h.GetXaxis().GetXmax(), h.GetMean()+3*hTemp.GetStdDev()) if self.binning.high is None else self.binning.high
                # reset axis with the new limits
                h.GetXaxis().Set( self.binning.nBins, low, up )
            else:
                self.logger.error( 'createHistogramFromTree(): no histogram created from TTree::Draw( "%s", "%s", "%s" )' % (self.command, cut.cut, drawOption) )
        else:
            h.GetXaxis().Set(self.binning.nBins, self.binning.low, self.binning.high)

        model = ROOT.RDF.TH1DModel( h )
        hdf = df.Define('v', str(self.command))\
                .Histo1D(model, 'v')

        h.Add(hdf.GetPtr())


        self.logger.debug( 'createHistogramFromTree(): calling TTree::Draw( "%s >> %s", "%s", "%s" )' % (self.command, h.GetName(), cut.cut, drawOption) )
       # tree.Draw( '%s >> %s' % (self.command, h.GetName()), cut.cut, opt, nEntries, firstEntry )

        if h:
            self.logger.debug( 'createHistogramFromTree(): created histogram with %d entries and an integral of %g' % (h.GetEntries(), h.Integral()) )
            if style:
                style.apply( h )
        else:
            self.logger.error( 'createHistogramFromTree(): no histogram created from TTree::Draw( "%s", "%s", "%s" )' % (self.command, cut.cut, drawOption) )

        DisableImplicitMT()
        return h
