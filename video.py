from pytube import YouTube
import os
import cv2
from datetime import timedelta
import numpy as np

NAME_VIDEO = 'temp/temp.mp4'

def getVideo(name):
    yt = YouTube(name)
    # yt.stream показывает какое видео ты можешь скачать
    # (mp4(720) + audio или только mp4(1080) без звука).
    # Сейчас стоит фильтр по mp4.
    print(yt.streams.filter(file_extension='mp4'))
    stream = yt.streams.get_by_itag(22) #выбираем по тегу, в каком формате будем скачивать.
    stream.download(filename=NAME_VIDEO) #загружаем видео.

def dell_video():
    os.remove(NAME_VIDEO)


# то есть, если видео длительностью 30 секунд, сохраняется 10 кадров в секунду = всего сохраняется 300 кадров
SAVING_FRAMES_PER_SECOND = 1

def format_timedelta(td):
    """Служебная функция для классного форматирования объектов timedelta (например, 00:00:20.05)
    исключая микросекунды и сохраняя миллисекунды"""
    result = str(td)
    try:
        result, ms = result.split(".")
    except ValueError:
        return "-" + result + ".00".replace(":", "-")
    ms = int(ms)
    ms = round(ms / 1e4)
    return f"-{result}.{ms:02}".replace(":", "-")


def get_saving_frames_durations(cap, saving_fps):
    """Функция, которая возвращает список длительностей сохраняемых кадров"""
    s = []
    # получаем длительность клипа, разделив количество кадров на количество кадров в секунду
    clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    # используем np.arange() для выполнения шагов с плавающей запятой
    for i in np.arange(0, clip_duration, 1 / saving_fps):
        s.append(i)
    return s


def create_img():
    video_file = NAME_VIDEO
    filename, _ = os.path.splitext(video_file)
    filename += "-img"
    # создаем папку по названию видео файла
    if not os.path.isdir(filename):
        os.mkdir(filename)
    # читать видео файл
    cap = cv2.VideoCapture(video_file)
    # получить FPS видео
    fps = cap.get(cv2.CAP_PROP_FPS)
    # если наше SAVING_FRAMES_PER_SECOND больше FPS видео, то установливаем минимальное
    saving_frames_per_second = min(fps, SAVING_FRAMES_PER_SECOND)
    # получить список длительностей кадров для сохранения
    saving_frames_durations = get_saving_frames_durations(cap, saving_frames_per_second)
    # начало цикла
    count = 0
    save_count = 0
    while True:
        is_read, frame = cap.read()
        if not is_read:
            # выйти из цикла, если нет фреймов для чтения
            break
        # получаем длительность, разделив текущее количество кадров на FPS
        frame_duration = count / fps
        try:
            # получить самую первоначальную длительность для сохранения
            closest_duration = saving_frames_durations[0]
        except IndexError:
            # список пуст, все кадры сохранены
            break
        if frame_duration >= closest_duration:
            # если ближайшая длительность меньше или равна длительности текущего кадра,
            # сохраняем фрейм
            frame_duration_formatted = format_timedelta(timedelta(seconds=frame_duration))
            saveframe_name = os.path.join(filename, f"frame{frame_duration_formatted}.jpg")
            cv2.imwrite(saveframe_name, frame)
            save_count += 1
            #print(f"{saveframe_name} сохранён")
            # удалить текущую длительность из списка, так как этот кадр уже сохранен
            try:
                saving_frames_durations.pop(0)
            except IndexError:
                pass
        # увеличить счечик кадров count
        count += 1

    print(f"Итого сохранено кадров {save_count}")