from PySide6.QtWidgets import QTableWidget, QStyledItemDelegate, QStyleOptionViewItem, QStyle
from PySide6.QtGui import QColor, QPainter
from PySide6.QtCore import QModelIndex, Signal, Slot


class HoverableTableWidget(QTableWidget):
    hover_index_changed = Signal(QModelIndex)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        index = self.indexAt(event.pos())
        self.hover_index_changed.emit(index)
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        # 👇 הכרחי כדי לעדכן צבעים מיד
        self.viewport().update()


class HoverDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.hover_row = -1

    @Slot(QModelIndex)
    def on_hover_index_changed(self, index):
        if index.isValid():
            self.hover_row = index.row()
        else:
            self.hover_row = -1

        parent_view = self.parent()
        if parent_view:
            parent_view.viewport().update()

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        custom_option = QStyleOptionViewItem(option)

        if index.row() == self.hover_row:
            custom_option.state &= ~QStyle.State_Selected
            painter.fillRect(custom_option.rect, QColor("#E1F5FE"))

        elif custom_option.state & QStyle.State_Selected:
            painter.fillRect(custom_option.rect, QColor("#CDEBF6"))

        super().paint(painter, custom_option, index)
