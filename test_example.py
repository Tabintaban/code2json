"""
Тестовый пример для демонстрации работы приложения
"""

from logic import CodeJSONConverter

def test_conversion():
    converter = CodeJSONConverter()
    
    # Тест 1: Преобразование кода в JSON
    sample_code = """def hello_world():
    print("Hello, World!")
    x = 5
    if x > 0:
        print("Positive number")
"""
    
    print("Исходный код:")
    print(sample_code)
    
    json_result = converter.code_to_json(sample_code)
    print("\nРезультат преобразования в JSON:")
    print(json_result)
    
    # Тест 2: Преобразование JSON обратно в код
    code_result = converter.json_to_code(json_result)
    print("\nРезультат преобразования JSON обратно в код:")
    print(code_result)
    
    # Тест 3: Универсальное преобразование
    print("\nТест универсального преобразования:")
    # Преобразуем код в JSON
    converted_to_json = converter.convert_text(sample_code)
    print("Код -> JSON:")
    print(converted_to_json)
    
    # Преобразуем JSON обратно в код
    converted_back_to_code = converter.convert_text(converted_to_json)
    print("\nJSON -> Код:")
    print(converted_back_to_code)

if __name__ == "__main__":
    test_conversion()