NOTE: this repo is moved to https://github.com/xiaohu-cern/readgen for easy external excess

# Introduction
This is a toolkit to read gen EDM files and output histograms.
The code is based on pythonic `DataFormats.FWLite`.

# Author
Xiaohu.Sun@cern.ch

# Check out the repo
git clone git@github.com:xiaohu-cern/readgen.git

# Setup
Use CMSSW_10_2_20_UL
```
source setup.sh
```

# Run
Configure the input / output files and run. For example, to read HH->bbmumu gen event records, do
```
python read_bbmm.py
```

# Tips

## Print the contents (labels etc.) of an EDM file
edmDumpEventContent xxx.root

