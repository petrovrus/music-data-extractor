import essentia.standard
from essentia.standard import *
import os
from extractors import *

for trackName in os.listdir("Music"):
    if ".mp3" not in trackName or ".sig" in trackName:
        continue
    fullTrackName = "Music/" + trackName
    loader = essentia.standard.MonoLoader(filename=fullTrackName)
    audio = loader()
    pool = essentia.Pool()
    extract_zcr(audio, pool)
    extract_danceability(audio, pool)
    outTrackName = 'dance_' + trackName + '.json'
    YamlOutput(filename=outTrackName)(pool)
    """
    extract_beats_loudness(audio,pool)
    extract_mfcc(audio, pool)
    outTrackName = 'mfcc_' + trackName + '.sig'
    YamlOutput(filename=outTrackName)(pool)
    aggrPool = PoolAggregator(defaultStats = [ 'mean', 'var' ])(pool)
    YamlOutput(filename='mfccaggr_' + trackName + '.sig')(pool)
    """


