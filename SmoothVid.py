import cv2
import numpy as np

def are_frames_similar(frame1, frame2, threshold=3, percentage=0.01):
    """ 比较两帧是否相似 """
    difference = cv2.absdiff(frame1, frame2)
    diff_gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
    non_zero_count = np.count_nonzero(diff_gray > threshold)
    total_pixels = diff_gray.shape[0] * diff_gray.shape[1]
    return (non_zero_count / total_pixels) < percentage

def process_video(input_file, output_file, start_time, end_time):
    cap = cv2.VideoCapture(input_file)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    start_frame = int(start_time * fps)
    end_frame = int(end_time * fps)

    frame_count = 0
    removed_frames = 0

    success, prev_frame = cap.read()
    if not success:
        print("无法读取视频文件的第一帧")
        return

    out.write(prev_frame)
    frame_count = 1

    while True:
        success, curr_frame = cap.read()
        if not success:
            break

        frame_count += 1

        if start_frame <= frame_count <= end_frame:
            # 在指定时间范围内
            if not are_frames_similar(prev_frame, curr_frame):
                out.write(curr_frame)
                print(f"第 {frame_count} 帧不同于前一帧，已写入。")
            else:
                removed_frames += 1
        else:
            # 在指定时间范围外，照常写入
            print(f"第 {frame_count} 帧不在检测时段，已写入。")
            out.write(curr_frame)

        prev_frame = curr_frame  # 更新前一帧

    cap.release()
    out.release()
    print(f"视频处理完成。总帧数: {frame_count}, 删除的帧数: {removed_frames}")

input_video = 'input.mp4'
output_video = 'output.mp4'
start_time = 0  # 开始时间（秒）
end_time = 10    # 结束时间（秒）
process_video(input_video, output_video, start_time, end_time)
