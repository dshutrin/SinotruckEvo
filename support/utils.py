import shutil
from zipfile import ZipFile
import os
from django.conf import settings


def fix_excel(excel_file):

    # Создаем временную папку
    tmp_folder = os.path.join(settings.BASE_DIR, '/media/tmp/convert_wrong_excel/')
    os.makedirs(tmp_folder, exist_ok=True)

    # Распаковываем excel как zip в нашу временную папку
    with ZipFile(excel_file) as excel_container:
        excel_container.extractall(tmp_folder)

    # Переименовываем файл с неверным названием
    wrong_file_path = os.path.join(tmp_folder, 'xl', 'SharedStrings.xml')
    correct_file_path = os.path.join(tmp_folder, 'xl', 'sharedStrings.xml')
    os.rename(wrong_file_path, correct_file_path)

    # Запаковываем excel обратно в zip и переименовываем в исходный файл
    shutil.make_archive('yourfile', 'zip', tmp_folder)
    os.remove(excel_file)
    os.rename('yourfile.zip', excel_file)
