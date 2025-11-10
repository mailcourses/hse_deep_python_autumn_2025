import unittest
import tempfile
import os
from io import StringIO
from file_filter import filter_file


class TestFileFilter(unittest.TestCase):
    
    def setUp(self):
        # Создаем временный файл для тестов
        self.test_content = [
            "а Роза упала на лапу Азора",
            "В лесу родилась елочка",
            "Мама мыла раму",
            "Кот сидит на окне",
            "Собака бежит по дороге",
            "Роза красная роза",
            "Азора нет в этой строке",
            "Кот и собака друзья"
        ]
        
    def test_filter_by_filename(self):
        # Тест с именем файла
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
            f.write('\n'.join(self.test_content))
            temp_filename = f.name
        
        try:
            search_words = ["роза", "кот"]
            stop_words = ["азора"]
            
            result = list(filter_file(temp_filename, search_words, stop_words))
            
            # Ожидаемые строки: "В лесу родилась елочка" (нет), "Мама мыла раму" (нет),
            # "Кот сидит на окне" (есть кот), "Собака бежит по дороге" (нет),
            # "Роза красная роза" (есть роза), "Кот и собака друзья" (есть кот)
            # "а Роза упала на лапу Азора" исключена из-за стоп-слова "азора"
            expected = [
                "Кот сидит на окне",
                "Роза красная роза", 
                "Кот и собака друзья"
            ]
            
            self.assertEqual(result, expected)
            
        finally:
            os.unlink(temp_filename)
    
    def test_filter_by_file_object(self):
        # Тест с файловым объектом
        file_obj = StringIO('\n'.join(self.test_content))
        
        search_words = ["роза", "кот"]
        stop_words = ["азора"]
        
        result = list(filter_file(file_obj, search_words, stop_words))
        
        expected = [
            "Кот сидит на окне",
            "Роза красная роза", 
            "Кот и собака друзья"
        ]
        
        self.assertEqual(result, expected)
    
    def test_case_insensitive_search(self):
        # Тест поиска без учета регистра
        file_obj = StringIO("РОЗА красная КОТ сидит")
        
        search_words = ["роза", "кот"]
        stop_words = []
        
        result = list(filter_file(file_obj, search_words, stop_words))
        
        self.assertEqual(result, ["РОЗА красная КОТ сидит"])
    
    def test_case_insensitive_stop_words(self):
        # Тест стоп-слов без учета регистра
        file_obj = StringIO("а Роза упала на лапу АЗОРА")
        
        search_words = ["роза"]
        stop_words = ["азора"]
        
        result = list(filter_file(file_obj, search_words, stop_words))
        
        self.assertEqual(result, [])
    
    def test_multiple_search_words_in_line(self):
        # Тест строки с несколькими словами поиска (должна вернуться один раз)
        file_obj = StringIO("роза и кот вместе")
        
        search_words = ["роза", "кот"]
        stop_words = []
        
        result = list(filter_file(file_obj, search_words, stop_words))
        
        self.assertEqual(result, ["роза и кот вместе"])
    
    def test_stop_word_priority(self):
        # Тест приоритета стоп-слов над словами поиска
        file_obj = StringIO("роза и азора вместе")
        
        search_words = ["роза"]
        stop_words = ["азора"]
        
        result = list(filter_file(file_obj, search_words, stop_words))
        
        self.assertEqual(result, [])
    
    def test_empty_file(self):
        # Тест пустого файла
        file_obj = StringIO("")
        
        search_words = ["роза"]
        stop_words = []
        
        result = list(filter_file(file_obj, search_words, stop_words))
        
        self.assertEqual(result, [])
    
    def test_no_matches(self):
        # Тест когда нет совпадений
        file_obj = StringIO("собака бежит по дороге")
        
        search_words = ["роза", "кот"]
        stop_words = []
        
        result = list(filter_file(file_obj, search_words, stop_words))
        
        self.assertEqual(result, [])
    
    def test_all_lines_filtered_by_stop_words(self):
        # Тест когда все строки отфильтрованы стоп-словами
        file_obj = StringIO("роза с азора\nкот с азора")
        
        search_words = ["роза", "кот"]
        stop_words = ["азора"]
        
        result = list(filter_file(file_obj, search_words, stop_words))
        
        self.assertEqual(result, [])
    
    def test_exact_word_match(self):
        # Тест точного совпадения слов
        file_obj = StringIO("розан не найден\nрозы не найдены\nроза найдена")
        
        search_words = ["роза"]
        stop_words = []
        
        result = list(filter_file(file_obj, search_words, stop_words))
        
        self.assertEqual(result, ["роза найдена"])
    
    def test_generator_behavior(self):
        # Тест что функция возвращает генератор
        file_obj = StringIO("роза красная")
        
        search_words = ["роза"]
        stop_words = []
        
        result = filter_file(file_obj, search_words, stop_words)
        
        self.assertTrue(hasattr(result, '__iter__'))
        self.assertTrue(hasattr(result, '__next__'))
