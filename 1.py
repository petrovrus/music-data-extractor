import essentia.standard
from essentia.standard import *
import os

def extract_mfcc(audio, pool):
    w = Windowing(type = 'hann')
    spectrum = Spectrum(size=2048)
    mfcc = MFCC()
    mfccs = []
    melbands = []
    for frame in FrameGenerator(audio, frameSize=2048, hopSize=1024, startFromZero=True):
        mfcc_bands, mfcc_coeffs = mfcc(spectrum(w(frame)))
        pool.add('lowlevel.mfcc', mfcc_coeffs)
        pool.add('lowlevel.mfcc_bands', mfcc_bands)

for trackName in os.listdir("Music"):
    fullTrackName = "Music/" + trackName
    loader = essentia.standard.MonoLoader(filename=fullTrackName)
    audio = loader()
    pool = essentia.Pool()
    extract_mfcc(audio, pool)
    outTrackName = 'mfcc_' + trackName + '.sig'
    YamlOutput(filename=outTrackName)(pool)
    aggrPool = PoolAggregator(defaultStats = [ 'mean', 'var' ])(pool)
    YamlOutput(filename='mfccaggr_' + trackName + '.sig')(pool)

