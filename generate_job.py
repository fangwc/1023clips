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


s = "data:image/jpeg;base64,"+img_to_base64('./modeling_db/ChatGPT202611423_55_25.png')
s2 = "data:video/mp4;base64,"+img_to_base64('./video_db/xinjiangwu.mp4')

# print(s2)

def submit_video_job(prompt: str, model: str = "klingai/kling-3.0-omni",
                     resolution: str = "1080p", duration: int = 15) -> str:
    """Step 1: 提交视频生成请求，返回 jobId"""
    url = f"{API_BASE}/videos"
    payload = {
        "model": model,
        # "content": [{"type": "text", "text": prompt}],
        "content": [
        {"type": "text", "text": """
本任务为“以图一的人物和场景为基础，参照视频一完整复刻舞蹈”。图一是唯一的人物身份、身材比例、服装、背景、光线和构图依据；视频一是唯一的舞蹈动作、节奏、时长和原音频依据。让图一中的小女孩在图一的赛里木湖畔场景中真实、自然地跳完视频一的舞蹈。

【人物身份与服装】
严格保持图一中的同一个小女孩：脸型、五官比例、肤色、发型、发饰、年龄感、头身比、肩宽、腰胯比例、腿长比例和整体身材与图一一致，保持儿童自然体态。保持图一中的红色上衣、蝴蝶结肩带、白色层叠裙裤、袜子和黑色鞋子，服装颜色、结构和细节全程稳定。
视频一中的人物仅提供身体动作，不作为容貌、年龄、身高、身材、服装或表情依据。全片不得出现视频一中的人物，不继承其面容和成人身材，不拉长肢体、不瘦身、不增高、不成人化。

【舞蹈动作复刻】
完整迁移视频一中主舞者从开始到结束的舞蹈动作。动作顺序、数量、节拍、手部轨迹、脚步交替、转身方向、身体朝向、重心变化和停顿时机与视频一对应，不遗漏、不重复、不简化、不自行编舞。
按照图一儿童的头身比和四肢长度自然调整动作幅度与步幅，保持原舞蹈的姿态、节奏和神韵，同时符合儿童自然身体结构。保持原速和原时长，不加速、不慢放、不循环，不增加开场等待或结尾动作。
人物从舞蹈起始姿态开始运动，不能为了维持照片中的手脚姿势而限制舞蹈。全身动作连贯，手臂、躯干和脚步协调；抬脚、落脚与身体重心同步，脚底接地可信，不打滑、不悬浮、不穿地。衣物和发丝随动作自然轻微摆动。

【表情管理：重点】
表情自然松弛，以图一小女孩原本的面部状态和神态为主，仅适度跟随动作节奏，不强行复制视频一人物的表情、笑脸或口型。
保持轻松、专注、自然开心的状态，允许自然眨眼、视线随转身变化、嘴角轻微收放，以及动作过程中短暂的认真神态。微笑自然变化，不要求全程露齿，不把照片中的笑容固定在每一帧。
脸部和嘴部自然生动，不僵硬、不咧嘴假笑、不刻意挤眉弄眼、不突然夸张大笑，不生成说话或唱歌口型。转头和侧脸时仍保持同一人物，表情变化不改变五官比例。

【背景与镜头】
全程沿用图一中的赛里木湖畔环境：蓝天、远山、湖水、帆船和前景草地，保持原有空间关系、光线方向和自然色调，不使用视频一的背景。
采用图一的正面全身景别与固定机位，人物初始大小和站位参照图一，允许随舞蹈自然移动。头顶、双手和鞋底始终完整入镜，两侧留出动作空间。镜头不跟随视频一推拉、摇移或切换，不切近景，不裁掉手脚。
人物在草地上自然站立与移动，身体受光、衣服明暗和接地阴影与环境一致，阴影随动作合理变化。背景稳定，湖面可有轻微自然波纹，不扭曲、不漂移、不闪烁。

【真实感】
呈现自然户外摄影质感，保留图一人物的自然肤色、肤质和面部细节，不额外美白、不磨皮、不放大眼睛、不改变脸型。人物与背景的清晰度、色温和光影协调，无贴图感、无轮廓光晕、无塑料皮肤、无过度锐化或美颜滤镜。

【音频与输出】
输出视频时长与视频一完全一致。直接保留视频一完整的原始音轨，包括原背景音乐、原声及已有环境音，保持原音色、音高、速度和时间位置；不重新演唱、不重新生成音乐、不替换、不删减、不添加人声或音效。动作与原音频节拍准确同步。
输出9:16竖屏高清视频，画面干净，不添加字幕、标题、贴纸、转场或水印。

重点保证：人物与场景来自图一，舞蹈动作与原音频来自视频一；动作完整、节奏准确、儿童身份稳定、表情自然松弛、全身清楚可见、户外光影真实。

避免：身份漂移、原视频人物残留、换脸感、五官变化、年龄增大、成人化、身材拉长、服装发型变化、表情僵硬、强行笑脸、过度露齿、口型迁移、嘴部变形、眼神呆滞、动作缺失或乱序、脚底滑动、悬浮、穿地、多余肢体、手指畸形、穿模、背景替换、镜头变化、手脚出画、闪烁、过度美颜、皮肤塑料感、音频缺失、音乐被替换、音画不同步。
        """}, 
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
    result = poll_until_done(job_id, interval=9, timeout=3600)

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