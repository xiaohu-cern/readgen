# utils for gen particles

import ROOT as R

# check if it decays from Higgs
def fromHiggs(p):
  for _p in p.motherRefVector():
    # self->self+radation: trace back to the original of the chain
    if _p.pdgId() == p.pdgId():
      fromHiggs(_p)
    if abs(_p.pdgId()) == 25:
      return True
  return False

# go down to the final-state particle after all radiation
# 2020-12-22: realise that gen particle list does not include the final-state particles after radiation, thus need this to get down to the particles
def afterRadiation(p):
  for _p in p.daughterRefVector():
    if _p.pdgId() == p.pdgId():
      afterRadiation(_p)
  return p

# check if this particle will radiate later
def checkRadiation(p):
  #print('DEBUG {0} decay products: {1}'.format(p.pdgId(), len(p.daughterRefVector())))
  #flag = False
  for _p in p.daughterRefVector():
    #print('DEBUG {0} -> {1}'.format(p.pdgId(), _p.pdgId()))
    if _p.pdgId() == p.pdgId():
    #  flag = True
      return True
  return False
  #return flag

# convert vec<particle> to vec<TLorentzVector>
def cvt_vparticle2vp4(list_part):
  _list = []
  for _part in list_part:
    _p4 = R.TLorentzVector()
    _p4.SetPtEtaPhiE(_part.pt(),_part.eta(),_part.phi(),_part.energy())
    _list.append(_p4)
  return _list

# match gen jet to quark
def match_j2quark(jets, quark, dR=0.4):
  _jmatch = None
  _dRmin = dR

  for _j in jets:
    _dR = _j.DeltaR(quark)
    if _dR < _dRmin:
      _jmatch = _j
      _dRmin = _dR

  return _jmatch
