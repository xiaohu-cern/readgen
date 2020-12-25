NOTE: this repo is moved to https://github.com/xiaohu-cern/readgen for easy external excess

# Introduction
This is a toolkit to read gen EDM files and output histograms.
The code is based on pythonic `DataFormats.FWLite`.

# Author
Xiaohu.Sun@cern.ch

# Check out the repo
Recommend to use ssh with easy ssh keys to pull and push without password.
```
git clone git@github.com:xiaohu-cern/readgen.git
```

To setup the ssh keys, see this link
```
https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent
```
Once you have the keys, do this setup everytime before your use git
```
git config --global user.name YOUR NAME
git config --global user.email YOUR@EMAIL
git config --global user.github YOUR_GIT_ACCOUNT
git config --global http.emptyAuth true
export VISUAL=vim
eval $(ssh-agent); ssh-add /YOURHOMEDIR/.ssh/id_rsa_github
```

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

