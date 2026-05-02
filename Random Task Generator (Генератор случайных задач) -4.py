
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import random
from datetime import datetime

class TaskGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator - Генератор случайных задач")
        self.root.geometry("1200x750")
        self.root.configure(bg='#1a1a2e')
        
        # Предопределённые задачи
        self.tasks = [
            {"name": "Прочитать статью по Python", "type": "учёба"},
            {"name": "Сделать утреннюю зарядку", "type": "спорт"},
            {"name": "Написать отчёт по работе", "type": "работа"},
            {"name": "Выучить 10 новых слов", "type": "учёба"},
            {"name": "Пробежать 3 км", "type": "спорт"},
            {"name": "Провести совещание", "type": "работа"},
            {"name": "Решить задачу", "type": "учёба"},
            {"name": "Сделать растяжку", "type": "спорт"},
            {"name": "Подготовить презентацию", "type": "работа"},
            {"name": "Посмотреть урок", "type": "учёба"},
            {"name": "Отжаться 30 раз", "type": "спорт"},
            {"name": "Созвониться с клиентами", "type": "работа"}
        ]
        
        # История сгенерированных задач
        self.history = []
        self.current_filter = "все"
        self.current_file = "tasks_history.json"
        
        # Загрузка истории
        self.load_history()
        
        # Создание интерфейса с прокруткой
        self.create_widgets()
        self.update_task_list()
        self.update_history_display()
        self.update_statistics()  # Вызываем при старте
    
    def create_widgets(self):
        # Создаем canvas с прокруткой для всего окна
        main_canvas = tk.Canvas(self.root, bg='#1a1a2e', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        scrollable_frame = tk.Frame(main_canvas, bg='#1a1a2e')
        
        scrollable_frame.bind("<Configure>", lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all")))
        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Заголовок
        title_frame = tk.Frame(scrollable_frame, bg='#1a1a2e')
        title_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(title_frame, text="🎲 RANDOM TASK GENERATOR", 
                font=('Arial', 20, 'bold'), fg='#00d4ff', bg='#1a1a2e').pack()
        
        tk.Label(title_frame, text="Генератор случайных задач", 
                font=('Arial', 10), fg='#e0e0e0', bg='#1a1a2e').pack()
        
        tk.Label(title_frame, text="© Сароян Роман Гагикович, 2026 г.", 
                font=('Arial', 9), fg='#f39c12', bg='#1a1a2e').pack(pady=5)
        
        # Основная панель
        main_frame = tk.Frame(scrollable_frame, bg='#1a1a2e')
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Три колонки
        left_panel = tk.Frame(main_frame, bg='#1a1a2e')
        left_panel.pack(side='left', fill='both', expand=True, padx=5)
        
        center_panel = tk.Frame(main_frame, bg='#1a1a2e')
        center_panel.pack(side='left', fill='both', expand=True, padx=5)
        
        right_panel = tk.Frame(main_frame, bg='#1a1a2e')
        right_panel.pack(side='right', fill='both', expand=True, padx=5)
        
        # ===== ЛЕВАЯ ПАНЕЛЬ - ГЕНЕРАЦИЯ =====
        gen_frame = tk.LabelFrame(left_panel, text=" 🎲 ГЕНЕРАЦИЯ ЗАДАЧИ ", 
                                   font=('Arial', 11, 'bold'), 
                                   fg='#00d4ff', bg='#16213e')
        gen_frame.pack(fill='x', pady=5)
        
        generate_btn = tk.Button(gen_frame, text="🔮 СГЕНЕРИРОВАТЬ ЗАДАЧУ", 
                                command=self.generate_task,
                                bg='#00d4ff', fg='#1a1a2e', font=('Arial', 13, 'bold'),
                                padx=15, pady=20, cursor='hand2')
        generate_btn.pack(padx=15, pady=15)
        
        # Результат
        result_frame = tk.Frame(gen_frame, bg='#16213e')
        result_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        tk.Label(result_frame, text="ТЕКУЩАЯ ЗАДАЧА:", 
                font=('Arial', 10, 'bold'), fg='#00d4ff', bg='#16213e').pack()
        
        self.current_task_label = tk.Label(result_frame, text="---", 
                                          font=('Arial', 12, 'bold'), 
                                          fg='#f39c12', bg='#0f3460',
                                          pady=10, relief='ridge')
        self.current_task_label.pack(fill='x', pady=8)
        
        # ===== ЛЕВАЯ ПАНЕЛЬ - УПРАВЛЕНИЕ =====
        tasks_frame = tk.LabelFrame(left_panel, text=" 📋 УПРАВЛЕНИЕ ЗАДАЧАМИ ", 
                                     font=('Arial', 11, 'bold'), 
                                     fg='#00d4ff', bg='#16213e')
        tasks_frame.pack(fill='both', expand=True, pady=5)
        
        # Добавление задачи
        add_frame = tk.Frame(tasks_frame, bg='#16213e')
        add_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(add_frame, text="Новая задача:", font=('Arial', 9), 
                fg='white', bg='#16213e').pack(side='left')
        
        self.new_task_entry = tk.Entry(add_frame, width=20, font=('Arial', 9))
        self.new_task_entry.pack(side='left', padx=5)
        
        self.task_type = ttk.Combobox(add_frame, values=['учёба', 'спорт', 'работа'], 
                                      width=8, font=('Arial', 9))
        self.task_type.set('учёба')
        self.task_type.pack(side='left', padx=5)
        
        tk.Button(add_frame, text="ДОБАВИТЬ", command=self.add_task,
                 bg='#0f3460', fg='white', font=('Arial', 9, 'bold'),
                 cursor='hand2').pack(side='left', padx=5)
        
        # Список задач
        list_frame = tk.Frame(tasks_frame, bg='#16213e')
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        columns = ('name', 'type')
        self.tasks_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=10)
        
        self.tasks_tree.heading('name', text='📝 ЗАДАЧА')
        self.tasks_tree.heading('type', text='🏷️ ТИП')
        
        self.tasks_tree.column('name', width=200)
        self.tasks_tree.column('type', width=80)
        
        scroll_tasks = ttk.Scrollbar(list_frame, orient='vertical', command=self.tasks_tree.yview)
        self.tasks_tree.configure(yscrollcommand=scroll_tasks.set)
        
        self.tasks_tree.pack(side='left', fill='both', expand=True)
        scroll_tasks.pack(side='right', fill='y')
        
        # Кнопка удаления
        tk.Button(tasks_frame, text="🗑️ УДАЛИТЬ ВЫБРАННУЮ ЗАДАЧУ", command=self.delete_task,
                 bg='#e94560', fg='white', font=('Arial', 10, 'bold'),
                 cursor='hand2', pady=5).pack(pady=10)
        
        # ===== ЦЕНТРАЛЬНАЯ ПАНЕЛЬ - ИСТОРИЯ =====
        history_frame = tk.LabelFrame(center_panel, text=" 📜 ИСТОРИЯ ЗАДАЧ ", 
                                       font=('Arial', 11, 'bold'), 
                                       fg='#00d4ff', bg='#16213e')
        history_frame.pack(fill='both', expand=True, pady=5)
        
        # Фильтрация
        filter_frame = tk.Frame(history_frame, bg='#16213e')
        filter_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(filter_frame, text="Фильтр по типу:", font=('Arial', 9), 
                fg='white', bg='#16213e').pack(side='left')
        
        self.filter_type = ttk.Combobox(filter_frame, values=['все', 'учёба', 'спорт', 'работа'], 
                                        width=12, font=('Arial', 9))
        self.filter_type.set('все')
        self.filter_type.pack(side='left', padx=10)
        
        tk.Button(filter_frame, text="🔍 ПРИМЕНИТЬ", command=self.apply_filter,
                 bg='#0f3460', fg='white', font=('Arial', 9, 'bold'),
                 cursor='hand2').pack(side='left', padx=5)
        
        tk.Button(filter_frame, text="🔄 СБРОСИТЬ", command=self.reset_filter,
                 bg='#533483', fg='white', font=('Arial', 9, 'bold'),
                 cursor='hand2').pack(side='left', padx=5)
        
        # Таблица истории
        history_table_frame = tk.Frame(history_frame, bg='#16213e')
        history_table_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        history_columns = ('date', 'task', 'type')
        self.history_tree = ttk.Treeview(history_table_frame, columns=history_columns, 
                                         show='headings', height=12)
        
        self.history_tree.heading('date', text='📅 ДАТА')
        self.history_tree.heading('task', text='📝 ЗАДАЧА')
        self.history_tree.heading('type', text='🏷️ ТИП')
        
        self.history_tree.column('date', width=110)
        self.history_tree.column('task', width=200)
        self.history_tree.column('type', width=80)
        
        scroll_history = ttk.Scrollbar(history_table_frame, orient='vertical', 
                                       command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scroll_history.set)
        
        self.history_tree.pack(side='left', fill='both', expand=True)
        scroll_history.pack(side='right', fill='y')
        
        # ===== ПРАВАЯ ПАНЕЛЬ - СТАТИСТИКА =====
        stats_frame = tk.LabelFrame(right_panel, text=" 📊 СТАТИСТИКА В РЕАЛЬНОМ ВРЕМЕНИ ", 
                                     font=('Arial', 11, 'bold'), 
                                     fg='#00d4ff', bg='#16213e')
        stats_frame.pack(fill='x', pady=5)
        
        self.stats_text = tk.Text(stats_frame, height=16, width=38,
                                  bg='#16213e', fg='#00d4ff',
                                  font=('Consolas', 9), wrap='word',
                                  relief='flat', borderwidth=0)
        self.stats_text.pack(padx=10, pady=10)
        
        # ===== ПРАВАЯ ПАНЕЛЬ - JSON =====
        json_frame = tk.LabelFrame(right_panel, text=" 💾 РАБОТА С JSON ", 
                                    font=('Arial', 11, 'bold'), 
                                    fg='#00d4ff', bg='#16213e')
        json_frame.pack(fill='x', pady=5)
        
        tk.Button(json_frame, text="💾 СОХРАНИТЬ В JSON", command=self.save_json,
                 bg='#0f3460', fg='white', font=('Arial', 11, 'bold'),
                 cursor='hand2', pady=8).pack(fill='x', padx=10, pady=5)
        
        tk.Button(json_frame, text="📂 ЗАГРУЗИТЬ ИЗ JSON", command=self.load_json,
                 bg='#0f3460', fg='white', font=('Arial', 11, 'bold'),
                 cursor='hand2', pady=8).pack(fill='x', padx=10, pady=5)
        
        tk.Button(json_frame, text="🗑️ ОЧИСТИТЬ ИСТОРИЮ", command=self.clear_history,
                 bg='#e94560', fg='white', font=('Arial', 11, 'bold'),
                 cursor='hand2', pady=8).pack(fill='x', padx=10, pady=5)
        
        self.file_info = tk.Label(json_frame, text=f"📄 Файл: {self.current_file}", 
                                  font=('Arial', 8), fg='#95a5a6', bg='#16213e')
        self.file_info.pack(pady=8)
        
        # ===== ИНСТРУКЦИЯ =====
        instr_frame = tk.LabelFrame(scrollable_frame, text=" 📖 ИНСТРУКЦИЯ ", 
                                    font=('Arial', 11, 'bold'), 
                                    fg='#00d4ff', bg='#16213e')
        instr_frame.pack(fill='x', padx=10, pady=10)
        
        instruction_text = """
╔═══════════════════════════════════════════════════════════════════════════════════════════╗
║                                    КАК ПОЛЬЗОВАТЬСЯ                                        ║
╠═══════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                           ║
║  🎲 ГЕНЕРАЦИЯ: Нажмите "СГЕНЕРИРОВАТЬ ЗАДАЧУ" → случайная задача                           ║
║  ➕ ДОБАВИТЬ: Введите задачу → выберите тип → "ДОБАВИТЬ"                                   ║
║  🗑️ УДАЛИТЬ: Выберите задачу → "УДАЛИТЬ ВЫБРАННУЮ ЗАДАЧУ"                                 ║
║  🔍 ФИЛЬТР: Выберите тип → "ПРИМЕНИТЬ" → "СБРОСИТЬ"                                        ║
║  💾 JSON: "СОХРАНИТЬ" / "ЗАГРУЗИТЬ" / "ОЧИСТИТЬ"                                           ║
║  📊 СТАТИСТИКА: Обновляется автоматически при каждом действии                             ║
║                                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════════════════════╝
        """
        
        tk.Label(instr_frame, text=instruction_text, font=('Courier', 9), 
                fg='#00d4ff', bg='#16213e', justify='left').pack(padx=10, pady=10)
    
    def update_statistics(self):
        """Обновление статистики в реальном времени"""
        self.stats_text.config(state='normal')
        self.stats_text.delete('1.0', tk.END)
        
        # Статистика по задачам в списке
        total_tasks = len(self.tasks)
        study_tasks = len([t for t in self.tasks if t['type'] == 'учёба'])
        sport_tasks = len([t for t in self.tasks if t['type'] == 'спорт'])
        work_tasks = len([t for t in self.tasks if t['type'] == 'работа'])
        
        # Статистика по истории генераций
        total_history = len(self.history)
        study_history = len([h for h in self.history if h['type'] == 'учёба'])
        sport_history = len([h for h in self.history if h['type'] == 'спорт'])
        work_history = len([h for h in self.history if h['type'] == 'работа'])
        
        # Проценты для истории
        study_percent = (study_history / total_history * 100) if total_history > 0 else 0
        sport_percent = (sport_history / total_history * 100) if total_history > 0 else 0
        work_percent = (work_history / total_history * 100) if total_history > 0 else 0
        
        # Статистика по дням
        unique_days = len(set([h['date'].split()[0] for h in self.history])) if self.history else 0
        avg_per_day = total_history / unique_days if unique_days > 0 else 0
        
        # Определяем самую популярную категорию
        categories = {"учёба": study_history, "спорт": sport_history, "работа": work_history}
        most_popular = max(categories, key=categories.get) if total_history > 0 else "нет данных"
        most_popular_count = categories.get(most_popular, 0) if total_history > 0 else 0
        
        stats = f"""
╔══════════════════════════════════════════╗
║    📊 СТАТИСТИКА (обновляется)           ║
╠══════════════════════════════════════════╣
║                                          ║
║  📋 СПИСОК ЗАДАЧ:                        ║
║  ──────────────────────────────────────  ║
║     Всего задач:           {total_tasks:>3}                    ║
║     📚 Учёба:              {study_tasks:>3}                    ║
║     🏃 Спорт:              {sport_tasks:>3}                    ║
║     💼 Работа:             {work_tasks:>3}                    ║
║                                          ║
║  📜 ИСТОРИЯ ГЕНЕРАЦИЙ:                   ║
║  ──────────────────────────────────────  ║
║     Всего генераций:       {total_history:>3}                    ║
║     📚 Учёба:              {study_history:>3}    ({study_percent:>5.1f}%)  ║
║     🏃 Спорт:              {sport_history:>3}    ({sport_percent:>5.1f}%)  ║
║     💼 Работа:             {work_history:>3}    ({work_percent:>5.1f}%)  ║
║                                          ║
║  🏆 ЛЮБИМАЯ КАТЕГОРИЯ:                   ║
║  ──────────────────────────────────────  ║
║     {self.get_emoji(most_popular)} {most_popular.capitalize()}: {most_popular_count} раз(а)                 ║
║                                          ║
║  📅 АКТИВНОСТЬ:                          ║
║  ──────────────────────────────────────  ║
║     Дней с задачами:       {unique_days:>3}                    ║
║     В среднем в день:      {avg_per_day:>5.1f}                    ║
║                                          ║
╚══════════════════════════════════════════╝
        """
        
        self.stats_text.insert('1.0', stats)
        self.stats_text.config(state='disabled')
    
    def get_emoji(self, category):
        """Возвращает эмодзи для категории"""
        emojis = {"учёба": "📚", "спорт": "🏃", "работа": "💼", "нет данных": "❓"}
        return emojis.get(category, "📝")
    
    def generate_task(self):
        """Генерация случайной задачи"""
        if not self.tasks:
            messagebox.showerror("Ошибка", "❌ Нет доступных задач! Добавьте хотя бы одну задачу.")
            return
        
        task = random.choice(self.tasks)
        
        type_emoji = {"учёба": "📚", "спорт": "🏃", "работа": "💼"}
        emoji = type_emoji.get(task['type'], "📝")
        
        self.current_task_label.config(text=f"{emoji} {task['name']}")
        
        history_entry = {
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'task': task['name'],
            'type': task['type']
        }
        self.history.insert(0, history_entry)
        
        self.update_history_display()
        self.update_statistics()  # ЖИВАЯ СТАТИСТИКА
        self.save_json()
        
        messagebox.showinfo("Успех", f"✅ Задача сгенерирована!\n\n📝 {task['name']}\n🏷️ Тип: {task['type']}")
    
    def add_task(self):
        """Добавление новой задачи"""
        task_name = self.new_task_entry.get().strip()
        task_type = self.task_type.get()
        
        if not task_name:
            messagebox.showerror("Ошибка", "❌ Введите название задачи!")
            return
        
        for task in self.tasks:
            if task['name'].lower() == task_name.lower():
                messagebox.showerror("Ошибка", f"❌ Задача '{task_name}' уже существует!")
                return
        
        self.tasks.append({"name": task_name, "type": task_type})
        self.update_task_list()
        self.update_statistics()  # ЖИВАЯ СТАТИСТИКА
        self.new_task_entry.delete(0, tk.END)
        
        messagebox.showinfo("Успех", f"✅ Задача добавлена!\n\n📝 {task_name}\n🏷️ Тип: {task_type}")
    
    def delete_task(self):
        """Удаление выбранной задачи"""
        selected = self.tasks_tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "❌ Выберите задачу для удаления!")
            return
        
        item = self.tasks_tree.item(selected[0])
        task_name = item['values'][0]
        
        self.tasks = [t for t in self.tasks if t['name'] != task_name]
        self.update_task_list()
        self.update_statistics()  # ЖИВАЯ СТАТИСТИКА
        
        messagebox.showinfo("Успех", f"✅ Задача удалена:\n\n📝 {task_name}")
    
    def update_task_list(self):
        """Обновление списка задач"""
        for item in self.tasks_tree.get_children():
            self.tasks_tree.delete(item)
        
        for task in self.tasks:
            type_emoji = {"учёба": "📚", "спорт": "🏃", "работа": "💼"}
            emoji = type_emoji.get(task['type'], "📝")
            self.tasks_tree.insert('', 'end', values=(task['name'], f"{emoji} {task['type']}"))
    
    def update_history_display(self):
        """Обновление истории"""
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        if self.current_filter == "все":
            filtered = self.history
        else:
            filtered = [h for h in self.history if h['type'] == self.current_filter]
        
        for record in filtered[:100]:
            type_emoji = {"учёба": "📚", "спорт": "🏃", "работа": "💼"}
            emoji = type_emoji.get(record['type'], "📝")
            self.history_tree.insert('', 'end', values=(
                record['date'],
                record['task'],
                f"{emoji} {record['type']}"
            ))
    
    def apply_filter(self):
        """Применение фильтра"""
        self.current_filter = self.filter_type.get()
        self.update_history_display()
        
        if self.current_filter == "все":
            count = len(self.history)
        else:
            count = len([h for h in self.history if h['type'] == self.current_filter])
        
        messagebox.showinfo("Фильтр", f"🔍 Показано записей: {count}\n🏷️ Тип: {self.current_filter}")
    
    def reset_filter(self):
        """Сброс фильтра"""
        self.current_filter = "все"
        self.filter_type.set("все")
        self.update_history_display()
        messagebox.showinfo("Фильтр", f"🔄 Фильтр сброшен. Всего записей: {len(self.history)}")
    
    def save_json(self):
        """Сохранение истории в JSON"""
        try:
            with open(self.current_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
            self.file_info.config(text=f"📄 Файл: {self.current_file} ✓ Сохранено")
            messagebox.showinfo("Успех", f"✅ История сохранена!\n\n📁 Файл: {self.current_file}\n📊 Записей: {len(self.history)}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"❌ Не удалось сохранить!\n{str(e)}")
    
    def load_json(self):
        """Загрузка истории из JSON"""
        file_path = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Выберите JSON файл для загрузки"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    loaded_data = json.load(f)
                    
                    if isinstance(loaded_data, list):
                        self.history = loaded_data
                        self.current_file = file_path
                        self.current_filter = "все"
                        self.filter_type.set("все")
                        self.update_history_display()
                        self.update_statistics()  # ЖИВАЯ СТАТИСТИКА
                        self.file_info.config(text=f"📄 Файл: {self.current_file}")
                        messagebox.showinfo("Успех", f"✅ Загружено {len(self.history)} записей!\n\n📁 Файл: {file_path}")
                    else:
                        messagebox.showerror("Ошибка", "❌ Неверный формат файла!")
                        
            except json.JSONDecodeError:
                messagebox.showerror("Ошибка", "❌ Файл повреждён или имеет неверный формат JSON!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"❌ Не удалось загрузить файл!\n{str(e)}")
    
    def load_history(self):
        """Загрузка истории при запуске"""
        if os.path.exists(self.current_file):
            try:
                with open(self.current_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            except:
                self.history = []
    
    def clear_history(self):
        """Очистка истории"""
        if messagebox.askyesno("Подтверждение", "🗑️ Очистить всю историю?\n\nЭто действие нельзя отменить!"):
            self.history = []
            self.update_history_display()
            self.update_statistics()  # ЖИВАЯ СТАТИСТИКА
            self.save_json()
            messagebox.showinfo("Успех", "✅ История успешно очищена!")


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskGenerator(root)
    root.mainloop()
