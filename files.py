
import os
from pprint import pprint

import pathlib
from pathlib import Path

def get_recipes_from_file(path):
    data = {}
    with open(path, encoding='utf-8') as file:        
        for lines in file:
            dish = lines.strip()
            counter = int(file.readline())
            data_ingridients = []

            for i in range(counter):
                
                ingredient_name, quantity, measure = file.readline().split('|')
                data_ingridients.append({'ingredient_name': ingredient_name.strip(),'quantity':quantity.strip(), 'measure':measure.strip()})                 
            
            data[dish] = data_ingridients            
            file.readline()

        return data


def get_shop_list_by_dishes(dishes, person_count):

    file_name = 'recipes.txt'
    # path = f'{os.getcwd()}\{file_name}'  #WIN
    path = f'{os.getcwd()}/{file_name}'  #LIN
    recipes = get_recipes_from_file(path)
    
    data_for_cook_dict = {}
    for dish in dishes:
        try:
            data_recipes = recipes[dish]
        except KeyError:
            data_recipes = None

        if data_recipes:
            for data in data_recipes:

                try:
                    ingredients = data_for_cook_dict[data['ingredient_name']]
                    new_quantity = ingredients['quantity'] + (int(data['quantity'])  *  person_count)
                    data_for_cook_dict[data['ingredient_name']] = {'measure': data['measure'], 'quantity': new_quantity}
                except KeyError:
                    data_for_cook_dict[data['ingredient_name']] = {'measure': data['measure'], 'quantity': int(data['quantity'])  *  person_count}
        else:
            print(f"{dish} no in recipe")
    return data_for_cook_dict


#  #2
# cook_book = ['Запеченный картофель','Жаренная картошка']
# cook_dishes = get_shop_list_by_dishes(cook_book,  2)
# pprint(cook_dishes)

#  #3
def get_data_from_files(count):
    path_list = []
    for i in range(1, count + 1):
        # path = {'path':f'{os.getcwd()}\{i}.txt','name':f'{i}.txt'}  #WIN      
        path = {'path': Path(pathlib.Path.cwd(), f'{i}.txt'),'name':f'{i}.txt'} 
        path_list.append(path)

    finish_file =  Path(pathlib.Path.cwd(), 'finish_file.txt')
    with open(finish_file, 'w'): pass

    for file_number, path in enumerate(path_list):
        finish_data = []
        file_number = file_number + 1
        try:

            with open(path['path'], 'r', encoding='utf-8') as file:
                finish_data.append(path['name'])  
                finish_data.append(len(file.readlines()))

        except FileNotFoundError:

            with open(path['path'], 'w', encoding='utf-8') as file:
                file.write('Тут каккой то текст')

            with open(path['path'], 'r', encoding='utf-8') as file:
                finish_data.append(path['name'])  
                finish_data.append(len(file.readlines()))

        with open(path['path'], encoding='utf-8') as file:     

            for str_number, line in enumerate(file): 
                str_number = str_number + 1
                finish_data.append(f'Строка номер {str_number} файла номер {file_number}') 

        with open(finish_file, 'a', encoding='utf-8') as file:

            for data in finish_data:
                file.write(f'{data}\n')

    print(f'finish_file.txt готов!')

files_count = [path for path in Path('.').glob('*.txt') if 'recipes' not in path.stem and 'finish_file' not in path.stem]
files_count = len(files_count)
input_answer = input(f'Хотите создать новые файлы к существующим? Сейчас в директории {files_count} файла. y/n ')
if input_answer == 'y':
    input_files_count = int(input('Введите конечное число файлов: '))
    files_count = input_files_count

get_data_from_files(files_count)