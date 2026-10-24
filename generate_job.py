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


s = "data:image/jpeg;base64,"+img_to_base64('./modeling_db/model7_yj_xiandai.jpg')  
s2 = "data:video/mp4;base64,"+img_to_base64('./video_db/video3.mp4')

print(s2)

def submit_video_job(prompt: str, model: str = "klingai/kling-3.0-omni",
                     resolution: str = "1080p", duration: int = 15) -> str:
    """Step 1: 提交视频生成请求，返回 jobId"""
    url = f"{API_BASE}/videos"
    payload = {
        "model": model,
        # "content": [{"type": "text", "text": prompt}],
        "content": [
        {"type": "text", "text": "以我提供的小女孩参考图作为唯一人物身份与身材依据，严格生成同一个小女孩：脸型、五官比例、肤色、发型、年龄感、头身比、肩宽、腰胯比例、腿长比例和整体身材必须与参考图一致，保持儿童自然体态，不因参考视频中模特身材修长而拉长腿部、瘦身、增高或成人化。参考跳舞视频中的人物仅作为动作、姿态、手部轨迹、脚步、转身、重心变化、表情、眼神、口型节奏、镜头角度、景别、机位运动和剪辑节奏的参考，不作为人物容貌、年龄、身高、身材比例和穿着依据。将模特动作完整迁移到小女孩身上：动作顺序、节拍、姿态和轨迹与参考视频一致，不增删动作；但根据小女孩的头身比和四肢长度做自然动作重定向，保持动作神韵一致且符合儿童身体特点，不拉长肢体、不模仿成人修长比例。穿着替换为适合小女孩的整洁得体童装，可保留原服装主色调和风格元素，但款式儿童化、日常化、安全得体，不暴露、不浓妆、不性感化。场景、背景、道具、光线、构图与参考视频保持一致。表情和口型节奏与参考视频一致，但保持小女孩自然天真的面部状态。输出真实、自然、美观的高清视频，面部稳定、身份一致、身材比例稳定、动作流畅、手指正常、无穿模无畸形。音频方面：完整保留参考视频的原背景音乐/原声，不静音、不替换、不删减，音乐节拍与动作节拍保持同步；如模型支持音频生成，请输出带原音乐音轨的视频，音画同步。避免出现：成人化、16岁感、青少年化、年龄增大、模特身材、修长比例、拉长腿、增高、瘦身、成人骨架、肩宽腰胯成人化、身份漂移、脸型变化、五官不一致、换脸感、发型变化、穿着成人化、性感化、浓妆、动作变形、动作缺失、动作顺序错乱、节奏错乱、镜头变化、场景变化、背景改变、手指畸形、多指、肢体扭曲、穿模、闪烁、模糊、卡通化、过度美颜、多余人物、静音、无音乐、音频缺失、音乐被替换、音画不同步。"}, 
        {"type": "image_url", "role": "reference_image", "image_url":{"url": s}},
        {"type": "video_url", "role": "reference_video", "video_url":{"url": s2}}
               ],
        "resolution": resolution,
        "duration": duration,
        # "ratio":"9:16"
    }

    # 可灵需要指定长宽比；
    if(model == "klingai/kling-3.0-omni"):
        payload['ratio'] = "9:16"
        payload['audio'] = "native" # 视频原声音，默认关闭

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
        model = "klingai/kling-3.0-omni", 
        # model = "alibaba/wan3.0-video",
        resolution="1080p", # 格式 720p/1080p/4k
        duration=15, # 长度
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