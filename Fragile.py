import hashlib
import time
from datetime import datetime
import platform

if platform.system() == "Windows":
    import winsound
    def alert_sound():
        winsound.Beep(1000, 500)
else:
    def alert_sound():
        print("\a")

list_file = "file_list.txt"
original_hashes = {}

def sha256_sum(file: str) -> str:
    with open(file, "rb") as f:
        h = hashlib.sha256()
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            h.update(chunk)
        hash = h.hexdigest()
    return hash

try:
    with open(list_file, "r", encoding="utf-8") as f:
        for file in f:
            file = file.strip()

            if not file or file.startswith("#"):
                continue

            try:
                    original_hashes[file] = sha256_sum(file)
            except FileNotFoundError:
                print(f"{file} はパスが通っていません！監視対象から除外します。")
                continue
            except PermissionError:
                print(f"{file} で権限がありません！監視対象から除外します。")
                continue
except FileNotFoundError:
    print("監視対象リスト file_list.txt を作成してください！")
except Exception as e:
    print(f"予期せぬエラーが発生しました: {e}")

files_str = ", ".join(original_hashes.keys())
print(f"監視対象: {files_str}")
print("Fragileは正常に起動しました。ファイルの監視を開始します……")

try:
    while True:
        for file in list(original_hashes.keys()):
            try:
                hash = sha256_sum(file)
                if hash != original_hashes[file]:
                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"{now}: 【警告】{file}に改竄を検知しました！")
                    alert_sound()
                    original_hashes[file] = hash

            except FileNotFoundError:
                print(f"{file} は移動・削除されたようです。監視対象から除外します。")
                original_hashes.pop(file, None)
                continue
            except PermissionError:
                print(f"{file} で権限が失われました。監視対象から除外します。")
        time.sleep(1)
except KeyboardInterrupt:
    print("監視が中断されました。Fragileを終了します。")
except Exception as e:
    print(f"予期せぬエラーが発生しました: {e}")