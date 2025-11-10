import unittest
from unittest import mock
from predict_mood import predict_message_mood, SomeModel


class TestPredictMessageMood(unittest.TestCase):
    
    def test_default_thresholds(self):
        assert predict_message_mood("Чапаев и пустота") == "отл"
        assert predict_message_mood("Вулкан") == "неуд"
        
    def test_custom_thresholds(self):
        assert predict_message_mood("Чапаев и пустота", 0.8, 0.99) == "норм"
        
    def test_normal_case(self):
        result = predict_message_mood("Обычное сообщение")
        self.assertEqual(result, "норм")
        
    def test_bad_threshold_boundary(self):
        result = predict_message_mood("Вулкан", 0.2, 0.8)
        self.assertEqual(result, "норм")
        
    def test_good_threshold_boundary(self):
        result = predict_message_mood("Чапаев и пустота", 0.3, 0.9)
        self.assertEqual(result, "норм")
        
    def test_model_integration(self):
        with mock.patch('predict_mood.SomeModel') as mock_model_class:
            mock_model = mock_model_class.return_value
            mock_model.predict.return_value = 0.5
            
            result = predict_message_mood("Тестовое сообщение")
            
            mock_model_class.assert_called_once()
            mock_model.predict.assert_called_once_with("Тестовое сообщение")
            self.assertEqual(result, "норм")
            
    def test_model_predict_called_with_message(self):
        with mock.patch('predict_mood.SomeModel') as mock_model_class:
            mock_model = mock_model_class.return_value
            mock_model.predict.return_value = 0.1
            
            predict_message_mood("Тестовое сообщение", 0.2, 0.8)
            
            mock_model.predict.assert_called_once_with("Тестовое сообщение")
