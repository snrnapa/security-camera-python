import cv2
import os
import glob

# 動画ファイルの読み込み
video_dir = "converted"
output_dir = "capture"

frame_skip = 20  

os.makedirs(output_dir, exist_ok=True)


video_files = glob.glob(os.path.join(video_dir, "*.mp4"))

frame_count = 0
saved_image_count = 0
for video_path in video_files:
    cap = cv2.VideoCapture(video_path)

    # 背景差分を使った動きの検出
    fgbg = cv2.createBackgroundSubtractorMOG2()


    while cap.isOpened():
        if not cap.isOpened():
            print(f"Error: Could not open video {video_path}")
            continue
        
        ret, frame = cap.read()
        
        if not ret:
            break


        frame_count += 1
    # 指定したフレーム間隔でのみ処理を行う
        if frame_count % frame_skip != 0:
            continue

        # 背景差分法で動きを検出
        fgmask = fgbg.apply(frame)

        # 特定のエリア（宅配ボックス周辺）にROIを設定する (例: 左上が (x, y), 幅w, 高さh)
        x, y, w, h = 700, 300, 400, 400  # 例: 宅配ボックスの位置に合わせて調整
        roi = fgmask[y:y+h, x:x+w]
        
        # フレームにROIの矩形を描画する
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # 緑色で矩形を描画

        # 動きが一定以上あった場合にフレームを保存
        if cv2.countNonZero(roi) > 20000:  # しきい値を調整
            saved_image_path = os.path.join(output_dir, f"frame_{frame_count}.jpg")
            cv2.imwrite(saved_image_path, frame)
            saved_image_count += 1

        # 描画されたフレームを表示
        cv2.imshow('Frame with ROI', frame)

        # if cv2.waitKey(30) & 0xFF == ord('q'):
        #     break

    cap.release()
    cv2.destroyAllWindows()

    print(f"Saved {saved_image_count} images with detected motion.")
