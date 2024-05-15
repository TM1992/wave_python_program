# wave_python_program

# ・This program is a program that removes most of the vocal sound from songs.
# ・We cannot be held responsible for any damage caused by using this program.
# ・The processing time is more than twice the length of the song.
# The processed wave file will have almost the same key as the original song by setting the speed to 0.92x, transpose to -1, and tune to -20.
# Requires tqdm installation.
# The music you want to process must be in stereo.

# In developing this program, I used Moromi-senpai's blob as a reference. (URL link below)
# https://moromisenpy.com/python_stft/
# https://moromisenpy.com/python_wav/

# How to use this program ...
# By modifying part of the code in test.py, you can remove the vocal sound from the song.
# 1. Prepare the L channel wav format data and the R channel wav format data of the song you want to process.
# 2. Save that data to the directory where test.py and wave_func_x.py are saved.
# 3. In test.py, file_name_1 = "./楽曲データのLチャンネル.wav"
#                file_name_2 = "./楽曲データのRチャンネル.wav"
#    Enter the file names of the L channel and R channel of the song you want to process.
# 4. Finally, run test.py to start processing.

#    that's all

# このプログラムは、楽曲からボーカル音の大部分を除去するプログラムです。
# 本プログラムの利用により生じたいかなる損害についても、当社は一切の責任を負いません。
# 処理時間は曲の長さの 2 倍以上かかります。
# 速度を 0.92 倍、トランスポーズを -1、チューニングを -20 に設定すると、処理された wave ファイルは元の曲とほぼ同じキーになります。
# tqdm のインストールが必要です。
# 処理したい楽曲はステレオである必要があります。

# このプログラムの開発には、「もろみ先輩」様のブロブを参考にさせて頂きました。（以下のURLリンク）
# https://moromisenpy.com/python_stft/
# https://moromisenpy.com/python_wav/



# このプログラムの使い方を解説します。
# test.pyのコードの一部を修正することで、楽曲からボーカルの音声を除去できます。
# 1. 処理したい楽曲のLチャンネルのwav形式のデータと、Rチャンネルのwav形式のデータを用意します。
# 2. そのデータをtest.pyおよびwave_func_x.pyが保存されたディレクトリに保存します。
# 3. test.py の中の、file_name_1 = "./楽曲データのLチャンネル.wav"
#                    file_name_2 = "./楽曲データのRチャンネル.wav"
#    に処理したい楽曲のLチャンネルおよびRチャンネルのファイル名を入れます。
# 4. 最後にtest.pyを実行すれば、処理が開始されます。
# 　 処理には、数分を要します。
# 以上

