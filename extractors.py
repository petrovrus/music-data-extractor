import essentia.standard
from essentia.standard import *

def extract_mfcc(audio, pool):
    w = Windowing(type = 'hann')
    spectrum = Spectrum(size=2048)
    mfcc = MFCC()
    for frame in FrameGenerator(audio, frameSize=2048, hopSize=1024, startFromZero=True):
        mfcc_bands, mfcc_coeffs = mfcc(spectrum(w(frame)))
        pool.add('lowlevel.mfcc', mfcc_coeffs)
        pool.add('lowlevel.mfcc_bands', mfcc_bands)

def extract_spectral_centroid(spectrum, pool):
    sct = SpectralCentroidTime()
    centroid = sct(spectrum)
    pool.add('centroid', centroid)

def extract_zcr(audio, pool):
    zcr = ZeroCrossingRate()
    zero_crossing_rate = zcr(audio)
    pool.add('zero-crossing rate', zero_crossing_rate)

def extract_beats_loudness(audio, pool):
    bln = BeatsLoudness()
    loudness = bln(audio)
    pool.add('beats loudness', bln)

def extract_energy(spectrum, pool):
    eng = Energy()
    energy = eng(spectrum)
    pool.add('energy', energy)

def extract_danceability(audio, pool):
    dnc = Danceability(maxTau=8800, minTau=310)
    danceability = dnc(audio)
    pool.add('danceability', danceability)

"""
def extract_mean()  of what
def extract_genre() ->streaming
def extract_mood() ->streaming
def extract_pitch() ->streaming
def extract_dissonance() ->streaming
def extract_mode() ->streaming
"""