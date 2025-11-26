from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QPushButton, QListWidget, QListWidgetItem, 
                             QLabel, QComboBox, QMenu, QSlider, QFileDialog, QMessageBox,
                             QGraphicsOpacityEffect, QApplication, QScrollArea, QTextEdit)
from PyQt6.QtCore import Qt, QPoint, QSize, QPropertyAnimation, QEasingCurve, QTimer, pyqtProperty
from PyQt6.QtGui import QIcon, QCursor, QFont
from prompt_dialog import PromptDialog
from stats_window import StatsWindow
from prompt_item_widget import PromptItemWidget
from pathlib import Path
import pyperclip


class PromptPreviewWindow(QWidget):
    """重新设计的 Prompt 预览窗口 - 简洁可靠"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.ToolTip | 
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        
        # 固定尺寸
        self.setFixedWidth(500)
        self.setMaximumHeight(600)
        
        # 主布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 内容容器
        container = QWidget()
        container.setObjectName("previewContainer")
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(20, 16, 20, 16)
        container_layout.setSpacing(12)
        
        # 标题
        self.title_label = QLabel()
        self.title_label.setWordWrap(True)
        self.title_label.setStyleSheet("""
            color: #FFFFFF;
            font-size: 14px;
            font-weight: bold;
            background: transparent;
        """)
        container_layout.addWidget(self.title_label)
        
        # 分类和标签
        self.meta_label = QLabel()
        self.meta_label.setWordWrap(True)
        self.meta_label.setStyleSheet("""
            color: rgba(180, 180, 195, 0.9);
            font-size: 11px;
            background: transparent;
        """)
        container_layout.addWidget(self.meta_label)
        
        # 分隔线
        separator = QWidget()
        separator.setFixedHeight(1)
        separator.setStyleSheet("background: rgba(90, 90, 95, 0.3);")
        container_layout.addWidget(separator)
        
        # 内容区域（可滚动）
        self.content_text = QTextEdit()
        self.content_text.setReadOnly(True)
        self.content_text.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.content_text.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.content_text.setStyleSheet("""
            QTextEdit {
                background: transparent;
                color: rgba(235, 235, 240, 0.95);
                font-size: 12px;
                border: none;
                padding: 0;
                line-height: 1.6;
            }
            QScrollBar:vertical {
                background: transparent;
                width: 6px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: rgba(120, 120, 125, 0.4);
                border-radius: 3px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(140, 140, 145, 0.6);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0;
            }
        """)
        container_layout.addWidget(self.content_text, 1)
        
        layout.addWidget(container)
        
        # 容器样式
        self.setStyleSheet("""
            QWidget#previewContainer {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(48, 48, 52, 0.98),
                    stop:1 rgba(32, 32, 36, 0.98)
                );
                border: 1px solid rgba(90, 90, 95, 0.6);
                border-radius: 12px;
            }
        """)
    
    def set_content(self, name, category, tags, content):
        """设置预览内容"""
        # 设置标题
        self.title_label.setText(name)
        
        # 设置分类和标签
        meta_parts = []
        if category:
            meta_parts.append(f"📁 {category}")
        if tags:
            tags_text = ' '.join([f"#{tag}" for tag in tags[:5]])
            meta_parts.append(tags_text)
        self.meta_label.setText('  |  '.join(meta_parts) if meta_parts else "")
        
        # 设置内容
        self.content_text.setPlainText(content)
        
        # 根据内容长度调整高度
        doc_height = self.content_text.document().size().height()
        content_height = min(int(doc_height) + 40, 400)
        total_height = content_height + 100  # 加上标题、标签、边距
        self.setFixedHeight(min(total_height, 600))


class ToastLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(10, 132, 255, 0.95),
                    stop:1 rgba(30, 144, 255, 0.95));
                color: white;
                padding: 14px 24px;
                border-radius: 10px;
                font-size: 14px;
                font-weight: 600;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
        """)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setWindowFlags(Qt.WindowType.ToolTip | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        
        # 添加透明度动画效果
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        
        # 淡入动画
        self.fade_in_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_in_animation.setDuration(200)
        self.fade_in_animation.setStartValue(0.0)
        self.fade_in_animation.setEndValue(1.0)
        self.fade_in_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # 淡出动画
        self.fade_out_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_out_animation.setDuration(200)
        self.fade_out_animation.setStartValue(1.0)
        self.fade_out_animation.setEndValue(0.0)
        self.fade_out_animation.setEasingCurve(QEasingCurve.Type.InCubic)
        self.fade_out_animation.finished.connect(self.deleteLater)
    
    def show_animated(self):
        """显示带动画的Toast"""
        self.show()
        self.fade_in_animation.start()
        # 2秒后开始淡出
        QTimer.singleShot(2000, self.fade_out_animation.start)


class GrainOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self.noise_pixmap = None
        self._init_noise()
        
    def _init_noise(self):
        # Load base64 noise image
        import base64
        from PyQt6.QtGui import QPixmap
        
        # This is the noise base64 we generated
        noise_b64 = "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"
        
        # Convert base64 to QPixmap
        img_data = base64.b64decode(noise_b64)
        self.noise_pixmap = QPixmap()
        self.noise_pixmap.loadFromData(img_data)
        
    def paintEvent(self, event):
        from PyQt6.QtGui import QPainter, QBrush
        if not self.noise_pixmap:
            return
            
        painter = QPainter(self)
        painter.setOpacity(0.15) # Lower opacity for subtle grain
        painter.drawTiledPixmap(self.rect(), self.noise_pixmap)


class MainWindow(QMainWindow):
    def __init__(self, data_manager, floating_ball=None):
        super().__init__()
        self.data_manager = data_manager
        self.floating_ball = floating_ball  # 浮动球引用
        self.dragging = False
        self.drag_position = QPoint()
        self.opacity_value = self.data_manager.config.get("opacity", 0.95)
        self.always_on_top = self.data_manager.config.get("always_on_top", True)
        self.position_locked = self.data_manager.config.get("position_locked", False)
        
        # Film Grain Overlay
        self.grain_overlay = None
        
        # 折叠状态 - 改为上下折叠
        self.is_collapsed = False
        self.collapse_animation = None
        # 如果有浮动球，强制禁用自动折叠（避免冲突）
        if self.floating_ball:
            self.auto_collapse_enabled = False
        else:
            self.auto_collapse_enabled = self.data_manager.config.get("auto_collapse", True)
        self.collapsed_height = 58  # 折叠后的高度（标题栏+padding = 28+15*2 = 58）
        self.expanded_height = None  # 展开状态的高度，稍后初始化
        
        # 鼓励语列表
        self.encouragements = [
            "💡 灵感在这里等你...",
            "✨ 准备好创造了吗？",
            "🚀 让想法起飞！",
            "💪 你可以做到的！",
            "🌟 每个想法都值得记录",
            "🎯 专注，然后实现",
            "⚡ 创意无限，继续前进",
            "🎨 用 Prompt 创造魔法",
            "🔥 保持热情，继续创作",
            "💎 每个 Prompt 都是宝藏",
        ]
        self.current_encouragement_index = 0
        
        # AI 分析器（启用 Key 池）
        from ai_analyzer import AIAnalyzer
        self.ai_analyzer = AIAnalyzer(
            api_key=self.data_manager.config.get("gemini_api_key"),
            use_key_pool=True  # 启用 312 个 Keys 轮询
        )
        
        # 风格管理器
        from style_manager import StyleManager
        self.style_manager = StyleManager()
        self.current_style = self.data_manager.config.get("ui_style", "premium")
        
        # Tooltip 预览
        self.current_tooltip = None
        
        # 鼠标位置检查定时器
        self.mouse_check_timer = QTimer(self)
        self.mouse_check_timer.timeout.connect(self.check_mouse_position)
        self.mouse_check_timer.setInterval(100)  # 每100ms检查一次
        
        # 展开保护期标志（防止展开后立即关闭）
        self.just_expanded = False
        
        # 浮动球始终显示选项
        self.ball_always_visible = self.data_manager.config.get("ball_always_visible", False)
        
        # 当前分区模式：prompts 或 api_docs
        self.current_mode = "prompts"
        
        self.init_ui()
        self.restore_window_state()
        self.refresh_prompt_list()
        
        # 启动定时器
        # 自动折叠模式：检查鼠标位置
        # 浮动球模式：检查窗口焦点状态（点击外部会失去焦点）
        if self.auto_collapse_enabled or self.floating_ball:
            self.mouse_check_timer.start()
        
        # 检查是否首次运行
        self.check_first_run()
    
    def init_ui(self):
        self.setWindowTitle("Prompt Manager")
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint if self.always_on_top else Qt.WindowType.Window
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.container = QWidget()
        self.container.setObjectName("container")
        # 不在这里设置样式，由风格系统管理
        
        # Initialize Grain Overlay
        self.grain_overlay = GrainOverlay(self.container)
        self.grain_overlay.resize(self.container.size())
        self.grain_overlay.hide() # Hidden by default until film style is active
        
        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(15, 15, 15, 15)
        container_layout.setSpacing(12)
        
        header_layout = QHBoxLayout()
        self.title_label = QLabel("💡 Prompt Manager")
        self.title_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold; background: transparent;")
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        
        settings_btn = QPushButton("⚙")
        settings_btn.setFixedSize(28, 28)
        settings_btn.setStyleSheet(self._get_icon_button_style())
        settings_btn.clicked.connect(self.show_settings_menu)
        settings_btn.setToolTip("设置")
        header_layout.addWidget(settings_btn)
        
        close_btn = QPushButton("×")
        close_btn.setFixedSize(28, 28)
        close_btn.setStyleSheet(self._get_icon_button_style())
        close_btn.clicked.connect(self.hide_to_ball)
        close_btn.setToolTip("隐藏为浮动球")
        header_layout.addWidget(close_btn)
        
        container_layout.addLayout(header_layout)
        
        # 分区切换 Tab
        tab_layout = QHBoxLayout()
        tab_layout.setSpacing(8)
        
        self.prompts_tab_btn = QPushButton("💡 提示词")
        self.prompts_tab_btn.setCheckable(True)
        self.prompts_tab_btn.setChecked(True)
        self.prompts_tab_btn.clicked.connect(lambda: self.switch_mode("prompts"))
        tab_layout.addWidget(self.prompts_tab_btn)
        
        self.api_docs_tab_btn = QPushButton("📄 API文档")
        self.api_docs_tab_btn.setCheckable(True)
        self.api_docs_tab_btn.setChecked(False)
        self.api_docs_tab_btn.clicked.connect(lambda: self.switch_mode("api_docs"))
        tab_layout.addWidget(self.api_docs_tab_btn)
        
        self.api_keys_tab_btn = QPushButton("🔑 密钥")
        self.api_keys_tab_btn.setCheckable(True)
        self.api_keys_tab_btn.setChecked(False)
        self.api_keys_tab_btn.clicked.connect(lambda: self.switch_mode("api_keys"))
        tab_layout.addWidget(self.api_keys_tab_btn)
        
        tab_layout.addStretch()
        container_layout.addLayout(tab_layout)
        
        # 应用 Tab 样式
        self._update_tab_styles()
        
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 搜索 Prompts...")
        self.search_input.setStyleSheet(self._get_search_style())
        self.search_input.textChanged.connect(self.on_search)
        search_layout.addWidget(self.search_input)
        
        container_layout.addLayout(search_layout)
        
        self.filter_layout = QHBoxLayout()
        self.category_filter = QComboBox()
        self.category_filter.setStyleSheet(self._get_combo_style())
        self.category_filter.currentTextChanged.connect(self.on_search)
        self.filter_layout.addWidget(self.category_filter)
        
        container_layout.addLayout(self.filter_layout)
        
        self.prompt_list = QListWidget()
        self.prompt_list.setStyleSheet(self._get_list_style())
        self.prompt_list.itemDoubleClicked.connect(self.on_prompt_double_click)
        self.prompt_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.prompt_list.customContextMenuRequested.connect(self.show_context_menu)
        # 启用悬停提示
        self.prompt_list.setMouseTracking(True)
        self.prompt_list.viewport().setMouseTracking(True)
        self.prompt_list.viewport().installEventFilter(self)
        container_layout.addWidget(self.prompt_list, 1)
        
        self.button_layout = QHBoxLayout()
        
        # 快速添加按钮
        self.quick_add_btn = QPushButton("⚡ 快速添加")
        self.quick_add_btn.setStyleSheet(self._get_button_style("#FF9500"))
        self.quick_add_btn.setToolTip("从剪贴板智能添加 (Cmd+Shift+A)")
        self.quick_add_btn.clicked.connect(lambda: self._animate_button_click(self.quick_add_btn))
        self.quick_add_btn.clicked.connect(self.on_quick_add_click)
        self.button_layout.addWidget(self.quick_add_btn)
        
        self.add_btn = QPushButton("➕ 添加")
        self.add_btn.setStyleSheet(self._get_button_style("#FF9500"))
        self.add_btn.setToolTip("手动添加 Prompt")
        self.add_btn.clicked.connect(lambda: self._animate_button_click(self.add_btn))
        self.add_btn.clicked.connect(self.on_add_click)
        self.button_layout.addWidget(self.add_btn)
        
        self.stats_btn = QPushButton("📊 统计")
        self.stats_btn.setStyleSheet(self._get_button_style("#3A3A3C"))
        self.stats_btn.clicked.connect(lambda: self._animate_button_click(self.stats_btn))
        self.stats_btn.clicked.connect(self.show_stats)
        self.button_layout.addWidget(self.stats_btn)
        
        container_layout.addLayout(self.button_layout)
        
        main_layout.addWidget(self.container)
        
        # 设置最小窗口尺寸，允许用户自由调整大小
        self.normal_min_height = 400  # 保存正常的最小高度
        self.setMinimumSize(420, self.normal_min_height)  # 最小宽度420px，确保列表项有足够空间
        
        # 最后应用风格
        self.apply_style(self.current_style)
    
    def show_settings_menu(self):
        menu = QMenu(self)
        menu.setStyleSheet(self._get_menu_style())
        
        opacity_menu = menu.addMenu("透明度")
        for opacity in [100, 95, 90, 80, 70, 60, 50]:
            action = opacity_menu.addAction(f"{opacity}%")
            action.triggered.connect(lambda checked, o=opacity: self.set_opacity(o))
        
        menu.addSeparator()
        
        always_on_top_action = menu.addAction("始终置顶")
        always_on_top_action.setCheckable(True)
        always_on_top_action.setChecked(self.always_on_top)
        always_on_top_action.triggered.connect(self.toggle_always_on_top)
        
        lock_position_action = menu.addAction("锁定位置")
        lock_position_action.setCheckable(True)
        lock_position_action.setChecked(self.position_locked)
        lock_position_action.triggered.connect(self.toggle_position_lock)
        
        menu.addSeparator()
        
        import_action = menu.addAction("导入 Prompts")
        import_action.triggered.connect(self.import_prompts)
        
        export_action = menu.addAction("导出 Prompts")
        export_action.triggered.connect(self.export_prompts)
        
        menu.addSeparator()
        
        autostart_action = menu.addAction("开机自启动设置")
        autostart_action.triggered.connect(self.show_autostart_settings)
        
        menu.addSeparator()
        
        # 风格切换
        style_action = menu.addAction("🎨 切换风格")
        style_action.triggered.connect(self.show_style_selector)
        
        menu.addSeparator()
        
        ai_settings_action = menu.addAction("AI 分析设置")
        ai_settings_action.triggered.connect(self.show_ai_settings)
        
        # 浮动球相关选项（仅在有浮动球时显示）
        if self.floating_ball:
            menu.addSeparator()
            ball_always_visible_action = menu.addAction("✨ 浮动球始终显示")
            ball_always_visible_action.setCheckable(True)
            ball_always_visible_action.setChecked(self.ball_always_visible)
            ball_always_visible_action.triggered.connect(self.toggle_ball_always_visible)
        else:
            # 无浮动球模式才显示自动折叠选项
            auto_collapse_action = menu.addAction("自动折叠窗口")
            auto_collapse_action.setCheckable(True)
            auto_collapse_action.setChecked(self.auto_collapse_enabled)
            auto_collapse_action.triggered.connect(self.toggle_auto_collapse)
        
        menu.exec(QCursor.pos())
    
    def set_opacity(self, opacity):
        """设置窗口透明度 - 使用 setWindowOpacity 不影响样式"""
        self.opacity_value = opacity / 100.0
        self.data_manager.config["opacity"] = self.opacity_value
        self.data_manager.save_config()
        
        # 使用 setWindowOpacity 设置整个窗口的透明度
        # 这样不会覆盖 style_manager 设置的样式
        self.setWindowOpacity(self.opacity_value)
        
        self.show_toast(f"透明度设置为 {opacity}%")
    
    def toggle_always_on_top(self, checked):
        self.always_on_top = checked
        self.data_manager.config["always_on_top"] = checked
        self.data_manager.save_config()
        
        flags = Qt.WindowType.FramelessWindowHint
        if checked:
            flags |= Qt.WindowType.WindowStaysOnTopHint
        
        self.setWindowFlags(flags)
        self.show()
        self.show_toast("始终置顶: " + ("开启" if checked else "关闭"))
    
    def toggle_position_lock(self, checked):
        self.position_locked = checked
        self.data_manager.config["position_locked"] = checked
        self.data_manager.save_config()
        self.show_toast("位置锁定: " + ("开启" if checked else "关闭"))
    
    def refresh_category_filter(self):
        current_text = self.category_filter.currentText()
        self.category_filter.clear()
        self.category_filter.addItem("全部分类")
        
        # 根据当前模式获取分类
        if self.current_mode == "prompts":
            categories = self.data_manager.get_categories()
        elif self.current_mode == "api_docs":
            categories = self.data_manager.get_api_doc_categories()
        else:
            categories = self.data_manager.get_api_key_categories()
        
        for cat in categories:
            self.category_filter.addItem(cat)
        
        index = self.category_filter.findText(current_text)
        if index >= 0:
            self.category_filter.setCurrentIndex(index)
    
    def refresh_prompt_list(self):
        self.refresh_category_filter()
        self.on_search()
    
    def on_search(self):
        query = self.search_input.text()
        category = self.category_filter.currentText()
        if category == "全部分类":
            category = None
        
        # 根据当前模式搜索不同的数据
        if self.current_mode == "prompts":
            items = self.data_manager.search_prompts(query, category)
        elif self.current_mode == "api_docs":
            items = self.data_manager.search_api_docs(query, category)
        else:
            items = self.data_manager.search_api_keys(query, category)
        
        self.prompt_list.clear()
        for index, item_data in enumerate(items):
            # 创建列表项
            item = QListWidgetItem(self.prompt_list)
            
            # API 密钥使用简化显示
            if self.current_mode == "api_keys":
                # 为密钥创建简化的数据结构（用于 PromptItemWidget）
                display_data = {
                    "name": item_data.get("name", "未命名"),
                    "category": item_data.get("category", ""),
                    "tags": [],
                    "content": self._mask_api_key(item_data.get("key", ""))
                }
                widget = PromptItemWidget(display_data, self.prompt_list)
            else:
                widget = PromptItemWidget(item_data, self.prompt_list)
            
            # 设置item的尺寸提示
            item.setSizeHint(widget.sizeHint())
            
            # 存储ID
            item.setData(Qt.ItemDataRole.UserRole, item_data["id"])
            
            # 存储完整信息用于tooltip
            if self.current_mode == "api_keys":
                item.setData(Qt.ItemDataRole.UserRole + 1, {
                    'name': item_data.get("name", "未命名"),
                    'category': item_data.get("category", ""),
                    'tags': [],
                    'content': self._mask_api_key(item_data.get("key", ""))
                })
            else:
                item.setData(Qt.ItemDataRole.UserRole + 1, {
                    'name': item_data.get("name", "未命名"),
                    'category': item_data.get("category", ""),
                    'tags': item_data.get("tags", []),
                    'content': item_data.get("content", "")
                })
            
            # 添加item并设置widget
            self.prompt_list.addItem(item)
            self.prompt_list.setItemWidget(item, widget)
        
        # 确保滚动到顶部，使第一个item可见
        if items:
            self.prompt_list.scrollToTop()
            QTimer.singleShot(50, self._ensure_first_item_visible)
            QTimer.singleShot(150, self._ensure_first_item_visible)
    
    def _ensure_first_item_visible(self):
        """确保第一个item可见"""
        if self.prompt_list.count() > 0:
            self.prompt_list.scrollToTop()
            first_item = self.prompt_list.item(0)
            if first_item:
                self.prompt_list.scrollToItem(first_item, QListWidget.ScrollHint.PositionAtTop)
    
    def on_prompt_double_click(self, item):
        item_id = item.data(Qt.ItemDataRole.UserRole)
        
        if self.current_mode == "prompts":
            data = self.data_manager.get_prompt(item_id)
            if data:
                pyperclip.copy(data["content"])
                self.data_manager.increment_usage(item_id)
                self.refresh_prompt_list()
                self.show_toast(f"已复制: {data['name']}")
        elif self.current_mode == "api_docs":
            data = self.data_manager.get_api_doc(item_id)
            if data:
                pyperclip.copy(data["content"])
                self.data_manager.increment_api_doc_usage(item_id)
                self.refresh_prompt_list()
                self.show_toast(f"已复制: {data['name']}")
        else:  # api_keys
            data = self.data_manager.get_api_key(item_id)
            if data:
                pyperclip.copy(data["key"])
                self.data_manager.increment_api_key_usage(item_id)
                self.refresh_prompt_list()
                self.show_toast(f"已复制密钥: {data['name']}")
    
    def show_context_menu(self, position):
        item = self.prompt_list.itemAt(position)
        if not item:
            return
        
        menu = QMenu(self)
        menu.setStyleSheet(self._get_menu_style())
        
        copy_action = menu.addAction("📋 复制")
        edit_action = menu.addAction("✏️ 编辑")
        delete_action = menu.addAction("🗑️ 删除")
        
        action = menu.exec(self.prompt_list.mapToGlobal(position))
        
        item_id = item.data(Qt.ItemDataRole.UserRole)
        
        if self.current_mode == "prompts":
            if action == copy_action:
                data = self.data_manager.get_prompt(item_id)
                if data:
                    pyperclip.copy(data["content"])
                    self.data_manager.increment_usage(item_id)
                    self.refresh_prompt_list()
                    self.show_toast(f"已复制: {data['name']}")
            elif action == edit_action:
                self.edit_prompt(item_id)
            elif action == delete_action:
                self.delete_prompt(item_id)
        elif self.current_mode == "api_docs":
            if action == copy_action:
                data = self.data_manager.get_api_doc(item_id)
                if data:
                    pyperclip.copy(data["content"])
                    self.data_manager.increment_api_doc_usage(item_id)
                    self.refresh_prompt_list()
                    self.show_toast(f"已复制: {data['name']}")
            elif action == edit_action:
                self.edit_api_doc(item_id)
            elif action == delete_action:
                self.delete_api_doc(item_id)
        else:  # api_keys
            if action == copy_action:
                data = self.data_manager.get_api_key(item_id)
                if data:
                    pyperclip.copy(data["key"])
                    self.data_manager.increment_api_key_usage(item_id)
                    self.refresh_prompt_list()
                    self.show_toast(f"已复制密钥: {data['name']}")
            elif action == edit_action:
                self.edit_api_key(item_id)
            elif action == delete_action:
                self.delete_api_key(item_id)
    
    def quick_add_from_clipboard(self):
        """从剪贴板快速添加（AI 自动分析）"""
        import pyperclip
        
        try:
            content = pyperclip.paste().strip()
        except Exception as e:
            self.show_toast("❌ 无法读取剪贴板")
            return
        
        if not content:
            self.show_toast("❌ 剪贴板为空")
            return
        
        if len(content) < 20:
            self.show_toast("❌ 内容太短（至少20字符）")
            return
        
        # 检查 AI 是否可用
        if not self.ai_analyzer or not self.ai_analyzer.api_key:
            # 如果没有 AI，弹出手动添加对话框
            self.show_toast("💡 未配置 AI，使用手动模式")
            dialog = PromptDialog(self, categories=self.data_manager.get_categories(), ai_analyzer=self.ai_analyzer)
            # 预填充内容
            dialog.content_input.setPlainText(content)
            if dialog.exec():
                data = dialog.get_data()
                if data["name"] and data["content"]:
                    try:
                        self.data_manager.add_prompt(
                            data["name"], data["category"], data["tags"], data["content"]
                        )
                        self.refresh_prompt_list()
                        self.show_toast(f"✓ 添加成功: {data['name']}")
                    except Exception as e:
                        QMessageBox.critical(self, "添加错误", f"添加失败: {str(e)}")
            return
        
        # 显示加载提示
        self.show_toast("🤖 AI 分析中...")
        
        # 使用 QTimer 异步处理（避免阻塞UI）
        from PyQt6.QtCore import QTimer
        
        def analyze_and_save():
            try:
                # AI 分析
                result = self.ai_analyzer.analyze_prompt(content)
                
                if result:
                    # 自动保存
                    self.data_manager.add_prompt(
                        name=result['name'],
                        category=result['category'],
                        tags=result['tags'],
                        content=content
                    )
                    self.refresh_prompt_list()
                    self.show_toast(f"✓ 已保存: {result['name']}")
                else:
                    # AI 分析失败，弹出手动编辑
                    self.show_toast("⚠️ AI 失败（可能是429配额），用手动模式")
                    dialog = PromptDialog(self, categories=self.data_manager.get_categories(), ai_analyzer=self.ai_analyzer)
                    dialog.content_input.setPlainText(content)
                    if dialog.exec():
                        data = dialog.get_data()
                        if data["name"] and data["content"]:
                            self.data_manager.add_prompt(
                                data["name"], data["category"], data["tags"], data["content"]
                            )
                            self.refresh_prompt_list()
                            self.show_toast(f"✓ 添加成功: {data['name']}")
            except Exception as e:
                self.show_toast(f"❌ 错误: {str(e)}")
        
        # 延迟执行，让 Toast 先显示
        QTimer.singleShot(100, analyze_and_save)
    
    def add_prompt(self):
        """手动添加 Prompt"""
        dialog = PromptDialog(self, categories=self.data_manager.get_categories(), ai_analyzer=self.ai_analyzer)
        if dialog.exec():
            data = dialog.get_data()
            if data["name"] and data["content"]:
                try:
                    self.data_manager.add_prompt(
                        data["name"], data["category"], data["tags"], data["content"]
                    )
                    self.refresh_prompt_list()
                    self.show_toast(f"✓ 添加成功: {data['name']}")
                except Exception as e:
                    QMessageBox.critical(self, "添加错误", f"添加失败: {str(e)}")
            else:
                QMessageBox.warning(self, "输入错误", "名称和内容不能为空")
    
    def edit_prompt(self, prompt_id):
        prompt = self.data_manager.get_prompt(prompt_id)
        if not prompt:
            QMessageBox.warning(self, "错误", "未找到该 Prompt")
            return
        
        dialog = PromptDialog(self, prompt=prompt, categories=self.data_manager.get_categories())
        if dialog.exec():
            data = dialog.get_data()
            if data["name"] and data["content"]:
                try:
                    self.data_manager.update_prompt(
                        prompt_id, data["name"], data["category"], data["tags"], data["content"]
                    )
                    self.refresh_prompt_list()
                    self.show_toast(f"更新成功: {data['name']}")
                except Exception as e:
                    QMessageBox.critical(self, "更新错误", f"更新失败: {str(e)}")
            else:
                QMessageBox.warning(self, "输入错误", "名称和内容不能为空")
    
    def copy_selected_prompt(self):
        """复制选中的 Prompt（Enter/Space 键）"""
        current_item = self.prompt_list.currentItem()
        if current_item:
            prompt_id = current_item.data(Qt.ItemDataRole.UserRole)
            prompt = self.data_manager.get_prompt(prompt_id)
            if prompt:
                import pyperclip
                pyperclip.copy(prompt["content"])
                self.show_toast(f"✓ 已复制: {prompt['name']}")
    
    def delete_selected_prompt(self):
        """删除选中的 Prompt（Delete 键）"""
        current_item = self.prompt_list.currentItem()
        if current_item:
            prompt_id = current_item.data(Qt.ItemDataRole.UserRole)
            self.delete_prompt(prompt_id)
    
    def edit_selected_prompt(self):
        """编辑选中的 Prompt（Cmd+E 键）"""
        current_item = self.prompt_list.currentItem()
        if current_item:
            prompt_id = current_item.data(Qt.ItemDataRole.UserRole)
            self.edit_prompt(prompt_id)
    
    def delete_prompt(self, prompt_id):
        prompt = self.data_manager.get_prompt(prompt_id)
        if not prompt:
            return
        
        reply = QMessageBox.question(
            self, "确认删除", 
            f"确定要删除 \"{prompt['name']}\" 吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.data_manager.delete_prompt(prompt_id)
            self.refresh_prompt_list()
            self.show_toast(f"✓ 已删除: {prompt['name']}")
    
    # ==================== API 文档相关方法 ====================
    
    def add_api_doc(self):
        """手动添加 API 文档"""
        dialog = PromptDialog(self, categories=self.data_manager.get_api_doc_categories(), ai_analyzer=self.ai_analyzer)
        dialog.setWindowTitle("添加 API 文档")
        if dialog.exec():
            data = dialog.get_data()
            if data["name"] and data["content"]:
                try:
                    self.data_manager.add_api_doc(
                        data["name"], data["category"], data["tags"], data["content"]
                    )
                    self.refresh_prompt_list()
                    self.show_toast(f"✓ 添加成功: {data['name']}")
                except Exception as e:
                    QMessageBox.critical(self, "添加错误", f"添加失败: {str(e)}")
            else:
                QMessageBox.warning(self, "输入错误", "名称和内容不能为空")
    
    def edit_api_doc(self, doc_id):
        """编辑 API 文档"""
        doc = self.data_manager.get_api_doc(doc_id)
        if not doc:
            QMessageBox.warning(self, "错误", "未找到该 API 文档")
            return
        
        dialog = PromptDialog(self, prompt=doc, categories=self.data_manager.get_api_doc_categories())
        dialog.setWindowTitle("编辑 API 文档")
        if dialog.exec():
            data = dialog.get_data()
            if data["name"] and data["content"]:
                try:
                    self.data_manager.update_api_doc(
                        doc_id, data["name"], data["category"], data["tags"], data["content"]
                    )
                    self.refresh_prompt_list()
                    self.show_toast(f"更新成功: {data['name']}")
                except Exception as e:
                    QMessageBox.critical(self, "更新错误", f"更新失败: {str(e)}")
            else:
                QMessageBox.warning(self, "输入错误", "名称和内容不能为空")
    
    def delete_api_doc(self, doc_id):
        """删除 API 文档"""
        doc = self.data_manager.get_api_doc(doc_id)
        if not doc:
            return
        
        reply = QMessageBox.question(
            self, "确认删除", 
            f"确定要删除 \"{doc['name']}\" 吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.data_manager.delete_api_doc(doc_id)
            self.refresh_prompt_list()
            self.show_toast(f"✓ 已删除: {doc['name']}")
    
    def quick_add_api_doc_from_clipboard(self):
        """从剪贴板快速添加 API 文档（使用 AI 自动分析）"""
        import pyperclip
        
        try:
            content = pyperclip.paste().strip()
        except Exception as e:
            self.show_toast("❌ 无法读取剪贴板")
            return
        
        if not content:
            self.show_toast("❌ 剪贴板为空")
            return
        
        if len(content) < 20:
            self.show_toast("❌ 内容太短（至少20字符）")
            return
        
        # 检查 AI 是否可用
        if not self.ai_analyzer or not self.ai_analyzer.api_key:
            # 如果没有 AI，弹出手动添加对话框
            self.show_toast("💡 未配置 AI，使用手动模式")
            dialog = PromptDialog(self, categories=self.data_manager.get_api_doc_categories(), ai_analyzer=self.ai_analyzer)
            dialog.setWindowTitle("添加 API 文档")
            dialog.content_input.setPlainText(content)
            if dialog.exec():
                data = dialog.get_data()
                if data["name"] and data["content"]:
                    try:
                        self.data_manager.add_api_doc(
                            data["name"], data["category"], data["tags"], data["content"]
                        )
                        self.refresh_prompt_list()
                        self.show_toast(f"✓ 添加成功: {data['name']}")
                    except Exception as e:
                        QMessageBox.critical(self, "添加错误", f"添加失败: {str(e)}")
            return
        
        # 显示加载提示
        self.show_toast("🤖 AI 分析中...")
        
        # 使用 QTimer 异步处理（避免阻塞UI）
        from PyQt6.QtCore import QTimer
        
        def analyze_and_save():
            try:
                # AI 分析
                result = self.ai_analyzer.analyze_prompt(content)
                
                if result:
                    # 自动保存
                    self.data_manager.add_api_doc(
                        name=result['name'],
                        category=result['category'],
                        tags=result['tags'],
                        content=content
                    )
                    self.refresh_prompt_list()
                    self.show_toast(f"✓ 已保存: {result['name']}")
                else:
                    # AI 分析失败，弹出手动编辑
                    self.show_toast("⚠️ AI 分析失败，使用手动模式")
                    dialog = PromptDialog(self, categories=self.data_manager.get_api_doc_categories(), ai_analyzer=self.ai_analyzer)
                    dialog.setWindowTitle("添加 API 文档")
                    dialog.content_input.setPlainText(content)
                    if dialog.exec():
                        data = dialog.get_data()
                        if data["name"] and data["content"]:
                            self.data_manager.add_api_doc(
                                data["name"], data["category"], data["tags"], data["content"]
                            )
                            self.refresh_prompt_list()
                            self.show_toast(f"✓ 添加成功: {data['name']}")
            except Exception as e:
                self.show_toast(f"❌ 错误: {str(e)}")
        
        # 延迟执行，让 Toast 先显示
        QTimer.singleShot(100, analyze_and_save)
    
    # ==================== API 密钥相关方法 ====================
    
    def _mask_api_key(self, key: str) -> str:
        """遮蔽 API 密钥，只显示前4位和后4位"""
        if not key:
            return ""
        if len(key) <= 8:
            return "*" * len(key)
        return key[:4] + "*" * (len(key) - 8) + key[-4:]
    
    def add_api_key(self):
        """添加 API 密钥"""
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox
        
        dialog = QDialog(self)
        dialog.setWindowTitle("添加 API 密钥")
        dialog.setMinimumWidth(400)
        dialog.setStyleSheet("""
            QDialog { background: #2C2C2E; }
            QLabel { color: white; font-size: 13px; }
            QLineEdit, QComboBox { 
                background: #3A3A3C; color: white; border: 1px solid #48484A; 
                border-radius: 6px; padding: 8px; font-size: 13px;
            }
            QPushButton {
                background: #FF9500; color: white; border: none; border-radius: 6px;
                padding: 10px 20px; font-size: 13px; font-weight: bold;
            }
            QPushButton:hover { background: #FFa726; }
            QPushButton#cancelBtn { background: #3A3A3C; }
            QPushButton#cancelBtn:hover { background: #48484A; }
        """)
        
        layout = QVBoxLayout(dialog)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 名称
        layout.addWidget(QLabel("名称"))
        name_input = QLineEdit()
        name_input.setPlaceholderText("例如: OpenAI API Key")
        layout.addWidget(name_input)
        
        # 密钥
        layout.addWidget(QLabel("API 密钥"))
        key_input = QLineEdit()
        key_input.setPlaceholderText("粘贴你的 API 密钥")
        layout.addWidget(key_input)
        
        # 分类（可选）
        layout.addWidget(QLabel("分类（可选）"))
        category_input = QComboBox()
        category_input.setEditable(True)
        category_input.addItem("")
        for cat in self.data_manager.get_api_key_categories():
            category_input.addItem(cat)
        layout.addWidget(category_input)
        
        # 按钮
        btn_layout = QHBoxLayout()
        cancel_btn = QPushButton("取消")
        cancel_btn.setObjectName("cancelBtn")
        cancel_btn.clicked.connect(dialog.reject)
        btn_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("保存")
        save_btn.clicked.connect(dialog.accept)
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)
        
        if dialog.exec():
            name = name_input.text().strip()
            key = key_input.text().strip()
            category = category_input.currentText().strip()
            
            if name and key:
                self.data_manager.add_api_key(name, key, category)
                self.refresh_prompt_list()
                self.show_toast(f"✓ 已添加: {name}")
            else:
                self.show_toast("❌ 名称和密钥不能为空")
    
    def edit_api_key(self, key_id):
        """编辑 API 密钥"""
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox
        
        api_key = self.data_manager.get_api_key(key_id)
        if not api_key:
            self.show_toast("❌ 未找到该密钥")
            return
        
        dialog = QDialog(self)
        dialog.setWindowTitle("编辑 API 密钥")
        dialog.setMinimumWidth(400)
        dialog.setStyleSheet("""
            QDialog { background: #2C2C2E; }
            QLabel { color: white; font-size: 13px; }
            QLineEdit, QComboBox { 
                background: #3A3A3C; color: white; border: 1px solid #48484A; 
                border-radius: 6px; padding: 8px; font-size: 13px;
            }
            QPushButton {
                background: #FF9500; color: white; border: none; border-radius: 6px;
                padding: 10px 20px; font-size: 13px; font-weight: bold;
            }
            QPushButton:hover { background: #FFa726; }
            QPushButton#cancelBtn { background: #3A3A3C; }
            QPushButton#cancelBtn:hover { background: #48484A; }
        """)
        
        layout = QVBoxLayout(dialog)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 名称
        layout.addWidget(QLabel("名称"))
        name_input = QLineEdit()
        name_input.setText(api_key["name"])
        layout.addWidget(name_input)
        
        # 密钥
        layout.addWidget(QLabel("API 密钥"))
        key_input = QLineEdit()
        key_input.setText(api_key["key"])
        layout.addWidget(key_input)
        
        # 分类
        layout.addWidget(QLabel("分类（可选）"))
        category_input = QComboBox()
        category_input.setEditable(True)
        category_input.addItem("")
        for cat in self.data_manager.get_api_key_categories():
            category_input.addItem(cat)
        category_input.setCurrentText(api_key.get("category", ""))
        layout.addWidget(category_input)
        
        # 按钮
        btn_layout = QHBoxLayout()
        cancel_btn = QPushButton("取消")
        cancel_btn.setObjectName("cancelBtn")
        cancel_btn.clicked.connect(dialog.reject)
        btn_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("保存")
        save_btn.clicked.connect(dialog.accept)
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)
        
        if dialog.exec():
            name = name_input.text().strip()
            key = key_input.text().strip()
            category = category_input.currentText().strip()
            
            if name and key:
                self.data_manager.update_api_key(key_id, name, key, category)
                self.refresh_prompt_list()
                self.show_toast(f"✓ 已更新: {name}")
            else:
                self.show_toast("❌ 名称和密钥不能为空")
    
    def delete_api_key(self, key_id):
        """删除 API 密钥"""
        api_key = self.data_manager.get_api_key(key_id)
        if not api_key:
            return
        
        reply = QMessageBox.question(
            self, "确认删除", 
            f"确定要删除 \"{api_key['name']}\" 吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.data_manager.delete_api_key(key_id)
            self.refresh_prompt_list()
            self.show_toast(f"✓ 已删除: {api_key['name']}")
    
    def show_stats(self):
        stats_window = StatsWindow(self, self.data_manager)
        stats_window.exec()
    
    def import_prompts(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "导入 Prompts", "", "JSON Files (*.json)"
        )
        if file_path:
            try:
                added, skipped = self.data_manager.import_prompts(file_path)
                self.refresh_prompt_list()
                self.show_toast(f"导入完成: 添加 {added} 个, 跳过 {skipped} 个")
            except Exception as e:
                QMessageBox.critical(self, "导入错误", f"导入失败: {str(e)}")
    
    def export_prompts(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出 Prompts", "prompts.json", "JSON Files (*.json)"
        )
        if file_path:
            try:
                if self.data_manager.export_prompts(file_path):
                    self.show_toast("导出成功!")
                else:
                    QMessageBox.warning(self, "导出警告", "导出失败，请检查文件路径权限")
            except Exception as e:
                QMessageBox.critical(self, "导出错误", f"导出失败: {str(e)}")
    
    def show_toast(self, text):
        toast = ToastLabel(text, self)
        toast_width = 280
        toast_height = 50
        
        x = self.x() + (self.width() - toast_width) // 2
        y = self.y() + self.height() - toast_height - 30
        
        toast.setGeometry(x, y, toast_width, toast_height)
        toast.show_animated()
    
    def _animate_button_click(self, button):
        """按钮点击时的缩放动画"""
        # 创建缩小动画
        shrink = QPropertyAnimation(button, b"minimumSize")
        shrink.setDuration(100)
        shrink.setStartValue(button.minimumSize())
        target_size = QSize(
            max(10, button.minimumSize().width() - 4),
            max(10, button.minimumSize().height() - 2)
        )
        shrink.setEndValue(target_size)
        shrink.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # 创建恢复动画
        restore = QPropertyAnimation(button, b"minimumSize")
        restore.setDuration(150)
        restore.setStartValue(target_size)
        restore.setEndValue(button.minimumSize())
        restore.setEasingCurve(QEasingCurve.Type.OutElastic)
        
        # 连接动画
        shrink.finished.connect(restore.start)
        shrink.start()
    
    def _animate_list_item_entrance(self, item, widget, delay_ms=0):
        """列表项入场动画 - 淡入 + 下滑"""
        # 确保widget是可见的
        widget.setVisible(True)
        widget.show()
        
        # 设置初始透明度效果
        opacity_effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(opacity_effect)
        opacity_effect.setOpacity(0.0)  # 从完全透明开始
        
        # 透明度动画
        opacity_anim = QPropertyAnimation(opacity_effect, b"opacity")
        opacity_anim.setDuration(300)
        opacity_anim.setStartValue(0.0)
        opacity_anim.setEndValue(1.0)
        opacity_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # 动画完成后确保widget完全可见
        def on_animation_finished():
            widget.setVisible(True)
            widget.show()
        
        opacity_anim.finished.connect(on_animation_finished)
        
        # 延迟启动
        if delay_ms > 0:
            QTimer.singleShot(delay_ms, opacity_anim.start)
        else:
            opacity_anim.start()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
    
    def mouseMoveEvent(self, event):
        if self.dragging and not self.position_locked:
            self.move(event.globalPosition().toPoint() - self.drag_position)
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
    
    def keyPressEvent(self, event):
        """处理键盘快捷键"""
        # Esc - 隐藏窗口并显示浮动球
        if event.key() == Qt.Key.Key_Escape:
            self.hide()
            # 如果不是始终显示模式，则需要显示浮动球
            if self.floating_ball and not self.ball_always_visible:
                self.floating_ball.show()
        
        # Cmd+F - 聚焦搜索框
        elif event.key() == Qt.Key.Key_F and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.search_input.setFocus()
            self.search_input.selectAll()
        
        # Cmd+N - 新建 Prompt
        elif event.key() == Qt.Key.Key_N and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.add_prompt()
        
        # Enter/Return - 复制选中的 Prompt
        elif event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.copy_selected_prompt()
        
        # Space - 也可以复制
        elif event.key() == Qt.Key.Key_Space:
            self.copy_selected_prompt()
        
        # Delete/Backspace - 删除选中的 Prompt
        elif event.key() in (Qt.Key.Key_Delete, Qt.Key.Key_Backspace):
            self.delete_selected_prompt()
        
        # Cmd+E - 编辑选中的 Prompt
        elif event.key() == Qt.Key.Key_E and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.edit_selected_prompt()
        
        else:
            super().keyPressEvent(event)
    
    def check_mouse_position(self):
        """定期检查 - 浮动球模式检查焦点，自动折叠模式检查鼠标位置"""
        # 如果在展开保护期内，不检查
        if self.just_expanded:
            return
        
        # 浮动球模式：检查窗口是否失去焦点（点击外部的可靠标志）
        if self.floating_ball:
            # 窗口可见但不是活动窗口 = 用户点击了外部
            if self.isVisible() and not self.isActiveWindow():
                self.hide_to_ball()
            return
        
        # 自动折叠模式：检查鼠标位置
        if not self.auto_collapse_enabled:
            return
        
        # 获取鼠标全局位置
        mouse_pos = QCursor.pos()
        # 检查鼠标是否在窗口内
        is_mouse_inside = self.geometry().contains(mouse_pos)
        
        # 如果是预览tooltip窗口，也算作"在窗口内"
        if self.current_tooltip and self.current_tooltip.isVisible():
            if self.current_tooltip.geometry().contains(mouse_pos):
                is_mouse_inside = True
        
        if is_mouse_inside:
            # 鼠标在窗口内，需要展开
            if self.is_collapsed:
                self.expand_window()
        else:
            # 鼠标不在窗口内，折叠窗口
            if not self.is_collapsed:
                self.collapse_window()
    
    def collapse_window(self):
        """折叠窗口 - 上下折叠成一行显示鼓励语"""
        if self.is_collapsed:
            return
        
        # 隐藏预览tooltip
        self.hide_prompt_preview()
        
        # 保存当前高度（展开状态的高度）
        self.expanded_height = self.height()
        
        # 临时降低最小高度，允许折叠到目标高度
        self.setMinimumHeight(self.collapsed_height)
        
        # 标记为折叠状态
        self.is_collapsed = True
        
        # 获取随机鼓励语并替换标题
        import random
        encouragement = random.choice(self.encouragements)
        self.title_label.setText(encouragement)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("""
            color: #FF9500;
            font-size: 15px;
            font-weight: 600;
            background: transparent;
        """)
        
        # 创建折叠动画
        if self.collapse_animation:
            self.collapse_animation.stop()
        
        self.collapse_animation = QPropertyAnimation(self, b"size")
        self.collapse_animation.setDuration(180)  # 更快，180ms
        self.collapse_animation.setStartValue(self.size())
        self.collapse_animation.setEndValue(QSize(self.width(), self.collapsed_height))
        self.collapse_animation.setEasingCurve(QEasingCurve.Type.OutCubic)  # 使用 OutCubic，更平滑
        
        # 动画开始后立即隐藏内容（使用 QTimer 延迟 10ms，让动画先启动）
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(10, self._hide_content_for_collapse)
        
        self.collapse_animation.start()
    
    def _hide_content_for_collapse(self):
        """隐藏内容（折叠时调用）"""
        if hasattr(self, 'search_input'):
            self.search_input.hide()
        if hasattr(self, 'category_filter'):
            self.category_filter.hide()
        if hasattr(self, 'prompt_list'):
            self.prompt_list.hide()
        if hasattr(self, 'button_layout') and self.button_layout.count() > 0:
            self.button_layout.itemAt(0).widget().hide()  # 快速添加
        if hasattr(self, 'button_layout') and self.button_layout.count() > 1:
            self.button_layout.itemAt(1).widget().hide()  # 添加
        if hasattr(self, 'stats_btn'):
            self.stats_btn.hide()
    
    def expand_window(self):
        """展开窗口 - 上下展开并显示所有内容"""
        if not self.is_collapsed:
            return
        
        # 恢复正常的最小高度
        self.setMinimumHeight(self.normal_min_height)
        
        # 标记为展开状态
        self.is_collapsed = False
        
        # 恢复标题文本和样式
        self.title_label.setText("💡 Prompt Manager")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.title_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold; background: transparent;")
        
        # 立即显示所有内容（在动画开始前）
        if hasattr(self, 'search_input'):
            self.search_input.show()
        if hasattr(self, 'category_filter'):
            self.category_filter.show()
        if hasattr(self, 'prompt_list'):
            self.prompt_list.show()
        if hasattr(self, 'button_layout') and self.button_layout.count() > 0:
            self.button_layout.itemAt(0).widget().show()  # 快速添加
        if hasattr(self, 'button_layout') and self.button_layout.count() > 1:
            self.button_layout.itemAt(1).widget().show()  # 添加
        if hasattr(self, 'stats_btn'):
            self.stats_btn.show()
        
        # 创建展开动画
        if self.collapse_animation:
            self.collapse_animation.stop()
        
        # 获取目标高度：优先使用保存的展开高度，否则使用配置中的高度，最后使用默认值
        if hasattr(self, 'expanded_height') and self.expanded_height > self.collapsed_height:
            target_height = self.expanded_height
        else:
            geometry = self.data_manager.config.get("window_geometry")
            target_height = geometry[1] if geometry and geometry[1] > self.collapsed_height else 600
        
        self.collapse_animation = QPropertyAnimation(self, b"size")
        self.collapse_animation.setDuration(200)  # 缩短到 200ms，更快速
        self.collapse_animation.setStartValue(self.size())
        self.collapse_animation.setEndValue(QSize(self.width(), target_height))
        self.collapse_animation.setEasingCurve(QEasingCurve.Type.OutCubic)  # 使用 OutCubic，更自然
        
        # 动画完成后，保存展开后的高度（使用 lambda 避免重复连接）
        self.collapse_animation.finished.connect(lambda: self._on_expand_finished() if not self.is_collapsed else None)
        
        self.collapse_animation.start()
    
    def _on_expand_finished(self):
        """展开动画完成后的回调"""
        # 保存展开后的实际高度
        if not self.is_collapsed:
            self.expanded_height = self.height()
    
    def toggle_auto_collapse(self, checked):
        """切换自动折叠"""
        self.auto_collapse_enabled = checked
        self.data_manager.config["auto_collapse"] = checked
        self.data_manager.save_config()
        
        if checked:
            self.mouse_check_timer.start()
            self.show_toast("✓ 自动折叠已启用")
        else:
            self.mouse_check_timer.stop()
            self.show_toast("自动折叠已禁用")
            # 如果当前是折叠状态，展开
            if self.is_collapsed:
                self.expand_window()
    
    def toggle_ball_always_visible(self, checked):
        """切换浮动球始终显示"""
        self.ball_always_visible = checked
        self.data_manager.config["ball_always_visible"] = checked
        self.data_manager.save_config()
        
        if checked:
            # 启用始终显示，确保浮动球可见
            if self.floating_ball:
                self.floating_ball.show()
                self.floating_ball.raise_()
            self.show_toast("✨ 浮动球将始终显示")
        else:
            # 禁用始终显示
            # 如果主窗口当前可见，隐藏浮动球
            if self.floating_ball and self.isVisible():
                self.floating_ball.hide()
            self.show_toast("浮动球将随窗口切换显示")
    
    def eventFilter(self, obj, event):
        """事件过滤器 - 处理列表项悬停"""
        if obj == self.prompt_list.viewport():
            if event.type() == event.Type.MouseMove:
                # 获取鼠标位置对应的列表项
                item = self.prompt_list.itemAt(event.pos())
                if item:
                    self.show_prompt_preview(item, event.globalPosition().toPoint())
                else:
                    self.hide_prompt_preview()
            elif event.type() == event.Type.Leave:
                self.hide_prompt_preview()
        
        return super().eventFilter(obj, event)
    
    def show_prompt_preview(self, item, global_pos):
        """显示 Prompt 预览 - 重新设计版"""
        # 获取存储的数据
        data = item.data(Qt.ItemDataRole.UserRole + 1)
        if not data:
            return
        
        name = data.get('name', '')
        category = data.get('category', '')
        tags = data.get('tags', [])
        content = data.get('content', '')
        
        # 创建或更新预览窗口
        if not self.current_tooltip:
            self.current_tooltip = PromptPreviewWindow(self)
        
        # 设置内容
        self.current_tooltip.set_content(name, category, tags, content)
        
        # 计算位置 - 显示在鼠标右侧
        screen = self.screen().geometry()
        preview_width = self.current_tooltip.width()
        preview_height = self.current_tooltip.height()
        
        x = global_pos.x() + 15
        y = global_pos.y() - 30
        
        # 右侧空间不足，显示在左侧
        if x + preview_width > screen.right() - 10:
            x = global_pos.x() - preview_width - 15
        
        # 确保不超出屏幕顶部和底部
        if y < screen.top() + 10:
            y = screen.top() + 10
        if y + preview_height > screen.bottom() - 10:
            y = screen.bottom() - preview_height - 10
        
        # 确保x坐标在屏幕内
        if x < screen.left() + 10:
            x = screen.left() + 10
        
        self.current_tooltip.move(x, y)
        self.current_tooltip.show()
        self.current_tooltip.raise_()
    
    def hide_prompt_preview(self):
        """隐藏 Prompt 预览"""
        if self.current_tooltip:
            self.current_tooltip.hide()
    
    def show_style_selector(self):
        """显示精美的风格选择对话框"""
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGridLayout, QScrollArea, QFrame
        from PyQt6.QtCore import Qt
        from PyQt6.QtGui import QFont
        
        dialog = QDialog(self)
        dialog.setWindowTitle("风格选择")
        dialog.setModal(True)
        dialog.setFixedSize(750, 520)
        
        # 对话框样式
        dialog.setStyleSheet("""
            QDialog {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a1a2e,
                    stop:1 #16213e
                );
            }
        """)
        
        layout = QVBoxLayout(dialog)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 顶部区域
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(255, 149, 0, 0.15),
                    stop:1 rgba(255, 149, 0, 0.05)
                );
                padding: 30px;
                border-bottom: 2px solid rgba(255, 149, 0, 0.3);
            }
        """)
        header_layout = QVBoxLayout(header)
        header_layout.setSpacing(12)
        
        # 标题
        title = QLabel("✨ 选择您的风格")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setWeight(QFont.Weight.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: #FFFFFF; background: transparent;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(title)
        
        # 副标题
        subtitle = QLabel("两种精心设计的高级渐变风格")
        subtitle.setStyleSheet("""
            color: rgba(255, 255, 255, 0.7);
            background: transparent;
            font-size: 14px;
            font-weight: 400;
            letter-spacing: 0.8px;
        """)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(subtitle)
        
        # 当前风格指示
        current_style_info = self.style_manager.STYLES[self.current_style]
        current_label = QLabel(f"当前使用：{current_style_info['icon']} {current_style_info['name']}")
        current_label.setStyleSheet("""
            color: #FF9500;
            background: rgba(255, 149, 0, 0.1);
            padding: 8px 20px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
            border: 1px solid rgba(255, 149, 0, 0.3);
        """)
        current_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(current_label)
        
        layout.addWidget(header)
        
        # 滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: rgba(255, 255, 255, 0.05);
                width: 10px;
                border-radius: 5px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 149, 0, 0.5);
                border-radius: 5px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(255, 149, 0, 0.7);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        scroll_widget = QWidget()
        scroll_widget.setStyleSheet("background: transparent;")
        scroll_layout = QGridLayout(scroll_widget)
        scroll_layout.setSpacing(20)
        scroll_layout.setContentsMargins(25, 25, 25, 25)
        
        # 创建风格卡片 - 水平排列两个
        row = 0
        col = 0
        for style_key, style_info in self.style_manager.STYLES.items():
            card = self._create_premium_style_card(style_key, style_info, dialog)
            scroll_layout.addWidget(card, row, col)
            
            col += 1
            if col >= 2:  # 每行2个
                col = 0
                row += 1
        
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll, 1)
        
        # 底部按钮区域
        footer = QFrame()
        footer.setStyleSheet("""
            QFrame {
                background: rgba(0, 0, 0, 0.3);
                padding: 20px;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        footer_layout = QHBoxLayout(footer)
        footer_layout.addStretch()
        
        close_btn = QPushButton("✕ 关闭")
        close_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.1);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                padding: 12px 35px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.15);
                border: 1px solid rgba(255, 149, 0, 0.5);
            }
            QPushButton:pressed {
                background: rgba(255, 149, 0, 0.2);
            }
        """)
        close_btn.clicked.connect(dialog.accept)
        footer_layout.addWidget(close_btn)
        
        layout.addWidget(footer)
        
        dialog.exec()
    
    def _create_premium_style_card(self, style_key, style_info, parent_dialog):
        """创建精美的风格卡片"""
        from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton
        from PyQt6.QtCore import Qt
        from PyQt6.QtGui import QFont
        
        card = QFrame()
        card.setFixedSize(320, 280)
        
        # 判断是否是当前风格
        is_current = (style_key == self.current_style)
        
        # 根据风格类型设置不同的背景色
        style_colors = {
            'premium': 'qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(45, 42, 55, 0.9), stop:0.5 rgba(32, 30, 42, 0.93), stop:1 rgba(22, 20, 32, 0.96))',
            'glass': 'qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(42, 48, 62, 0.86), stop:0.5 rgba(30, 36, 52, 0.9), stop:1 rgba(20, 26, 42, 0.94))',
            'film': 'qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba(40, 35, 30, 0.9), stop:1 rgba(30, 25, 20, 0.94))'
        }
        
        style_bg = style_colors.get(style_key, 'rgba(50, 50, 50, 0.9)')
        
        if is_current:
            card.setStyleSheet(f"""
                QFrame {{
                    background: {style_bg};
                    border: 3px solid #FF9500;
                    border-radius: 16px;
                }}
            """)
        else:
            card.setStyleSheet(f"""
                QFrame {{
                    background: {style_bg};
                    border: 2px solid rgba(255, 255, 255, 0.15);
                    border-radius: 16px;
                }}
                QFrame:hover {{
                    border: 2px solid rgba(255, 149, 0, 0.6);
                    transform: translateY(-2px);
                }}
            """)
        
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(12)
        card_layout.setContentsMargins(20, 20, 20, 20)
        
        # 大图标
        icon_label = QLabel(style_info['icon'])
        icon_font = QFont()
        icon_font.setPointSize(48)
        icon_label.setFont(icon_font)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 根据风格设置图标颜色
        icon_colors = {
            'premium': '#A78BFA',
            'glass': '#8BC6FF',
            'film': '#FF9966'
        }
        icon_label.setStyleSheet(f"color: {icon_colors.get(style_key, '#FFFFFF')}; background: transparent;")
        card_layout.addWidget(icon_label)
        
        # 名称
        name_label = QLabel(style_info['name'])
        name_font = QFont()
        name_font.setPointSize(16)
        name_font.setWeight(QFont.Weight.Bold)
        name_label.setFont(name_font)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 根据风格设置文字颜色
        text_colors = {
            'premium': '#FFFFFF',
            'glass': '#FFFFFF',
            'film': '#F0E0D0'
        }
        name_label.setStyleSheet(f"color: {text_colors.get(style_key, '#FFFFFF')}; background: transparent;")
        card_layout.addWidget(name_label)
        
        # 英文名
        name_en = QLabel(style_info['name_en'])
        name_en.setStyleSheet(f"""
            color: {text_colors.get(style_key, '#FFFFFF')};
            background: transparent;
            font-size: 11px;
            font-style: italic;
            opacity: 0.7;
        """)
        name_en.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(name_en)
        
        # 描述
        desc = QLabel(style_info['description'])
        desc.setStyleSheet(f"""
            color: {text_colors.get(style_key, '#FFFFFF')};
            background: transparent;
            font-size: 11px;
            opacity: 0.8;
        """)
        desc.setWordWrap(True)
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(desc)
        
        card_layout.addStretch()
        
        # 按钮
        if is_current:
            btn = QLabel("✓ 正在使用")
            btn.setStyleSheet("""
                QLabel {
                    background: #FF9500;
                    color: #FFFFFF;
                    border-radius: 8px;
                    padding: 10px;
                    font-size: 12px;
                    font-weight: bold;
                }
            """)
            btn.setAlignment(Qt.AlignmentFlag.AlignCenter)
            card_layout.addWidget(btn)
        else:
            btn = QPushButton("应用风格")
            btn.setStyleSheet("""
                QPushButton {
                    background: rgba(255, 149, 0, 0.9);
                    color: #FFFFFF;
                    border: none;
                    border-radius: 8px;
                    padding: 10px;
                    font-size: 12px;
                    font-weight: 700;
                }
                QPushButton:hover {
                    background: #FF9500;
                }
                QPushButton:pressed {
                    background: rgba(255, 149, 0, 0.7);
                }
            """)
            btn.clicked.connect(lambda: self.apply_and_save_style(style_key, parent_dialog))
            card_layout.addWidget(btn)
        
        return card
    
    def apply_and_save_style(self, style_key, dialog):
        """应用并保存风格"""
        self.current_style = style_key
        self.data_manager.config["ui_style"] = style_key
        self.data_manager.save_config()
        
        # 关闭对话框
        dialog.accept()
        
        # 应用风格
        self.apply_style(style_key)
        
        # 显示提示
        self.show_toast(f"✓ 已切换到 {self.style_manager.STYLES[style_key]['name']} 风格")
        
        # 强制刷新整个窗口
        self.update()
        self.repaint()
    
    def apply_style(self, style_key):
        """应用指定风格"""
        print(f"正在应用风格: {style_key}")
        stylesheet = self.style_manager.get_style_stylesheet(style_key)
        
        # Toggle grain overlay
        if hasattr(self, 'grain_overlay') and self.grain_overlay:
            if style_key == 'film':
                self.grain_overlay.show()
                self.grain_overlay.raise_()
            else:
                self.grain_overlay.hide()
        
        # 应用新样式到容器
        if hasattr(self, 'container'):
            # 先清除旧样式
            self.container.setStyleSheet("")
            # 强制处理事件
            QApplication.processEvents()
            
            # 应用新样式
            self.container.setStyleSheet(stylesheet)
            print(f"已设置样式表，长度: {len(stylesheet)}")
            
            # 强制刷新容器和所有子控件
            self.container.style().unpolish(self.container)
            self.container.style().polish(self.container)
            self.container.update()
            
            # 刷新所有子控件
            for child in self.container.findChildren(QWidget):
                child.style().unpolish(child)
                child.style().polish(child)
                child.update()
        
        # 同步更新浮动球风格
        if self.floating_ball:
            self.floating_ball.set_style(style_key)
        
        print(f"✓ 风格已应用: {self.style_manager.STYLES[style_key]['name']}")
    
    def hide_to_ball(self):
        """隐藏窗口并显示浮动球"""
        self.hide()
        # 如果浮动球不是始终显示，则需要显示它
        if self.floating_ball and not self.ball_always_visible:
            self.floating_ball.show()
        # 如果是始终显示，浮动球本来就在显示，无需额外操作
    
    def show_from_ball(self):
        """从浮动球展开显示"""
        # 计算窗口位置：在浮动球附近展开
        if self.floating_ball:
            ball_pos = self.floating_ball.pos()
            ball_size = self.floating_ball.size()
            screen = self.floating_ball.screen().geometry()
            
            # 计算浮动球中心点
            ball_center_x = ball_pos.x() + ball_size.width() // 2
            ball_center_y = ball_pos.y() + ball_size.height() // 2
            
            # 窗口大小
            window_width = self.width()
            window_height = self.height()
            
            # 默认：窗口显示在浮动球右侧
            target_x = ball_pos.x() + ball_size.width() + 10
            target_y = ball_pos.y() - (window_height - ball_size.height()) // 2
            
            # 边界检查：如果右侧空间不够，显示在左侧
            if target_x + window_width > screen.right():
                target_x = ball_pos.x() - window_width - 10
            
            # 边界检查：如果左侧空间也不够，显示在上方或下方
            if target_x < screen.left():
                target_x = ball_center_x - window_width // 2
                # 显示在下方
                target_y = ball_pos.y() + ball_size.height() + 10
                # 如果下方空间不够，显示在上方
                if target_y + window_height > screen.bottom():
                    target_y = ball_pos.y() - window_height - 10
            
            # 确保窗口完全在屏幕内
            target_x = max(screen.left(), min(target_x, screen.right() - window_width))
            target_y = max(screen.top(), min(target_y, screen.bottom() - window_height))
            
            # 移动窗口到目标位置
            self.move(target_x, target_y)
            
            # 根据配置决定是否隐藏浮动球
            if not self.ball_always_visible:
                self.floating_ball.hide()
        
        # 设置展开保护期（0.3秒内不检查鼠标位置，避免展开瞬间误触）
        self.just_expanded = True
        QTimer.singleShot(300, self._clear_expand_protection)
        
        # 显示主窗口
        self.show()
        self.raise_()
        self.activateWindow()
    
    def _clear_expand_protection(self):
        """清除展开保护期"""
        self.just_expanded = False
    
    def changeEvent(self, event):
        """窗口状态变化事件 - 监听失去焦点"""
        if event.type() == event.Type.WindowDeactivate:
            # 窗口失去焦点（用户点击了外部）
            if self.isVisible() and not self.just_expanded:
                # 延迟一点点，避免在某些情况下闪烁
                QTimer.singleShot(100, self._check_and_hide)
        super().changeEvent(event)
    
    def _check_and_hide(self):
        """检查并隐藏窗口"""
        # 再次确认窗口可见且不在保护期
        if self.isVisible() and not self.just_expanded and not self.isActiveWindow():
            self.hide_to_ball()
    
    def closeEvent(self, event):
        self.save_window_state()
        event.ignore()
        self.hide()
        # 显示浮动球（如果不是始终显示模式）
        if self.floating_ball and not self.ball_always_visible:
            self.floating_ball.show()
    
    def save_window_state(self):
        self.data_manager.config["window_position"] = [self.x(), self.y()]
        self.data_manager.config["window_geometry"] = [self.width(), self.height()]
        self.data_manager.save_config()
    
    def resizeEvent(self, event):
        """当窗口大小改变时自动保存新的尺寸"""
        super().resizeEvent(event)
        
        # Resize overlay if it exists
        if hasattr(self, 'grain_overlay') and self.grain_overlay:
            if hasattr(self, 'container'):
                self.grain_overlay.resize(self.container.size())
        
        # 如果窗口处于折叠状态，不保存尺寸（避免保存折叠后的小尺寸）
        if self.is_collapsed:
            return
        
        # 如果正在进行折叠/展开动画，不保存尺寸
        if hasattr(self, 'collapse_animation') and self.collapse_animation and self.collapse_animation.state() == QPropertyAnimation.State.Running:
            return
        
        # 更新展开状态的高度（用户手动调整大小时）
        self.expanded_height = self.height()
        
        # 更新所有列表项的字体大小以适应新宽度
        self._update_list_items_font()
        
        # 保存新的窗口尺寸到配置
        self.data_manager.config["window_geometry"] = [self.width(), self.height()]
        self.data_manager.save_config()
    
    def _update_list_items_font(self):
        """更新所有列表项的字体大小"""
        if not hasattr(self, 'prompt_list'):
            return
            
        list_width = self.prompt_list.width()
        for i in range(self.prompt_list.count()):
            item = self.prompt_list.item(i)
            widget = self.prompt_list.itemWidget(item)
            if widget and isinstance(widget, PromptItemWidget):
                widget.adjust_font_sizes(list_width)
    
    def restore_window_state(self):
        # 恢复窗口位置
        position = self.data_manager.config.get("window_position")
        if position:
            self.move(position[0], position[1])
        
        # 恢复窗口大小（如果没有保存的大小，使用默认值 450x600）
        geometry = self.data_manager.config.get("window_geometry")
        if geometry:
            self.resize(geometry[0], geometry[1])
        else:
            self.resize(450, 600)  # 默认尺寸
        
        # 初始化展开高度为当前窗口高度
        self.expanded_height = self.height()
        
        # 恢复窗口透明度
        self.setWindowOpacity(self.opacity_value)
    
    def _get_search_style(self):
        """搜索框 - 柔性黑背景 + 24px圆角"""
        return """
            QLineEdit {
                background: rgba(45, 45, 48, 0.85);
                color: rgba(255, 255, 255, 0.95);
                border: 1px solid rgba(90, 90, 95, 0.3);
                border-radius: 24px;
                padding: 14px 20px;
                font-size: 14px;
                selection-background-color: rgba(10, 132, 255, 0.35);
            }
            QLineEdit:hover {
                border: 1px solid rgba(110, 110, 115, 0.4);
                background: rgba(50, 50, 53, 0.9);
            }
            QLineEdit:focus {
                border: 1.5px solid rgba(10, 132, 255, 0.7);
                background: rgba(52, 52, 55, 0.95);
            }
        """
    
    def _get_combo_style(self):
        """下拉框 - 柔和圆角 + 微光"""
        return """
            QComboBox {
                background: rgba(45, 45, 48, 0.85);
                color: rgba(255, 255, 255, 0.95);
                border: 1px solid rgba(90, 90, 95, 0.3);
                border-radius: 20px;
                padding: 11px 16px;
                font-size: 13px;
                min-height: 20px;
            }
            QComboBox:hover {
                border: 1px solid rgba(110, 110, 115, 0.4);
                background: rgba(50, 50, 53, 0.9);
            }
            QComboBox:on {
                border: 1.5px solid rgba(10, 132, 255, 0.7);
            }
            QComboBox::drop-down {
                border: none;
                width: 28px;
                background: transparent;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid rgba(200, 200, 205, 0.85);
                margin-right: 8px;
            }
            QComboBox::down-arrow:hover {
                border-top: 6px solid rgba(255, 255, 255, 0.95);
            }
            QComboBox QAbstractItemView {
                background: rgba(42, 42, 46, 0.95);
                color: rgba(255, 255, 255, 0.95);
                selection-background-color: rgba(10, 132, 255, 0.4);
                border: 1px solid rgba(80, 80, 85, 0.4);
                border-radius: 16px;
                padding: 6px;
                outline: none;
            }
            QComboBox QAbstractItemView::item {
                padding: 9px 14px;
                border-radius: 12px;
                min-height: 22px;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: rgba(58, 58, 62, 0.75);
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: rgba(10, 132, 255, 0.4);
            }
        """
    
    def _get_list_style(self):
        """列表 - 柔和间距 + 透明分隔线 + 20px圆角"""
        return """
            QListWidget {
                background: rgba(38, 38, 42, 0.7);
                color: rgba(255, 255, 255, 0.95);
                border: 1px solid rgba(75, 75, 80, 0.3);
                border-radius: 24px;
                padding: 12px 8px;
                font-size: 13px;
                outline: none;
            }
            QListWidget::item {
                border-radius: 20px;
                margin: 3px 4px;
                padding: 2px 8px;
                background: rgba(48, 48, 52, 0.5);
                border: none;
            }
            QListWidget::item:hover {
                background: rgba(58, 58, 62, 0.75);
                border: 1px solid rgba(255, 255, 255, 0.08);
            }
            QListWidget::item:selected {
                background: rgba(10, 132, 255, 0.35);
                border: 1px solid rgba(10, 132, 255, 0.5);
            }
            QListWidget::item:selected:hover {
                background: rgba(20, 142, 255, 0.45);
                border: 1px solid rgba(10, 132, 255, 0.6);
            }
            QScrollBar:vertical {
                background: transparent;
                width: 5px;
                border-radius: 2px;
                margin: 2px;
            }
            QScrollBar::handle:vertical {
                background: rgba(100, 100, 105, 0.4);
                border-radius: 2px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(120, 120, 125, 0.6);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """
    
    def _get_button_style(self, bg_color):
        """按钮 - 柔和圆角 + 微光hover"""
        hover_color = self._lighten_color(bg_color)
        pressed_color = self._darken_color(bg_color)
        
        return f"""
            QPushButton {{
                background: {bg_color};
                color: rgba(255, 255, 255, 0.95);
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 26px;
                padding: 13px 22px;
                font-size: 13px;
                font-weight: 600;
                min-height: 22px;
            }}
            QPushButton:hover {{
                background: {hover_color};
                border: 1px solid rgba(255, 255, 255, 0.2);
            }}
            QPushButton:pressed {{
                background: {pressed_color};
                border: 1px solid rgba(0, 0, 0, 0.2);
                padding: 14px 22px 12px 22px;
            }}
            QPushButton:disabled {{
                background: rgba(48, 48, 52, 0.4);
                color: rgba(140, 140, 145, 0.5);
                border: 1px solid rgba(80, 80, 85, 0.2);
            }}
        """
    
    def _get_icon_button_style(self):
        """图标按钮 - 微光 + 14px圆角"""
        return """
            QPushButton {
                background: rgba(52, 52, 56, 0.65);
                color: rgba(210, 210, 215, 0.9);
                border: 1px solid rgba(85, 85, 90, 0.25);
                border-radius: 14px;
                font-size: 15px;
                font-weight: 500;
            }
            QPushButton:hover {
                background: rgba(65, 65, 70, 0.85);
                color: rgba(255, 255, 255, 0.95);
                border: 1px solid rgba(105, 105, 110, 0.35);
            }
            QPushButton:pressed {
                background: rgba(40, 40, 45, 0.9);
                border: 1px solid rgba(65, 65, 70, 0.5);
                padding: 1px 0 0 1px;
            }
        """
    
    def _get_menu_style(self):
        return """
            QMenu {
                background-color: #2C2C2E;
                color: white;
                border: 1px solid #3A3A3C;
                border-radius: 8px;
                padding: 5px;
            }
            QMenu::item {
                padding: 8px 20px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #3A3A3C;
            }
            QMenu::separator {
                height: 1px;
                background: #3A3A3C;
                margin: 5px 10px;
            }
        """
    
    def _lighten_color(self, color, amount=0.15):
        """加亮颜色"""
        if color == "#3A3A3C":
            return "#48484A" if amount > 0.1 else "#424244"
        elif color == "#FF9500":
            if amount > 0.15:
                return "#FFA726"
            elif amount > 0.05:
                return "#FFB74D"
            return "#FFCC80"
        elif color == "#48484A":
            return "#58585A"
        elif color == "#409CFF":
            return "#60ACFF"
        return color
    
    def _darken_color(self, color, amount=0.15):
        """变暗颜色"""
        if color == "#3A3A3C":
            return "#2C2C2E" if amount > 0.1 else "#323234"
        elif color == "#FF9500":
            if amount > 0.15:
                return "#E68900"
            elif amount > 0.05:
                return "#CC7A00"
            return "#B36B00"
        elif color == "#48484A":
            return "#38383A"
        elif color == "#0066CC":
            return "#0055BB"
        return color
    
    def _get_tab_style(self, is_active):
        """分区Tab按钮样式"""
        if is_active:
            return """
                QPushButton {
                    background: rgba(255, 149, 0, 0.85);
                    color: rgba(255, 255, 255, 0.95);
                    border: 1px solid rgba(255, 255, 255, 0.15);
                    border-radius: 16px;
                    padding: 8px 16px;
                    font-size: 12px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background: rgba(255, 160, 30, 0.9);
                }
            """
        else:
            return """
                QPushButton {
                    background: rgba(58, 58, 60, 0.6);
                    color: rgba(180, 180, 185, 0.9);
                    border: 1px solid rgba(85, 85, 90, 0.25);
                    border-radius: 16px;
                    padding: 8px 16px;
                    font-size: 12px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background: rgba(75, 75, 80, 0.7);
                    color: rgba(220, 220, 225, 0.95);
                }
            """
    
    def _update_tab_styles(self):
        """更新Tab按钮样式"""
        self.prompts_tab_btn.setStyleSheet(self._get_tab_style(self.current_mode == "prompts"))
        self.api_docs_tab_btn.setStyleSheet(self._get_tab_style(self.current_mode == "api_docs"))
        self.api_keys_tab_btn.setStyleSheet(self._get_tab_style(self.current_mode == "api_keys"))
    
    def switch_mode(self, mode):
        """切换分区模式"""
        if mode == self.current_mode:
            return
        
        self.current_mode = mode
        
        # 更新按钮选中状态
        self.prompts_tab_btn.setChecked(mode == "prompts")
        self.api_docs_tab_btn.setChecked(mode == "api_docs")
        self.api_keys_tab_btn.setChecked(mode == "api_keys")
        
        # 更新样式
        self._update_tab_styles()
        
        # 更新UI提示
        if mode == "prompts":
            self.search_input.setPlaceholderText("🔍 搜索 Prompts...")
            self.title_label.setText("💡 Prompt Manager")
            self.add_btn.setToolTip("手动添加 Prompt")
            self.quick_add_btn.setToolTip("从剪贴板智能添加 (Cmd+Shift+A)")
            self.quick_add_btn.show()
        elif mode == "api_docs":
            self.search_input.setPlaceholderText("🔍 搜索 API 文档...")
            self.title_label.setText("📄 API 文档库")
            self.add_btn.setToolTip("手动添加 API 文档")
            self.quick_add_btn.setToolTip("从剪贴板快速添加 API 文档")
            self.quick_add_btn.show()
        else:  # api_keys
            self.search_input.setPlaceholderText("🔍 搜索 API 密钥...")
            self.title_label.setText("🔑 API 密钥库")
            self.add_btn.setToolTip("添加 API 密钥")
            self.quick_add_btn.hide()  # 密钥不需要快速添加
        
        # 清空搜索并刷新列表
        self.search_input.clear()
        self.refresh_prompt_list()
    
    def on_add_click(self):
        """根据当前模式添加条目"""
        if self.current_mode == "prompts":
            self.add_prompt()
        elif self.current_mode == "api_docs":
            self.add_api_doc()
        else:
            self.add_api_key()
    
    def on_quick_add_click(self):
        """根据当前模式快速添加"""
        if self.current_mode == "prompts":
            self.quick_add_from_clipboard()
        elif self.current_mode == "api_docs":
            self.quick_add_api_doc_from_clipboard()
        # api_keys 不需要快速添加
    
    def check_first_run(self):
        """检查是否首次运行，询问是否启用开机自启动"""
        # 检查是否已经询问过
        if self.data_manager.config.get("asked_autostart", False):
            return
        
        # 延迟显示对话框，等待主窗口完全加载
        QTimer.singleShot(1000, self.show_autostart_dialog)
    
    def show_autostart_dialog(self):
        """显示开机自启动询问对话框"""
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QCheckBox
        
        dialog = QDialog(self)
        dialog.setWindowTitle("欢迎使用 Prompt Manager")
        dialog.setModal(True)
        dialog.setMinimumWidth(450)
        
        layout = QVBoxLayout(dialog)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # 欢迎标题
        title = QLabel("🎉 欢迎使用 Prompt Manager！")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        layout.addWidget(title)
        
        # 说明文字
        desc = QLabel(
            "这是一个优雅的 Prompt 管理工具。\n\n"
            "您可以启用「开机自启动」功能，让程序在系统启动时\n"
            "自动在后台运行，随时按 Ctrl+Shift+P 即可调用。"
        )
        desc.setStyleSheet("color: #E5E5E7; font-size: 13px; line-height: 1.6;")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # 功能说明
        features = QLabel(
            "✨ 主要功能：\n"
            "  • 管理和分类您的 Prompt 模板\n"
            "  • 双击列表项即可复制到剪贴板\n"
            "  • 全局快捷键 Ctrl+Shift+P 随时调用\n"
            "  • 支持搜索、筛选、导入导出"
        )
        features.setStyleSheet("color: #C0C0C2; font-size: 12px; padding: 10px; background-color: rgba(50, 50, 52, 0.5); border-radius: 8px;")
        layout.addWidget(features)
        
        # 询问区域
        question_layout = QVBoxLayout()
        question_layout.setSpacing(12)
        
        question = QLabel("💡 是否启用开机自启动？")
        question.setStyleSheet("font-size: 15px; font-weight: 600; color: white;")
        question_layout.addWidget(question)
        
        hint = QLabel("（开启后，每次开机程序会自动在后台运行）")
        hint.setStyleSheet("font-size: 11px; color: #A0A0A2;")
        question_layout.addWidget(hint)
        
        layout.addLayout(question_layout)
        
        # 不再询问选项
        self.dont_ask_checkbox = QCheckBox("不再询问")
        self.dont_ask_checkbox.setStyleSheet("""
            QCheckBox {
                color: #A0A0A2;
                font-size: 12px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border-radius: 3px;
                border: 1.5px solid rgba(80, 80, 82, 0.6);
                background-color: rgba(44, 44, 46, 0.8);
            }
            QCheckBox::indicator:hover {
                border: 1.5px solid rgba(100, 100, 102, 0.8);
            }
            QCheckBox::indicator:checked {
                background-color: #FF9500;
                border: 1.5px solid #FF9500;
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNMTAgM0w0LjUgOC41TDIgNiIgc3Ryb2tlPSJ3aGl0ZSIgc3Ryb2tlLXdpZHRoPSIyIiBmaWxsPSJub25lIi8+PC9zdmc+);
            }
        """)
        layout.addWidget(self.dont_ask_checkbox)
        
        layout.addSpacing(10)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        no_btn = QPushButton("暂不启用")
        no_btn.setStyleSheet(self._get_button_style("#3A3A3C"))
        no_btn.setMinimumWidth(110)
        no_btn.setMinimumHeight(38)
        no_btn.clicked.connect(lambda: self.handle_autostart_choice(dialog, False))
        button_layout.addWidget(no_btn)
        
        yes_btn = QPushButton("✓ 启用")
        yes_btn.setStyleSheet(self._get_button_style("#FF9500"))
        yes_btn.setMinimumWidth(110)
        yes_btn.setMinimumHeight(38)
        yes_btn.clicked.connect(lambda: self.handle_autostart_choice(dialog, True))
        button_layout.addWidget(yes_btn)
        
        layout.addLayout(button_layout)
        
        # 设置对话框样式
        dialog.setStyleSheet("""
            QDialog {
                background-color: #1C1C1E;
                border-radius: 12px;
            }
        """)
        
        dialog.exec()
    
    def handle_autostart_choice(self, dialog, enable):
        """处理开机自启动选择"""
        # 标记已询问
        self.data_manager.config["asked_autostart"] = True
        self.data_manager.save_config()
        
        if enable:
            # 启用开机自启动
            import subprocess
            import sys
            autostart_script = Path(__file__).parent / "autostart.py"
            
            try:
                result = subprocess.run(
                    [sys.executable, str(autostart_script), "enable"],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    self.show_toast("✓ 开机自启动已启用")
                else:
                    QMessageBox.warning(self, "启用失败", f"启用开机自启动时出错：\n{result.stderr}")
            except Exception as e:
                QMessageBox.warning(self, "启用失败", f"启用开机自启动时出错：\n{str(e)}")
        else:
            # 根据"不再询问"选项显示不同消息
            if self.dont_ask_checkbox.isChecked():
                self.show_toast("已记住您的选择")
            else:
                self.show_toast("可随时在设置中启用")
        
        dialog.accept()
    
    def show_autostart_settings(self):
        """显示开机自启动设置对话框"""
        import subprocess
        import sys
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
        
        # 检查当前状态
        autostart_script = Path(__file__).parent / "autostart.py"
        try:
            result = subprocess.run(
                [sys.executable, str(autostart_script), "status"],
                capture_output=True,
                text=True
            )
            is_enabled = "已启用" in result.stdout
        except:
            is_enabled = False
        
        # 创建对话框
        dialog = QDialog(self)
        dialog.setWindowTitle("开机自启动设置")
        dialog.setModal(True)
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout(dialog)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # 状态显示
        status_label = QLabel(f"当前状态: {'✅ 已启用' if is_enabled else '❌ 未启用'}")
        status_label.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {'#FF9500' if is_enabled else '#8E8E93'};")
        layout.addWidget(status_label)
        
        # 说明
        desc = QLabel(
            "开机自启动功能可以让 Prompt Manager\n"
            "在系统启动时自动在后台运行，\n"
            "随时按 Ctrl+Shift+P 即可调用。"
        )
        desc.setStyleSheet("color: #E5E5E7; font-size: 13px;")
        layout.addWidget(desc)
        
        layout.addSpacing(10)
        
        # 按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        if is_enabled:
            disable_btn = QPushButton("禁用开机自启动")
            disable_btn.setStyleSheet(self._get_button_style("#636366"))
            disable_btn.setMinimumWidth(140)
            disable_btn.setMinimumHeight(38)
            disable_btn.clicked.connect(lambda: self.toggle_autostart(dialog, False))
            button_layout.addWidget(disable_btn)
        else:
            enable_btn = QPushButton("✓ 启用开机自启动")
            enable_btn.setStyleSheet(self._get_button_style("#FF9500"))
            enable_btn.setMinimumWidth(140)
            enable_btn.setMinimumHeight(38)
            enable_btn.clicked.connect(lambda: self.toggle_autostart(dialog, True))
            button_layout.addWidget(enable_btn)
        
        close_btn = QPushButton("关闭")
        close_btn.setStyleSheet(self._get_button_style("#3A3A3C"))
        close_btn.setMinimumWidth(100)
        close_btn.setMinimumHeight(38)
        close_btn.clicked.connect(dialog.accept)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
        dialog.setStyleSheet("QDialog { background-color: #1C1C1E; }")
        dialog.exec()
    
    def toggle_autostart(self, dialog, enable):
        """切换开机自启动状态"""
        import subprocess
        import sys
        
        autostart_script = Path(__file__).parent / "autostart.py"
        command = "enable" if enable else "disable"
        
        try:
            result = subprocess.run(
                [sys.executable, str(autostart_script), command],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.show_toast(f"✓ 已{'启用' if enable else '禁用'}开机自启动")
                dialog.accept()
            else:
                QMessageBox.warning(self, "操作失败", f"操作时出错：\n{result.stderr}")
        except Exception as e:
            QMessageBox.warning(self, "操作失败", f"操作时出错：\n{str(e)}")
    
    def show_ai_settings(self):
        """显示 AI 设置对话框"""
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit
        
        dialog = QDialog(self)
        dialog.setWindowTitle("AI 分析设置")
        dialog.setModal(True)
        dialog.setMinimumWidth(500)
        
        layout = QVBoxLayout(dialog)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # 标题
        title = QLabel("🤖 Gemini AI 分析设置")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        layout.addWidget(title)
        
        # 说明
        desc = QLabel(
            "配置 Google Gemini API Key 后，\n"
            "可以使用 AI 自动分析 Prompt 内容，\n"
            "智能生成名称、分类和标签。"
        )
        desc.setStyleSheet("color: #E5E5E7; font-size: 13px;")
        layout.addWidget(desc)
        
        # API Key 输入
        key_label = QLabel("API Key:")
        key_label.setStyleSheet("color: white; font-size: 14px; margin-top: 10px;")
        layout.addWidget(key_label)
        
        api_key_input = QLineEdit()
        api_key_input.setPlaceholderText("请输入 Google Gemini API Key")
        current_key = self.data_manager.config.get("gemini_api_key", "")
        if current_key:
            api_key_input.setText(current_key)
        api_key_input.setStyleSheet("""
            QLineEdit {
                background-color: #2C2C2E;
                color: white;
                border: 1.5px solid rgba(80, 80, 82, 0.6);
                border-radius: 8px;
                padding: 10px 14px;
                font-size: 13px;
                font-family: monospace;
            }
            QLineEdit:focus {
                border: 2px solid #FF9500;
            }
        """)
        layout.addWidget(api_key_input)
        
        # 获取 API Key 提示
        hint = QLabel(
            "💡 获取 API Key: <a href='https://aistudio.google.com/apikey' style='color:#FF9500;'>Google AI Studio</a>"
        )
        hint.setOpenExternalLinks(True)
        hint.setStyleSheet("color: #A0A0A2; font-size: 12px;")
        layout.addWidget(hint)
        
        # 测试按钮
        test_layout = QHBoxLayout()
        test_btn = QPushButton("测试连接")
        test_btn.setStyleSheet(self._get_button_style("#3A3A3C"))
        test_btn.setMinimumHeight(36)
        
        test_result_label = QLabel("")
        test_result_label.setStyleSheet("color: #E5E5E7; font-size: 12px;")
        
        def test_api():
            key = api_key_input.text().strip()
            if not key:
                test_result_label.setText("❌ 请先输入 API Key")
                test_result_label.setStyleSheet("color: #8E8E93;")
                return
            
            test_result_label.setText("⏳ 测试中...")
            test_result_label.setStyleSheet("color: #FFA500;")
            dialog.repaint()
            
            from ai_analyzer import AIAnalyzer
            test_analyzer = AIAnalyzer(key)
            success, message = test_analyzer.test_connection()
            
            if success:
                test_result_label.setText(f"✅ {message}")
                test_result_label.setStyleSheet("color: #FF9500;")
            else:
                test_result_label.setText(f"❌ {message}")
                test_result_label.setStyleSheet("color: #8E8E93;")
        
        test_btn.clicked.connect(test_api)
        test_layout.addWidget(test_btn)
        test_layout.addWidget(test_result_label)
        test_layout.addStretch()
        layout.addLayout(test_layout)
        
        layout.addSpacing(10)
        
        # 按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_btn = QPushButton("取消")
        cancel_btn.setStyleSheet(self._get_button_style("#3A3A3C"))
        cancel_btn.setMinimumWidth(100)
        cancel_btn.setMinimumHeight(38)
        cancel_btn.clicked.connect(dialog.reject)
        button_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("✓ 保存")
        save_btn.setStyleSheet(self._get_button_style("#FF9500"))
        save_btn.setMinimumWidth(100)
        save_btn.setMinimumHeight(38)
        
        def save_settings():
            key = api_key_input.text().strip()
            self.data_manager.config["gemini_api_key"] = key
            self.data_manager.save_config()
            self.ai_analyzer.set_api_key(key)
            self.show_toast("✓ AI 设置已保存")
            dialog.accept()
        
        save_btn.clicked.connect(save_settings)
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
        
        dialog.setStyleSheet("QDialog { background-color: #1C1C1E; }")
        dialog.exec()
