## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#  Plotting Outputs
#
#  (from covariance and sensitivity
#  calculations)
#
## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import ROOT
from ROOT import TFile, TCanvas, TH2D, TH1D, TGraph, TGraph2D, TStyle, TLegend
import argparse
import os


## Main function
## ~~~~~~~~~~~~~

def main(args):

    # Covariance, fractional covariance and correlation

    covfile = TFile(args.covfile)

    covcanvas = TCanvas()

    gStyle = TStyle()
    gStyle.SetPadLeftMargin(0.25); gStyle.SetPadRightMargin(0.15)
    gStyle.SetPalette(56)

    for matname in ('cov', 'fcov', 'corr'):

        mat = covfile.Get(matname)

        mat.GetYaxis().LabelsOption('v')    # doesn't work...
        mat.GetYaxis().SetLabelSize(0.07)
        mat.GetXaxis().SetLabelSize(0.07)

        mat.SetTitleSize(0.3, 't')  # doesn't work...

        if matname == 'corr': mat.GetZaxis().SetRangeUser(-0.4, 1)

        mat.Draw("colz")
        mat.SetStats(False)
        covcanvas.SaveAs(args.outdir + "cov_plot.pdf")


    # Chi squareds
    
    chi2file = TFile(args.chifile)
    
    chi2 = chi2file.Get('chisq')
    
    chi2canvas = TCanvas()
    
    chi2.SetTitle('#chi^{2}; log_{10}(sin^{2}(2#theta)); log_{10}(#Delta m^{2}); #chi^{2}');
    gStyle.SetPalette(1)
    chi2.Draw('surf1')
    chi2canvas.SaveAs(args.outdir + "chisq.pdf")
    
    # Contours
    contcanvas = TCanvas('cont_canvas', '', 1020, 990)
    gStyle.SetPadLeftMargin(0.15); gStyle.SetPadRightMargin(0.15)
    
    colours = [30, 38, 46]
    contours = [chi2file.Get('90pct'), 
                chi2file.Get('3sigma'), 
                chi2file.Get('5sigma')]
    
    for g in range(len(contour_graphs)):
        
        contours[g].SetMarkerStyle(20)
        contours[g].SetMarkerSize(0.25)
        contours[g].SetMarkerColor(colours[g])
        contours[g].SetLineColor(colours[g])
    
    gr_range = TGraph()
    gr_range.SetPoint(0, 0.001, 0.01)
    gr_range.SetPoint(1, 1, 100)
    gr_range.SetMarkerColor(0)
    
    bestfit = TGraph()
    bestfit.SetPoint(0, 0.062, 1.7)
    bestfit.SetMarkerStyle(29)
    bestfit.SetMarkerSize(1.6)
    bestfit.SetMarkerColor(40)
    
    gr_range.SetTitle('SBN Sensitivity; sin^{2}(2#theta); #Delta m^{2} (eV^{2})')
    
    legend = TLegend()
    legend.AddEntry(contours[0], '90% CL', 'l')
    legend.AddEntry(contours[1], '3#sigma CL', 'l')
    legend.AddEntry(contours[2], '5#sigma CL', 'l')
    legend.AddEntry(bestfit, 'Best Fit Point', 'p')
    
    contcanvas.SetLogy()
    contcanvas.SetLogx()
    
    gr_range.Draw('AP')
    gr_range.GetXaxis().SetRangeUser(0.001, 1)
    gr_range.GetYaxis().SetRangeUser(0.01, 100)
    
    contours[0].Draw('P same')
    contours[1].Draw('P same')
    contours[2].Draw('P same')
    
    legend.Draw()
    bestfit.Draw('P same')
    
    contcanvas.SaveAs(args.outdir+'Sensitivity.pdf')
    


def compare_w_proposal(args):
    
    pass
    ## nothing...


if __name__ == "__main__":
    
    buildpath = os.environ['SBN_LIB_DIR']
    if not buildpath:
        print('ERROR: SBNDDAQ_ANALYSIS_BUILD_PATH not set')
        sys.exit()
    
    ROOT.gROOT.ProcessLine('.L ' + buildpath + '/libsbnanalysis_Event.so')
    ROOT.gROOT.ProcessLine('.L ' + buildpath + '/libsbnanalysis_SBNOsc_classes.so')
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-chi", "--chifile", required = True)
    parser.add_argument("-cov", "--covfile", required = True)
    parser.add_argument("-o", "--outdir", required = True)
    parser.add_argument("-comp", "--compare", default = False)

    main(parser.parse_args())
    
    if parser.parse_args().compare: compare_w_proposal(parser_parse_args())






