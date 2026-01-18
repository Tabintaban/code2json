import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext, Menu
from logic import CodeJSONConverter

class AppGUI:
    """
    Графический интерфейс для приложения преобразования кода в JSON и обратно
    """
    
    def __init__(self, root):
        self.root = root
        self.converter = CodeJSONConverter()
        self.setup_ui()
    
    def setup_ui(self):
        """
        Настройка пользовательского интерфейса
        """
        self.root.title("Конвертер кода в JSON")
        self.root.geometry("1200x700")
        
        # Создаем главный фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Настройка веса для растягивания
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # Левый фрейм для ввода
        left_frame = ttk.LabelFrame(main_frame, text="Входные данные", padding="5")
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(0, weight=1)
        
        # Текстовое поле для ввода
        self.input_text = scrolledtext.ScrolledText(left_frame, wrap=tk.WORD, state='normal')
        self.input_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Правый фрейм для вывода
        right_frame = ttk.LabelFrame(main_frame, text="Результат", padding="5")
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)
        
        # Текстовое поле для вывода
        self.output_text = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, state='normal')
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Создаем контекстные меню
        self.create_context_menu(self.input_text)
        self.create_context_menu(self.output_text)
        
        # Добавляем обработчики событий для отладки
        self.input_text.bind("<KeyPress>", self.on_input_keypress)
        self.input_text.bind("<Button-1>", self.on_input_click)
        self.input_text.bind("<Button-3>", lambda event: self.show_context_menu(event, self.input_text))
        
        self.output_text.bind("<KeyPress>", self.on_output_keypress)
        self.output_text.bind("<Button-1>", self.on_output_click)
        self.output_text.bind("<Button-3>", lambda event: self.show_context_menu(event, self.output_text))
        
        # Фрейм для кнопок
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0), sticky=(tk.W, tk.E))
        button_frame.columnconfigure(0, weight=1)
        
        # Кнопки управления
        ttk.Button(button_frame, text="Преобразовать", command=self.convert).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Сохранить результат", command=self.save_result).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Загрузить файл", command=self.load_file).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Сохранить вход", command=self.save_input).grid(row=0, column=3, padx=5)
        ttk.Button(button_frame, text="Копировать вправо", command=self.copy_left_to_right).grid(row=0, column=4, padx=5)
        ttk.Button(button_frame, text="Копировать влево", command=self.copy_right_to_left).grid(row=0, column=5, padx=5)
    
    def convert(self):
        """
        Преобразование текста из левого поля в правое
        """
        input_text = self.input_text.get(1.0, tk.END).strip()
        result = self.converter.convert_text(input_text)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(1.0, result)
    
    def save_result(self):
        """
        Сохранение результата в файл
        """
        result_text = self.output_text.get(1.0, tk.END).strip()
        if not result_text:
            messagebox.showwarning("Предупреждение", "Нет данных для сохранения!")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(result_text)
                messagebox.showinfo("Успех", "Файл успешно сохранен!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при сохранении файла: {str(e)}")
    
    def save_input(self):
        """
        Сохранение входного текста в файл
        """
        input_text = self.input_text.get(1.0, tk.END).strip()
        if not input_text:
            messagebox.showwarning("Предупреждение", "Нет данных для сохранения!")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("Python files", "*.py"), ("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(input_text)
                messagebox.showinfo("Успех", "Файл успешно сохранен!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при сохранении файла: {str(e)}")
    
    def load_file(self):
        """
        Загрузка текста из файла
        """
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Text files", "*.txt"),
                ("Python files", "*.py"),
                ("JSON files", "*.json"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                self.input_text.delete(1.0, tk.END)
                self.input_text.insert(1.0, content)
                
                # Автоматически преобразуем после загрузки
                self.convert()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при чтении файла: {str(e)}")
    
    def copy_left_to_right(self):
        """
        Копирование текста из левого поля в правое
        """
        input_text = self.input_text.get(1.0, tk.END)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(1.0, input_text)
    
    def copy_right_to_left(self):
        """
        Копирование текста из правого поля в левое
        """
        output_text = self.output_text.get(1.0, tk.END)
        self.input_text.delete(1.0, tk.END)
        self.input_text.insert(1.0, output_text)
    
    def on_input_keypress(self, event):
        """Обработчик нажатия клавиш в левом поле"""
        # Проверяем, что поле доступно для редактирования
        if self.input_text.cget('state') != 'normal':
            print(f"DEBUG: Состояние левого поля изменилось на {self.input_text.cget('state')}")
            self.input_text.config(state='normal')
    
    def on_input_click(self, event):
        """Обработчик клика в левом поле"""
        # Проверяем, что поле доступно для редактирования
        if self.input_text.cget('state') != 'normal':
            print(f"DEBUG: Состояние левого поля изменилось на {self.input_text.cget('state')}")
            self.input_text.config(state='normal')
    
    def on_output_keypress(self, event):
        """Обработчик нажатия клавиш в правом поле"""
        # Проверяем, что поле доступно для редактирования
        if self.output_text.cget('state') != 'normal':
            print(f"DEBUG: Состояние правого поля изменилось на {self.output_text.cget('state')}")
            self.output_text.config(state='normal')
    
    def on_output_click(self, event):
        """Обработчик клика в правом поле"""
        # Проверяем, что поле доступно для редактирования
        if self.output_text.cget('state') != 'normal':
            print(f"DEBUG: Состояние правого поля изменилось на {self.output_text.cget('state')}")
            self.output_text.config(state='normal')
    
    def create_context_menu(self, text_widget):
        """
        Создает контекстное меню для текстового поля
        """
        context_menu = Menu(text_widget, tearoff=0)
        context_menu.add_command(label="Вырезать", command=lambda: self.cut_text(text_widget))
        context_menu.add_command(label="Копировать", command=lambda: self.copy_text(text_widget))
        context_menu.add_command(label="Вставить", command=lambda: self.paste_text(text_widget))
        context_menu.add_separator()
        context_menu.add_command(label="Очистить", command=lambda: self.clear_text(text_widget))
        
        text_widget.context_menu = context_menu
    
    def show_context_menu(self, event, text_widget):
        """
        Отображает контекстное меню при клике правой кнопкой мыши
        """
        try:
            text_widget.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            text_widget.context_menu.grab_release()
    
    def cut_text(self, text_widget):
        """
        Вырезает выделенный текст
        """
        try:
            text_widget.event_generate("<<Cut>>")
        except tk.TclError:
            # Игнорировать ошибку, если нет выделенного текста
            pass
    
    def copy_text(self, text_widget):
        """
        Копирует выделенный текст
        """
        try:
            text_widget.event_generate("<<Copy>>")
        except tk.TclError:
            # Игнорировать ошибку, если нет выделенного текста
            pass
    
    def paste_text(self, text_widget):
        """
        Вставляет текст из буфера обмена
        """
        try:
            text_widget.event_generate("<<Paste>>")
        except tk.TclError:
            # Игнорировать ошибку, если буфер обмена пуст
            pass
    
    def clear_text(self, text_widget):
        """
        Очищает текстовое поле
        """
        text_widget.delete(1.0, tk.END)

def main():
    root = tk.Tk()
    app = AppGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()