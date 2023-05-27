# Создание датасета для решения задачи распознавания отчетов Енисейской губернии

Программа реализована в рамках выполнения курсового проекта

В папке "01color" находятся первоначальные изображения, которые будут подвергаться обработке

## В чем суть?

На вход программы поступают отсканированные изображения отчетов Енисейской губернии ->
на выходе получаются изображения, "нарезанные" на сроки, котрые в дальнейшем используются для дообучения нейронной сети.

## final_program.py

Программа поочередно сохраняет изображения на каждом этапе выполнения программы (для наглядного представления)

*папки:
01color -> 02grey -> 03binary -> 04white_fields -> 05grey_fields_withSpaces -> 06grey_fields -> 07full_grey_fields -> 08lines -> 09final_lines

## without_interim_results.py

Прогрмма не сохраняет промежуточные этапы, а сразу записывает "нарезанные" на сроки в финальную папку

*папки:
01color -> final_lines
