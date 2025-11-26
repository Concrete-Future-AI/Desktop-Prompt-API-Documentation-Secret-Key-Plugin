from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy, QGraphicsOpacityEffect
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QFontMetrics, QFont, QPainter, QColor, QLinearGradient
import re


class PromptItemWidget(QWidget):
    """自定义的 Prompt 列表项 Widget - 自适应字体和多行布局"""
    
    @staticmethod
    def _clean_text_static(text):
        """静态方法：清理文本 - 移除标记和多余空白"""
        if not text:
            return ""
        
        # 移除 <...> 这样的标记（包括 <use_interesting_fonts> 等）
        text = re.sub(r'<[^>]+>', '', text)
        
        # 移除 XML/HTML 实体
        text = re.sub(r'&[a-zA-Z]+;', '', text)
        
        # 移除多余的空白和换行，合并成单行
        text = " ".join(text.split())
        
        return text.strip()
    
    def __init__(self, prompt_data, parent=None):
        super().__init__(parent)
        self.prompt_data = prompt_data
        # 只显示两行（名称+分类标签），内容通过tooltip显示
        self.item_height = 72
        
        # 悬停状态和动画
        self._hover_progress = 0.0
        self._hover_animation = None
        self.setMouseTracking(True)
        
        # 提取数据并清理
        raw_name = prompt_data.get("name", "未命名")
        self.name = self._clean_text_static(raw_name) if raw_name != "未命名" else raw_name
        if not self.name:
            self.name = "未命名"
            
        self.category = prompt_data.get("category", "")
        self.tags = prompt_data.get("tags", [])
        self.content = prompt_data.get("content", "")
        self.usage_count = prompt_data.get("usage_count", 0)
        
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(4)
        
        # 第一行：名称
        self.name_label = QLabel(self.name)
        self.name_label.setWordWrap(True)
        # 初始设置字体 - 增强视觉层次
        name_font = QFont()
        name_font.setPointSize(16)
        name_font.setWeight(QFont.Weight.Bold)
        name_font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 0.3)
        self.name_label.setFont(name_font)
        self.name_label.setStyleSheet("""
            color: rgba(255, 255, 255, 0.97);
            background: transparent;
        """)
        layout.addWidget(self.name_label)
        
        # 第二行：分类 + 标签
        meta_text = self._build_meta_text()
        self.meta_label = QLabel(meta_text)
        self.meta_label.setWordWrap(True)
        # 初始设置字体 - 更精致的二级信息
        meta_font = QFont()
        meta_font.setPointSize(12)
        meta_font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 0.2)
        self.meta_label.setFont(meta_font)
        self.meta_label.setStyleSheet("""
            color: rgba(180, 180, 195, 0.85);
            background: transparent;
        """)
        layout.addWidget(self.meta_label)
        
        # 不使用原生Qt tooltip（黄色背景，简陋）
        # 只使用MainWindow中的自定义tooltip（美观，完整内容）
        
        # 设置尺寸策略
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
    def _build_meta_text(self):
        """构建分类和标签文本"""
        parts = []
        if self.category:
            # 清理分类文本
            clean_category = self._clean_text_static(self.category)
            if clean_category:
                parts.append(f"[{clean_category}]")
        if self.tags:
            # 限制标签数量，避免太长，并清理每个标签
            clean_tags = []
            for tag in self.tags[:5]:
                clean_tag = self._clean_text_static(tag)
                if clean_tag:
                    clean_tags.append(f"#{clean_tag}")
            if clean_tags:
                parts.append(" ".join(clean_tags))
        if self.usage_count > 0:
            parts.append(f"({self.usage_count}次)")
        return " ".join(parts) if parts else "无分类"
    
    def sizeHint(self):
        """返回推荐大小 - 紧凑布局"""
        # 使用固定的紧凑高度计算
        # 名称：最多1.5行 = ~30px
        # 分类标签：1行 = ~18px  
        # Margins: 12+12 = 24px
        # Spacing: 6px
        # 总计: 约78px
        
        return QSize(self.width(), 78)
    
    def adjust_font_sizes(self, available_width):
        """根据可用宽度自适应调整字体大小"""
        # 减去边距
        text_width = available_width - 24  # 左右边距各12px
        
        # 调整名称字体
        self._adjust_label_font(self.name_label, self.name, text_width, 
                                [16, 15, 14], max_lines=2)
        
        # 调整分类标签字体
        meta_text = self._build_meta_text()
        self._adjust_label_font(self.meta_label, meta_text, text_width,
                                [13, 12, 11], max_lines=2)
        
    def _adjust_label_font(self, label, text, max_width, font_sizes, max_lines=1):
        """调整标签字体大小以适应宽度"""
        for size in font_sizes:
            font = QFont()
            font.setPointSize(size)
            font.setWeight(QFont.Weight.DemiBold if label == self.name_label else QFont.Weight.Normal)
            label.setFont(font)
            
            metrics = QFontMetrics(font)
            
            # 计算文本所需的高度
            rect = metrics.boundingRect(0, 0, max_width, 1000, 
                                       Qt.TextFlag.TextWordWrap, text)
            
            # 计算实际行数
            line_height = metrics.height()
            actual_lines = (rect.height() + line_height - 1) // line_height
            
            # 如果行数符合要求，使用此字号
            if actual_lines <= max_lines:
                return
        
        # 如果所有字号都不合适，使用最小的并启用省略
        font = QFont()
        font.setPointSize(font_sizes[-1])
        font.setWeight(QFont.Weight.DemiBold if label == self.name_label else QFont.Weight.Normal)
        label.setFont(font)
        
    def resizeEvent(self, event):
        """窗口大小改变时重新调整字体"""
        super().resizeEvent(event)
        self.adjust_font_sizes(self.width())
    
    # 悬停动画属性
    @pyqtProperty(float)
    def hover_progress(self):
        """获取悬停进度值"""
        return self._hover_progress
    
    @hover_progress.setter
    def hover_progress(self, value):
        """设置悬停进度值并触发重绘"""
        self._hover_progress = value
        self.update()
    
    def enterEvent(self, event):
        """鼠标进入时触发渐变悬停效果"""
        super().enterEvent(event)
        self._animate_hover(1.0)
    
    def leaveEvent(self, event):
        """鼠标离开时恢复"""
        super().leaveEvent(event)
        self._animate_hover(0.0)
    
    def _animate_hover(self, target_value):
        """平滑动画悬停进度"""
        if self._hover_animation:
            self._hover_animation.stop()
        
        self._hover_animation = QPropertyAnimation(self, b"hover_progress")
        self._hover_animation.setDuration(200)
        self._hover_animation.setStartValue(self._hover_progress)
        self._hover_animation.setEndValue(target_value)
        self._hover_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._hover_animation.start()
    
    def paintEvent(self, event):
        """自定义绘制 - 添加悬停高亮效果"""
        super().paintEvent(event)
        
        if self._hover_progress > 0:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            # 根据悬停进度计算透明度
            alpha = int(self._hover_progress * 25)  # 最大25的alpha值
            
            # 绘制微妙的高亮边框
            highlight_color = QColor(255, 255, 255, alpha)
            painter.setPen(highlight_color)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 22, 22)
