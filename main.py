import essentia.streaming
import essentia.standard
from essentia.streaming import *
from essentia.standard import YamlOutput, PoolAggregator
import os

frameSize = 2048
hopSize = 1024
sampleRate = 44100

for trackName in os.listdir("music"):
    if ".mp3" not in trackName or ".json" in trackName:
        continue
    fullTrackName = "music/" + trackName

    #describe functions
    metadataReader = essentia.standard.MetadataReader(filename=fullTrackName)

    loader = MonoLoader(filename=fullTrackName, sampleRate=sampleRate)
    frameCutter = FrameCutter(frameSize=frameSize, hopSize=hopSize, lastFrameToEndOfFile=True, startFromZero=True)
    spectralCentroidTime = SpectralCentroidTime()
    window = Windowing(type='hann')
    spectrum = Spectrum(size=frameSize)
    danceability = Danceability(maxTau=8800, minTau=310)
    mfcc = MFCC()
    hpcp = HPCP()
    rhythm = PercivalBpmEstimator(sampleRate=sampleRate)
    spectralPeaks = SpectralPeaks()
    dissonance = Dissonance()
    energy = Energy()
    loudness = Loudness()
    key = Key()
    """
    chords = ChordsDetection()
    chordsDescription = ChordsDescriptors()
    """

    pool = essentia.Pool()
    extensionLength = trackName.rfind('.')
    # trackNameWithoutExtension = trackName[:extensionLength]
    # print(trackNameWithoutExtension)
    # pool.add("name", trackNameWithoutExtension)
    id = trackName[:extensionLength]
    name = metadataReader()[0]
    artist = metadataReader()[1]
    genre = metadataReader()[4]
    pool.add("name", name)
    pool.add("artist", artist)
    pool.add("genre", genre)
    pool.add("id", id)

    #connect algorithms
    loader.audio >> frameCutter.signal
    loader.audio >> rhythm.signal
    loader.audio >> danceability.signal
    frameCutter.frame >> window.frame >> spectrum.frame
    spectrum.spectrum >> energy.array
    spectrum.spectrum >> loudness.signal
    spectrum.spectrum >> spectralCentroidTime.array
    spectrum.spectrum >> spectralPeaks.spectrum
    spectralPeaks.magnitudes >> hpcp.magnitudes
    spectralPeaks.frequencies >> hpcp.frequencies
    spectralPeaks.magnitudes >> dissonance.magnitudes
    spectralPeaks.frequencies >> dissonance.frequencies
    hpcp.hpcp >> key.pcp
    """
    hpcp.hpcp >> chords.pcp
    chords.chords >> chordsDescription.chords
    chords.strength >> None
    key.key >> chordsDescription.key
    key.scale >> chordsDescription.scale
    """

    danceability.danceability >> (pool, 'danceability')
    energy.energy >> (pool, 'energy')
    loudness.loudness >> (pool, 'loudness')
    rhythm.bpm >> (pool, 'bpm')
    spectralCentroidTime.centroid >> (pool, 'centroid')
    dissonance.dissonance >> (pool, 'dissonance')
    key.key >> (pool, 'key')
    key.scale >> (pool, 'scale')
    key.strength >> (pool, 'strength')
    """
    chordsDescription.chordsHistogram >> (pool, 'chords histogram')
    chordsDescription.chordsNumberRate >> None
    chordsDescription.chordsChangesRate >> None
    chordsDescription.chordsKey >> None
    chordsDescription.chordsScale >> None
    """

    #get the result
    essentia.run(loader)
    aggrPool = PoolAggregator(defaultStats=['mean', 'var'])(pool)
    outTrackName = trackName + '.json'
    #YamlOutput(filename='full_' + outTrackName, format='json')(pool)
    YamlOutput(filename='aggr_' + outTrackName, format='json')(aggrPool)

"""
gaia transform:
extract_genre()
extract_mood()
"""