from vad.VadModel import VadModel

if __name__ == '__main__':
    model = VadModel()
    model.start('粤A9J1H1.m4a')
import librosa

import soundfile as  sf

import noisereduce as nr


# load data
# audio_data, rate = librosa.load('粤A9J1H1.wav')
# # audio_data = audio_data.astype(np.float32) / np.iinfo(np.int16).max
# noise = audio_data[rate*37:rate*40]
# reduced_noise  = nr.reduce_noise(audio_clip=audio_data, noise_clip=noise, verbose=False)
# # audio_data = (audio_data * np.iinfo(np.int16).max).astype(np.int16)
# sf.write('output_file.wav', reduced_noise, rate)
# rate, noise_data = wavfile.read("vad/noise.wav")
# # perform noise reduction
# # optimized for speech
# reduced_noise = nr.reduce_noise(
#     audio_clip=data,
#     noise_clip=noise_data
# )
#
# wavfile.write("mywav_reduced_noise.wav", rate, reduced_noise.reshape(orig_shape))