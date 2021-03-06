import sys
import matplotlib

from datetime import datetime
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

STANDART_ITEMS = {'Приземная скорость ветра': 'surface_wind_speed', 'Приземная температура': 'surface_temp',
                'Приземная влажность': 'surface_wet', 'Приземное давление': 'surface_press', 'BX': 'bx_mmp', 'BY': 'by_mmp',
                'BZ': 'bz_mmp', 'B-Vector': 'b_vector_mmp', 'Плотность протонов солнеччного ветра': 'proton_density',
                'Скорость плазмы солнечного ветра': 'plasma_speed', 'Давление солнечного ветра': 'press_sun_wind',
                'КР': 'kp_index', 'Радиоизлучение': 'radio_emission', 'Рентгеновское излучение Солнца-1': 'xray_sun_one',
                'Рентгеновское излучение Солнца-2': 'xray_sun_two', 'Ультрофиолет-A': 'ultraviolet_a',
                'Ультрофиолет-B': 'ultraviolet_b', 'Ультрофиолет-C': 'ultraviolet_c'}

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
        self.from_date.setDate(Service.get_min_date())
        self.to_date.setDate(Service.get_max_date())

        # Обновление боксов и фрейма данных
        self.set_data_frame(QFrameDefault)
        self.update_boxes()
        self.show()

    def set_creation_popup_params(self):
        name = self.ui.lineEdit_name.text().strip() if self.ui.lineEdit_name.text().strip() is not '' else \
            self.ui.lineEdit_name.setStyleSheet("color: red;")
        surname = self.ui.lineEdit_surname.text().strip()
        patronymic = self.ui.lineEdit_patr.text().strip()
        age = self.ui.lineEdit_age.text().strip()
        sex = self.ui.radioButton_sex.text().strip() \
            if self.ui.radioButton_sex2.text().strip() is None else self.ui.radioButton_sex2.text().strip()
        birthday = self.ui.date_birth.text().strip()
        stay_in_north = self.ui.lineEdit_north.text().strip()
        part_in_geliomed = self.ui.lineEdit_geliomed.text().strip()
        obesity = self.ui.checkBox_obesity.checkState()
        weight = self.ui.lineEdit_weight.text().strip()
        height = self.ui.lineEdit_height.text().strip()
        imt = self.ui.lineEdit_imt.text().strip()
        alcohol = self.ui.lineEdit_alco.text().strip()
        physical_inactivity = self.ui.checkBox_gipo.checkState()
        monitoring_point = self.ui.lineEdit_mon_point.text().strip()
        nationality = self.ui.lineEdit_nation.text().strip()
        birth_place = self.ui.lineEdit_birth_place.text().strip()
        smoking = self.ui.lineEdit_smoke.text().strip()
        ag_heredity = self.ui.lineEdit_ag.text().strip()
        sss_heredity = self.ui.lineEdit_sss.text().strip()
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
        self.from_date.setDate(Service.get_min_date())
        self.to_date.setDate(Service.get_max_date())
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
        self.from_date.setDate(Service.get_min_date())
        self.to_date.setDate(Service.get_max_date())
        self.update_boxes()

    def update_boxes(self):
        if self.to_date.date() > Service.get_max_date():
            error_dialog('Ошибка! Дата не должна превосходить максимально возможную: ' + Service.get_max_date().strftime('%d.%m.%Y'))
            self.to_date.setDate(Service.get_max_date())
        if self.from_date.date() < Service.get_min_date():
            error_dialog('Ошибка! Дата не должна быть меньше минимальной возможной: ' + Service.get_min_date().strftime('%d.%m.%Y'))
            self.from_date.setDate(Service.get_min_date())

        Sample.samples = {}
        Standard.standards = {}
        self.from_date.text()
        self.to_date.text()
        std_items = []
        self.lead_box.clear()
        self.slave_box.clear()
        from_date = self.from_date.text()
        to_date = self.to_date.text()
        self.samples_list = Service.get_all_patients_full_name_date_filter(from_date, to_date)
        if int(Service.get_all_weather_date_filter_count(from_date, to_date)) != 0:
            self.stds_list = [*STANDART_ITEMS.keys()]
        else:
            self.stds_list = []
        if self.stds_list is not None:
            for standart in STANDART_ITEMS.keys():
                weather_params = Service.get_weather_measurement(from_date, to_date, STANDART_ITEMS.get(standart))
                Standard(standart, weather_params)
            std_items = ["Погода: " + str(self.stds_list[i]) for i in range(len(self.stds_list))]
        if self.samples_list is not None:
            symmetry_all_state = []
            for sample in self.samples_list:
                patients_id = sample.split('(')[1].split(')')[0]
                symmetry_all_state.append(Service.get_all_patients_params_date_filter(patients_id, from_date, to_date, 1))
                symmetry_all_state.append(Service.get_all_patients_params_date_filter(patients_id, from_date, to_date, 2))
                symmetry_all_state.append(Service.get_all_patients_params_date_filter(patients_id, from_date, to_date, 3))
                symmetry_all_state.append(Service.get_all_patients_params_date_filter(patients_id, from_date, to_date, 4))
                Sample(sample, symmetry_all_state)
            if len(self.samples_list) != 0:
                self.samples_list.append("--Групповой--")
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
        lead = self.lead_box.currentText().split(': ')[1]
        slave = self.slave_box.currentText().split(': ')[1]

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
