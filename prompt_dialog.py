from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QTextEdit, QPushButton, QComboBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class PromptDialog(QDialog):
    def __init__(self, parent=None, prompt=None, categories=None, ai_analyzer=None):
        super().__init__(parent)
        self.prompt = prompt
        self.categories = categories or []
        self.ai_analyzer = ai_analyzer
        self.init_ui()
        
        if prompt:
            self.load_prompt(prompt)
    
    def init_ui(self):
        self.setWindowTitle("添加 Prompt" if not self.prompt else "编辑 Prompt")
        self.setModal(True)
        self.setMinimumWidth(500)
        self.setMinimumHeight(500)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title_label = QLabel("添加新 Prompt" if not self.prompt else "编辑 Prompt")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        layout.addWidget(title_label)
        
        name_label = QLabel("名称:")
        name_label.setStyleSheet("color: #E5E5E7; font-size: 13px;")
        layout.addWidget(name_label)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("输入 Prompt 名称")
        self.name_input.setStyleSheet(self._get_input_style())
        layout.addWidget(self.name_input)
        
        category_label = QLabel("分类:")
        category_label.setStyleSheet("color: #E5E5E7; font-size: 13px;")
        layout.addWidget(category_label)
        
        self.category_input = QComboBox()
        self.category_input.setEditable(True)
        self.category_input.addItem("")
        for cat in self.categories:
            self.category_input.addItem(cat)
        self.category_input.setStyleSheet(self._get_combo_style())
        layout.addWidget(self.category_input)
        
        tags_label = QLabel("标签 (用逗号分隔):")
        tags_label.setStyleSheet("color: #E5E5E7; font-size: 13px;")
        layout.addWidget(tags_label)
        
        self.tags_input = QLineEdit()
        self.tags_input.setPlaceholderText("例如: Python, 编程, AI")
        self.tags_input.setStyleSheet(self._get_input_style())
        layout.addWidget(self.tags_input)
        
        content_label_layout = QHBoxLayout()
        content_label = QLabel("内容:")
        content_label.setStyleSheet("color: #E5E5E7; font-size: 13px;")
        content_label_layout.addWidget(content_label)
        
        # AI 分析按钮
        if self.ai_analyzer and self.ai_analyzer.api_key:
            ai_btn = QPushButton("✨ AI 智能分析")
            ai_btn.setStyleSheet(self._get_button_style("#FF9500"))
            ai_btn.setMinimumHeight(28)
            ai_btn.setMaximumWidth(120)
            ai_btn.clicked.connect(self.analyze_with_ai)
            ai_btn.setToolTip("使用 AI 自动分析内容并生成名称、分类、标签")
            content_label_layout.addWidget(ai_btn)
        
        content_label_layout.addStretch()
        layout.addLayout(content_label_layout)
        
        self.content_input = QTextEdit()
        self.content_input.setPlaceholderText("输入 Prompt 内容...")
        self.content_input.setStyleSheet(self._get_text_edit_style())
        self.content_input.setMinimumHeight(200)
        layout.addWidget(self.content_input)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_btn = QPushButton("取消")
        cancel_btn.setStyleSheet(self._get_button_style("#3A3A3C"))
        cancel_btn.setMinimumWidth(100)
        cancel_btn.setMinimumHeight(36)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("保存")
        save_btn.setStyleSheet(self._get_button_style("#FF9500"))
        save_btn.setMinimumWidth(100)
        save_btn.setMinimumHeight(36)
        save_btn.clicked.connect(self.accept)
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        self.setStyleSheet("QDialog { background-color: #1C1C1E; }")
    
    def analyze_with_ai(self):
        """使用 AI 分析 Prompt 内容"""
        content = self.content_input.toPlainText().strip()
        if not content:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "提示", "请先输入 Prompt 内容")
            return
        
        # 显示加载状态
        original_text = self.sender().text()
        self.sender().setText("⏳ 分析中...")
        self.sender().setEnabled(False)
        self.repaint()
        
        # 调用 AI 分析
        result = self.ai_analyzer.analyze_prompt(content)
        
        # 恢复按钮
        self.sender().setText(original_text)
        self.sender().setEnabled(True)
        
        if result:
            # 填充结果
            if not self.name_input.text():  # 只在名称为空时填充
                self.name_input.setText(result['name'])
            
            if not self.category_input.currentText():  # 只在分类为空时填充
                self.category_input.setCurrentText(result['category'])
            
            if not self.tags_input.text():  # 只在标签为空时填充
                self.tags_input.setText(", ".join(result['tags']))
            
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.information(
                self, 
                "✅ 分析完成", 
                f"AI 分析结果：\n\n"
                f"名称: {result['name']}\n"
                f"分类: {result['category']}\n"
                f"标签: {', '.join(result['tags'])}"
            )
        else:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "分析失败", "AI 分析失败，请检查网络连接和 API Key 设置")
    
    def load_prompt(self, prompt):
        self.name_input.setText(prompt.get("name", ""))
        self.category_input.setCurrentText(prompt.get("category", ""))
        self.tags_input.setText(", ".join(prompt.get("tags", [])))
        self.content_input.setPlainText(prompt.get("content", ""))
    
    def get_data(self):
        tags_text = self.tags_input.text().strip()
        tags = [tag.strip() for tag in tags_text.split(",")] if tags_text else []
        
        return {
            "name": self.name_input.text().strip(),
            "category": self.category_input.currentText().strip(),
            "tags": tags,
            "content": self.content_input.toPlainText().strip()
        }
    
    def _get_input_style(self):
        return """
            QLineEdit {
                background-color: #2C2C2E;
                color: white;
                border: 1px solid #3A3A3C;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #FF9500;
            }
        """
    
    def _get_combo_style(self):
        return """
            QComboBox {
                background-color: #2C2C2E;
                color: white;
                border: 1px solid #3A3A3C;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QComboBox:focus {
                border: 1px solid #FF9500;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid white;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: #2C2C2E;
                color: white;
                selection-background-color: #3A3A3C;
                border: 1px solid #3A3A3C;
            }
        """
    
    def _get_text_edit_style(self):
        return """
            QTextEdit {
                background-color: #2C2C2E;
                color: white;
                border: 1px solid #3A3A3C;
                border-radius: 6px;
                padding: 8px;
                font-size: 13px;
                font-family: 'SF Mono', 'Monaco', 'Consolas', monospace;
            }
            QTextEdit:focus {
                border: 1px solid #FF9500;
            }
        """
    
    def _get_button_style(self, bg_color):
        return f"""
            QPushButton {{
                background-color: {bg_color};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self._lighten_color(bg_color)};
            }}
            QPushButton:pressed {{
                background-color: {self._darken_color(bg_color)};
            }}
        """
    
    def _lighten_color(self, color):
        if color == "#3A3A3C":
            return "#48484A"
        elif color == "#FF9500":
            return "#FFA726"
        return color
    
    def _darken_color(self, color):
        if color == "#3A3A3C":
            return "#2C2C2E"
        elif color == "#FF9500":
            return "#E68900"
        return color
