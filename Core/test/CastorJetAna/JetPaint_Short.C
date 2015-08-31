void SetUpHist(TH1* h,EColor col=kBlue)
{
  h->SetLineColor(col);
  h->SetMarkerColor(col);
  h->SetLineWidth(2);

  h->GetXaxis()->SetTitle("E [GeV]");
  h->GetYaxis()->SetTitle("N");
}

void JetPaint_Short()
{
  gStyle->SetOptStat("e");

  TFile * file = TFile::Open("plotsGenJetAnalysis.root");

  TH1* hJetE = (TH1F*)file->Get("data_CastorJets_Run2015A/hdNdEak5CastorJetsHOT");
  TH1* hJetE_TrgMedJet = (TH1F*)file->Get("data_CastorJets_Run2015A/hdNdEak5CastorJetsHOT_TrgMedJet");
  TH1* hJetE_TrgHighJet = (TH1F*)file->Get("data_CastorJets_Run2015A/hdNdEak5CastorJetsHOT_TrgHighJet");

  SetUpHist(hJetE,kBlack);
  SetUpHist(hJetE_TrgMedJet,kBlue);
  SetUpHist(hJetE_TrgHighJet,kRed);

  TCanvas * c1 = new TCanvas("c1"); c1->cd()->SetLogy();

  hJetE->Draw();
  hJetE_TrgMedJet->Draw("same");
  hJetE_TrgHighJet->Draw("same");

  TLegend* leg = new TLegend(0.4,0.6,0.9,0.9);
  leg->AddEntry((TObject*)0, "Dataset:", "");
  leg->AddEntry((TObject*)0, "/L1MinimumBiasHF1/Run2015A-PromptReco-v1/RECO", "");
  leg->AddEntry(hJetE,"Hottest Jet","ple");
  leg->AddEntry(hJetE_TrgMedJet,"Medium Jet Trigger - Hottest Jet","ple");
  leg->AddEntry(hJetE_TrgHighJet,"Medium High Trigger - Hottest Jet","ple");
  // leg->SetTextSize(0.02);
  leg->Draw("same");

  c1->Print("MinBias_JetE_Dist.png");


  TEfficiency * eff1 = new TEfficiency(*hJetE_TrgMedJet,*hJetE);
  TCanvas * ceff1 = new TCanvas("ceff1"); ceff1->cd();
  eff1->Draw("ap");
  ceff1->Update();
  TGraphAsymmErrors * gr1 =  eff1->GetPaintedGraph();
  gr1->SetLineColor(kBlue);
  gr1->SetMarkerColor(kBlue);
  gr1->SetLineWidth(2);
  TF1* fcdf_normal = new TF1("fcdf_normal","[2] * 0.5 * ( 1 + TMath::Erf( (x-[0])/([1]*sqrt(2)) ) )");
  fcdf_normal->SetParNames("mean","sigma","final_eff");
  fcdf_normal->SetParameters(2000,600,1.0);
  gr1->Fit(fcdf_normal,"EX0 S","",0,5000);
  
  TLatex * ltx = new TLatex();
  ltx->DrawLatex(2000,0.6,"#epsilon_{final}#times#frac{1}{2}#left[1+erf#left(#frac{x-#mu}{#sigma#sqrt{2}}#right)#right]");
  ltx->DrawLatex(2000,0.45,"#mu = 1280 #pm 1 GeV");
  ltx->DrawLatex(2000,0.35,"#sigma = 344.3 #pm 0.4 GeV");
  ltx->DrawLatex(2000,0.25,"#epsilon_{final} = 99.7 #pm 0.1 %");


  ceff1->Print("MedJetEffTrigger.png");


  TEfficiency * eff2 = new TEfficiency(*hJetE_TrgHighJet,*hJetE);
  TCanvas * ceff2 = new TCanvas("ceff2"); ceff2->cd();
  eff2->Draw("ap");
  ceff2->Update();
  TGraphAsymmErrors * gr2 =  eff2->GetPaintedGraph();
  gr2->SetLineColor(kBlue);
  gr2->SetMarkerColor(kBlue);
  gr2->SetLineWidth(2);
  TF1* fcdf_normal_v2 = new TF1("fcdf_normal_v2","[2] * 0.5 * ( 1 + TMath::Erf( (x-[0])/([1]*sqrt(2)) ) )");
  fcdf_normal_v2->SetParNames("mean","sigma","final_eff");
  fcdf_normal_v2->SetParameters(2000,600,1.0);
  gr2->Fit(fcdf_normal_v2,"EX0 S","",0,6000);
  

  ceff2->Print("HighJetEffTrigger.png");




  TH2F* hEVsFem_TrgMedJet = (TH2F*)file->Get("data_CastorJets_Run2015A/hEvsFem_ak5CastorJetsHOT_TrgMedJet");
  TH2F* hEVsFem_TrgHighJet = (TH2F*)file->Get("data_CastorJets_Run2015A/hEvsFem_ak5CastorJetsHOT_TrgHighJet");

  TCanvas * c2 = new TCanvas("c2"); c2->cd()->SetLogz();
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
  c2->Print("Energy_Vs_EemEtotRatio_MedJetTrg_SmallBlocksHighJetTrg.png");


  TCanvas * c2eff = new TCanvas("c2eff"); c2eff->cd();

  TH2F* hEVsFem_Eff = (TH2F*)hEVsFem_TrgHighJet->Clone("hEVsFem_Eff");
  hEVsFem_Eff->Divide(hEVsFem_TrgMedJet);

  // hEVsFem_Eff->SetMaximum(1);
  hEVsFem_Eff->Draw("colz");
  c2eff->Print("Energy_Vs_EemEtotRatio_Efficiency.png");


  // TH1* hJetECasJet = (TH1F*)file->Get("data_CastorJets_Run2015A/hdNdEak5CastorJetsHOT");
  // TH1* hJetECasJet_TrgMedJet = (TH1F*)file->Get("data_CastorJets_Run2015A/hdNdEak5CastorJetsHOT_TrgMedJet");
  // TH1* hJetECasJet_TrgHighJet = (TH1F*)file->Get("data_CastorJets_Run2015A/hdNdEak5CastorJetsHOT_TrgHighJet");  

  // SetUpHist(hJetECasJet,kBlack);
  // SetUpHist(hJetECasJet_TrgMedJet,kBlue);
  // SetUpHist(hJetECasJet_TrgHighJet,kRed);

  // TCanvas * c1CasJet = new TCanvas("c1CasJet"); c1CasJet->cd()->SetLogy();

  // hJetECasJet->Draw();
  // hJetECasJet_TrgMedJet->Draw("same");
  // hJetECasJet_TrgHighJet->Draw("same");

  // TLegend* legCasJet = new TLegend(0.45,0.7,0.9,0.9);
  // legCasJet->AddEntry((TObject*)0, "Dataset:", "");
  // legCasJet->AddEntry((TObject*)0, "/CastorJets/Run2015A-PromptReco-v1/RECO", "");
  // legCasJet->AddEntry(hJetECasJet,"Hottest Jet","ple");
  // legCasJet->AddEntry(hJetECasJet_TrgMedJet,"Medium Jet Trigger - Hottest Jet","ple");
  // legCasJet->AddEntry(hJetECasJet_TrgHighJet,"Medium High Trigger - Hottest Jet","ple");
  // // legCasJet->SetTextSize(0.02);
  // legCasJet->Draw("same");


  // TEfficiency * eff2 = new TEfficiency(*hJetECasJet_TrgHighJet,*hJetECasJet_TrgMedJet);
  // TCanvas * ceff2 = new TCanvas("ceff2"); ceff2->cd();
  // eff2->Draw("ap");
  // ceff2->Update();
  // TGraphAsymmErrors * gr2 =  eff2->GetPaintedGraph();
  // gr2->SetLineColor(kBlue);
  // gr2->SetMarkerColor(kBlue);
  // gr2->SetLineWidth(2);
  // fcdf_normal->SetParameters(2000,600,1.0);
  // gr2->Fit(fcdf_normal,"EX0 S","",0,5000);

  // c1->Print("MinBias_JetE_Dist.png");
  // c1CasJet->Print("CasJet_JetE_Dist.png");
}