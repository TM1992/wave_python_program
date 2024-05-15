import wave_func_x as wx

# 楽曲からボーカルの音声をほとんど除去するプログラムです
# 処理時間は、楽曲の長さの倍以上の時間がかかります。
# 処理後のwaveファイルは、スピードを0.92倍、トランスポーズは-1、チューンは-20にすると原曲のキーとほぼ同じになります。
# tqdmのインストールが必要です

file_name_1 = "./楽曲データのLチャンネル.wav" # L の音声データ
file_name_2 = "./楽曲データのRチャンネル.wav" # R の音声データ

wx.inst(file_name_1, file_name_2)


   

