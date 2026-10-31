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


s = "data:image/jpeg;base64,"+img_to_base64('./modeling_db/model4_yj_red.jpg')
s2 = "data:video/mp4;base64,"+img_to_base64('./video_db/xwn_mv.mp4')

# print(s2)

def submit_video_job(prompt: str, model: str = "klingai/kling-3.0-omni",
                     resolution: str = "1080p", duration: int = 15) -> str:
    """Step 1: 提交视频生成请求，返回 jobId"""
    url = f"{API_BASE}/videos"
    payload = {
        "model": model,
        # "content": [{"type": "text", "text": prompt}],
        "content": [
        {"type": "text", "text": "以上传视频为待编辑底片，照片为替换人物唯一身份依据。将视频中的主角从头到尾逐帧替换为照片人物，原主角零残留、不出现、后半段不变回、不身份漂移；其他人物、背景、场景、光线、镜头、构图、时长均保留原视频。声音必须完整保留原视频原声/歌声/音乐/环境音，不静音、不替换、不改唱、不变调，音量与节奏保持原样，音画严格同步。 替换人物不产生新声音。动作严格复刻原视频：顺序、数量、手部轨迹、脚步、转身、重心、停顿、节奏和幅度一致，不增删、不简化、不自由发挥。唱歌嘴型必须跟随原视频主角的演唱口型、歌词字词、换气、停顿、重音和节奏，口型自然对得上歌词，不滞后、不夸张、不迁移原人物容貌。 表情跟随原视频唱歌情绪：微笑、眼神、眉毛、嘴角、开心、专注等时机和强度一致，自然丰富，不面瘫、不单一。照片人物的脸型、五官、发型、年龄感、身材比例和穿着与照片一致，不继承原主角容貌、身材和服装；身份全片稳定。允许适度自然美颜：皮肤干净、发型整洁、光影柔和，但不改变五官、年龄感和身份，不换脸、不过度美颜。人物与背景光影、透视、遮挡自然融合，无贴图感；成片有舞台级吸引力：主体突出、光影有层次、画面干净高级、节奏有张力，但只做自然融合与轻量画质提升，不重建场景、不替换背景、不堆特效。 特别注意：原主角零残留；身份稳定；声音完整且与原视频一致；嘴型对歌词；动作完整复刻；背景来自原视频；手指正常；无穿模、畸形、闪烁；不拉长身材、不成人化；不静音、不音频缺失、不音画不同步。"}, 
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