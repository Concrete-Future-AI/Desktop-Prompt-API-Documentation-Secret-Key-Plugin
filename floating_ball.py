#!/usr/bin/env python3
"""
浮动球窗口 - 现代玻璃拟态设计
极致精美的UI设计，灵感来自iOS和macOS的设计语言
"""

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGraphicsDropShadowEffect, QGraphicsBlurEffect
from PyQt6.QtCore import Qt, QPoint, QPointF, QPropertyAnimation, QEasingCurve, QTimer, pyqtSignal, QRect, QRectF, QVariantAnimation
from PyQt6.QtGui import (QPainter, QColor, QRadialGradient, QPen, QFont,
                          QLinearGradient, QConicalGradient, QPainterPath)
import math


class FloatingBall(QWidget):
    """现代化浮动球 - 玻璃拟态设计"""
    
    # 信号：点击球时发出
    clicked = pyqtSignal()
    
    def __init__(self, data_manager, style="premium"):
        super().__init__()
        self.data_manager = data_manager
        self.style = style
        self.dragging = False
        self.drag_position = QPoint()
        self.press_global_pos = None
        self.is_animating = False
        self.hover = False
        self.has_focus = False  # 追踪焦点状态
        
        # 球的大小 - 60px提供更好的设计空间
        self.ball_size = 60
        
        # 动画相关
        self.pulse_value = 0.0  # 脉冲动画值 0.0-1.0
        self.glow_opacity = 0.0  # 光晕透明度
        
        self.init_ui()
        self.load_position()
        self.start_pulse_animation()
        
    def init_ui(self):
        """初始化UI"""
        # 设置窗口属性 - 与主窗口相同的配置，确保真正的始终置顶
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
            # 移除Tool类型！Tool会让窗口自动"让路"，导致无法真正置顶
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # 设置固定大小
        self.setFixedSize(self.ball_size, self.ball_size)
        
        # 工具提示
        self.setToolTip("Prompt Manager\n点击展开 • 拖拽移动")
        
    def start_pulse_animation(self):
        """启动微妙的脉冲动画"""
        self.pulse_animation = QVariantAnimation(self)
        self.pulse_animation.setStartValue(0.0)
        self.pulse_animation.setEndValue(1.0)
        self.pulse_animation.setDuration(3000)  # 3秒一个周期
        self.pulse_animation.setLoopCount(-1)  # 无限循环
        self.pulse_animation.setEasingCurve(QEasingCurve.Type.InOutSine)
        self.pulse_animation.valueChanged.connect(self.on_pulse_changed)
        self.pulse_animation.start()
    
    def on_pulse_changed(self, value):
        """脉冲值变化"""
        self.pulse_value = value
        # 仅在非悬停状态下使用脉冲效果
        if not self.hover:
            self.update()
        
    def paintEvent(self, event):
        """绘制现代化的浮动球"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        
        # 中心点和半径
        center_x = self.ball_size / 2
        center_y = self.ball_size / 2
        center = QPointF(center_x, center_y)
        base_radius = self.ball_size / 2 - 8
        
        # 悬停和脉冲效果
        if self.hover:
            radius = base_radius * 1.05
            glow_alpha = 60
        else:
            # 微妙的脉冲效果（±2%）
            pulse_scale = 1.0 + math.sin(self.pulse_value * 2 * math.pi) * 0.02
            radius = base_radius * pulse_scale
            glow_alpha = int(30 + math.sin(self.pulse_value * 2 * math.pi) * 15)
        
        # 1. 外发光效果
        self.draw_outer_glow(painter, center, radius, glow_alpha)
        
        # 2. 主球体 - 玻璃拟态效果
        self.draw_glass_ball(painter, center, radius)
        
        # 3. 内部装饰
        self.draw_inner_decoration(painter, center, radius)
        
        # 4. 图标
        self.draw_icon(painter, center)
        
        # 5. 边缘高光
        self.draw_edge_highlight(painter, center, radius)
    
    def draw_outer_glow(self, painter, center, radius, alpha):
        """绘制外发光"""
        glow_radius = radius + 10
        
        gradient = QRadialGradient(center, glow_radius)
        
        if self.style == "premium":
            # 紫色光晕
            gradient.setColorAt(0.7, QColor(138, 99, 210, alpha))
            gradient.setColorAt(1.0, QColor(138, 99, 210, 0))
        else:
            # 蓝色光晕
            gradient.setColorAt(0.7, QColor(99, 150, 220, alpha))
            gradient.setColorAt(1.0, QColor(99, 150, 220, 0))
        
        painter.setBrush(gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(center, glow_radius, glow_radius)
    
    def draw_glass_ball(self, painter, center, radius):
        """绘制玻璃拟态主球体"""
        # 主渐变 - 从上到下
        gradient = QLinearGradient(center.x(), center.y() - radius, 
                                   center.x(), center.y() + radius)
        
        if self.style == "premium":
            # 紫色玻璃球
            gradient.setColorAt(0.0, QColor(178, 149, 240, 200))
            gradient.setColorAt(0.5, QColor(138, 99, 210, 220))
            gradient.setColorAt(1.0, QColor(108, 69, 180, 240))
        else:
            # 蓝色玻璃球
            gradient.setColorAt(0.0, QColor(159, 210, 255, 200))
            gradient.setColorAt(0.5, QColor(99, 150, 220, 220))
            gradient.setColorAt(1.0, QColor(69, 120, 190, 240))
        
        painter.setBrush(gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(center, radius, radius)
        
        # 玻璃高光 - 上半部分
        highlight = QRadialGradient(
            QPointF(center.x() - radius * 0.3, center.y() - radius * 0.3),
            radius * 0.7
        )
        highlight.setColorAt(0.0, QColor(255, 255, 255, 100))
        highlight.setColorAt(0.5, QColor(255, 255, 255, 40))
        highlight.setColorAt(1.0, QColor(255, 255, 255, 0))
        
        painter.setBrush(highlight)
        painter.drawEllipse(center, radius, radius)
    
    def draw_inner_decoration(self, painter, center, radius):
        """绘制内部装饰 - 同心圆环"""
        # 内圈 - 半透明边框
        inner_radius = radius * 0.7
        
        if self.style == "premium":
            pen_color = QColor(200, 170, 255, 80)
        else:
            pen_color = QColor(170, 220, 255, 80)
        
        pen = QPen(pen_color)
        pen.setWidth(1)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(center, inner_radius, inner_radius)
        
        # 更小的内圈
        inner_radius2 = radius * 0.5
        pen.setColor(QColor(pen_color.red(), pen_color.green(), pen_color.blue(), 40))
        painter.setPen(pen)
        painter.drawEllipse(center, inner_radius2, inner_radius2)
    
    def draw_icon(self, painter, center):
        """绘制中心图标"""
        # 图标
        if self.style == "premium":
            icon_text = "✨"
            icon_color = QColor(255, 255, 255, 240)
        else:
            icon_text = "🔮"
            icon_color = QColor(255, 255, 255, 240)
        
        font = QFont()
        font.setPointSize(22)  # 使用系统字体
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(icon_color)
        
        # 居中绘制
        text_rect = QRectF(center.x() - 15, center.y() - 15, 30, 30)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, icon_text)
    
    def draw_edge_highlight(self, painter, center, radius):
        """绘制边缘高光"""
        # 顶部弧形高光
        path = QPainterPath()
        rect = QRectF(center.x() - radius, center.y() - radius, 
                      radius * 2, radius * 2)
        path.arcMoveTo(rect, 135)
        path.arcTo(rect, 135, -90)  # 从135度到45度的弧
        
        if self.style == "premium":
            edge_color = QColor(200, 170, 255, 100)
        else:
            edge_color = QColor(170, 220, 255, 100)
        
        pen = QPen(edge_color)
        pen.setWidth(2)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(path)
        
        # 整体边缘
        edge_pen = QPen(QColor(255, 255, 255, 30))
        edge_pen.setWidth(1)
        painter.setPen(edge_pen)
        painter.drawEllipse(center, radius - 0.5, radius - 0.5)
    
    def mousePressEvent(self, event):
        """鼠标按下"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.press_global_pos = event.globalPosition().toPoint()
            self.drag_position = self.press_global_pos - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """鼠标移动 - 拖拽"""
        if self.dragging:
            new_pos = event.globalPosition().toPoint() - self.drag_position
            self.move(new_pos)
            event.accept()
    
    def mouseReleaseEvent(self, event):
        """鼠标释放"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            
            release_pos = event.globalPosition().toPoint()
            press_pos = self.press_global_pos or release_pos
            distance = (release_pos - press_pos).manhattanLength()
            self.press_global_pos = None
            
            if distance < 5:
                self.clicked.emit()
            else:
                self.snap_to_edge()
                self.save_position()
            
            event.accept()
    
    def snap_to_edge(self):
        """吸附到屏幕边缘"""
        if self.is_animating:
            return
        
        screen = self.screen().geometry()
        current_pos = self.pos()
        
        left_distance = current_pos.x() - screen.left()
        right_distance = screen.right() - (current_pos.x() + self.width())
        top_distance = current_pos.y() - screen.top()
        bottom_distance = screen.bottom() - (current_pos.y() + self.height())
        
        min_distance = min(left_distance, right_distance, top_distance, bottom_distance)
        target_pos = QPoint(current_pos.x(), current_pos.y())
        margin = 5
        
        if min_distance == left_distance:
            target_pos.setX(screen.left() + margin)
        elif min_distance == right_distance:
            target_pos.setX(screen.right() - self.width() - margin)
        elif min_distance == top_distance:
            target_pos.setY(screen.top() + margin)
        else:
            target_pos.setY(screen.bottom() - self.height() - margin)
        
        target_pos.setX(max(screen.left() + margin, min(target_pos.x(), screen.right() - self.width() - margin)))
        target_pos.setY(max(screen.top() + margin, min(target_pos.y(), screen.bottom() - self.height() - margin)))
        
        self.animate_to_position(target_pos)
    
    def animate_to_position(self, target_pos):
        """动画移动到目标位置"""
        self.is_animating = True
        
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(400)  # 稍慢一点更优雅
        self.animation.setStartValue(self.pos())
        self.animation.setEndValue(target_pos)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.finished.connect(self._on_animation_finished)
        self.animation.start()
    
    def _on_animation_finished(self):
        """动画完成"""
        self.is_animating = False
    
    def save_position(self):
        """保存位置到配置"""
        pos = self.pos()
        self.data_manager.config["floating_ball_position"] = [pos.x(), pos.y()]
        self.data_manager.save_config()
        print(f"💾 浮动球位置已保存: ({pos.x()}, {pos.y()})")
    
    def load_position(self):
        """从配置加载位置，如果没有则使用默认位置"""
        saved_pos = self.data_manager.config.get("floating_ball_position")
        screen = self.screen().geometry()
        
        if saved_pos and len(saved_pos) == 2:
            x, y = saved_pos
            # 确保位置在屏幕内
            if 0 <= x <= screen.right() - self.width() and 0 <= y <= screen.bottom() - self.height():
                self.move(x, y)
                print(f"✅ 浮动球位置已加载: ({x}, {y})")
                return
        
        # 使用默认位置（屏幕右中）
        default_x = screen.center().x() + 200
        default_y = screen.center().y() - self.height() // 2
        self.move(default_x, default_y)
        print(f"🎯 浮动球使用默认位置: ({default_x}, {default_y})")
        print(f"📐 屏幕大小: {screen.width()}x{screen.height()}")
    
    def set_style(self, style):
        """切换风格"""
        self.style = style
        self.update()
    
    def showEvent(self, event):
        """显示事件 - 提升到最上层"""
        super().showEvent(event)
        self.raise_()
        self.update_opacity()
    
    def focusOutEvent(self, event):
        """失去焦点后延迟恢复置顶"""
        super().focusOutEvent(event)
        self.has_focus = False
        self.update_opacity()
        # 1秒后温和地恢复置顶
        QTimer.singleShot(1000, self.gentle_raise)
    
    def focusInEvent(self, event):
        """获得焦点"""
        super().focusInEvent(event)
        self.has_focus = True
        self.raise_()
        self.update_opacity()
    
    def enterEvent(self, event):
        """鼠标进入时确保可见"""
        self.hover = True
        self.raise_()  # 立即提升到最上层
        self.update_opacity()
        self.update()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """鼠标离开"""
        self.hover = False
        self.update_opacity()
        self.update()
        super().leaveEvent(event)
    
    def gentle_raise(self):
        """温和地提升窗口 - 不干扰用户操作"""
        if self.isVisible() and not self.hover and not self.has_focus:
            # 仅在可见、非悬停、无焦点时提升
            self.raise_()
    
    def update_opacity(self):
        """更新窗口透明度 - 非活跃时半透明"""
        if self.hover or self.has_focus:
            self.setWindowOpacity(1.0)  # 完全不透明
        else:
            self.setWindowOpacity(0.85)  # 稍微透明，减少视觉干扰


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    from data_manager import PromptManager
    import sys
    
    app = QApplication(sys.argv)
    dm = PromptManager()
    ball = FloatingBall(dm)
    ball.show()
    sys.exit(app.exec())
