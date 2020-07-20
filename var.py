   def createHistogramFromTree( self, tree, title='', weightExpression=None, drawOption='', style=None, nEntries=-1, firstEntry=0 ):
        if not tree:
            return
        if not nEntries or nEntries < 0:
            from ROOT import TTree
            nEntries = TTree.kMaxEntries

        cut = weightExpression if weightExpression else Cut()
        cut *= self.defaultCut

        if not cut.cut: cut = '1'
        else: cut = cut.cut
        if not weightExpression.cut : weightExpression = '1'
        else: weightExpression = weightExpression.cut
        self.logger.debug('createHistogramFromTree(): setting up weightExpression: %s' % weightExpression)
        self.logger.debug('createHistogramFromTree(): setting up cut: %s' % cut)

        # create an empty histogram
        h = self.createHistogram( title )

        # define unic weight name and variable name and make it compatible with C++
        histName = h.GetName()
        wName = (histName + '_weight').replace('-', '_')
        varNameX = (histName + '_variable').replace('-', '_')
        self.logger.debug('createHistogramFromTree(): wName: %s' % wName)
        self.logger.debug('createHistogramFromTree(): varNameX: %s' % varNameX)

        EnableImplicitMT()

        # no range set, need to determine from values
        if self.binning.low is None or self.binning.high is None:
            self.logger.debug( 'createHistogramFromTree(): missing range from binning - determining range automatically.' )
            dfTemp = RDataFrame(tree)
            hdfTemp = dfTemp.Filter(cut)\
                            .Range(1000)\
                            .Define(varNameX, '%s'%(self.command))\
                            .Histo1D(varNameX)

            hTemp = hdfTemp.GetPtr()

            if hTemp:
                low = max(hTemp.GetXaxis().GetXmin(), hTemp.GetMean()-3*hTemp.GetStdDev()) if self.binning.low is None else self.binning.low
                up = min(hTemp.GetXaxis().GetXmax(), hTemp.GetMean()+3*hTemp.GetStdDev()) if self.binning.high is None else self.binning.high
                # reset axis with the new limits
                h.GetXaxis().Set( self.binning.nBins, low, up )
            else:
                self.logger.error('createHistogramFromTree(): no histogram created from RDataFrame')
        else:
            h.GetXaxis().Set(self.binning.nBins, self.binning.low, self.binning.high)

        model = ROOT.RDF.TH1DModel(h)
        df = RDataFrame(tree)
        # I tried using .Range(firstEntry,nEntries), but it doesn't work.
        self.logger.debug('createHistogramFromTree(): Running TH1')
        self.logger.debug('createHistogramFromTree(): self.command: %s' % self.command)
        hdf = df.Filter(cut)\
                .Define(varNameX, '%s'%(self.command))\
                .Define(wName, '%s'%(weightExpression))\
                .Histo1D(model, varNameX, wName)

        h.Add(hdf.GetPtr())

        if h:
            self.logger.debug( 'createHistogramFromTree(): created histogram with %d entries and an integral of %g' % (h.GetEntries(), h.Integral()) )

            if style:
                style.apply( h )
                self.logger.error(style)
        else:
            self.logger.error( 'createHistogramFromTree(): no histogram created from RDataFrame')

        DisableImplicitMT()

        return h
