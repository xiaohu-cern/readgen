### Read Gen particle information for gg->HH->bbmumu
### Support Powheg-Box-V2 interfaced with Pythia8 (note the particle status)
# muons have status 1 (final state) or 23 (outgoing)

import ROOT as R
import sys
from DataFormats.FWLite import Events, Handle

from gen_util import *

#
inputfile = './sample/HIG-RunIIFall18wmLHEGS-00000.root.keepit'
outputfile = 'test_hist_bbmm.root'
label_info, handle_info = 'generator', Handle('GenEventInfoProduct')
label_part, handle_part = 'genParticles', Handle('std::vector<reco::GenParticle>')
label_jet, handle_jet = 'ak4GenJets', Handle('std::vector<reco::GenJet>')

# global constant

#
ctr_totevt = 0
ctr_negw = 0
ctr_posw = 0

# hist
h_m1_pt = R.TH1F('h_m1_pt','p_{T}(#mu1) [GeV]',40,0,200)
h_m1_eta = R.TH1F('h_m1_eta','#eta(#mu1)',40,-3,3)
h_m2_pt = R.TH1F('h_m2_pt','p_{T}(#mu2) [GeV]',40,0,200)
h_m2_eta = R.TH1F('h_m2_eta','#eta(#mu2)',40,-3,3)

h_j1_pt = R.TH1F('h_j1_pt','p_{T}(jet1) [GeV]',40,0,200)
h_j1_eta = R.TH1F('h_j1_eta','#eta(jet1)',40,-3,3)
h_j2_pt = R.TH1F('h_j2_pt','p_{T}(jet2) [GeV]',40,0,200)
h_j2_eta = R.TH1F('h_j2_eta','#eta(jet2)',40,-3,3)

h_hmm_m = R.TH1F('h_hmm_m','m(H#to#mu#mu)',40,80,160)
h_hbb_m = R.TH1F('h_hbb_m','m(H#tobb)',40,80,160)
h_hh_m = R.TH1F('h_hh_m','m(bb#mu#mu)',50,200,1200)

_list_h = [h_m1_pt, h_m1_eta, h_m2_pt, h_m2_eta, \
           h_j1_pt, h_j1_eta, h_j2_pt, h_j2_eta, \
           h_hmm_m, h_hbb_m, h_hh_m ]

#
events = Events(inputfile)

#
for event in events:
  
  # counters
  ctr_totevt += 1
  _n_allmuon_fromH = 0 # security check for H->mm
  _n_allbquark_fromH = 0 # secutiry check for H->bb

  # retrieve the handlers
  event.getByLabel(label_info, handle_info)
  _info = handle_info.product()
  event.getByLabel(label_part, handle_part)
  _part = handle_part.product()
  event.getByLabel(label_jet, handle_jet)
  _jet = handle_jet.product()

  # get MC weight
  _w = _info.weight()
  if _w > 0:
    ctr_posw += 1
  else:
    ctr_negw += 1

  # containers for selected objects
  _list_muon = []
  _list_jet = []
  _list_bquark = []

  # mem id
  _list_memid = []

  # loop particles
  for _p in _part:

    # particles to look at
    if abs(_p.pdgId()) == 13 or abs(_p.pdgId()) == 5:
      pass
    else:
      continue

    # after radiation
    _p = afterRadiation(_p)
    # make sure this particle was not used before
    if id(_p) in _list_memid:
      continue
    else:
      _list_memid.append(_p)

    # muon
    #if abs(_p.pdgId()) == 13 and _p.status() == 1 and _p.statusFlags().isPrompt() and fromHiggs(_p):
    if abs(_p.pdgId()) == 13 and fromHiggs(_p):

      #print('DEBUG status: {0}'.format(_p.status()))
      _n_allmuon_fromH += 1

      # muon object selection
      if _p.pt() > 25 and abs(_p.eta()) < 2.4:
        __m = R.TLorentzVector()
        __m.SetPtEtaPhiE(_p.pt(), _p.eta(), _p.phi(), _p.energy())
        _list_muon.append(__m)

    # b-quark
    if abs(_p.pdgId()) == 5 and fromHiggs(_p):

      _n_allbquark_fromH += 1

      # bquark acceptance
      if _p.pt() > 25 and abs(_p.eta()) < 2.5:
        __b = R.TLorentzVector()
        __b.SetPtEtaPhiE(_p.pt(), _p.eta(), _p.phi(), _p.energy())
        _list_bquark.append(__b)

  # truth topology check
  if _n_allmuon_fromH == 2 and _n_allbquark_fromH == 2:
    pass
  else:
    print('WARNING: this event has {0} muons and {1} bquarks from HH in the truth record'.format(_n_allmuon_fromH, _n_allbquark_fromH))
    continue # !!! !!! !!!
  
  # topology after acceptance, cut events
  if len(_list_muon) == 2 and len(_list_bquark) == 2:
    pass
  else:
    continue

  # pT ordering
  _list_muon.sort(key=lambda p:p.Pt(), reverse=True)
  _list_bquark.sort(key=lambda p:p.Pt(), reverse=True)

  # match jets to bquark
  _list_alljet = cvt_vparticle2vp4(_jet)
  _list_jet = [ match_j2quark(_list_alljet, _list_bquark[0]),\
                match_j2quark(_list_alljet, _list_bquark[1]) ]

  # drop events if <2 jets matched to quark
  # or the 2 matched jets are the same
  if None in _list_jet:
    print('WARNING <2 jets matched to bquark. SKIP EVENT')
    continue
  if id(_list_jet[0]) == id(_list_jet[1]):
    print('WARNING 2 matched jets are identical. SKIP EVENT')
    continue

  # event selection

  # kinematics
  h_m1_pt .Fill(_list_muon[0].Pt(),_w)
  h_m1_eta.Fill(_list_muon[0].Eta(),_w)
  h_m2_pt .Fill(_list_muon[1].Pt(),_w)
  h_m2_eta.Fill(_list_muon[1].Eta(),_w)
  
  h_j1_pt .Fill(_list_jet[0].Pt(),_w)
  h_j1_eta.Fill(_list_jet[0].Eta(),_w)
  h_j2_pt .Fill(_list_jet[1].Pt(),_w)
  h_j2_eta.Fill(_list_jet[1].Eta(),_w)
  
  mm = _list_muon[0]+_list_muon[1]
  bb = _list_jet[0]+_list_jet[1]
  bbmm = bb+mm
  h_hmm_m.Fill(mm.M(),_w)
  h_hbb_m.Fill(bb.M(),_w)
  h_hh_m .Fill(bbmm.M(),_w)

outfile = R.TFile.Open(outputfile, 'RECREATE')
for _h in _list_h:
  _h.Write()
outfile.Close()

#
print('Total events: {0}'.format(ctr_totevt))
print('Events with positive weight: {0}'.format(ctr_posw))
print('Events with negative weight: {0}'.format(ctr_negw))

