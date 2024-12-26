import subprocess
import os
import glob


# 使用例
INPUT_DIRECTORY = "raw"  # 元のh264ファイルが入っているディレクトリ
OUTPUT_DIRECTORY = "converted"  # 変換後のファイルを保存するディレクトリ
START_TEMPLATE = "{format}ファイルが{file_count}件見つかりました。変換を開始します。"


def convert_avi_to_mp4(input_file, output_file):
    command = [
        "ffmpeg",
        "-y",  # 自動的に上書き
        "-i",
        input_file,
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-loglevel",
        "error",
        output_file,
    ]
    subprocess.run(command)


# h264ファイルをMP4に変換する関数
def convert_h264_to_mp4(input_file, output_file):
    command = [
        "ffmpeg",
        "-y",  # 自動的に上書き
        "-i",
        input_file,
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-loglevel",
        "error",
        output_file,
    ]
    subprocess.run(command)


# raw_movieディレクトリのすべてのファイルを変換
def check_target_files(ext_type: str, raw_files: list):

    for file in raw_files:
        # ファイル名だけを取得し、拡張子を.mp4に変更
        file_name = os.path.splitext(os.path.basename(file))[0]
        output_file = os.path.join(OUTPUT_DIRECTORY, f"{file_name}.mp4")

        # 変換を実行
        print(f"Converting {file} to {output_file}...")
        if ext_type == "h264":
            convert_h264_to_mp4(file, output_file=output_file)
        elif ext_type == "avi":
            convert_avi_to_mp4(file, output_file=output_file)
        convert_h264_to_mp4(file, output_file)


def main():
    raw_files = [
        os.path.join(INPUT_DIRECTORY, file)
        for file in os.listdir(os.path.join(INPUT_DIRECTORY))
    ]
    print("最初の取得したリスト", raw_files)
    h264_files_list = [file for file in raw_files if file.endswith(".h264")]
    avi_files_list = [file for file in raw_files if file.endswith(".avi")]

    if len(h264_files_list) > 0:
        print(START_TEMPLATE.format(format="h264", file_count=len(h264_files_list)))
        print(h264_files_list)
        check_target_files(ext_type="h264", raw_files=h264_files_list)

    if len(avi_files_list) > 0:
        print(START_TEMPLATE.format(format="avi", file_count=len(avi_files_list)))
        check_target_files(ext_type="avi", raw_files=avi_files_list)


if __name__ == "__main__":
    main()
