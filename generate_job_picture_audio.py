#!/usr/bin/env python3
"""
ZenMux 视频生成客户端
用法:
    export ZENMUX_API_KEY="your-key"
    python video_gen.py
"""

import os
import time
import sys
import requests

API_BASE = "https://zenmux.ai/api/v1"
API_KEY = sys.argv[1]  #参数

if not API_KEY:
    sys.exit("错误: 请先设置环境变量 ZENMUX_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}


import base64

def img_to_base64(path: str) -> str:
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')


p0 = "data:image/jpeg;base64,"+img_to_base64('./modeling_db/ChatGPT202611423_55_25.png')
# p1 = "data:image/jpeg;base64,"+img_to_base64('./modeling_db/slmh_scene.jpg')
# p2 = "data:image/jpeg;base64,"+img_to_base64('./modeling_db/cake.jpg')
s2 = "data:audio/mpeg;base64,"+img_to_base64('./video_db/two_tiger.mp3')

raw_prompt = """
以输入照片中的一年级小朋友为唯一主角，以输入的《两只老虎》音频为演唱与舞蹈依据，生成一段自然、可爱、表情丰富的边唱边跳视频。视频时长与输入音频完全一致，约14.6秒，保留原音频及其速度。整体呈现小朋友面对镜头开心表演儿歌的感觉，天真、活泼，带一点认真表演的小得意。

人物一致性：
严格保持参考照片中人物的五官比例、脸型、眼睛形状、鼻子、嘴唇、肤色、发型、服装与配饰，保留原本的容貌、辨识度及一年级儿童的年龄感。表情变化符合人物自身面部结构，笑容自然好看。保留照片中的背景、光线方向、色调和场景空间关系。

演唱与口型同步：
人物在整段有歌词的地方自然跟唱，呈现声音由这个人物唱出来的感觉。以输入音频中的实际人声为唯一口型依据，逐字匹配歌词发音的起止、音节转换、嘴唇开合、圆唇与展唇，以及下颌运动；延长音保持相应的演唱口型，收音与停顿自然闭合或放松。口型跟随人声发音，身体动作跟随音乐节拍。重复歌词也要分别对应实际演唱时机，嘴部动作连贯、适度，保持原有嘴唇形状和脸型。

演唱过程中，开心、惊讶和疑惑主要通过眉毛、眼神、脸颊及头部姿态表达，嘴部优先完成正确发音。笑着唱时嘴角自然上扬，同时保留清晰的演唱口型。抿嘴、微嘟嘴、闭嘴微笑等动作仅安排在实际歌词间隙或收音之后。

镜头与舞蹈：
稳定的正面机位，一个连续镜头，完整展示手脚动作，同时保证脸部与口型清晰可辨。人物大部分时间面向镜头，在画面中央活动。采用适合一年级小朋友的简单儿歌律动：小步点踏、轻微屈膝、左右摆动、小幅原地跑、虎爪手势、指示动作和摊手。动作轻巧、协调，有准备、展开和收势，保持连续的身体律动。

按音频约每分钟149拍的节奏编排，每两拍或四拍完成一个主要手势。以下时间为大致定位，实际动作、表情和口型必须跟随音频中的对应歌词：

约0—4秒，“两只老虎，两只老虎”：
看向镜头边唱边左右小步点踏，双手在肩膀两侧做轻巧、圆润的小虎爪手势，先向一侧展示，再向另一侧展示，保持脸部无遮挡。第一遍眼神明亮、嘴角略带笑意；第二遍轻轻歪头，脸颊抬起，笑意更加明显，像开心地向观众介绍两只小老虎。嘴唇持续准确完成歌词发音。

约4—7.3秒，“跑得快，跑得快”：
自然过渡为原地轻快小跑，双臂交替摆动，脚步轻盈，人物位置稳定。保持面向镜头演唱，表情变得兴奋，眉毛略抬，眼睛带笑，呈现“看我跑得多快”的儿童式小得意。唱到延长的“快”时，口型跟随原音频延续，身体保持有弹性的轻快律动。

约7.3—10.6秒，“一只没有眼睛，一只没有尾巴”：
脚下继续小幅踏步，小跑动作自然收小。唱到“眼睛”时，一只手在眼睛旁做指示，保持眼睛与嘴部清晰可见；眉毛轻轻抬起，笑意稍收，出现刚刚发现问题的疑惑。唱到“尾巴”时，另一只手向身体侧后方示意，头部轻微侧倾，视线重新回到镜头。全程继续准确跟唱，用眉眼和头部表现疑问。手势只表达歌词含义，人物身体与面部结构始终完整、正常。

约10.6秒至结束，“真奇怪，真奇怪”：
第一遍边唱边轻轻摊手，头向一侧微倾，眉毛抬起，眼神带着清楚而可爱的疑问；嘴部准确唱出“真奇怪”，并跟随延长音完成收音。第二遍轻轻转回正面，配合一次小幅耸肩，看着镜头像在问“你也觉得奇怪吧？”，继续完成同步口型。最后一个字唱完后，自然收起演唱口型，嘴角扬起，留下俏皮、柔和的微笑，并随音乐结尾完成平衡、好看的收势。

整体表演：
情绪沿着“开心介绍—兴奋跑动—发现异常—俏皮疑惑—带笑回应”自然推进。每个表情有形成、短暂保持和放松的过程，重复歌词的第二遍略有递进。保留小朋友认真唱跳时的自然感，表情生动而不过度，动作简单而有节奏，始终保持与镜头的亲切交流。

质量要求：
人物身份与年龄感稳定，口型与人声同步，面部结构自然，笑容美观，手脚结构正确，脚步与地面接触真实，头发和衣物随动作自然摆动。避免口型提前或滞后、机械开合嘴、唱词过程中突然抿嘴、嘴部过度张大、五官漂移、脸型变化、僵硬笑容、肢体扭曲、脚底滑动、动作突跳及背景变形。

"""

def submit_video_job(prompt: str, model: str = "klingai/kling-3.0-omni",
                     resolution: str = "1080p", duration: int = 15) -> str:
    """Step 1: 提交视频生成请求，返回 jobId"""
    url = f"{API_BASE}/videos"
    payload = {
        "model": model,
        "content": [
        {"type": "text", "text": prompt}, 
        {"type": "image_url", "role": "reference_image", "image_url":{"url": p0}},
        # {"type": "image_url", "role": "reference_image", "image_url":{"url": p1}},
        # {"type": "image_url", "role": "reference_image", "image_url":{"url": p2}},
        # {"type": "video_url", "role": "reference_video", "video_url":{"url": s2}}
        {"type": "audio_url", "role": "reference_audio", "audio_url":{"url": s2}}
               ],
        "resolution": resolution,
        "duration": duration,
        "ratio":"9:16"
    }

    # 可灵需要指定长宽比；
    if(model == "klingai/kling-3.0-omni"):
        payload['ratio'] = "9:16"
        payload['generate_audio'] = "native" # 视频原声音打开，关闭off，参数不对

    print(payload)

    resp = requests.post(url, headers=HEADERS, json=payload, timeout=300)
    resp.raise_for_status()
    data = resp.json()

    # 不同 API 返回字段可能不同，做兼容处理
    job_id = data.get("id") or data.get("jobId") or data.get("job_id")
    if not job_id:
        raise RuntimeError(f"响应中没有找到 jobId: {data}")

    print(f"[提交成功] jobId = {job_id}  状态 = {data.get('status')}")
    return job_id


def poll_until_done(job_id: str, interval: int = 5, timeout: int = 600) -> dict:
    """Step 2: 轮询直到状态为 succeeded 或 failed"""
    url = f"{API_BASE}/videos/{job_id}"
    start = time.time()

    while True:
        elapsed = time.time() - start
        if elapsed > timeout:
            raise TimeoutError(f"轮询超时 ({timeout}s)，jobId={job_id}")

        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        status = data.get("status", "").lower()
        print(f"[{elapsed:6.1f}s] 状态: {status}")

        if status == "succeeded":
            return data
        if status in ("failed", "error", "cancelled"):
            raise RuntimeError(f"任务失败: {data}")

        time.sleep(interval)


def download_video(video_url: str, out_path: str = "output.mp4") -> None:
    """下载生成的视频"""
    print(f"[下载中] {video_url}")
    with requests.get(video_url, stream=True, timeout=60) as r:
        r.raise_for_status()
        with open(out_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"[下载完成] 已保存到 {out_path}")


def main():
    # ---- 1. 提交 ----
    job_id = submit_video_job(
        prompt=raw_prompt,
        # model = "klingai/kling-3.0-omni", 
        model = "alibaba/wan3.0-video",
        resolution="1080p", # 格式 720p/1080p/4k
        # resolution="720p", # 格式 720p/1080p/4k
        duration=14, # 长度
    )

    # ---- 2. 轮询 ----
    result = poll_until_done(job_id, interval=10, timeout=3600)

    # ---- 3. 提取 video_url ----
    video_url = (
        result.get("content", {}).get("video_url")
        or result.get("video_url")
    )
    if not video_url:
        raise RuntimeError(f"任务成功但没找到 video_url: {result}")

    print(f"[完成] video_url = {video_url}")

    # ---- 4. 可选：下载到本地 ----
    download_video(video_url, out_path=f"{job_id}.mp4")


if __name__ == "__main__":
    main()