import os
import shutil

fail_list, success_list = [], []

def create_file(path, file_name):
    try:
        os.chdir(path)
        file_list = os.listdir(path)

        with open("file", "a", encoding="utf-8") as f:
            for i in range(len(file_list)):
                suffix = str(i).rjust(10,'0') + ".ts"
                full_path = "file " + os.path.join(path, suffix) + "\n"

                f.write(full_path)

        res = os.system(f"ffmpeg -f concat -safe 0 -i file -c copy {file_name}.mp4")
        if res == 0:
            des = "/Users/jackie/Desktop/ThirdParty/Download_91Porn/deal"
            src = os.path.join(path, file_name) + ".mp4"
            move = shutil.move(src, des)
            if move:
                for file in file_list:
                    if ".ts" in file or file == "file":
                        os.remove(os.path.join(path, file))

            success_list.append(file_name)
            print(f"============= {file_name} success =============")
        else:
            fail_list.append(file_name)
            print(f"============= {file_name} fail =============")
    except IOError as e:
        fail_list.append(file_name)
        print("download error: ", e)
    except Exception as e:
        fail_list.append(file_name)
        print("convert error: ", e)

    print(f"\nsuccess list: {len(success_list)} ", success_list)
    print(f"fail list: {len(fail_list)} ", fail_list)

# file_name = "调教小骚货的意外惊喜"
# path = "/Users/jackie/Desktop/ThirdParty/Download_91Porn/video/" + file_name
# create_file(path, file_name)