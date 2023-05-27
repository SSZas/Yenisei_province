import numpy as np
import cv2
import os
from math import floor

folder_dir = "C:\study\kursach\my_result"
number_name = 12
count_lines = 1
for image in os.listdir(folder_dir + "\\" + "01color"):

    # 01 начальное изображение в серый
    im_color = cv2.imread(folder_dir + "\\" + "01color" + "\\" + image)
    im_grey = cv2.cvtColor(im_color, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(folder_dir + "\\" + "02grey" + "\\" + "grey00" + str(number_name) + ".jpg", im_grey)
    # cv2.imshow("im", im_gray)
    # cv2.waitKey(0)

    # 02 серое изображение в бинарное
    # порог и изображение
    ret, im_binary = cv2.threshold(im_grey, 200, 255, cv2.THRESH_BINARY)
    cv2.imwrite(folder_dir + "\\" + "03binary" + "\\" + "binary00" + str(number_name) + ".jpg", im_binary)

    height, width = im_binary.shape

    # 03 красим черные поля в белый
    # Если в столбце больше черного, чем белого, то перекрашиваем в белый
    start_mask = 0
    length_mask_width = floor(width * 0.001)
    for w in range(0, width, length_mask_width):
        mask = im_binary[0:height, start_mask:(start_mask + length_mask_width)]
        white = np.sum(mask == 255)
        black = np.sum(mask == 0)
        if (black * 5 > white):
            im_binary[0:height, start_mask:(start_mask + length_mask_width)] = 255
        start_mask = start_mask + length_mask_width

    # 04 Если в строке больше черного, чем белого, то перекрашиваем в белый
    start_mask = 0
    length_mask_height = floor(height * 0.001)
    for h in range(0, height, length_mask_height):
        mask = im_binary[start_mask:(start_mask + length_mask_height), 0:width]
        white = np.sum(mask == 255)
        black = np.sum(mask == 0)
        if (black * 4 > white):
            im_binary[start_mask:(start_mask + length_mask_height), 0:width] = 255
        start_mask = start_mask + length_mask_height

    im_white_fields = im_binary
    cv2.imwrite(folder_dir + "\\" + "04white_fields" + "\\" + "white_fields00" + str(number_name) + ".jpg", im_white_fields)

    # 05 Если меньше 600 черных, красим в серый
    start_mask = 0
    length_mask_width = floor(width * 0.001)
    for w in range(0, width, length_mask_width):
        mask = im_white_fields[0:height, start_mask:(start_mask + length_mask_width)]
        black = np.sum(mask == 0)

        if (black < 150):
            im_white_fields[0:height, start_mask:(start_mask + length_mask_width)] = 150
        start_mask = start_mask + length_mask_width

    im_grey_fields_withSpaces = im_white_fields
    cv2.imwrite(folder_dir + "\\" + "05grey_fields_withSpaces" + "\\" +
                "grey_fields_withSpaces00" + str(number_name) + ".jpg", im_grey_fields_withSpaces)

    # 06 закрашиваем промежутки между серыми столбцами
    not_grey_count = 0
    x_not_grey_start = 0

    for w in range(1, width - 1):
        if (im_grey_fields_withSpaces[0, w - 1] == 150 and im_grey_fields_withSpaces[0, w] == 255):
            x_not_grey_start = w
            w2 = w
            while (im_grey_fields_withSpaces[0, w2 + 1] == 255):
                not_grey_count = not_grey_count + 1
                w2 = w2 + 1
            if (not_grey_count + 1 < floor(width * 0.05)):  # меньше 50ти шагов
                im_grey_fields_withSpaces[0:height, x_not_grey_start:x_not_grey_start + not_grey_count + 1] = 150
            not_grey_count = 0
            x_not_grey_start = 0
    im_grey_fields = im_grey_fields_withSpaces
    cv2.imwrite(folder_dir + "\\" + "06grey_fields" + "\\" + "grey_fields00" + str(number_name) + ".jpg", im_grey_fields)

    # 07 закрашиваем в серый поля сверху и снизу
    x_not_grey_start1 = 0
    x_not_grey_end1 = 0
    x_not_grey_start2 = 0
    x_not_grey_end2 = 0
    for w in range(1, width):
        if (im_grey_fields[0, w] == 255 and im_grey_fields[0, w - 1] == 150):
            if (x_not_grey_start1 == 0):
                x_not_grey_start1 = w
            else:
                x_not_grey_start2 = w
        if (im_grey_fields[0, w] == 255 and im_grey_fields[0, w + 1] == 150):
            if (x_not_grey_end1 == 0):
                x_not_grey_end1 = w + 1
            else:
                x_not_grey_end2 = w + 1

    start_mask_height = 0
    length_mask_height = floor(height * 0.1)
    length_mask_width_okno = floor((x_not_grey_end1 - x_not_grey_start1) * 0.5)
    length_mask_width_okno2 = floor((x_not_grey_end2 - x_not_grey_start2) * 0.5)


    for h in range(0, height, length_mask_height):

        mask = im_grey_fields[start_mask_height:(start_mask_height + length_mask_height),
               x_not_grey_start1:x_not_grey_end1]
        white = np.sum(mask == 255)
        black = np.sum(mask == 0)

        mask2 = mask[0:length_mask_height, 0:length_mask_width_okno]
        mask3 = mask[0:length_mask_height, length_mask_width_okno:length_mask_width_okno * 2]
        black2 = np.sum(mask2 == 0)
        black3 = np.sum(mask3 == 0)
        if (white > black * 110 or abs(black2 - black3) > black / 1.75):
            im_grey_fields[start_mask_height:start_mask_height + length_mask_height,
            x_not_grey_start1:x_not_grey_end1] = 150

        ################ вторая станица

        mask = im_grey_fields[start_mask_height:(start_mask_height + length_mask_height),
               x_not_grey_start2:x_not_grey_end2]
        white = np.sum(mask == 255)
        black = np.sum(mask == 0)
        mask2 = mask[0:length_mask_height, 0:length_mask_width_okno2]
        mask3 = mask[0:length_mask_height, length_mask_width_okno2:length_mask_width_okno2 * 2]
        black2 = np.sum(mask2 == 0)
        black3 = np.sum(mask3 == 0)

        if (white > black * 110 or abs(black2 - black3) > black / 1.75):
            im_grey_fields[start_mask_height:start_mask_height + length_mask_height,
            x_not_grey_start2:x_not_grey_end2] = 150

        start_mask_height = start_mask_height + length_mask_height

    # если верх-низ не закрасился, то докрашиваем
    y_not_grey_start1 = 0
    y_not_grey_end1 = 0
    y_not_grey_start2 = 0
    y_not_grey_end2 = 0
    for h in range(1, height - 1):
        if (im_grey_fields[h, x_not_grey_start1] == 255 and im_grey_fields[h - 1, x_not_grey_start1] == 150):
            if (y_not_grey_start1 == 0):
                y_not_grey_start1 = h
        if (im_grey_fields[h, x_not_grey_start1] == 255 and im_grey_fields[h + 1, x_not_grey_start1] == 150):
            if (y_not_grey_end1 == 0):
                y_not_grey_end1 = h + 1
        if (im_grey_fields[h, x_not_grey_start2] == 255 and im_grey_fields[h - 1, x_not_grey_start2] == 150):
            if (y_not_grey_start2 == 0):
                y_not_grey_start2 = h
        if (im_grey_fields[h, x_not_grey_start2] == 255 and im_grey_fields[h + 1, x_not_grey_start2] == 150):
            if (y_not_grey_end2 == 0):
                y_not_grey_end2 = h + 1

    if y_not_grey_start1 == 0 or y_not_grey_start2 == 0:
        not_zero = max(y_not_grey_start1, y_not_grey_start2)
        y_not_grey_start1 = not_zero
        y_not_grey_start2 = not_zero
        im_grey_fields[0:y_not_grey_start1, x_not_grey_start1:x_not_grey_end1] = 150
        im_grey_fields[0:y_not_grey_start2, x_not_grey_start2:x_not_grey_end2] = 150

    im_full_grey_fields = im_grey_fields
    cv2.imwrite(folder_dir + "\\" + "07full_grey_fields" + "\\" +
                "full_grey_fields00" + str(number_name) + ".jpg", im_full_grey_fields)

    # 08 делим на сроки
    # 1 страница
    start_mask_height = y_not_grey_start1
    length_mask_height = floor((y_not_grey_end1 - y_not_grey_start1) * 0.005)
    for h in range(y_not_grey_start1, y_not_grey_end1, length_mask_height):

        mask = im_full_grey_fields[start_mask_height:(start_mask_height + length_mask_height),
               x_not_grey_start1:x_not_grey_end1]
        white = np.sum(mask == 255)
        black = np.sum(mask == 0)
        # print("1 ", white, black)

        if (white > black * 400):
            im_full_grey_fields[start_mask_height:start_mask_height + length_mask_height,
            x_not_grey_start1:x_not_grey_end1] = 150

        start_mask_height = start_mask_height + length_mask_height


    # 2 станица
    start_mask_height = y_not_grey_start1
    length_mask_height = floor((y_not_grey_end2 - y_not_grey_start2) * 0.005)
    for h in range(y_not_grey_start2, y_not_grey_end2, length_mask_height):
        mask = im_full_grey_fields[start_mask_height:(start_mask_height + length_mask_height),
               x_not_grey_start2:x_not_grey_end2]
        white = np.sum(mask == 255)
        black = np.sum(mask == 0)
        # print("2 ", white, black)

        if (white > black * 400):
            im_full_grey_fields[start_mask_height:start_mask_height + length_mask_height,
            x_not_grey_start2:x_not_grey_end2] = 150

        start_mask_height = start_mask_height + length_mask_height

    im_bad_lines = im_full_grey_fields

    # создаем список из начальных и конечных координат всех строк (вместе с лишними)
    list_start_end_1 = []
    list_start_end_2 = []

    for h in range(y_not_grey_start1, y_not_grey_end1):
        if ((abs(im_bad_lines[h, x_not_grey_start1] - 255) < 10 or abs(im_bad_lines[h, x_not_grey_start1]) < 10)
                and abs(im_bad_lines[h - 1, x_not_grey_start1] - 150) < 10):
            if (start_mask_height == 0):
                start_mask_height = h
            list_start_end_1.append(start_mask_height)

        if ((abs(im_bad_lines[h, x_not_grey_start1] - 255) < 10 or abs(im_bad_lines[h, x_not_grey_start1]) < 10)and abs(
                im_bad_lines[h + 1, x_not_grey_start1] - 150) < 10):
            if (end_mask_height == 0):
                end_mask_height = h+1
            list_start_end_1.append(end_mask_height)
        end_mask_height = 0
        start_mask_height = 0

        if ((abs(im_bad_lines[h, x_not_grey_start2] - 255) < 10 or abs(im_bad_lines[h, x_not_grey_start2]) < 10)
             and abs(im_bad_lines[h - 1, x_not_grey_start2] - 150) < 10):
            if (start_mask_height == 0):
                start_mask_height = h
            list_start_end_2.append(start_mask_height)

        if (abs(im_bad_lines[h, x_not_grey_start2] - 255) < 10
                and abs(im_bad_lines[h + 1, x_not_grey_start2] - 150) < 10):
            if (end_mask_height == 0):
                end_mask_height = h+1
            list_start_end_2.append(end_mask_height)
        end_mask_height = 0
        start_mask_height = 0

    # если строк больше, чем 17, то избавляемся от лишних
    remove_list1 = []
    remove_list2 = []
    if (len(list_start_end_1) != 34):
        for line in range(0, int(len(list_start_end_1)), 2):
            if (list_start_end_1[line+1]-list_start_end_1[line]<=length_mask_height*2):
                im_bad_lines[list_start_end_1[line]:list_start_end_1[line+1],
                x_not_grey_start1:x_not_grey_end1] = 150
                remove_list1.append(list_start_end_1[line])
                remove_list1.append(list_start_end_1[line+1])

        for n in remove_list1:
            list_start_end_1.remove(n)
        remove_list1.clear()


        # проходимся по каждой строке вертикальной маской 1/10
        start_mask_width = x_not_grey_start1
        length_mask_width = floor((x_not_grey_end1 - x_not_grey_start1) * 0.1)

        for line in range(0, int(len(list_start_end_1)), 2):
            black = np.sum((im_bad_lines[list_start_end_1[line]:list_start_end_1[line + 1],
                       x_not_grey_start1:x_not_grey_end1]) == 0)
            for w in range(x_not_grey_start1, x_not_grey_end1, length_mask_width):
                mask = im_bad_lines[list_start_end_1[line]:list_start_end_1[line + 1],
                       start_mask_width:start_mask_width + length_mask_width]
                black_mask = np.sum(mask == 0)
                #print(black, black_mask)
                if (black_mask*2 > black):  # !!!!
                    im_bad_lines[list_start_end_1[line]:list_start_end_1[line + 1],
                    x_not_grey_start1:x_not_grey_end1] = 150
                    remove_list1.append(list_start_end_1[line])
                    remove_list1.append(list_start_end_1[line + 1])
                    break

                start_mask_width = start_mask_width + length_mask_width
            start_mask_width = x_not_grey_start1

        for n in remove_list1:
            list_start_end_1.remove(n)
        remove_list1.clear()


    if (len(list_start_end_2) != 34):
        for line in range(0, int(len(list_start_end_2)), 2):
            if (list_start_end_2[line+1]-list_start_end_2[line]<=length_mask_height*2):
                im_bad_lines[list_start_end_2[line]:list_start_end_2[line+1],
                x_not_grey_start2:x_not_grey_end2] = 150
                remove_list2.append(list_start_end_2[line])
                remove_list2.append(list_start_end_2[line + 1])
            # проходимся по каждой строке вертикальной маской 1/10

        for n in remove_list2:
            list_start_end_2.remove(n)
        remove_list2.clear()

        # проходимся по каждой строке вертикальной маской 1/10
        start_mask_width = x_not_grey_start2
        length_mask_width = floor((x_not_grey_end2 - x_not_grey_start2) * 0.1)

        for line in range(0, int(len(list_start_end_2)), 2):
            black = np.sum((im_bad_lines[list_start_end_2[line]:list_start_end_2[line + 1],
                            x_not_grey_start2:x_not_grey_end2]) == 0)
            for w in range(x_not_grey_start2, x_not_grey_end2, length_mask_width):
                mask = im_bad_lines[list_start_end_2[line]:list_start_end_2[line + 1],
                       start_mask_width:start_mask_width + length_mask_width]
                black_mask = np.sum(mask == 0)
                # print(black, black_mask)
                if (black_mask * 2 > black):  # !!!!
                    im_bad_lines[list_start_end_2[line]:list_start_end_2[line + 1],
                    x_not_grey_start2:x_not_grey_end2] = 150
                    remove_list2.append(list_start_end_2[line])
                    remove_list2.append(list_start_end_2[line + 1])
                    break

                start_mask_width = start_mask_width + length_mask_width
            start_mask_width = x_not_grey_start2

        for n in remove_list2:
            list_start_end_2.remove(n)
        remove_list2.clear()

    im_lines = im_bad_lines
    cv2.imwrite(folder_dir + "\\" + "08lines" + "\\" +
                "lines00" + str(number_name) + ".jpg", im_lines)

    # 09 делим на отдельные линии и сохраняем

    for line in range(0, int(len(list_start_end_1)), 2):
        croped = im_lines[list_start_end_1[line]:list_start_end_1[line + 1], x_not_grey_start1:x_not_grey_end1]
        if count_lines < 10:
            cv2.imwrite(folder_dir + "\\" + "09final_lines" + "\\" + "line000" + str(count_lines) + ".tif", croped)
        elif count_lines < 100:
            cv2.imwrite(folder_dir + "\\" + "09final_lines" + "\\" + "line00" + str(count_lines) + ".tif", croped)
        elif count_lines < 1000:
            cv2.imwrite(folder_dir + "\\" + "09final_lines" + "\\" + "line0" + str(count_lines) + ".tif", croped)
        count_lines = count_lines + 1

    for line in range(0, int(len(list_start_end_2)), 2):
        croped = im_lines[list_start_end_2[line]:list_start_end_2[line + 1], x_not_grey_start2:x_not_grey_end2]
        if count_lines < 10:
            cv2.imwrite(folder_dir + "\\" + "09final_lines" + "\\" + "line000" + str(count_lines) + ".tif", croped)
        elif count_lines < 100:
            cv2.imwrite(folder_dir + "\\" + "09final_lines" + "\\" + "line00" + str(count_lines) + ".tif", croped)
        elif count_lines < 1000:
            cv2.imwrite(folder_dir + "\\" + "09final_lines" + "\\" + "line0" + str(count_lines) + ".tif", croped)
        count_lines = count_lines + 1


    number_name = number_name + 1






