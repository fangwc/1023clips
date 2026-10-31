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


p0 = "data:image/jpeg;base64,"+img_to_base64('./modeling_db/model_xueshan1.jpg')
p1 = "data:image/jpeg;base64,"+img_to_base64('./modeling_db/model4_yj_red.jpg')
s2 = "data:video/mp4;base64,"+img_to_base64('./video_db/video_tomyheart.mp4')

# print(s2)

def submit_video_job(prompt: str, model: str = "klingai/kling-3.0-omni",
                     resolution: str = "1080p", duration: int = 15) -> str:
    """Step 1: 提交视频生成请求，返回 jobId"""
    url = f"{API_BASE}/videos"
    payload = {
        "model": model,
        # "content": [{"type": "text", "text": prompt}],
        "content": [
        {"type": "text", "text": "本任务为“以图1风景照为场景、参照视频动作生成视频”：图1是唯一的背景、场景、光线、色调和构图依据，同时提供远景人物身份；图2是近景人物的身份依据；上传视频是唯一的动作脚本。输出视频全程使用图1的背景、场景、道具、环境、光线、色调和构图，不用视频背景、不重建、不替换场景，背景稳定不漂移不闪烁；机位和景别按视频区分远景和近景，但画面场景始终来自图1。按视频镜头分段：远景镜头使用图1中的人物，保持其脸型、五官、发型、年龄感、身材比例和穿着；近景镜头使用图2全身艺术照人物，保持其脸型、五官、发型、年龄感、身材比例和艺术照妆造。两张图不得串用，远景不得出现图2妆造，近景不得出现图1人物造型；切换严格发生在视频远景转近景切点，不提前不延后，切换自然，形成远景风景照人物与近景艺术照人物的反差感。图2近景允许适度美颜：皮肤更白皙通透、肤色均匀提亮、轻量磨皮、笑容更美更自然，但保留真实皮肤质感、原始五官比例、年龄感和身份，不网红脸、不过度磨皮、不改变脸型。动作严格参照视频：顺序、数量、手部轨迹、脚步、转身、重心、停顿、节奏和幅度一致，不增删、不简化、不自由发挥；人物朝向按视频每段动作自然重定向。面部表情跟随视频：微笑、眨眼、眼神、眉毛、嘴角等自然表情的时机、强度和节奏与视频对应，表情丰富生动，不面瘫、不单一、不滞后；但身份始终与对应图片一致，不迁移说话口型和夸张表情。人物与图1场景的光影、透视、遮挡自然融合，无贴图感。输出要求：背景来自图1、远景图1人物、近景图2人物，切换准确、图2美颜适度、动作完整复刻、表情自然丰富、身份稳定、手指正常、无穿模无畸形无闪烁。音频完整保留视频原声/音乐，不静音不替换，音画同步。  一定要避免的：使用视频背景、背景来自视频、场景替换、重建场景、背景漂移、背景闪烁、构图变化、原视频人物残留、身份漂移、前后人物不一致、照片动起来、贴图感、动作缺失、动作简化、动作顺序改变、节奏错乱、朝向错误、成人化、身材拉长、换脸感、五官不一致、美颜过度、手指畸形、穿模、闪烁、静音、音频缺失、音画不同步、表情僵硬、面瘫、表情单一、表情滞后、口型迁移、远景误用图2、近景误用图1、两图串用、两张脸混合、切换时机错误、提前切换、延后切换、远景出现艺术照妆造、近景出现风景照人物造型、切换突兀、反差感缺失、图2美颜改变身份、图2过度美白、图2网红脸。"}, 
        {"type": "image_url", "role": "reference_image", "image_url":{"url": p0}},
        {"type": "image_url", "role": "reference_image", "image_url":{"url": p1}},
        {"type": "video_url", "role": "reference_video", "video_url":{"url": s2}}
               ],
        "resolution": resolution,
        "duration": duration,
        # "ratio":"9:16"
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
        prompt="",
        # model = "klingai/kling-3.0-omni", 
        model = "alibaba/wan3.0-video",
        resolution="1080p", # 格式 720p/1080p/4k
        # resolution="720p", # 格式 720p/1080p/4k
        duration=7, # 长度
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