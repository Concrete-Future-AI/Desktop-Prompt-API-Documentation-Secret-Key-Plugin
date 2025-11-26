#!/usr/bin/env python3
"""
风格管理器 - 支持多种 UI 风格切换
"""

class StyleManager:
    """UI 风格管理器"""
    
    # 所有可用风格 - 精选高级风格
    STYLES = {
        "premium": {
            "name": "高级渐变",
            "name_en": "Premium Gradient",
            "icon": "✨",
            "description": "深邃渐变，紫色微光，高级质感"
        },
        "glass": {
            "name": "玻璃拟态",
            "name_en": "Glassmorphism",
            "icon": "🔮",
            "description": "通透玻璃，蓝色光晕，现代未来"
        },
        "film": {
            "name": "胶片颗粒",
            "name_en": "Analog Film",
            "icon": "🎞️",
            "description": "怀旧暖调，颗粒质感，复古胶片"
        }
    }
    
    @staticmethod
    def get_style_stylesheet(style_name):
        """获取指定风格的样式表"""
        if style_name == "premium":
            return StyleManager._get_premium_style()
        elif style_name == "glass":
            return StyleManager._get_glass_style()
        elif style_name == "film":
            return StyleManager._get_film_style()
        else:
            return StyleManager._get_premium_style()
    
    @staticmethod
    def _get_film_style():
        """胶片风格 - 暖色调 + 颗粒感"""
        return """
            /* 主容器 - 暖色深色背景 */
            QWidget#container {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(40, 35, 30, 0.95),
                    stop:1 rgba(30, 25, 20, 0.98)
                );
                border: 1px solid rgba(255, 153, 102, 0.3);
                border-radius: 16px;
            }
            
            /* 标签 */
            QLabel {
                color: #e0e0e0;
                background: transparent;
            }
            
            /* 输入框 - 复古暖色 */
            QLineEdit {
                background: rgba(0, 0, 0, 0.3);
                border: 1px solid rgba(255, 153, 102, 0.3);
                border-radius: 8px;
                color: #f0f0f0;
                padding: 12px;
                font-size: 14px;
                selection-background-color: rgba(255, 126, 95, 0.4);
            }
            QLineEdit:hover {
                border: 1px solid rgba(255, 153, 102, 0.5);
                background: rgba(0, 0, 0, 0.4);
            }
            QLineEdit:focus {
                border: 2px solid rgba(255, 126, 95, 0.7);
                background: rgba(0, 0, 0, 0.5);
            }
            
            /* 按钮 - 暖色渐变 */
            QPushButton {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(255, 153, 102, 0.8),
                    stop:1 rgba(255, 94, 98, 0.8)
                );
                color: #FFFFFF;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                padding: 12px 20px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(255, 153, 102, 0.9),
                    stop:1 rgba(255, 94, 98, 0.9)
                );
                border: 1px solid rgba(255, 255, 255, 0.4);
            }
            QPushButton:pressed {
                background: rgba(200, 80, 80, 0.9);
                padding: 13px 20px 11px 20px;
            }
            
            /* 列表 - 暖色调 */
            QListWidget {
                background: rgba(20, 15, 10, 0.6);
                border: 1px solid rgba(255, 153, 102, 0.2);
                border-radius: 12px;
                color: #e0e0e0;
                outline: none;
                padding: 10px;
            }
            QListWidget::item {
                border-radius: 8px;
                padding: 12px;
                margin: 5px;
                border: 1px solid transparent;
                background: rgba(255, 255, 255, 0.03);
            }
            QListWidget::item:hover {
                background: rgba(255, 153, 102, 0.15);
                border: 1px solid rgba(255, 153, 102, 0.3);
            }
            QListWidget::item:selected {
                background: rgba(255, 94, 98, 0.3);
                border: 1px solid rgba(255, 94, 98, 0.5);
                color: #ffffff;
            }
            
            /* 下拉框 */
            QComboBox {
                background: rgba(0, 0, 0, 0.3);
                border: 1px solid rgba(255, 153, 102, 0.3);
                border-radius: 8px;
                color: #e0e0e0;
                padding: 8px 12px;
            }
            QComboBox:hover {
                border: 1px solid rgba(255, 153, 102, 0.5);
            }
            QComboBox QAbstractItemView {
                background: rgba(40, 35, 30, 0.95);
                color: #e0e0e0;
                selection-background-color: rgba(255, 126, 95, 0.4);
                border: 1px solid rgba(255, 153, 102, 0.3);
            }
            
            /* 滚动条 - 暖色 */
            QScrollBar:vertical {
                background: rgba(0, 0, 0, 0.1);
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 153, 102, 0.4);
                border-radius: 4px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(255, 153, 102, 0.6);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """
    
    @staticmethod
    def _get_premium_style():
        """高级渐变风格 - 深邃紫黑渐变 + 极致质感"""
        return """
            /* 主容器 - 深邃渐变 + 紫色微光 + 32px圆角 */
            QWidget#container {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(52, 45, 68, 0.92),
                    stop:0.3 rgba(42, 35, 58, 0.94),
                    stop:0.6 rgba(32, 28, 48, 0.96),
                    stop:1 rgba(24, 20, 38, 0.98)
                );
                border-radius: 32px;
                border: 1px solid rgba(158, 119, 230, 0.28);
            }
            
            /* 标签 */
            QLabel {
                color: #FFFFFF;
                background: transparent;
            }
            
            /* 输入框 - 深邃渐变 + 紫光边框 */
            QLineEdit {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(65, 58, 85, 0.65),
                    stop:0.35 rgba(55, 48, 75, 0.75),
                    stop:0.7 rgba(45, 38, 65, 0.85),
                    stop:1 rgba(35, 28, 55, 0.92)
                );
                border: 1.5px solid rgba(158, 119, 230, 0.32);
                border-radius: 26px;
                color: rgba(255, 255, 255, 0.96);
                padding: 15px 22px;
                font-size: 14px;
                selection-background-color: rgba(178, 149, 250, 0.42);
            }
            QLineEdit:hover {
                border: 1.5px solid rgba(178, 139, 250, 0.48);
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(75, 68, 95, 0.72),
                    stop:0.35 rgba(65, 58, 85, 0.82),
                    stop:0.7 rgba(55, 48, 75, 0.88),
                    stop:1 rgba(45, 38, 65, 0.94)
                );
            }
            QLineEdit:focus {
                border: 2px solid rgba(188, 159, 255, 0.72);
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(85, 75, 108, 0.82),
                    stop:0.35 rgba(72, 62, 95, 0.88),
                    stop:0.7 rgba(62, 52, 85, 0.92),
                    stop:1 rgba(52, 42, 75, 0.96)
                );
            }
            
            /* 按钮 - 紫色渐变 + 发光效果 */
            QPushButton {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(168, 129, 240, 0.82),
                    stop:0.4 rgba(148, 109, 220, 0.88),
                    stop:0.75 rgba(128, 89, 200, 0.92),
                    stop:1 rgba(108, 69, 180, 0.95)
                );
                color: rgba(255, 255, 255, 0.98);
                border: 1.5px solid rgba(188, 159, 250, 0.45);
                border-radius: 26px;
                padding: 14px 24px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(198, 159, 255, 0.92),
                    stop:0.4 rgba(178, 139, 245, 0.96),
                    stop:0.75 rgba(158, 119, 230, 0.98),
                    stop:1 rgba(138, 99, 215, 1.0)
                );
                border: 1.5px solid rgba(218, 189, 255, 0.68);
            }
            QPushButton:pressed {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(118, 79, 200, 0.92),
                    stop:0.4 rgba(98, 59, 180, 0.96),
                    stop:0.75 rgba(88, 49, 170, 0.98),
                    stop:1 rgba(78, 39, 160, 1.0)
                );
                padding: 15px 24px 13px 24px;
                border: 1.5px solid rgba(148, 119, 220, 0.75);
            }
            
            /* 下拉框 */
            QComboBox {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(45, 45, 48, 0.7),
                    stop:1 rgba(35, 35, 38, 0.85)
                );
                border: 1px solid rgba(90, 90, 95, 0.3);
                border-radius: 20px;
                color: #FFFFFF;
                padding: 11px 16px;
                font-size: 13px;
            }
            QComboBox:hover {
                border: 1px solid rgba(138, 99, 210, 0.5);
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(55, 55, 58, 0.8),
                    stop:1 rgba(45, 45, 48, 0.9)
                );
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 8px;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(42, 42, 46, 0.95),
                    stop:1 rgba(32, 32, 36, 0.98)
                );
                border: 1px solid rgba(80, 80, 85, 0.4);
                border-radius: 16px;
                color: #FFFFFF;
                selection-background-color: rgba(138, 99, 210, 0.35);
                padding: 6px;
            }
            
            /* 列表 - 深邃背景 + 紫光微光 */
            QListWidget {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(38, 35, 48, 0.65),
                    stop:0.5 rgba(28, 25, 38, 0.75),
                    stop:1 rgba(20, 18, 30, 0.85)
                );
                border: 1px solid rgba(138, 99, 210, 0.2);
                border-radius: 28px;
                color: rgba(255, 255, 255, 0.95);
                outline: none;
                padding: 14px 10px;
            }
            QListWidget::item {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(55, 50, 68, 0.5),
                    stop:0.5 rgba(45, 40, 58, 0.6),
                    stop:1 rgba(35, 30, 48, 0.7)
                );
                border-radius: 22px;
                padding: 12px 16px;
                margin: 7px 5px;
                border: 1px solid rgba(138, 99, 210, 0.1);
            }
            QListWidget::item:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(75, 68, 90, 0.7),
                    stop:0.5 rgba(65, 58, 80, 0.8),
                    stop:1 rgba(55, 48, 70, 0.85)
                );
                border: 1px solid rgba(158, 119, 230, 0.4);
            }
            QListWidget::item:selected {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(138, 99, 210, 0.45),
                    stop:0.5 rgba(118, 79, 190, 0.55),
                    stop:1 rgba(98, 59, 170, 0.65)
                );
                border: 1px solid rgba(168, 139, 230, 0.7);
            }
            
            /* 复选框 */
            QCheckBox {
                color: #FFFFFF;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 10px;
                border: 2px solid rgba(120, 120, 125, 0.5);
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(50, 50, 55, 0.7),
                    stop:1 rgba(40, 40, 45, 0.85)
                );
            }
            QCheckBox::indicator:hover {
                border: 2px solid rgba(138, 99, 210, 0.7);
            }
            QCheckBox::indicator:checked {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(138, 99, 210, 0.9),
                    stop:1 rgba(118, 79, 190, 0.95)
                );
                border: 2px solid rgba(138, 99, 210, 0.8);
            }
            
            /* 滚动条 - 紫色发光滚动条 */
            QScrollBar:vertical {
                background: rgba(30, 27, 40, 0.4);
                width: 10px;
                border-radius: 5px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(138, 99, 210, 0.6),
                    stop:0.5 rgba(158, 119, 230, 0.7),
                    stop:1 rgba(138, 99, 210, 0.6)
                );
                border-radius: 5px;
                min-height: 40px;
                border: 1px solid rgba(168, 139, 230, 0.3);
            }
            QScrollBar::handle:vertical:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(158, 119, 230, 0.75),
                    stop:0.5 rgba(178, 139, 250, 0.85),
                    stop:1 rgba(158, 119, 230, 0.75)
                );
                border: 1px solid rgba(188, 159, 250, 0.5);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """
    
    @staticmethod
    def _get_glass_style():
        """玻璃拟态风格 - 通透蓝色渐变 + 玻璃质感"""
        return """
            /* 主容器 - 通透玻璃渐变 + 蓝色光晕 + 32px圆角 */
            QWidget#container {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(48, 58, 78, 0.88),
                    stop:0.3 rgba(38, 48, 68, 0.91),
                    stop:0.6 rgba(28, 38, 58, 0.94),
                    stop:1 rgba(20, 30, 50, 0.97)
                );
                border-radius: 32px;
                border: 1px solid rgba(119, 170, 240, 0.32);
            }
            
            /* 标签 */
            QLabel {
                color: #FFFFFF;
                background: transparent;
            }
            
            /* 输入框 - 通透蓝色渐变 */
            QLineEdit {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(60, 75, 100, 0.62),
                    stop:0.35 rgba(50, 65, 90, 0.72),
                    stop:0.7 rgba(40, 55, 80, 0.82),
                    stop:1 rgba(30, 45, 70, 0.88)
                );
                border: 1.5px solid rgba(119, 170, 240, 0.35);
                border-radius: 26px;
                color: rgba(255, 255, 255, 0.96);
                padding: 15px 22px;
                font-size: 14px;
                selection-background-color: rgba(129, 200, 255, 0.42);
            }
            QLineEdit:hover {
                border: 1.5px solid rgba(149, 190, 255, 0.52);
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(70, 88, 115, 0.7),
                    stop:0.35 rgba(60, 78, 105, 0.8),
                    stop:0.7 rgba(50, 68, 95, 0.86),
                    stop:1 rgba(40, 58, 85, 0.92)
                );
            }
            QLineEdit:focus {
                border: 2px solid rgba(169, 210, 255, 0.75);
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(78, 98, 128, 0.78),
                    stop:0.35 rgba(68, 88, 118, 0.86),
                    stop:0.7 rgba(58, 78, 108, 0.91),
                    stop:1 rgba(48, 68, 98, 0.95)
                );
            }
            
            /* 按钮 - 蓝色玻璃渐变 */
            QPushButton {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(129, 180, 250, 0.78),
                    stop:0.4 rgba(109, 160, 230, 0.84),
                    stop:0.75 rgba(89, 140, 210, 0.88),
                    stop:1 rgba(69, 120, 190, 0.92)
                );
                color: rgba(255, 255, 255, 0.98);
                border: 1.5px solid rgba(169, 210, 255, 0.48);
                border-radius: 26px;
                padding: 14px 24px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(159, 210, 255, 0.88),
                    stop:0.4 rgba(139, 190, 245, 0.93),
                    stop:0.75 rgba(119, 170, 230, 0.96),
                    stop:1 rgba(99, 150, 220, 0.98)
                );
                border: 1.5px solid rgba(189, 230, 255, 0.68);
            }
            QPushButton:pressed {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(79, 140, 210, 0.9),
                    stop:0.4 rgba(59, 120, 190, 0.94),
                    stop:0.75 rgba(49, 110, 180, 0.96),
                    stop:1 rgba(39, 100, 170, 0.98)
                );
                padding: 15px 24px 13px 24px;
                border: 1.5px solid rgba(119, 170, 230, 0.75);
            }
            
            /* 下拉框 */
            QComboBox {
                background: rgba(50, 50, 50, 0.6);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                color: #FFFFFF;
                padding: 6px 12px;
                font-size: 13px;
            }
            QComboBox:hover {
                border: 1px solid rgba(255, 149, 0, 0.5);
                background: rgba(60, 60, 60, 0.7);
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 8px;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView {
                background: rgba(40, 40, 40, 0.95);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 6px;
                color: #FFFFFF;
                selection-background-color: rgba(255, 149, 0, 0.3);
                padding: 4px;
            }
            
            /* 列表 - 通透玻璃 + 蓝色光晕 */
            QListWidget {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(35, 45, 60, 0.6),
                    stop:0.5 rgba(25, 35, 50, 0.7),
                    stop:1 rgba(18, 28, 42, 0.8)
                );
                border: 1px solid rgba(99, 150, 220, 0.25);
                border-radius: 28px;
                color: rgba(255, 255, 255, 0.95);
                outline: none;
                padding: 14px 10px;
            }
            QListWidget::item {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(50, 65, 85, 0.45),
                    stop:0.5 rgba(40, 55, 75, 0.55),
                    stop:1 rgba(30, 45, 65, 0.65)
                );
                border-radius: 22px;
                padding: 12px 16px;
                margin: 7px 5px;
                border: 1px solid rgba(99, 150, 220, 0.15);
            }
            QListWidget::item:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(68, 88, 115, 0.65),
                    stop:0.5 rgba(58, 78, 105, 0.75),
                    stop:1 rgba(48, 68, 95, 0.8)
                );
                border: 1px solid rgba(119, 170, 240, 0.45);
            }
            QListWidget::item:selected {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(99, 150, 220, 0.5),
                    stop:0.5 rgba(79, 130, 200, 0.6),
                    stop:1 rgba(59, 110, 180, 0.7)
                );
                border: 1px solid rgba(139, 190, 255, 0.7);
            }
            
            /* 复选框 */
            QCheckBox {
                color: #FFFFFF;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 1px solid rgba(255, 255, 255, 0.3);
                background: rgba(50, 50, 50, 0.6);
            }
            QCheckBox::indicator:hover {
                border: 1px solid rgba(255, 149, 0, 0.5);
            }
            QCheckBox::indicator:checked {
                background: #FF9500;
                border: 1px solid #FF9500;
            }
            
            /* 滚动条 - 蓝色发光滚动条 */
            QScrollBar:vertical {
                background: rgba(25, 35, 48, 0.35);
                width: 10px;
                border-radius: 5px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(99, 150, 220, 0.6),
                    stop:0.5 rgba(119, 170, 240, 0.7),
                    stop:1 rgba(99, 150, 220, 0.6)
                );
                border-radius: 5px;
                min-height: 40px;
                border: 1px solid rgba(139, 190, 255, 0.35);
            }
            QScrollBar::handle:vertical:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(119, 170, 240, 0.75),
                    stop:0.5 rgba(139, 190, 255, 0.85),
                    stop:1 rgba(119, 170, 240, 0.75)
                );
                border: 1px solid rgba(159, 210, 255, 0.55);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """
    
    @staticmethod
    def _get_flat_style():
        """极简平面风格 - Material Design Flat"""
        return """
            /* 主容器 */
            QWidget#container {
                background: #FFFFFF;
                border: 2px solid #E5E5E5;
                border-radius: 12px;
            }
            
            /* 标签 */
            QLabel {
                color: #212121;
                background: transparent;
                font-weight: 500;
            }
            
            /* 输入框 */
            QLineEdit {
                background: #F5F5F5;
                border: none;
                border-bottom: 2px solid #E0E0E0;
                border-radius: 4px 4px 0px 0px;
                color: #212121;
                padding: 12px 8px;
                font-size: 14px;
                selection-background-color: rgba(255, 149, 0, 0.3);
            }
            QLineEdit:focus {
                border-bottom: 2px solid #FF9500;
                background: #FAFAFA;
            }
            
            /* 按钮 */
            QPushButton {
                background: #FFFFFF;
                color: #212121;
                border: 2px solid #212121;
                border-radius: 4px;
                padding: 10px 24px;
                font-size: 13px;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            QPushButton:hover {
                background: #212121;
                color: #FFFFFF;
            }
            QPushButton:pressed {
                background: #FF9500;
                color: #FFFFFF;
                border-color: #FF9500;
            }
            
            /* 下拉框 */
            QComboBox {
                background: #F5F5F5;
                border: none;
                border-bottom: 2px solid #E0E0E0;
                border-radius: 4px 4px 0px 0px;
                color: #212121;
                padding: 8px 12px;
                font-size: 13px;
                font-weight: 500;
            }
            QComboBox:hover {
                background: #EEEEEE;
                border-bottom: 2px solid #FF9500;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background: #FFFFFF;
                border: 1px solid #E0E0E0;
                color: #212121;
                selection-background-color: #FFEBCC;
                outline: none;
            }
            
            /* 列表 */
            QListWidget {
                background: #FAFAFA;
                border: none;
                color: #212121;
                outline: none;
            }
            QListWidget::item {
                border: none;
                border-left: 4px solid transparent;
                padding: 14px 12px;
                margin: 0px;
                font-size: 14px;
            }
            QListWidget::item:hover {
                background: #F0F0F0;
                border-left: 4px solid #FF9500;
            }
            QListWidget::item:selected {
                background: #FFF3E0;
                border-left: 4px solid #FF9500;
                color: #212121;
            }
            
            /* 复选框 */
            QCheckBox {
                color: #212121;
                spacing: 8px;
                font-weight: 500;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 2px;
                border: 2px solid #757575;
                background: #FFFFFF;
            }
            QCheckBox::indicator:hover {
                border: 2px solid #FF9500;
            }
            QCheckBox::indicator:checked {
                background: #FF9500;
                border: 2px solid #FF9500;
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiI+PHBhdGggZD0iTSA0IDYgTCA1IDcgTCA4IDQiIHN0cm9rZT0id2hpdGUiIGZpbGw9Im5vbmUiIHN0cm9rZS13aWR0aD0iMiIvPjwvc3ZnPg==);
            }
            
            /* 滚动条 */
            QScrollBar:vertical {
                background: #F5F5F5;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #BDBDBD;
                border-radius: 4px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: #9E9E9E;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """
    
    @staticmethod
    def _get_retro_style():
        """复古 Windows 95/98 风格"""
        return """
            /* 主容器 */
            QWidget#container {
                background: #C0C0C0;
                border-top: 2px solid #FFFFFF;
                border-left: 2px solid #FFFFFF;
                border-right: 2px solid #808080;
                border-bottom: 2px solid #808080;
                border-radius: 0px;
            }
            
            /* 标签 */
            QLabel {
                color: #000000;
                background: transparent;
                font-family: "MS Sans Serif", "Microsoft Sans Serif", Arial;
                font-size: 11px;
            }
            
            /* 输入框 */
            QLineEdit {
                background: #FFFFFF;
                border-top: 1px solid #808080;
                border-left: 1px solid #808080;
                border-right: 1px solid #DFDFDF;
                border-bottom: 1px solid #DFDFDF;
                border-radius: 0px;
                color: #000000;
                padding: 3px 4px;
                font-size: 11px;
                font-family: "MS Sans Serif", "Microsoft Sans Serif", Arial;
                selection-background-color: #000080;
                selection-color: #FFFFFF;
            }
            QLineEdit:focus {
                border-top: 2px solid #000000;
                border-left: 2px solid #000000;
                border-right: 2px solid #808080;
                border-bottom: 2px solid #808080;
            }
            
            /* 按钮 */
            QPushButton {
                background: #C0C0C0;
                color: #000000;
                border-top: 2px solid #FFFFFF;
                border-left: 2px solid #FFFFFF;
                border-right: 2px solid #808080;
                border-bottom: 2px solid #808080;
                border-radius: 0px;
                padding: 5px 12px;
                font-size: 11px;
                font-family: "MS Sans Serif", "Microsoft Sans Serif", Arial;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #D4D0C8;
            }
            QPushButton:pressed {
                border-top: 2px solid #808080;
                border-left: 2px solid #808080;
                border-right: 2px solid #FFFFFF;
                border-bottom: 2px solid #FFFFFF;
                padding: 6px 11px 4px 13px;
            }
            
            /* 下拉框 */
            QComboBox {
                background: #FFFFFF;
                border-top: 1px solid #808080;
                border-left: 1px solid #808080;
                border-right: 1px solid #DFDFDF;
                border-bottom: 1px solid #DFDFDF;
                color: #000000;
                padding: 2px 4px;
                font-size: 11px;
                font-family: "MS Sans Serif", "Microsoft Sans Serif", Arial;
            }
            QComboBox::drop-down {
                background: #C0C0C0;
                border-left: 1px solid #808080;
                width: 18px;
            }
            QComboBox QAbstractItemView {
                background: #FFFFFF;
                border: 1px solid #000000;
                color: #000000;
                selection-background-color: #000080;
                selection-color: #FFFFFF;
                font-family: "MS Sans Serif", "Microsoft Sans Serif", Arial;
            }
            
            /* 列表 */
            QListWidget {
                background: #FFFFFF;
                border-top: 2px solid #808080;
                border-left: 2px solid #808080;
                border-right: 2px solid #DFDFDF;
                border-bottom: 2px solid #DFDFDF;
                color: #000000;
                font-family: "MS Sans Serif", "Microsoft Sans Serif", Arial;
                font-size: 11px;
                outline: none;
            }
            QListWidget::item {
                padding: 3px 4px;
                margin: 0px;
                border: 1px dotted transparent;
            }
            QListWidget::item:hover {
                background: #D4D0C8;
            }
            QListWidget::item:selected {
                background: #000080;
                color: #FFFFFF;
                border: 1px dotted #FFFFFF;
            }
            
            /* 复选框 */
            QCheckBox {
                color: #000000;
                spacing: 6px;
                font-family: "MS Sans Serif", "Microsoft Sans Serif", Arial;
                font-size: 11px;
            }
            QCheckBox::indicator {
                width: 13px;
                height: 13px;
                border: none;
                background: #FFFFFF;
                border-top: 1px solid #808080;
                border-left: 1px solid #808080;
                border-right: 1px solid #DFDFDF;
                border-bottom: 1px solid #DFDFDF;
            }
            QCheckBox::indicator:checked {
                background: #FFFFFF;
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iOSIgaGVpZ2h0PSI5IiB2aWV3Qm94PSIwIDAgOSA5Ij48cGF0aCBkPSJNIDEgNCBMIDMgNiBMIDggMSIgc3Ryb2tlPSIjMDAwMDAwIiBmaWxsPSJub25lIiBzdHJva2Utd2lkdGg9IjIiLz48L3N2Zz4=);
            }
            
            /* 滚动条 */
            QScrollBar:vertical {
                background: #C0C0C0;
                width: 16px;
                border: none;
            }
            QScrollBar::handle:vertical {
                background: #C0C0C0;
                border-top: 1px solid #FFFFFF;
                border-left: 1px solid #FFFFFF;
                border-right: 1px solid #808080;
                border-bottom: 1px solid #808080;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical {
                background: #C0C0C0;
                height: 16px;
                subcontrol-position: bottom;
                border-top: 1px solid #FFFFFF;
                border-left: 1px solid #FFFFFF;
                border-right: 1px solid #808080;
                border-bottom: 1px solid #808080;
            }
            QScrollBar::sub-line:vertical {
                background: #C0C0C0;
                height: 16px;
                subcontrol-position: top;
                border-top: 1px solid #FFFFFF;
                border-left: 1px solid #FFFFFF;
                border-right: 1px solid #808080;
                border-bottom: 1px solid #808080;
            }
        """
    
    @staticmethod
    def _get_swiss_style():
        """瑞士设计风格"""
        return """
            QWidget#container {
                background: #FFFFFF;
                border: 4px solid #000000;
                border-radius: 0px;
            }
            QLineEdit {
                background: #FFFFFF;
                border: none;
                border: 3px solid #000000;
                border-radius: 0px;
                color: #000000;
                padding: 12px;
                font-size: 16px;
                font-weight: 500;
                font-family: "Helvetica Neue", Helvetica, Arial;
            }
            QLineEdit:focus {
                border: 3px solid #FF0000;
            }
            QPushButton {
                background: #000000;
                color: #FFFFFF;
                border: none;
                border-radius: 0px;
                padding: 14px 24px;
                font-size: 14px;
                font-weight: 700;
                font-family: "Helvetica Neue", Helvetica, Arial;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background: #FF0000;
            }
            QPushButton:pressed {
                background: #CC0000;
            }
            QListWidget {
                background: #F8F8F8;
                border: 3px solid #000000;
                color: #000000;
                font-family: "Helvetica Neue", Helvetica, Arial;
            }
            QListWidget::item {
                border: none;
                border-bottom: 1px solid #E0E0E0;
                padding: 16px 12px;
                margin: 0px;
            }
            QListWidget::item:hover {
                background: #FFF0F0;
            }
            QListWidget::item:selected {
                background: #FF0000;
                color: #FFFFFF;
                border: none;
            }
            QComboBox, QLabel {
                color: #000000;
                font-family: "Helvetica Neue", Helvetica, Arial;
                font-weight: 500;
            }
            QCheckBox {
                color: #000000;
                font-family: "Helvetica Neue", Helvetica, Arial;
            }
        """
    
    @staticmethod
    def _get_sketch_style():
        """手绘涂鸦风格 - 温暖随性"""
        return """
            QWidget#container {
                background: #FFFEF8;
                border: 3px dashed #8B7355;
                border-radius: 12px;
            }
            QLineEdit {
                background: #FFFFFF;
                border: 2px solid #4A4A4A;
                border-radius: 6px;
                color: #2C2C2C;
                padding: 10px;
                font-size: 14px;
                font-family: "Comic Sans MS", "Bradley Hand", cursive;
            }
            QLineEdit:focus {
                border: 3px solid #FF8C42;
                background: #FFFEF8;
            }
            QPushButton {
                background: qlineargradient(
                    x1:0, y1:0, x2:0.1, y2:0.1,
                    stop:0 #FFE4B5,
                    stop:1 #FFD180
                );
                color: #2C2C2C;
                border: 2px solid #4A4A4A;
                border-radius: 8px;
                padding: 10px 18px;
                font-size: 13px;
                font-weight: 600;
                font-family: "Comic Sans MS", "Bradley Hand", cursive;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:0.1, y2:0.1,
                    stop:0 #FFD180,
                    stop:1 #FFA726
                );
                border: 3px solid #FF8C42;
            }
            QPushButton:pressed {
                background: #FFB74D;
                transform: translateY(2px);
            }
            QListWidget {
                background: #FFFEF8;
                border: 2px solid #8B7355;
                border-radius: 6px;
                color: #2C2C2C;
                font-family: "Comic Sans MS", "Bradley Hand", cursive;
            }
            QListWidget::item {
                border: 1px dashed transparent;
                border-radius: 6px;
                padding: 10px;
                margin: 3px;
            }
            QListWidget::item:hover {
                background: #FFF4E6;
                border: 1px dashed #FF8C42;
            }
            QListWidget::item:selected {
                background: #FFE0B2;
                border: 2px solid #FF8C42;
            }
            QComboBox, QLabel {
                color: #2C2C2C;
                font-family: "Comic Sans MS", "Bradley Hand", cursive;
            }
            QCheckBox {
                color: #2C2C2C;
                font-family: "Comic Sans MS", "Bradley Hand", cursive;
            }
        """
    
    @staticmethod
    def _get_neon_style():
        """霓虹赛博朋克风格 - 未来科技"""
        return """
            QWidget#container {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(26, 26, 46, 0.95),
                    stop:1 rgba(10, 14, 39, 0.95)
                );
                border: 2px solid #00F0FF;
                border-radius: 12px;
            }
            QLineEdit {
                background: rgba(0, 0, 0, 0.7);
                border: 2px solid #00F0FF;
                border-radius: 6px;
                color: #00F0FF;
                padding: 10px;
                font-size: 14px;
                font-family: "Courier New", monospace;
            }
            QLineEdit:focus {
                border: 2px solid #FF00FF;
                background: rgba(0, 0, 0, 0.9);
                color: #FF00FF;
            }
            QPushButton {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(0, 240, 255, 0.3),
                    stop:1 rgba(255, 0, 255, 0.3)
                );
                color: #FFFFFF;
                border: 2px solid #00F0FF;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: 600;
                font-family: "Courier New", monospace;
                text-transform: uppercase;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(0, 240, 255, 0.5),
                    stop:1 rgba(255, 0, 255, 0.5)
                );
                border: 2px solid #FF00FF;
                color: #FF00FF;
            }
            QPushButton:pressed {
                background: rgba(255, 0, 255, 0.7);
                color: #000000;
            }
            QListWidget {
                background: rgba(0, 0, 0, 0.6);
                border: 2px solid #00F0FF;
                border-radius: 8px;
                color: #00F0FF;
                font-family: "Courier New", monospace;
            }
            QListWidget::item {
                border: 1px solid transparent;
                border-radius: 4px;
                padding: 10px;
                margin: 2px;
            }
            QListWidget::item:hover {
                background: rgba(0, 240, 255, 0.2);
                border: 1px solid #00F0FF;
            }
            QListWidget::item:selected {
                background: rgba(255, 0, 255, 0.3);
                border: 1px solid #FF00FF;
                color: #FF00FF;
            }
            QComboBox, QLabel {
                color: #00F0FF;
                font-family: "Courier New", monospace;
            }
            QCheckBox {
                color: #00F0FF;
                font-family: "Courier New", monospace;
            }
        """


if __name__ == "__main__":
    # 测试代码
    print("可用风格：")
    for key, style in StyleManager.STYLES.items():
        print(f"{style['icon']} {style['name']} ({style['name_en']})")
        print(f"   {style['description']}")
