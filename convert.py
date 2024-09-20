import subprocess
import os
import glob


# 使用例
input_directory = 'raw'   # 元のh264ファイルが入っているディレクトリ
output_directory = 'converted'  # 変換後のファイルを保存するディレクトリ

# h264ファイルをMP4に変換する関数
def convert_h264_to_mp4(input_file, output_file):
    command = ['ffmpeg', '-i', input_file, '-c:v', 'copy', output_file]
    subprocess.run(command)

# raw_movieディレクトリのすべてのファイルを変換
def convert_all_h264_in_directory(input_dir, output_dir):
    # 出力ディレクトリが存在しない場合は作成
    os.makedirs(output_dir, exist_ok=True)

    # .h264ファイルを全て取得
    raw_files = glob.glob(os.path.join(input_dir, '*.h264'))

    for file in raw_files:
        # ファイル名だけを取得し、拡張子を.mp4に変更
        file_name = os.path.splitext(os.path.basename(file))[0]
        output_file = os.path.join(output_dir, f"{file_name}.mp4")

        # 変換を実行
        print(f"Converting {file} to {output_file}...")
        convert_h264_to_mp4(file, output_file)


def main():
    convert_all_h264_in_directory(input_directory, output_directory)

if __name__ == '__main__':
    main()

