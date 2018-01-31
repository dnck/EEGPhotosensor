The functions here are for a very specific and common need. If you're also working on it, please get in contact with me. See Things That Need to be Done and Gotchas. 

# Status:
The functions in ```photosensor_analysis.py``` are currently working for, 

```Python 2.7.12 :: Anaconda custom (x86_64)```

with ```conda v.4.3.23```.

on a ```macOS Sierra v.10.13.2```.

# Dependencies:
```
import os
import mne
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import mlab
```

# Basic Usage: 
```
test = mne.io.read_raw_edf("path/to/yourdata.bdf",preload=True)
dat0 = plotTrials(test, triggerCodes=[10], xlim=[-100,1100], ylim=[-0.1,2.25])
onsetTimes0 = plotSingleTrialPeaks(dat0=dat0, msFromOnset=45, xlim=[0,45], ylim=[-0.2, 2.5], plotAll=False)
```

# Things that need to be done:
* Better doc strings in the functions
* Better documentation overall for what each function does - but see README in main directory for an idea
* Modularize with classes
* Test on different platforms

# Gotchas:
* Assumes trial numbers divisible by 5 (e.g. 100 trials for trigger # 10) 
* Assumes sampling rate of 2048 in some places (e.g. easily fixed with find/replace)
* ```getPeak()``` is not yet ideal, but is fairly good ~5% trial peaks not found


