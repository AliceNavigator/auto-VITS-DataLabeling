from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import os

'''
inference_pipeline = pipeline(
    task=Tasks.auto_speech_recognition,
    model='./Model/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch',
)

rec_result = inference_pipeline(audio_in='ge_1570_2.wav')
print(rec_result)
# {'text': '欢迎大家来体验达摩院推出的语音识别模型'}
'''

parent_dir = "./raw_audio/"
local_dir_root = "./Model/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch"
target_sr = 44100

# speaker_annos = []
# speaker_annos_bert = []
complete_list = []
filelist = list(os.walk(parent_dir))[0][2]

if os.path.exists('long_character_anno.txt'):
    with open("./long_character_anno.txt", 'r', encoding='utf-8') as f:
        for line in f.readlines():
            pt, _, _ = line.strip().split('|')
            complete_list.append(pt)

inference_pipeline = pipeline(
    task=Tasks.auto_speech_recognition,
    model=local_dir_root,
)

for file in filelist:
    if file[-3:] != 'wav':
        print(f"{file} not supported, ignoring...\n")
        continue
    print(f"transcribing {parent_dir + file}...\n")

    character_name = file.rstrip(".wav").split("_")[0]
    savepth = "./dataset/" + character_name + "/" + file

    if savepth in complete_list:
        print(f'{file} is already done, skip!')
        continue

    rec_result = inference_pipeline(audio_in=parent_dir + file)

    if 'text' not in rec_result:
        print("Text is not recognized，ignoring...\n")
        continue

    annos_text = rec_result['text']
    annos_text = '[ZH]' + annos_text.replace("\n", "") + '[ZH]'
    annos_text = annos_text + "\n"
    # speaker_annos.append(savepth + "|" + character_name + "|" + annos_text)
    line1 = savepth + "|" + character_name + "|" + annos_text
    # speaker_annos_bert.append(savepth + "|" + character_name + "|ZH|" + rec_result['text'] + "\n")
    line2 = savepth + "|" + character_name + "|ZH|" + rec_result['text'] + "\n"
    with open("./long_character_anno.txt", 'a', encoding='utf-8') as f:
        f.write(line1)
    with open(f"./barbara.list", 'a', encoding='utf-8') as f:
        f.write(line2)
    print(rec_result)
print("Done!\n")
