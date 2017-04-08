import essentia.standard
from essentia.standard import *
import os

def extract_data(audio, pool):
    window = Windowing(type = 'hann')
    spectrum = Spectrum(size=frameSize)
    mfcc = MFCC()
    danceability = Danceability(maxTau=8800, minTau=310)(audio)
    rhythm = PercivalBpmEstimator(sampleRate=sampleRate)(audio)
    pool.add('bpm', rhythm)
    pool.add('danceability', danceability)
    for frame in FrameGenerator(audio, frameSize=frameSize, hopSize=hopSize, startFromZero=True):
        centroid = SpectralCentroidTime()(spectrum(window(frame)))
        zcr = ZeroCrossingRate()(frame)
        energy = Energy()(spectrum(window(frame)))
        loudness = Loudness()(frame)
        mfcc_bands, mfcc_coeffs = mfcc(spectrum(window(frame)))
        frequencies, magnitudes = SpectralPeaks()(spectrum(window(frame)))
        pitch_class_profile = HPCP()(frequencies, magnitudes)
        dissonance = Dissonance()(frequencies, magnitudes)
        key, scale, strength, fst_to_scnd_rel_str = Key()(pitch_class_profile)
        #chords = ChordsDetection()(pitch_class_profile)

        pool.add('centroid', centroid)
        pool.add('zero-crossing rate', zcr)
        pool.add('energy', energy)

        pool.add('loudness', loudness)
        pool.add('dissonance', dissonance)
        #pool.add('chords', chords)
        pool.add('scale', scale)

"""
gaia transform:
extract_genre()
extract_mood()
"""

frameSize = 2048
hopSize = 1024
sampleRate = 44100
for trackName in os.listdir("music"):
    if ".mp3" not in trackName or ".json" in trackName:
        continue
    fullTrackName = "music/" + trackName
    loader = essentia.standard.MonoLoader(filename=fullTrackName, sampleRate=sampleRate)
    audio = loader()
    pool = essentia.Pool()
    extract_data(audio, pool)
    aggrPool = PoolAggregator(defaultStats=['mean', 'var'])(pool)
    outTrackName = 'dance_' + trackName + '.json'
    YamlOutput(filename=outTrackName, format='json')(pool)
    YamlOutput(filename='aggr_' + outTrackName, format='json')(aggrPool)