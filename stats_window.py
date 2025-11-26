from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QScrollArea, 
                             QWidget, QPushButton, QHBoxLayout)
from PyQt6.QtCore import Qt


class StatsWindow(QDialog):
    def __init__(self, parent=None, data_manager=None):
        super().__init__(parent)
        self.data_manager = data_manager
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("使用统计")
        self.setMinimumWidth(500)
        self.setMinimumHeight(600)
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowStaysOnTopHint)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title_label = QLabel("📊 使用统计")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        layout.addWidget(title_label)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(15)
        
        total_prompts = len(self.data_manager.get_all_prompts())
        total_label = QLabel(f"总 Prompt 数: {total_prompts}")
        total_label.setStyleSheet("font-size: 16px; color: #E5E5E7; padding: 10px;")
        scroll_layout.addWidget(total_label)
        
        category_stats = self.data_manager.get_category_stats()
        if category_stats:
            cat_title = QLabel("分类统计")
            cat_title.setStyleSheet("font-size: 18px; font-weight: bold; color: white; margin-top: 10px;")
            scroll_layout.addWidget(cat_title)
            
            for category, count in sorted(category_stats.items(), key=lambda x: x[1], reverse=True):
                cat_widget = self._create_stat_item(category, count)
                scroll_layout.addWidget(cat_widget)
        
        top_prompts = self.data_manager.get_top_prompts(5)
        if top_prompts:
            top_title = QLabel("最常用 Prompts (Top 5)")
            top_title.setStyleSheet("font-size: 18px; font-weight: bold; color: white; margin-top: 20px;")
            scroll_layout.addWidget(top_title)
            
            for i, prompt in enumerate(top_prompts, 1):
                usage = prompt.get("usage_count", 0)
                name = prompt.get("name", "未命名")
                top_widget = self._create_top_item(i, name, usage)
                scroll_layout.addWidget(top_widget)
        
        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        
        close_btn = QPushButton("关闭")
        close_btn.setStyleSheet(self._get_button_style())
        close_btn.setMinimumHeight(36)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)
        self.setStyleSheet("QDialog { background-color: #1C1C1E; }")
    
    def _create_stat_item(self, category, count):
        widget = QWidget()
        widget.setStyleSheet("""
            QWidget {
                background-color: #2C2C2E;
                border-radius: 8px;
                padding: 12px;
            }
        """)
        
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(12, 12, 12, 12)
        
        name_label = QLabel(category)
        name_label.setStyleSheet("color: white; font-size: 14px;")
        layout.addWidget(name_label)
        
        layout.addStretch()
        
        count_label = QLabel(str(count))
        count_label.setStyleSheet("color: #0A84FF; font-size: 16px; font-weight: bold;")
        layout.addWidget(count_label)
        
        return widget
    
    def _create_top_item(self, rank, name, usage):
        widget = QWidget()
        widget.setStyleSheet("""
            QWidget {
                background-color: #2C2C2E;
                border-radius: 8px;
                padding: 12px;
            }
        """)
        
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(12, 12, 12, 12)
        
        rank_label = QLabel(f"#{rank}")
        rank_label.setStyleSheet("color: #FFD60A; font-size: 16px; font-weight: bold; min-width: 40px;")
        layout.addWidget(rank_label)
        
        name_label = QLabel(name)
        name_label.setStyleSheet("color: white; font-size: 14px;")
        name_label.setWordWrap(True)
        layout.addWidget(name_label, 1)
        
        usage_label = QLabel(f"{usage} 次")
        usage_label.setStyleSheet("color: #0A84FF; font-size: 14px;")
        layout.addWidget(usage_label)
        
        return widget
    
    def _get_button_style(self):
        return """
            QPushButton {
                background-color: #3A3A3C;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #48484A;
            }
            QPushButton:pressed {
                background-color: #2C2C2E;
            }
        """
