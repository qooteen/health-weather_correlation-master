import sys
import matplotlib

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QLabel, QMainWindow, QTextEdit
from PyQt5.QtCore import QEvent, Qt
from src.form import Ui_MainBaseForm
from src.science import ClassesError, ScienceError
from src.science.classes import *
from src.logic import dialog_open, set_main_window, error_dialog
from src.logic.standard import QFrameStdSample, QFrameStdMulSamples
from src.logic.sample import QFrameSampleStd
from src.logic.utils import QFrameDefault
from src.frames.utils.popup_creation import Ui_Form
from src.frames.utils.popup_update import Ui_Form_update
from src.db.service.db_service import Service

SAMPLE_ITEMS = ['Приземная скорость ветра', 'Приземная температура', 'Приземная влажность',
                'Приземное давление', 'BX', 'BY', 'BZ', 'B-Vector', 'Плотность протонов солнеччного ветра',
                'Скорость плазмы солнечного ветра', 'Давление солнечного ветра', 'КР', 'Радиоизлучение',
                'Рентгеновское излучение Солнца-1', 'Рентгеновское излучение Солнца-2', 'Ультрофиолет-A',
                'Ультрофиолет-A', 'Ультрофиолет-B', 'Ультрофиолет-C']

matplotlib.use("Qt5Agg")


class Main(Ui_MainBaseForm, Ui_Form, Ui_Form_update):
    # noinspection PyArgumentList,PyUnresolvedReferences
    def __init__(self):
        self.popupWin = None
        self.ui = Ui_Form()
        self.ui_update = Ui_Form_update()
        self.popupWin = QtWidgets.QWidget()
        self.popupUpdate = QtWidgets.QWidget()
        self.ui_update.setupUi(self.popupUpdate)
        self.ui.setupUi(self.popupWin)
        self.dummy = QWidget()
        self.horizontalLayout = QHBoxLayout(self.dummy)
        self.setCentralWidget(self.dummy)
        self.samples_list = []
        self.stds_list = []
        # фрейм данных
        self.data_frame = None
        # для автоскейлинга графиков
        set_main_window(self)

    def open_creation_popup(self):
        self.popupWin.show()

    def close_creation_popup(self):
        self.clear_params()
        self.popupWin.close()

    def open_update_popup(self):
        self.ui_update.sampels_box.clear()
        data = Service.get_all_patients_full_name()
        self.ui_update.sampels_box.addItems(data)
        self.popupUpdate.show()

    # noinspection PyUnresolvedReferences
    def start(self):
        # Создание пациента
        self.add_sample_btn.clicked.connect(self.open_creation_popup)
        # Создание эталона
        self.add_std_btn.clicked.connect(self.add_std_btn_clicked)
        # Кастомные фреймы
        self.lead_box.activated.connect(self.lead_box_activated)
        self.slave_box.activated.connect(self.choose_data_frame)
        self.from_date.dateChanged.connect(self.update_boxes)
        self.to_date.dateChanged.connect(self.update_boxes)
        # Отчет
        self.report_btn.clicked.connect(self.report_btn_clicked)
        self.report_group_btn.clicked.connect(self.report_group_btn_clicked)

        # Кнопки
        self.ui.pushButton.clicked.connect(self.set_creation_popup_params)
        self.ui.pushButton_2.clicked.connect(self.close_creation_popup)
        self.pushButton_add.clicked.connect(self.open_update_popup)
        self.ui_update.pushButton.clicked.connect(self.add_sample_btn_clicked)

        # Обновление боксов и фрейма данных
        self.set_data_frame(QFrameDefault)
        self.update_boxes()
        self.show()

    def set_creation_popup_params(self):
        name = self.ui.lineEdit_name.text()
        surname = self.ui.lineEdit_surname.text()
        patronymic = self.ui.lineEdit_patr.text()
        age = self.ui.lineEdit_age.text()
        sex = self.ui.radioButton_sex.text() \
            if self.ui.radioButton_sex2.text() is None else self.ui.radioButton_sex2.text()
        birthday = self.ui.date_birth.text()
        stay_in_north = self.ui.lineEdit_north.text()
        part_in_geliomed = self.ui.lineEdit_geliomed.text()
        obesity = self.ui.checkBox_obesity.checkState()
        weight = self.ui.lineEdit_weight.text()
        height = self.ui.lineEdit_height.text()
        imt = self.ui.lineEdit_imt.text()
        alcohol = self.ui.lineEdit_alco.text()
        physical_inactivity = self.ui.checkBox_gipo.checkState()
        monitoring_point = self.ui.lineEdit_mon_point.text()
        nationality = self.ui.lineEdit_nation.text()
        birth_place = self.ui.lineEdit_birth_place.text()
        smoking = self.ui.lineEdit_smoke.text()
        ag_heredity = self.ui.lineEdit_ag.text()
        sss_heredity = self.ui.lineEdit_sss.text()
        params = {'name': name, 'surname': surname, 'patronymic': patronymic, 'age': age, 'sex': sex,
                  'birthday': birthday, 'stay_in_north': stay_in_north, 'part_in_geliomed': part_in_geliomed,
                  'obesity': obesity, 'weight': weight, 'height': height, 'imt': imt, 'alcohol': alcohol,
                  'physical_inactivity': physical_inactivity, 'monitoring_point': monitoring_point,
                  'nationality': nationality, 'birth_place': birth_place, 'smoking': smoking,
                  'ag_heredity': ag_heredity, 'sss_heredity': sss_heredity}
        Service.add_main_patients_params(params)
        self.clear_params()
        self.update_boxes()
        self.popupWin.close()

    def clear_params(self):
        self.ui.lineEdit_name.clear()
        self.ui.lineEdit_surname.clear()
        self.ui.lineEdit_patr.clear()
        self.ui.lineEdit_ag.clear()
        self.ui.lineEdit_smoke.clear()
        self.ui.lineEdit_birth_place.clear()
        self.ui.lineEdit_nation.clear()
        self.ui.lineEdit_mon_point.clear()
        self.ui.lineEdit_alco.clear()
        self.ui.lineEdit_age.clear()
        self.ui.lineEdit_imt.clear()
        self.ui.lineEdit_height.clear()
        self.ui.lineEdit_weight.clear()
        self.ui.lineEdit_geliomed.clear()
        self.ui.lineEdit_north.clear()
        self.ui.date_birth.clear()
        self.ui.lineEdit_sss.clear()

    def add_sample(self, fname):
        try:
            datas = science.read_xlsx_sample(fname)
        except ClassesError as e:
            error_dialog(e)
            return
        except Exception as e:
            error_dialog(e, unknown=True)
            return
        patients_id = self.ui_update.sampels_box.currentText().split('(')[1].split(')')[0]
        for data in datas:
            Service.add_health_measurements_params(data, patients_id)
        self.update_boxes()

    def add_std(self, fname):
        try:
            datas = science.read_xlsx_std(fname)
        except ClassesError as e:
            error_dialog(e)
            return
        except Exception as e:
            error_dialog(e, unknown=True)
            return
        for data in datas:
            Service.add_weather_measurements_params(data)
        self.update_boxes()

    def update_boxes(self):

        self.from_date.text()
        self.to_date.text()
        std_items = []
        self.lead_box.clear()
        self.slave_box.clear()
        from_date = self.from_date.text()
        to_date = self.to_date.text()
        self.samples_list = Service.get_all_patients_full_name_date_filter(from_date, to_date)
        if int(Service.get_all_weather_date_filter_count(from_date, to_date)) != 0:
            self.stds_list = SAMPLE_ITEMS
        else:
            self.stds_list = []
        if len(self.samples_list) == 0:
            self.samples_list.append("--Групповой--")
        if self.stds_list is not None:
            std_items = ["Погода: " + str(self.stds_list[i]) for i in range(len(self.stds_list))]
        if self.samples_list is not None:
            sample_items = ["Образец: " + str(self.samples_list[i]) for i in range(len(self.samples_list))]
        self.lead_box.addItems(std_items + sample_items)

    def set_data_frame(self, frame_class, *args):
        if self.data_frame is not None:
            self.data_layout.removeWidget(self.data_frame)
            self.data_frame.hide()
            self.data_frame = None
        try:
            self.data_frame = frame_class(self, *args)
            self.data_layout.insertWidget(0, self.data_frame)
        except (ScienceError, Exception) as e:
            raise ValueError from e
            if frame_class == QFrameDefault:
                error_dialog("Ошибка в окне по умолчанию. Свяжитесь с разработчиком")
                sys.exit(1)
            error_dialog(e, unknown=True)
            self.data_frame = None
            self.set_data_frame(QFrameDefault)

    def choose_data_frame(self):
        orientation = self.lead_box.currentText().split(' ')[0] == "Погода:"
        lead = self.lead_box.currentText().split(' ')[1]
        slave = self.slave_box.currentText().split(' ')[1]

        # Погода - образец
        if orientation:
            if lead in Standard.standards and (slave in Sample.samples or slave == "--Групповой--"):
                self.set_data_frame(QFrameStdSample, lead, slave)
            elif lead in Standard.standards and slave == "--Группа--":
                if len(Sample.samples) < 3:
                    error_dialog("Для составления отчета по группе эталонов необходимо как минимум 3 образца")
                    return
                self.set_data_frame(QFrameStdMulSamples, lead)
            else:
                error_dialog("Необработанный случай выбора фрейма: lead={}, slave={}, orient={}"
                             .format(lead, slave, orientation), unknown=True)
        # Образец - погода
        else:
            if (lead in Sample.samples or lead == "--Групповой--") and slave in Standard.standards:
                self.set_data_frame(QFrameSampleStd, lead, slave)
            else:
                error_dialog("Необработанный случай выбора фрейма: lead={}, slave={}, orient={}"
                             .format(lead, slave, orientation), unknown=True)

    # КНОПКИ
    def lead_box_activated(self):
        lead_type = self.lead_box.currentText().split(' ')[0]
        if lead_type == 'Образец:':
            items = ["Погода: " + str(self.stds_list[i]) for i in range(len(self.stds_list))]
        elif lead_type == 'Погода:':
            items = ["Образец: " + str(self.samples_list[i]) for i in range(len(self.samples_list))] + \
                    ["Образец: --Группа--"]
        else:
            error_dialog("Неизвестный тип данных в боксе: {}".format(lead_type), unknown=True)
            return
        if self.slave_box.count():
            slave_type = self.slave_box.currentText().split(' ')[0]
            if slave_type != lead_type:
                self.choose_data_frame()
                return
        self.slave_box.clear()
        self.slave_box.addItems(items)

    def add_std_btn_clicked(self):
        fnames = dialog_open("Выбрать эталон", "xlsx")
        if fnames:
            for fname in fnames:
                self.add_std(fname)

    def add_sample_btn_clicked(self):
        fnames = dialog_open("Выбрать файл пациента", "xlsx")
        if fnames:
            for fname in fnames:
                self.add_sample(fname)

    def report_btn_clicked(self):
        if self.data_frame is not None and hasattr(self.data_frame, "save_report"):
            try:
                self.data_frame.save_report()
            except (ScienceError, Exception) as e:
                error_dialog(e, unknown=True)
        elif self.data_frame is not None:
            error_dialog("Функция save_report не реализована у окна {}. Пожалуйста, свяжитесь с разработчиком"
                         .format(type(self.data_frame).__name__))

    def report_group_btn_clicked(self):
        if self.data_frame is not None and hasattr(self.data_frame, "save_report_group"):
            try:
                self.data_frame.save_report_group()
            except (ScienceError, Exception) as e:
                error_dialog(e, unknown=True)
        elif self.data_frame is not None:
            error_dialog("Функция save_report_group не реализована у окна {}. Пожалуйста, свяжитесь с разработчиком"
                         .format(type(self.data_frame).__name__))

    def eventFilter(self, widget, event):
        event_types = [QEvent.Resize, QEvent.Show, 24]

        if event.type() in event_types and isinstance(widget, QLabel) and hasattr(widget, 'plot_pixmap'):
            widget.setPixmap(widget.plot_pixmap.scaled(widget.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        if event.type() in event_types and isinstance(widget, QTextEdit) and hasattr(widget, 'c_updating'):
            if widget.c_updating:
                widget.c_updating = False
            else:
                widget.c_updating = True
                doc_height = widget.document().size().toSize().height()
                widget.setMinimumHeight(doc_height)
        # noinspection PyCallByClass,PyTypeChecker
        return QMainWindow.eventFilter(self, widget, event)
