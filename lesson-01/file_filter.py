from typing import Union, List, Iterator, TextIO


def filter_file(
    file_input: Union[str, TextIO],
    search_words: List[str],
    stop_words: List[str]
) -> Iterator[str]:
    """
    Генератор для чтения и фильтрации файла.
    
    Args:
        file_input: Имя файла или файловый объект
        search_words: Список слов для поиска
        stop_words: Список стоп-слов
    
    Yields:
        str: Строки файла, содержащие хотя бы одно слово из search_words
              и не содержащие стоп-слов
    """
    # Определяем, нужно ли закрывать файл
    should_close = isinstance(file_input, str)
    
    if should_close:
        file_obj = open(file_input, 'r', encoding='utf-8')
    else:
        file_obj = file_input
    
    try:
        for line in file_obj:
            line = line.strip()
            if not line:
                continue
                
            # Разбиваем строку на слова (без учета регистра)
            words_in_line = [word.lower() for word in line.split()]
            
            # Проверяем наличие стоп-слов
            has_stop_words = any(
                stop_word.lower() in words_in_line 
                for stop_word in stop_words
            )
            
            if has_stop_words:
                continue
            
            # Проверяем наличие слов для поиска
            has_search_words = any(
                search_word.lower() in words_in_line 
                for search_word in search_words
            )
            
            if has_search_words:
                yield line
                
    finally:
        if should_close:
            file_obj.close()
