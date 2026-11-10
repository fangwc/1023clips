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


p0 = "data:image/jpeg;base64,"+img_to_base64('./modeling_db/model4_yj_red.jpg')
p1 = "data:image/jpeg;base64,"+img_to_base64('./modeling_db/slmh_scene.jpg')
# p2 = "data:image/jpeg;base64,"+img_to_base64('./modeling_db/cake.jpg')
s2 = "data:video/mp4;base64,"+img_to_base64('./video_db/qingpingguoleyuan.mp4')

raw_prompt = """
生成单镜头、9:16竖屏、真实摄影风格的舞蹈视频：图1中的小女孩，在图2的风景场景中，按照视频1的舞蹈动作和节拍跳舞。人物身份与服装来自图1，背景与环境光线来自图2，舞蹈动作与原音频来自视频1。

主角是图1中的同一个小学一年级小女孩。保持她的脸型、五官特征、肤色、发型、发饰和服装，保留自然稚嫩的儿童面部轮廓与年龄感。身体保持一年级儿童自然的头身比、肩宽和四肢长度，体态轻巧，正面、侧面和转身时身份与年龄感始终稳定。参考舞者只提供动作，不影响小女孩的容貌、身材和穿着。

完整参照视频1的动作顺序、关键姿势、手臂轨迹、脚步交替、转身方向、重心变化和停顿节拍，保持原速与原时长。按小女孩的身体比例自然调整步幅、伸臂距离和动作幅度，表现出小朋友认真、轻快地跳舞的感觉。儿童身体结构优先，不为匹配参考舞者的动作位置而拉长四肢。全身运动协调连贯，支撑脚接地稳定，抬脚、落脚与重心转移对应，衣摆和发丝随动作自然摆动。

表情自然松弛，以图1小女孩原本的神态为主，适度随舞蹈节奏变化，不强行复制视频1的表情和笑脸。自然眨眼，视线随身体朝向合理变化，嘴角轻微收放，偶尔露出认真、专注的神态。微笑自然出现和放松，不要求全程露齿，不固定照片中的笑容，不咧嘴假笑。嘴部自然，无说话或唱歌口型。

场景使用图2中的风景，保留主要景物、地形、空间关系和自然色调。小女孩站在前景合理、平整的地面上，周围留有舞蹈空间。人物大小、地面透视与环境协调，受光方向、色温和明暗层次符合图2，脚底有真实接触，投影随身体动作合理变化。背景稳定，水面或草叶等环境元素可轻微自然运动。整体像在现场拍摄的儿童舞蹈视频，保留自然肤质、真实衣料细节和适度清晰度。

固定机位，平视全身镜头，一镜到底。头顶、双手和鞋底始终完整入镜，人物左右留出移动空间。无推拉、摇移、景别切换或额外转场。

音频沿用视频1完整的原始音轨，保持原音乐、原声、音色、速度和时间位置，舞蹈节拍与原音频同步。不重新演唱或替换配乐，无新增台词、旁白、人声和音效。输出时长与视频1一致，画面无字幕、贴纸或水印。

避免：身份漂移、年龄增大、成人身材、长腿化、成熟妆感、参考舞者面容残留、服装变化、僵硬假笑、过度露齿、五官变形、动作遗漏或乱序、肢体畸形、脚底打滑、悬浮穿地、人物贴图感、背景替换或扭曲、镜头变化、手脚出画、过度磨皮、音画不同步。

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
        {"type": "image_url", "role": "reference_image", "image_url":{"url": p1}},
        # {"type": "image_url", "role": "reference_image", "image_url":{"url": p2}},
        {"type": "video_url", "role": "reference_video", "video_url":{"url": s2}}
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