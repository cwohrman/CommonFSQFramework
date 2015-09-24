void SetUpHist(TH1* h,Color_t col=kBlue, int mkstyle=20)
{
  h->SetLineColor(col);
  h->SetMarkerColor(col);
  h->SetLineWidth(2);
  h->SetMarkerStyle(mkstyle);
  h->SetMarkerSize(1.0);

  h->GetXaxis()->SetTitle("E [GeV]");
  h->GetYaxis()->SetTitle("N");
}

void SetUpTEff(TEfficiency* eff, Color_t col=kBlue, int mkstyle=20)
{
  eff->SetLineColor(col);
  eff->SetMarkerColor(col);
  eff->SetLineWidth(2);

  eff->SetMarkerStyle(mkstyle);
  eff->SetMarkerSize(1.0);
}

double ScaleHist(TH1* h, double scale = -1)
{
  if( scale == -1 ) {
    double binsize = h->GetBinWidth(1);
    double entries = h->Integral();
    scale = 1./binsize/entries;
  }

  h->Scale(scale);
  h->GetYaxis()->SetTitle("1/N dN/dE");

  return scale;
}

void SetPhiHistAxis(TH1* h) 
{
  h->GetXaxis()->SetTitle("#phi [rad]");
  h->GetYaxis()->SetTitle("1/N dN/d#phi");
  h->GetYaxis()->SetTitleOffset(1.4);
}

TH1F* GetOneBinXProjection(TH2* h, int binnbr=1, TString prefix="")
{
  char buf[128];
  TString name = h->GetName(); name += prefix + "_px%d";
  sprintf(buf,name,binnbr);

  return (TH1F*)h->ProjectionX(buf,binnbr,binnbr);
}

void PrintGraphPoints(TGraph* gr)
{
  for(int i=0; i<gr->GetN(); i++) {
    double x,y;
    gr->GetPoint(i,x,y);
    Printf("%f %f %f %f %f %f",x,y,gr->GetErrorXlow(i),gr->GetErrorXhigh(i),gr->GetErrorYlow(i),gr->GetErrorYhigh(i));
  }
}

void PrintEffPoints(TEfficiency* eff)
{
  Printf("%s",eff->GetTitle());
  Printf("Xvalue, Npassed, Ntotal, Eff, LowerEffErr, UpperEffErr");

  int Nbins = eff->GetPassedHistogram()->GetNbinsX();
  for(int ibin=1; ibin<=Nbins; ibin++) {
    int Npassed = eff->GetPassedHistogram()->GetBinContent(ibin);
    int Ntotal  = eff->GetTotalHistogram()->GetBinContent(ibin);

    double xvalue = eff->GetPassedHistogram()->GetBinCenter(ibin);
    double Efficiency = eff->GetEfficiency(ibin);
    double LowerEffErr = eff->GetEfficiencyErrorLow(ibin);
    double UpperEffErr = eff->GetEfficiencyErrorUp(ibin);

    Printf("%f %d %d %f %f %f",xvalue, Npassed, Ntotal, Efficiency, LowerEffErr, UpperEffErr);
  }
}

void CreateRatioEffPlot(TH1* hRatio, TEfficiency * eData, TEfficiency * eMc)
{
  // Fill hist
  for(int ibin=1; ibin<=hRatio->GetNbinsX(); ibin++)
  {
    double eff_data = eData->GetEfficiency(ibin);
    double eff_mc = eMc->GetEfficiency(ibin);

    // Printf("ibin=%d, eff_data=%f, eff_mc=%f",ibin,eff_data,eff_mc);

    if( eff_data == 0.0 || eff_mc == 0.0 ) continue;

    double err_eff_data = eData->GetEfficiencyErrorLow(ibin);
    if( eData->GetEfficiencyErrorUp(ibin) > err_eff_data ) err_eff_data = eData->GetEfficiencyErrorUp(ibin);
    double err_eff_mc = eMc->GetEfficiencyErrorLow(ibin);
    if( eMc->GetEfficiencyErrorUp(ibin) > err_eff_mc ) err_eff_mc = eMc->GetEfficiencyErrorUp(ibin);

    double eff_ratio = eff_data/eff_mc;
    double err_eff_ration = eff_ratio * sqrt( (err_eff_data/eff_data)*(err_eff_data/eff_data) + (err_eff_mc/eff_mc)*(err_eff_mc/eff_mc) );

    hRatio->SetBinContent(ibin,eff_ratio);
    hRatio->SetBinError(ibin,err_eff_ration);
  }
}

void SetupRatioCanvas(TCanvas * c)
{
  c->Divide(1,2,0.0001,0.0001);
  c->cd(1)->SetPad(0,0.34,1,1);
  c->cd(1)->SetBottomMargin(0.);

  c->cd(2)->SetPad(0,0,1,0.34);
  c->cd(2)->SetTopMargin(0.);
  c->cd(2)->SetBottomMargin(0.15);
  c->cd(2)->SetTitle("");
}

void SetupRatioCanvas_WithAxisRange(TCanvas * c, 
                                    double xlow, double xup,
                                    double uppad_ylow, double uppad_yup,
                                    double lowpad_ylow, double lowpad_yup,
                                    TString xTitle,
                                    TString uppad_yTitle, TString lowpad_yTitle)
{
  SetupRatioCanvas(c);

  // fake hist for draw
  TH1F * hsetup1 = new TH1F("hsetup1","",100,xlow,xup);
  TH1F * hsetup2 = new TH1F("hsetup2","",100,xlow,xup);



  c->cd(1);
  hsetup1->SetMinimum(uppad_ylow); hsetup1->SetMaximum(uppad_yup);
  hsetup1->Draw();
  hsetup1->GetYaxis()->SetLabelSize(0.035);
  hsetup1->GetYaxis()->SetTitle(uppad_yTitle);
  // hsetup1->GetYaxis()->CenterTitle();

  TLine * lh = new TLine(xlow,1.,xup,1.0);
  lh->SetLineStyle(3);

  c->cd(2);
  hsetup2->SetMinimum(lowpad_ylow); hsetup2->SetMaximum(lowpad_yup);
  hsetup2->Draw();
  lh->Draw("same");

  double new_label_size = 0.035*(1-0.34)/0.34;
  hsetup2->GetXaxis()->SetLabelSize(new_label_size);
  hsetup2->GetYaxis()->SetLabelSize(new_label_size);

  hsetup2->GetXaxis()->SetTitle(xTitle);
  hsetup2->GetYaxis()->SetTitle(lowpad_yTitle);
  hsetup2->GetYaxis()->CenterTitle();

  hsetup2->GetXaxis()->SetTitleSize(new_label_size);
  hsetup2->GetYaxis()->SetTitleSize(new_label_size);

  hsetup2->GetYaxis()->SetTitleOffset(0.035/new_label_size);
}

void ScaleTriggerHist(TH1* hall, TH1* hmed, TH1* hhigh)
{
  double scale = ScaleHist(hall);
  ScaleHist(hmed,scale);
  ScaleHist(hhigh,scale);
}

void DrawRatioHist(TH1* hData, TH1* hMc)
{
  TString title = "Ratio_"; 
  title += hData->GetTitle();

  TH1F* hRatio = (TH1F*)hData->Clone(title);
  hRatio->Divide(hMc);

  hRatio->Draw("same");
}

void JetPaint_Short()
{

  bool doprint = false;

  gStyle->SetOptStat("");

  TFile * file = TFile::Open("plotsGenJetAnalysis_8Sep.root");

  TString dataset_name = "data_SumL1MinimumBiasHF_Run2015A";
  // TString dataset_name = "data_CastorJets_Run2015A";
  TString mcset_name_NoMag = "MinBias_TuneMBR_13TeV-pythia8_MagnetOff";
  TString mcset_name       = "MinBias_TuneMBR_13TeV-pythia8";

  TH1* hJetE = (TH1F*)file->Get(dataset_name + "/hdNdEak5CastorJetsHOT");
  TH1* hJetE_TrgMedJet = (TH1F*)file->Get(dataset_name + "/hdNdEak5CastorJetsHOT_TrgMedJet");
  TH1* hJetE_TrgHighJet = (TH1F*)file->Get(dataset_name + "/hdNdEak5CastorJetsHOT_TrgHighJet");

  TH1* hJetE_mc = (TH1F*)file->Get(mcset_name + "/hdNdEak5CastorJetsHOT");
  TH1* hJetE_TrgMedJet_mc = (TH1F*)file->Get(mcset_name + "/hdNdEak5CastorJetsHOT_TrgMedJet");
  TH1* hJetE_TrgHighJet_mc = (TH1F*)file->Get(mcset_name + "/hdNdEak5CastorJetsHOT_TrgHighJet");  

  TH1* hJetE_mc_NoMag = (TH1F*)file->Get(mcset_name_NoMag + "/hdNdEak5CastorJetsHOT");
  TH1* hJetE_TrgMedJet_mc_NoMag = (TH1F*)file->Get(mcset_name_NoMag + "/hdNdEak5CastorJetsHOT_TrgMedJet");
  TH1* hJetE_TrgHighJet_mc_NoMag = (TH1F*)file->Get(mcset_name_NoMag + "/hdNdEak5CastorJetsHOT_TrgHighJet");  

  SetUpHist(hJetE,kBlack,21);
  SetUpHist(hJetE_TrgMedJet,kBlue,21);
  SetUpHist(hJetE_TrgHighJet,kRed,21);

  SetUpHist(hJetE_mc_NoMag,kBlack,22);
  SetUpHist(hJetE_TrgMedJet_mc_NoMag,kBlue,22);
  SetUpHist(hJetE_TrgHighJet_mc_NoMag,kRed,22);



  TEfficiency * eff1 = new TEfficiency(*hJetE_TrgMedJet,*hJetE);
  TEfficiency * eff1_mc = new TEfficiency(*hJetE_TrgMedJet_mc,*hJetE_mc);
  TEfficiency * eff1_mc_NoMag = new TEfficiency(*hJetE_TrgMedJet_mc_NoMag,*hJetE_mc_NoMag);

  eff1->SetTitle("Eff MedJet data_SumL1MinimumBiasHF_Run2015A");
  SetUpTEff(eff1,kBlue,21);
  eff1_mc_NoMag->SetTitle("Eff MedJet MinBias_TuneMBR_13TeV-pythia8_MagnetOff");
  SetUpTEff(eff1_mc_NoMag,kRed,22);

  // plot ratio eff hist
  TH1F * htmp_eff_ratio = (TH1F*)hJetE_TrgMedJet->Clone("htmp_eff_ratio");
  CreateRatioEffPlot(htmp_eff_ratio,eff1,eff1_mc_NoMag);

  TCanvas * ceff1 = new TCanvas("ceff1","Eff MedJet Data & MC");
  // SetupRatioCanvas(ceff1);
  SetupRatioCanvas_WithAxisRange(ceff1,0,4500,0,1.1,0,2,"E [GeV]","eff. medium jet trigger","DATA / MC");

  ceff1->cd(1);
  eff1->Draw("p same");
  eff1_mc_NoMag->Draw("same");
  ceff1->Update();
  // PrintEffPoints(eff1);
  // PrintEffPoints(eff1_mc_NoMag);

  TGraphAsymmErrors * gr1 =  eff1->GetPaintedGraph();
  TF1* fcdf_normal = new TF1("fcdf_normal","[2] * 0.5 * ( 1 + TMath::Erf( (x-[0])/([1]*sqrt(2)) ) )");
  fcdf_normal->SetParNames("mean","sigma","final_eff");
  fcdf_normal->SetParameters(1500,300,1.0);
  fcdf_normal->FixParameter(2,1.0);
  fcdf_normal->SetLineColor(kBlue);
  fcdf_normal->SetLineStyle(kDashed);
  gr1->Fit(fcdf_normal,"EX0 S","",0,5000);
  // PrintGraphPoints(gr1);
  
  TGraphAsymmErrors * gr1_mc_NoMag =  eff1_mc_NoMag->GetPaintedGraph();
  TF1* fcdf_normal_mc_NoMag = new TF1("fcdf_normal_mc_NoMag","[2] * 0.5 * ( 1 + TMath::Erf( (x-[0])/([1]*sqrt(2)) ) )");
  fcdf_normal_mc_NoMag->SetParNames("mean","sigma","final_eff");
  fcdf_normal_mc_NoMag->SetParameters(1500,300,1.0);
  fcdf_normal_mc_NoMag->FixParameter(2,1.0);
  fcdf_normal_mc_NoMag->SetLineColor(kRed);
  fcdf_normal_mc_NoMag->SetLineStyle(kDashed);
  gr1_mc_NoMag->Fit(fcdf_normal_mc_NoMag,"EX0 S","",0,5000);

  ceff1->cd(2);
  htmp_eff_ratio->Draw("same");

  ceff1->Print("MedJetEffTrigger_MCcompared.png");

  // TLatex * ltx = new TLatex();
  // ltx->DrawLatex(2000,0.6,"#epsilon_{final}#times#frac{1}{2}#left[1+erf#left(#frac{x-#mu}{#sigma#sqrt{2}}#right)#right]");
  // ltx->DrawLatex(2000,0.45,"#mu = 1280 #pm 1 GeV");
  // ltx->DrawLatex(2000,0.35,"#sigma = 344.3 #pm 0.4 GeV");
  // ltx->DrawLatex(2000,0.25,"#epsilon_{final} = 99.7 #pm 0.1 %");



  // for test purpose
  // return;

  ScaleTriggerHist(hJetE,
                   hJetE_TrgMedJet,
                   hJetE_TrgHighJet);
  ScaleTriggerHist(hJetE_mc_NoMag,
                   hJetE_TrgMedJet_mc_NoMag,
                   hJetE_TrgHighJet_mc_NoMag);

  TCanvas * c1 = new TCanvas("c1","dN/dE Data & MC");
  SetupRatioCanvas_WithAxisRange(c1,0,4500,2e-9,8e-3,0,2,"E [GeV]","1/N dN/dE [1/GeV]","DATA / MC");

  c1->cd(1)->SetLogy();
  hJetE->Draw("same");
  hJetE_TrgMedJet->Draw("same");
  hJetE_TrgHighJet->Draw("same");

  hJetE_mc_NoMag->Draw("same");
  hJetE_TrgMedJet_mc_NoMag->Draw("same");
  hJetE_TrgHighJet_mc_NoMag->Draw("same");

  c1->cd(2);
  DrawRatioHist(hJetE,hJetE_mc_NoMag);
  DrawRatioHist(hJetE_TrgMedJet,hJetE_TrgMedJet_mc_NoMag);
  DrawRatioHist(hJetE_TrgHighJet,hJetE_TrgHighJet_mc_NoMag);

  // hRatio_JetE->Draw("same");
  // hRatio_JetE_TrgMedJet->Draw("same");
  // hRatio_JetE_TrgHighJet->Draw("same");

  c1->cd(1);
  TLegend* leg = new TLegend(0.4,0.6,0.9,0.9);
  leg->AddEntry((TObject*)0, "Dataset:", "");
  leg->AddEntry((TObject*)0, "/L1MinimumBiasHF1/Run2015A-PromptReco-v1/RECO", "");
  leg->AddEntry(hJetE,"Hottest Jet","ple");
  leg->AddEntry(hJetE_TrgMedJet,"Medium Jet Trigger - Hottest Jet","ple");
  leg->AddEntry(hJetE_TrgHighJet,"Medium High Trigger - Hottest Jet","ple");
  // leg->SetTextSize(0.02);
  // leg->Draw("same");

  // c1->Print("MinBias_JetE_Dist_UncalibRecHits.png");
  c1->Print("MinBias_JetE_Dist_MCcompared.png");
  


  // TEfficiency * eff2 = new TEfficiency(*hJetE_TrgHighJet,*hJetE);
  // TCanvas * ceff2 = new TCanvas("ceff2"); ceff2->cd();
  // eff2->Draw("ap");
  // ceff2->Update();
  // TGraphAsymmErrors * gr2 =  eff2->GetPaintedGraph();
  // gr2->SetLineColor(kBlue);
  // gr2->SetMarkerColor(kBlue);
  // gr2->SetLineWidth(2);
  // TF1* fcdf_normal_v2 = new TF1("fcdf_normal_v2","[2] * 0.5 * ( 1 + TMath::Erf( (x-[0])/([1]*sqrt(2)) ) )");
  // fcdf_normal_v2->SetParNames("mean","sigma","final_eff");
  // fcdf_normal_v2->SetParameters(200e3,50e3,1.0);
  // gr2->Fit(fcdf_normal_v2,"W S","",0,450e3);

  // // cout << fcdf_normal_v2->GetParameter("mean") << endl;


  // TLatex * ltx2 = new TLatex();
  // ltx2->SetTextSize(0.04);
  // ltx2->DrawLatex(100,0.95,"#epsilon_{final}#times#frac{1}{2}#left[1+erf#left(#frac{x-#mu}{#sigma#sqrt{2}}#right)#right]");
  // ltx2->DrawLatex(100,0.8,"#mu = 162 #pm 4 x10^3 fC");
  // ltx2->DrawLatex(100,0.7,"#sigma = 44 #pm 6 x10^3 fC");
  // ltx2->DrawLatex(100,0.6,"#epsilon_{final} = 96.5 #pm 2.2 %");
  // ceff2->Print("HighJetEffTrigger_UncalibRecHits.png");
  




  TH2F* hEVsFem_TrgMedJet = (TH2F*)file->Get(dataset_name + "/hEvsFem_ak5CastorJetsHOT_TrgMedJet");
  TH2F* hEVsFem_TrgHighJet = (TH2F*)file->Get(dataset_name + "/hEvsFem_ak5CastorJetsHOT_TrgHighJet");

  TCanvas * c2 = new TCanvas("c2","E Vs EM/HAD"); c2->cd()->SetLogz();
  hEVsFem_TrgMedJet->SetMaximum(200000);
  hEVsFem_TrgMedJet->Draw("colz");

  TH2F* htmp = new TH2F("htmp","",90,0,7500,30,0,1);

  for(int i=1;i<31;i++) for(int j=1;j<11;j++) {
    double binCx = hEVsFem_TrgHighJet->GetXaxis()->GetBinCenter(i);
    double binCy = hEVsFem_TrgHighJet->GetYaxis()->GetBinCenter(j);
    int nBin = htmp->FindBin(binCx,binCy);

    double binCnt = hEVsFem_TrgHighJet->GetBinContent(i,j);
    htmp->SetBinContent(nBin,binCnt);
  }

  htmp->SetMaximum(200000);
  htmp->Draw("same col");
  


  TCanvas * c2eff = new TCanvas("c2eff","Eff Vs EM/HAD"); c2eff->cd();

  TH2F* hEVsFem_Eff = (TH2F*)hEVsFem_TrgHighJet->Clone("hEVsFem_Eff");
  hEVsFem_Eff->Divide(hEVsFem_TrgMedJet);

  // hEVsFem_Eff->SetMaximum(1);
  hEVsFem_Eff->Draw("colz");
  


  // TH1F* hTowE_TrgMedJet = (TH1F*)file->Get("data_CastorJets_Run2015A/Tower_Energy_TrgMedJet");
  // TH1F* hTowE_TrgHighJet = (TH1F*)file->Get("data_CastorJets_Run2015A/Tower_Energy_TrgHighJet");

  // TCanvas * c3 = new TCanvas("c3","Hottest Tower Energy",1200,600);
  // c3->Divide(2,1);

  // SetUpHist(hTowE_TrgMedJet,kBlue);
  // SetUpHist(hTowE_TrgHighJet,kRed);
  // c3->cd(1)->SetLogy();

  // hTowE_TrgMedJet->Draw();
  // hTowE_TrgHighJet->Draw("same");

  // c3->cd(2);
  // TEfficiency * eff3 = new TEfficiency(*hTowE_TrgHighJet, *hTowE_TrgMedJet);
  // eff3->Draw("ap");
  // c3->Update();
  // // TGraphAsymmErrors * gr3 =  eff3->GetPaintedGraph();
  // // gr3->SetLineColor(kBlue);
  // // gr3->SetMarkerColor(kBlue);
  // // gr3->SetLineWidth(2);
  // // TF1* fcdf_normal_v3 = new TF1("fcdf_normal_v3","[2] * 0.5 * ( 1 + TMath::Erf( (x-[0])/([1]*sqrt(2)) ) )");
  // // fcdf_normal_v3->SetParNames("mean","sigma","final_eff");
  // // fcdf_normal_v3->SetParameters(200e3,200e3,1.0);
  // // // fcdf_normal_v3->FixParameter(2,1.0);
  // // gr3->Fit(fcdf_normal_v3,"EX0 S","",150e3,350e3);
  // // c3->Print("Tower_Energy_Dist_Eff.png");



  TH1* hJetPhi = (TH1F*)file->Get(dataset_name + "/hdNdPhiak5CastorJetsHOT");
  TH1* hJetPhi_TrgMedJet = (TH1F*)file->Get(dataset_name + "/hdNdPhiak5CastorJetsHOT_TrgMedJet");
  TH1* hJetPhi_TrgHighJet = (TH1F*)file->Get(dataset_name + "/hdNdPhiak5CastorJetsHOT_TrgHighJet");

  TH1* hJetPhi_mc_NoMag = (TH1F*)file->Get(mcset_name_NoMag + "/hdNdPhiak5CastorJetsHOT");
  TH1* hJetPhi_TrgMedJet_mc_NoMag = (TH1F*)file->Get(mcset_name_NoMag + "/hdNdPhiak5CastorJetsHOT_TrgMedJet");
  TH1* hJetPhi_TrgHighJet_mc_NoMag = (TH1F*)file->Get(mcset_name_NoMag + "/hdNdPhiak5CastorJetsHOT_TrgHighJet");

  SetUpHist(hJetPhi,kBlack,21);
  SetUpHist(hJetPhi_TrgMedJet,kBlue,21);
  SetUpHist(hJetPhi_TrgHighJet,kRed,21);

  SetUpHist(hJetPhi_mc_NoMag,kBlack,22);
  SetUpHist(hJetPhi_TrgMedJet_mc_NoMag,kBlue,22);
  SetUpHist(hJetPhi_TrgHighJet_mc_NoMag,kRed,22);

  scale = ScaleHist(hJetPhi);
  ScaleHist(hJetPhi_TrgMedJet,scale);
  ScaleHist(hJetPhi_TrgHighJet,scale);

  scale = ScaleHist(hJetPhi_mc_NoMag);
  ScaleHist(hJetPhi_TrgMedJet_mc_NoMag,scale);
  ScaleHist(hJetPhi_TrgHighJet_mc_NoMag,scale);

  SetPhiHistAxis(hJetPhi);
  SetPhiHistAxis(hJetPhi_TrgMedJet);
  SetPhiHistAxis(hJetPhi_TrgHighJet);

  SetPhiHistAxis(hJetPhi_mc_NoMag);
  SetPhiHistAxis(hJetPhi_TrgMedJet_mc_NoMag);
  SetPhiHistAxis(hJetPhi_TrgHighJet_mc_NoMag);



  TH1* hJetPhi_Ecut = (TH1F*)file->Get(dataset_name + "/hdNdPhiak5CastorJetsHOT_Ecut");
  TH1* hJetPhi_TrgMedJet_Ecut = (TH1F*)file->Get(dataset_name + "/hdNdPhiak5CastorJetsHOT_TrgMedJet_Ecut");
  TH1* hJetPhi_TrgHighJet_Ecut = (TH1F*)file->Get(dataset_name + "/hdNdPhiak5CastorJetsHOT_TrgHighJet_Ecut");

  TH1* hJetPhi_mc_NoMag_Ecut = (TH1F*)file->Get(mcset_name_NoMag + "/hdNdPhiak5CastorJetsHOT_Ecut");
  TH1* hJetPhi_TrgMedJet_mc_NoMag_Ecut = (TH1F*)file->Get(mcset_name_NoMag + "/hdNdPhiak5CastorJetsHOT_TrgMedJet_Ecut");
  TH1* hJetPhi_TrgHighJet_mc_NoMag_Ecut = (TH1F*)file->Get(mcset_name_NoMag + "/hdNdPhiak5CastorJetsHOT_TrgHighJet_Ecut");


  TEfficiency * effphi = new TEfficiency(*hJetPhi_TrgMedJet_Ecut,*hJetPhi_Ecut);
  TEfficiency * effphi_mc_NoMag = new TEfficiency(*hJetPhi_TrgMedJet_mc_NoMag_Ecut,*hJetPhi_mc_NoMag_Ecut);


  TCanvas * c4 = new TCanvas("c4","Phi distribution",1200,600);
  c4->Divide(2,1);

  c4->cd(1)->SetLogy();
  hJetPhi->SetMinimum(1e-7);
  hJetPhi->Draw();
  hJetPhi_TrgMedJet->Draw("same");
  hJetPhi_TrgHighJet->Draw("same");
  hJetPhi_mc_NoMag->Draw("same");
  hJetPhi_TrgMedJet_mc_NoMag->Draw("same");
  hJetPhi_TrgHighJet_mc_NoMag->Draw("same");

  c4->cd(2);
  SetUpTEff(effphi,kBlue,21);
  SetUpTEff(effphi_mc_NoMag,kRed,22);
  effphi->Draw("ap");
  effphi_mc_NoMag->Draw("same");

  // c4->Print("PhiDistribution_And_Eff_Of_Jets.png");


  TH2F * hJetPhi_Vs_Energy = (TH2F*)file->Get(dataset_name + "/hdNdEdPhiak5CastorJetsHOT");
  TH2F * hJetPhi_Vs_Energy_TrgMedJet = (TH2F*)file->Get(dataset_name + "/hdNdEdPhiak5CastorJetsHOT_TrgMedJet");
  TH2F * hJetPhi_Vs_Energy_TrgHighJet = (TH2F*)file->Get(dataset_name + "/hdNdEdPhiak5CastorJetsHOT_TrgHighJet");

  TH2F * hJetPhi_Vs_Energy_mc_NoMag = (TH2F*)file->Get(mcset_name_NoMag + "/hdNdEdPhiak5CastorJetsHOT");
  TH2F * hJetPhi_Vs_Energy_TrgMedJet_mc_NoMag = (TH2F*)file->Get(mcset_name_NoMag + "/hdNdEdPhiak5CastorJetsHOT_TrgMedJet");
  TH2F * hJetPhi_Vs_Energy_TrgHighJet_mc_NoMag = (TH2F*)file->Get(mcset_name_NoMag + "/hdNdEdPhiak5CastorJetsHOT_TrgHighJet");

  TCanvas * c5 = new TCanvas("c5","Jet E per Phi-Bin",1000,1000);
  c5->Divide(4,4);

  TCanvas * c6 = new TCanvas("c6","Eff per Phi-Bin",1000,1000);
  c6->Divide(4,4);

  TH1F * hJetPhi_Vs_Energy_px[16];
  TH1F * hJetPhi_Vs_Energy_TrgMedJet_px[16];
  TEfficiency * effsec[16];
  
  TH1F * hJetPhi_Vs_Energy_mc_NoMag_px[16];
  TH1F * hJetPhi_Vs_Energy_TrgMedJet_mc_NoMag_px[16];
  TEfficiency * effsec_mc_NoMag[16];

  TH1F * htmp2 = new TH1F("htmp2","",32,0,4000);
  htmp2->SetMaximum(1.2);
  htmp2->SetMinimum(0);

  char buf[128];
  for(int isec=0; isec<16; isec++) {
    hJetPhi_Vs_Energy_px[isec] = GetOneBinXProjection(hJetPhi_Vs_Energy,isec+1);
    hJetPhi_Vs_Energy_TrgMedJet_px[isec] = GetOneBinXProjection(hJetPhi_Vs_Energy_TrgMedJet,isec+1);
    effsec[isec] = new TEfficiency(*hJetPhi_Vs_Energy_TrgMedJet_px[isec],*hJetPhi_Vs_Energy_px[isec]);

    hJetPhi_Vs_Energy_mc_NoMag_px[isec] = GetOneBinXProjection(hJetPhi_Vs_Energy_mc_NoMag,isec+1,"_mc_NoMag");
    hJetPhi_Vs_Energy_TrgMedJet_mc_NoMag_px[isec] = GetOneBinXProjection(hJetPhi_Vs_Energy_TrgMedJet_mc_NoMag,isec+1,"_mc_NoMag");
    effsec_mc_NoMag[isec] = new TEfficiency(*hJetPhi_Vs_Energy_TrgMedJet_mc_NoMag_px[isec],*hJetPhi_Vs_Energy_mc_NoMag_px[isec]);

    c5->cd(isec+1)->SetLogy();
    SetUpHist(hJetPhi_Vs_Energy_px[isec],kBlack,21);
    SetUpHist(hJetPhi_Vs_Energy_TrgMedJet_px[isec],kBlue,21);
    scale = ScaleHist(hJetPhi_Vs_Energy_px[isec]);
    ScaleHist(hJetPhi_Vs_Energy_TrgMedJet_px[isec],scale);
    hJetPhi_Vs_Energy_px[isec]->Draw();
    hJetPhi_Vs_Energy_TrgMedJet_px[isec]->Draw("same");

    SetUpHist(hJetPhi_Vs_Energy_mc_NoMag_px[isec],kGray+2,22);
    SetUpHist(hJetPhi_Vs_Energy_TrgMedJet_mc_NoMag_px[isec],kAzure,22);
    scale = ScaleHist(hJetPhi_Vs_Energy_mc_NoMag_px[isec]);
    ScaleHist(hJetPhi_Vs_Energy_TrgMedJet_mc_NoMag_px[isec],scale);
    hJetPhi_Vs_Energy_mc_NoMag_px[isec]->Draw("same");
    hJetPhi_Vs_Energy_TrgMedJet_mc_NoMag_px[isec]->Draw("same");


    c6->cd(isec+1);
    SetUpTEff(effsec[isec],kBlue,21);
    SetUpTEff(effsec_mc_NoMag[isec],kRed,22);
    htmp2->Draw();
    effsec[isec]->Draw("same");
    effsec_mc_NoMag[isec]->Draw("same");
  }
  // c5->Print("JetEDist_per_PhiBin.png");
  // c6->Print("Eff_per_PhiBin.png");

}