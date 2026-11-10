from pathlib import Path
import subprocess, wave, json
from concurrent.futures import ThreadPoolExecutor
import numpy as np

ROOT = Path(__file__).resolve().parent
FPS, SR, DURATION = 30, 48000, 15

def run(args):
    result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if result.returncode:
        raise RuntimeError(result.stderr[-6000:])
    return result.stdout

# Original synthesized score and effects; no third-party music recording.
rng = np.random.default_rng(36)
audio = np.zeros((SR * DURATION, 2), np.float64)
def add(start, signal, gain=1., pan=0.):
    begin = round(start * SR)
    count = min(len(signal), len(audio)-begin)
    if begin < 0 or count <= 0: return
    audio[begin:begin+count, 0] += signal[:count] * gain * np.sqrt((1-pan)/2)
    audio[begin:begin+count, 1] += signal[:count] * gain * np.sqrt((1+pan)/2)

def pluck(freq, seconds=.34):
    t = np.arange(int(seconds*SR))/SR
    env = (1-np.exp(-t*450))*np.exp(-t*13)
    return env*(np.sin(2*np.pi*freq*t)+.3*np.sin(4*np.pi*freq*t)+.1*np.sin(6*np.pi*freq*t))

notes = [72,76,79,76,74,77,81,77,71,74,79,74,72,76,79,84]
for i, beat in enumerate(np.arange(0,15,.5)):
    note = notes[i%len(notes)]
    add(beat, pluck(440*2**((note-69)/12)), .16, -.22 if i%2 else .22)
    t = np.arange(int(.12*SR))/SR
    kick = np.sin(2*np.pi*(62*t+35*.035*(1-np.exp(-t/.035))))*np.exp(-t*38)
    if i%2==0: add(beat,kick,.12)
    if i%2:
        noise=rng.normal(size=len(t))
        add(beat,noise*np.exp(-t*65)*np.minimum(t*700,1),.018)

for start in [2.86,6.86,10.86]:
    t=np.arange(int(.22*SR))/SR
    noise=rng.normal(size=len(t))
    noise=np.convolve(noise,np.ones(11)/11,mode='same')
    add(start,noise*np.sin(np.pi*t/.22)**2,.19)
for start,note in [(7.12,76),(7.53,79),(7.94,84)]:
    add(start,pluck(440*2**((note-69)/12),.4),.24)
for start,note in [(11.15,67),(11.38,64),(11.61,60)]:
    add(start,pluck(440*2**((note-69)/12),.45),.22)
add(13.2,pluck(523.25,.6),.22)
add(13.22,pluck(659.25,.6),.16)
audio[:int(.08*SR)] *= np.linspace(0,1,int(.08*SR))[:,None]
audio[-int(.65*SR):] *= np.linspace(1,0,int(.65*SR))[:,None]
audio *= .76/max(np.max(np.abs(audio)),.76)
with wave.open(str(ROOT/'soundtrack.wav'),'wb') as f:
    f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR)
    f.writeframes((audio*32767).astype('<i2').tobytes())

header='''[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Main,Microsoft YaHei,70,&H00FFFFFF,&H000000FF,&H001E211E,&H60000000,-1,0,0,0,100,100,2,0,1,3.5,2,5,60,60,0,1
Style: Small,Microsoft YaHei,31,&H00FFFFFF,&H000000FF,&H00302E25,&H70000000,0,0,0,0,100,100,1,0,1,2,0,7,0,0,0,1
Style: Label,Microsoft YaHei,25,&H00FFFFFF,&H000000FF,&H00302E25,&H70000000,0,0,0,0,100,100,0,0,1,1.5,0,9,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
def stamp(s):
    return f'{int(s//3600)}:{int(s//60)%60:02}:{int(s)%60:02}.{round((s%1)*100):02}'
def event(start,end,text,style='Main',tags=''):
    return f'Dialogue: 1,{stamp(start)},{stamp(end)},{style},,0,0,0,,{{{tags}}}{text}\n'

ass=header
ass+=event(0,15,'杭州降温 · 西湖先穿上了','Small',r'\pos(65,150)')
ass+=event(0,15,'AI创意演绎','Label',r'\pos(1000,155)')
ass+=event(.15,3,'杭州这次降温\\N{\\c&H0089DFFF&}有多认真？',tags=r'\pos(540,1435)\fad(140,80)\fscx94\fscy94\t(0,180,\fscx100\fscy100)')
ass+=event(3.05,7,'雷峰塔：\\N{\\c&H0089DFFF&}羽绒服，安排！',tags=r'\pos(540,1450)\fad(80,80)\fscx90\fscy90\t(0,160,\fscx100\fscy100)')
ass+=event(7.05,11,'三潭印月：\\N{\\c&H0089DFFF&}帽子围巾，全员到位',tags=r'\pos(540,1450)\fs64\fad(80,80)')
ass+=event(11.05,13.2,'西湖都穿上了\\N{\\c&H0089DFFF&}你还穿这么薄？',tags=r'\pos(540,1450)\fad(80,60)')
ass+=event(13.2,15,'明早出门\\N{\\c&H0089DFFF&}记得加件衣服',tags=r'\pos(540,1450)\fad(100,220)')
(ROOT/'captions.ass').write_text(ass,encoding='utf-8-sig')

scenes=[('01_lake.png',3,'1.0+0.075*on/89'),('02_pagoda.png',4,'1.0+0.045*on/119'),('03_hats.png',4,'1.06-0.06*on/119'),('04_visitor.png',4,'1.0+0.09*on/119')]
def make_scene(item):
    i,(file,seconds,zoom)=item
    if i != 1 and (ROOT/f'scene_{i}.mp4').exists():
        return f'scene {i} reused'
    n=seconds*FPS
    y='0' if i == 1 else 'ih/2-ih/zoom/2'
    vf=(f'scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,'
        f"zoompan=z='{zoom}':x='iw/2-iw/zoom/2':y='{y}':d={n}:s=1080x1920:fps=30,"
        'setsar=1,format=yuv420p')
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',file,'-vf',vf,'-frames:v',str(n),
         '-c:v','libx264','-preset','fast','-crf','18','-threads','2',f'scene_{i}.mp4'])
    return f'scene {i} complete'
with ThreadPoolExecutor(max_workers=2) as pool:
    for status in pool.map(make_scene,enumerate(scenes)):
        print(status,flush=True)
(ROOT/'concat.txt').write_text(''.join(f"file 'scene_{i}.mp4'\n" for i in range(4)),encoding='utf-8')
run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i','concat.txt',
     '-i','soundtrack.wav','-vf',"drawbox=x=0:y=1310:w=iw:h=265:color=black@0.22:t=fill,ass=captions.ass",
     '-map','0:v:0','-map','1:a:0','-t','15','-c:v','libx264','-preset','fast','-crf','19',
     '-pix_fmt','yuv420p','-af','volume=6dB','-c:a','aac','-b:a','192k','-movflags','+faststart',
     '-metadata','title=杭州降温，连西湖都穿上了','-metadata','comment=AI-generated imagery; edited motion-still video with original synthesized audio.',
     'hangzhou_cold_15s.mp4'])
probe=run(['ffprobe','-v','error','-show_entries','format=duration,size:stream=codec_name,width,height,r_frame_rate,duration','-of','json','hangzhou_cold_15s.mp4'])
(ROOT/'verification.json').write_text(probe,encoding='utf-8')
print(probe,flush=True)
run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i','hangzhou_cold_15s.mp4','-vf',
     "select='eq(n,45)+eq(n,150)+eq(n,270)+eq(n,360)',scale=270:480,tile=4x1",'-frames:v','1','review.jpg'])
print('FINAL: '+str(ROOT/'hangzhou_cold_15s.mp4'),flush=True)
