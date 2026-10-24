import os
import sys
import time
import requests

API_BASE = "https://zenmux.ai/api/v1"
API_KEY = sys.argv[1]

if not API_KEY:
    sys.exit("错误: 请先设置环境变量 ZENMUX_API_KEY")

HEADERS = {"Authorization": f"Bearer {API_KEY}"}


def poll_job(job_id: str, interval: int = 5, timeout: int = 600) -> dict:
    """轮询直到 succeeded，返回完整响应；失败或超时抛异常"""
    url = f"{API_BASE}/videos/{job_id}"
    start = time.time()

    while True:
        elapsed = time.time() - start
        if elapsed > timeout:
            raise TimeoutError(f"轮询超时 ({timeout}s)，jobId={job_id}")

        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        status = str(data.get("status", "")).lower()
        print(f"[{elapsed:6.1f}s] 状态: {status}")

        if status == "succeeded":
            return data
        if status in ("failed", "error", "cancelled"):
            raise RuntimeError(f"任务失败: {data}")

        time.sleep(interval)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("用法: python poll_video.py <jobId>")

    job_id = sys.argv[2]
    result = poll_job(job_id, interval=5, timeout=1000)

    video_url = (
        result.get("content", {}).get("video_url")
        or result.get("video_url")
    )
    print(f"[完成] video_url = {video_url}")