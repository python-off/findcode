import time
import find
import video


if __name__ == '__main__':
    start_time = time.time()

    print('начинаем скачивание')
    #video.getVideo('https://www.youtube.com/watch?v=rYrIgFqCOb4')
    video.getVideo('https://www.youtube.com/watch?v=wGU6usfAyPI')
    print("видео скачено")

    print('разбиваем на картинки')
    video.create_img()
    print("поиск по картинкам")
    find.Go()
    print("удаляем видео")
    video.dell_video()
    print("удаляем картинки")
    find.del_image()

    print("--- %s seconds ---" % (time.time() - start_time))
