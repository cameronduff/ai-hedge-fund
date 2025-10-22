import subprocess, os, platform
from pathlib import Path
from datetime import datetime, timedelta
from loguru import logger


def _duration_from_times(start: str, end: str, video_duration: float) -> str:
    fmt = "%H:%M:%S"
    t1 = datetime.strptime(start, fmt)
    t2 = datetime.strptime(end, fmt)

    # If start == end, add 5 seconds but not beyond video duration
    if t1 == t2:
        proposed_end = t2 + timedelta(seconds=5)
        max_end = datetime.strptime(
            str(timedelta(seconds=int(video_duration))), "%H:%M:%S"
        )
        if proposed_end > max_end:
            proposed_end = max_end
        t2 = proposed_end

    sec = (t2 - t1).total_seconds()
    if sec <= 0:
        raise ValueError(f"Invalid range {start}→{end}")
    return str(sec)


def _get_video_duration(input_path: str) -> float:
    """Return the total duration of the video in seconds."""
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        input_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe failed: {result.stderr}")
    return float(result.stdout.strip())


def clip_video_ffmpeg(
    input_path: str, start_time: str, end_time: str, output_path: str
) -> None:
    if not os.path.isfile(input_path):
        raise FileNotFoundError(input_path)

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    sysname = platform.system().lower()
    hwaccel = []
    video_codec = "libx264"
    preset = "ultrafast"  # x264 speed

    # Prefer HW on Mac / NVIDIA Linux
    if "darwin" in sysname:
        hwaccel = ["-hwaccel", "videotoolbox"]
        video_codec = "h264_videotoolbox"
        preset = None
    elif "linux" in sysname and os.path.exists("/dev/nvidia0"):
        hwaccel = ["-hwaccel", "cuda"]
        video_codec = "h264_nvenc"
        preset = "p4"

    # Get video duration to ensure we don’t go beyond the end
    video_duration = _get_video_duration(input_path)

    duration = _duration_from_times(start_time, end_time, video_duration)

    base = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        *hwaccel,
        "-ss",
        start_time,
        "-i",
        input_path,
        "-t",
        duration,
        "-map",
        "0:v:0",
        "-map",
        "0:a:0?",
        "-sn",
        "-dn",
        "-c:v",
        video_codec,
        "-movflags",
        "+faststart",
        "-avoid_negative_ts",
        "make_zero",
    ]
    if preset:
        base += ["-preset", preset]

    # Try fastest path: copy audio if compatible
    try_cmd = base + ["-c:a", "copy", str(out)]
    proc = subprocess.run(try_cmd, capture_output=True)
    if proc.returncode == 0:
        logger.info("Clip created!")
        return

    # Fallback to re-encoding audio
    fallback_cmd = base + ["-c:a", "aac", "-b:a", "192k", str(out)]
    proc2 = subprocess.run(fallback_cmd, capture_output=True)
    if proc2.returncode != 0:
        raise RuntimeError(proc2.stderr.decode(errors="ignore"))

    logger.info("Clip created!")


# --- Manual Test Example ---
if __name__ == "__main__":
    clip_video_ffmpeg(
        input_path="/path/to/video/source.mp4",
        start_time="00:00:02",
        end_time="00:00:05",
        output_path="/path/to/output/clip.mp4",
    )
