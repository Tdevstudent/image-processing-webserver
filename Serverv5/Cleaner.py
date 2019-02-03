import config
import os
import datetime


def remove(filename):

    print("removing " + filename)
    try:
        os.remove(filename)
    except Exception:
        pass


def file_info(folders):
    info = []
    now = datetime.datetime.now()
    for folder in folders:
        for path, dirs, files in os.walk(folder):
            for file in files:
                filename = os.path.join(path, file)
                size = os.path.getsize(filename)
                mtime = os.path.getmtime(filename)
                age = now - datetime.datetime.fromtimestamp(mtime)
                info.append((filename, size, age))
    return info


def clean(folders, size_threshold, age_threshold):
    data = file_info(folders)  # [(filename, size, age)]

    total_size = 0
    for entry in data:
        total_size += os.path.getsize(entry[0])
    print(total_size)

    data = sorted(data, key=lambda data: data[2], reverse=True)

    if age_threshold is not None:
        for filename, size, age in data:
            if age > age_threshold:
                remove(filename)

    if size_threshold is not None:
        for filename, size, age in data:
            if total_size > size_threshold:
                total_size -= size
                remove(filename)
            else:
                break


def run():
    print("beep beep")
    clean([config.input_folder, config.output_folder],
          config.input_size_threshold, config.input_age_threshold)

# TODO: remove log


if __name__ == '__main__':
    run()
