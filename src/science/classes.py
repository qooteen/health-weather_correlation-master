import src.science.funcs as funcs
import numpy as np

from src import science

DATA_LENGTH_DEFAULT = -1
DATA_LENGTH = DATA_LENGTH_DEFAULT
GROUP_SAMPLE_NAME = 'group'


class Sample:
    samples = {}
    group = None

    def __init__(self, name, datas):
        # инициализация атрибутов
        self.name = name
        self.data, self.seq_max, self.seq_max0 = [], [], []
        for data in datas:
            self.data.append(data)
            self.seq_max.append(data if data is None else funcs.sequence_max(data))
            self.seq_max0.append(data if data is None else funcs.sequence_max0(data))
        # добавление образца в глобальный список
        if name != GROUP_SAMPLE_NAME:
            Sample.samples[name] = self
        # обновление группового образца
        self.handle_group()

    def handle_group(self):
        if self.name == GROUP_SAMPLE_NAME:
            return
        if Sample.group is None:
            datas = [[0] * DATA_LENGTH for _factor in range(4)]
            Sample.group = Sample(GROUP_SAMPLE_NAME, datas)
            print('Групповой образец инициализирован')
        # обновляем групповой образец
        for factor in range(4):
            for idx in range(DATA_LENGTH):
                Sample.group.data[factor][idx] += self.data[factor][idx]
        Sample.group.seq_max = [funcs.sequence_max(data) for data in Sample.group.data]
        Sample.group.seq_max0 = [funcs.sequence_max0(data) for data in Sample.group.data]

    def display(self):
        if self.name == GROUP_SAMPLE_NAME:
            return "Групповой образец"
        else:
            return "Образец: " + self.name

    def display_file(self, factor=science.FACTORS_ALL):
        fname = self.display().replace(":", "")
        if factor != science.FACTORS_ALL:
            fname += " " + science.FACTORS_L[factor]
        return fname

    @staticmethod
    def display_file_group(factor=science.FACTORS_ALL):
        fname = "Группа образцов"
        if factor != science.FACTORS_ALL:
            fname += " " + science.FACTORS_L[factor]
        return fname

    def display_g(self):
        if self.name == GROUP_SAMPLE_NAME:
            return "группового образца"
        else:
            return "образца " + self.name


class Standard:
    #ВСЕ ПОГОДЫ, ОТСЮДА ИХ УДАЛЯЮТ И СЧИТЫВАЮТ
    standards = {}

    def __init__(self, name, data):
        # инициализация атрибутов
        self.name = name
        self.data = data
        self.seq_max = funcs.sequence_max(self.data)
        self.seq_max0 = funcs.sequence_max0(self.data)
        self.seq_max_apl = funcs.sequence_max_ampl(self.data, np.mean(self.data))
        # добавление эталона в глобальный список
        Standard.standards[name] = self

    def display(self):
        return "Погода: " + self.name

    def display_file(self):
        return self.display().replace(":", "")