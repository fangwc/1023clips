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
本任务为“以图一中的小女孩和赛里木湖畔场景为基础，参照视频一完整复刻舞蹈”。图一提供人物身份、发型、服装和场景，视频一提供舞蹈动作、节拍、时长和原音频。

【最高优先级：保持小学一年级儿童的样子】
主角是一名小学一年级的小女孩。全片必须保持这一年龄阶段自然、稚嫩的脸部特征、身体比例和神态，不得在运动、转身或表情变化时逐渐变成高年级学生、青少年或成年人。
保留图一人物可辨认的五官特征、发型和发饰，同时保持自然柔和的儿童面部轮廓、饱满的脸颊、稚气的眉眼和下巴，不削尖下巴、不强化鼻梁、不塑造成熟立体妆容，不放大眼睛或做成卡通娃娃脸。
保持儿童自然头身比、较窄的肩部、自然的躯干和四肢长度，体态轻巧，不套用成人舞者的骨架和身材。若图一存在生成造成的腿部偏长或比例偏成熟，以小学一年级儿童的自然比例为准做轻微校正，保留人物身份，不换成另一个孩子。

【人物与服装】
始终是图一中的同一个小女孩，肤色、发型、发饰和人物特征全程稳定。保留图一中的红色上衣、蝴蝶结肩带、白色层叠裙裤、袜子和黑色鞋子，服装颜色与结构稳定，穿着符合儿童体态。
视频一中的人物仅作为身体动作参考，不作为容貌、年龄、身高、身材、服装或表情依据。全片不出现原舞者，不继承其面容和成熟气质。

【舞蹈动作】
完整迁移视频一主舞者的动作顺序、脚步交替、手部轨迹、转身方向、身体朝向、重心变化、停顿与节拍。保持原速和原时长，不遗漏、不重复、不自行编舞，不增加开场等待或结尾动作。
动作必须按照小女孩的四肢长度和身体比例自然适配：步幅、抬腿高度、伸臂距离和身体倾斜幅度适合小学一年级儿童。保留舞蹈的关键动作与节奏，不为了追求与成人姿势完全重合而拉长四肢、扩大肩部或改变骨架。
整体呈现小朋友认真、轻快地学跳舞的感觉，动作自然有弹性。手臂、躯干和脚步协调，落脚与重心同步，脚底接地可信，不滑步、不悬浮、不穿地。衣物和发丝随动作自然摆动。

【表情与神态】
表情自然松弛，以图一小女孩本身的神态为主，仅适度跟随动作节奏，不复制视频一人物的笑脸、口型或成熟表演神态。
呈现孩子跳舞时的轻松、开心和专注，允许自然眨眼、嘴角轻微收放和短暂认真看动作的表情。微笑自然变化，不全程露齿、不固定笑容、不咧嘴假笑，不刻意挑眉、抿嘴或摆出成熟表情。
嘴部自然放松，不生成说话或唱歌口型。侧脸、转头和运动过程中都保持儿童面部特征与同一人物身份。

【场景与镜头】
全程使用图一的赛里木湖畔场景，保持蓝天、远山、湖水、帆船和草地的空间关系、光线方向与自然色调，不使用视频一的背景。
固定机位、正面全身景别，人物从头顶到鞋底完整入镜，左右留出舞蹈空间。镜头不推拉、不摇移、不切近景，不裁掉手脚。
人物受光、衣服明暗、地面透视与接地阴影和环境一致，阴影随动作合理变化。背景稳定，湖水可有轻微自然波纹。

【真实感与音频】
保留自然儿童肤质和面部细节，不额外美白、磨皮、瘦脸或加妆，不产生塑料皮肤和美颜滤镜感。人物与背景的清晰度、色温和光影协调。
输出9:16竖屏高清视频，时长与视频一一致。完整保留视频一原始音轨，保持原音色、音高、速度和时间位置，不重新生成音乐、不改唱、不替换、不删减、不新增人声，舞蹈动作与原音频节拍同步。
不添加字幕、标题、贴纸、转场或水印。

优先顺序：小学一年级儿童的年龄感与身份稳定，其次是自然身体结构，再是动作姿态的匹配精度。动作可以按儿童体型调整幅度，但节拍、顺序和关键姿势保持对应。

避免：年龄增大、青少年化、成人骨架、模特身材、长腿化、瘦脸尖下巴、成熟妆感、成熟表演神态、身份漂移、原舞者面容残留、服装发型变化、僵硬假笑、过度露齿、五官变形、动作乱序、肢体拉伸、手脚畸形、脚底打滑、悬浮穿地、背景替换、镜头变化、闪烁、过度美颜、音频被替换、音画不同步。
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
        duration=15, # 长度
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