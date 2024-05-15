#-- coding: utf-8 --
import numpy as np
import matplotlib.pyplot as plt
import wave
from tqdm import tqdm

import cmath
import math
 
def binary2float(frames, length, sampwidth):
    if sampwidth==1:
        data = np.frombuffer(frames, dtype=np.uint8)
        data = data - 128
    elif sampwidth==2:
        data = np.frombuffer(frames, dtype=np.int16)
    elif sampwidth==3:
        a8 = np.frombuffer(frames, dtype=np.uint8)
        tmp = np.empty([length, 4], dtype=np.uint8)
        tmp[:, :sampwidth] = a8.reshape(-1, sampwidth)
        tmp[:, sampwidth:] = (tmp[:, sampwidth-1:sampwidth] >> 7) * 255
        data = tmp.view("int32")[:, 0]
    elif sampwidth==4:
        data = np.frombuffer(frames, dtype=np.int32)
    data = data.astype(float)/(2**(8*sampwidth-1)) # Normalize (int to float)
    return data
 
def float2binary(data, sampwidth):
    data = (data*(2**(8*sampwidth-1)-1)).reshape(data.size, 1) # Normalize (float to int)
    if sampwidth==1:
        data = data+128
        frames = data.astype(np.uint8).tobytes()
    elif sampwidth==2:
        frames = data.astype(np.int16).tobytes()
    elif sampwidth==3:
        a32 = np.asarray(data, dtype = np.int32)
        a8 = (a32.reshape(a32.shape + (1,)) >> np.array([0, 8, 16])) & 255
        frames = a8.astype(np.uint8).tobytes()
    elif sampwidth==4:
        frames = data.astype(np.int32).tobytes()
    return frames
 
def read_wave(file_name, start=0, end=0):
    file = wave.open(file_name, "rb") # open file
    sampwidth = file.getsampwidth()
    nframes = file.getnframes()
    file.setpos(start)
    if end == 0:
        length = nframes-start
    else:
        length = end-start+1
    frames = file.readframes(length)
    file.close() # close file
    return binary2float(frames, length, sampwidth) # binary to float
 
def write_wave(file_name, data, sampwidth=3, fs=48000):
    file = wave.open(file_name, "wb") # open file
    # setting parameters
    file.setnchannels(1)
    file.setsampwidth(sampwidth)
    file.setframerate(fs)
    frames = float2binary(data, sampwidth) # float to binary
    file.writeframes(frames)
    file.close() # close file
 
def getParams(file_name):
    file = wave.open(file_name) # open file
    params = file.getparams()
    file.close() # close file
    return params

# STFT (s: signal(1D-array), Lf: length of frame(window), noverlap: number of overlap)
def STFT(s, Lf, noverlap=None):
    # https://moromisenpy.com/python_stft/
    if noverlap==None:
        noverlap = Lf//2
    l = s.shape[0]
    win = np.hanning(Lf)
    Mf = Lf//2 + 1
    Nf = int(np.ceil((l-noverlap)/(Lf-noverlap)))-1
    S = np.empty([Mf, Nf], dtype=np.complex128)
    for n in range(Nf):
        S[:,n] = np.fft.rfft(s[(Lf-noverlap)*n:(Lf-noverlap)*n+Lf] * win, n=Lf, axis=0)
    return S

# 追加した関数群

def iSTFT(S, noverlap, mode="precision"):
    Mf, Nf = S.shape
    # 逆変換をするとなぜかピッチが１つ分上がる
    # https://moromisenpy.com/python_stft/
    # 逆STFT（iSTFT関数）は、楽曲の長さの倍以上の時間がかかります。
    Lf = (Mf - 1) * 2
    k = Lf//noverlap + 1
    l = Nf * ( Lf - noverlap) +  noverlap
    s = np.zeros([l], dtype=np.float32)
    s_= np.zeros([l], dtype=np.float32)
    for n in tqdm(range(Nf)):
        if mode == "rough":
            s[(Lf-noverlap)*n:(Lf-noverlap)*n+Lf] = np.fft.irfft(S[:,n], n=Lf, axis=0)
        if mode == "precision":
            s_[(Lf-noverlap)*n:(Lf-noverlap)*n+Lf] = np.fft.irfft(S[:,n], n=Lf, axis=0) / k
            s = s + s_
            s_= s_ * 0
    return s

def inst(file_name_1, file_name_2, mode="precision"):
    inst_test(file_name_1, file_name_2, mode, Lf_ = 2**11, phase_ = 0.0)

# 楽曲のLとRのデータを入力することで、インストルメンタルデータを生成する関数
def inst_test(file_name_1, file_name_2, mode="precision", Lf_ = 2**11, phase_ = 0.0):
    # file_name_1 = "./michizure_L.wav" # L or R の音声データ
    # file_name_2 = "./michizure_R.wav" # L or R の音声データ
    # mode = "precision":逆STFTが精密（遅い） or "rough":逆STFT粗い（速い）

    # Lf_で短時間フーリエ変換での１フレームの長さを指定（大きい方が周波数特性は良くなるが、時間特性は悪くなる）
    # phase_でLとRチャンネルの位相をずらす 度数表示で入力する

    # https://moromisenpy.com/python_stft/
    # 逆STFT（iSTFT関数）は、楽曲の長さの倍以上の時間がかかります。

    start = 0 # [s]
    end = 0 # [s] (if end==0 =&amp;amp;amp;gt; full size)

    s_1 = read_wave(file_name_1, start, end)
    s_2 = read_wave(file_name_2, start, end)
    s_1_max = np.max(s_1)
    s_2_max = np.max(s_2)
    
    if s_1_max >= s_2_max:
        s_max = s_1_max
    else:
        s_max = s_2_max

    Lf = Lf_ # 2**8
    noverlap = Lf//2 #
    if noverlap == 0:
        noverlap = 1

    S_1 = STFT(s_1, Lf, noverlap) # 2次元の配列
    S_2 = STFT(s_2, Lf, noverlap) # 2次元の配列
    S_mono = (S_1/2) + (S_2/2)
    S_mono_max = np.max(np.abs(S_mono))

    # 度数の位相をラジアンにする
    phase_rad = phase_ * ( math.pi/180)

    S_ = (S_1 / 2) - (( S_2 / 2) * cmath.rect(1,phase_rad))

    S_max_ = np.max(np.abs(S_))
    S_ /= S_max_ #
    S_max_ = np.max(np.abs(S_))
    S_ *= ( S_mono_max / (S_max_ * 2))

    s_ = iSTFT(S_, noverlap, mode) # 1次元の配列 mode = "precision" or "rough"
    s_max_ = np.max(s_)
    s_ *= (s_max / s_max_)

    # "rough"モードの時に、ファイル名にモードを入れ、それ以外の時は、入れない
    if mode == "rough":
        pass
    else:
        mode = ""

    file_name_ = file_name_1 + "_" + "Lf={}".format(Lf) + "_" + "phase={:.2f}".format(phase_) +"_" + mode + ".wav"
    write_wave(file_name_, s_, sampwidth=3, fs=48000)

