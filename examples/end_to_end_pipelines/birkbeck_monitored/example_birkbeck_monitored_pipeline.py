from pathlib import Path

from examples.end_to_end_pipelines.common.pipeline_lib import run_monitored

result = run_monitored(video_seconds=6, log_path=Path(__file__).with_name("log.md"))
print("run_id:", result["run_id"])
print("still:", result["still_path"])
print("video:", result["video_path"])
print(f"total: {result['total_seconds']:.2f}s")
print("log:", result["log_path"])
