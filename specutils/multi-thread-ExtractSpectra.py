from joblib import Parallel, delayed
import os
from pathlib import Path
from ExtractSpectraToH5 import ExtractSpectraToH5
from multiprocessing import cpu_count

datDir = '/media/nsbruce/Backup Plus/460MHz/'
nfft = 50000
navg = 100
fc = 460000000
fs = 50000000
tTrim = 1000

datPath = Path(datDir)
num_cpus = cpu_count()

datFiles = list(datPath.glob("*.dat"))
print(len(datFiles))

def callExtraction(datFile, saveDir='/home/nsbruce/Documents/RFI/460DATA/'):
    root, ext = os.path.splitext(datFile)
    t0 = os.path.basename(root)
    outputName = saveDir+t0+'.h5'
    print("Building "+outputName)
    
    ExtractSpectraToH5(datFile, outputName, nfft, navg, fc, fs, int(t0), tTrim)


Parallel(n_jobs=num_cpus)(delayed(callExtraction)(i) for i in datFiles)
