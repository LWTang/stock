import sys
from random import randint
from PyQt5.QtWidgets import QWidget, QListWidget, \
    QStackedWidget, QHBoxLayout, QListWidgetItem, QLabel, QApplication
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon


class LeftTabWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resize(800, 600)
        layout = QHBoxLayout(self, spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)
        # 左侧列表
        self.listWidget = QListWidget(self)
        layout.addWidget(self.listWidget)
        # 右侧窗口
        self.stackedWidget = QStackedWidget(self)
        layout.addWidget(self.stackedWidget)
        self.initui()

    def initui(self):
        self.listWidget.currentRowChanged.connect(
            self.stackedWidget.setCurrentIndex
        )
        # 去掉边框
        self.listWidget.setFrameShape(QListWidget.NoFrame)
        # self.listWidget.setLineWidth(60)
        # 隐藏滚动条
        self.listWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.listWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        for i in range(2):
            item = QListWidgetItem(
                QIcon('images/%d.ico' % randint(1, 2)), str('选项%s' % i), self.listWidget
            )
            item.setSizeHint(QSize(60, 60))
            item.setTextAlignment(Qt.AlignCenter)

        for i in range(2):
            label = QLabel('我是页面%d' % i, self)
            label.setAlignment(Qt.AlignCenter)
            self.stackedWidget.addWidget(label)


# 美化样式表
Stylesheet = """
QListWidget, QListView{
    outline:0px
}

QListWidget{
    min-width:120px;
    max-width:120px;
    color:black;
    background:white;
}

QListWidget::item:selected{
    background: rgb(135, 206, 250);
    border-left: 2px solid rgb(9, 187, 7);
}

HistoryPanel::item:hover{
    background: rgb(52, 52, 52);
}

"""


if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setStyleSheet(Stylesheet)
    w = LeftTabWidget()
    w.show()


    sys.exit(app.exec_())
