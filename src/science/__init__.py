import os
from io import BytesIO

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5 import FigureCanvasQT

from openpyxl import load_workbook

FACTORS = [
    "Без нагрузки",
    "С физической нагрузкой",
    "С эмоциональной нагрузкой",
    "После отдыха"
]
FACTORS_L = [factor.lower() for factor in FACTORS]
FACTORS_ALL = -1


class ScienceError(Exception):
    pass


class ClassesError(ValueError):
    pass


class ParseError(ValueError):
    pass

#достаем имя файла без типа из path
def file_base_name(filename: str):
    return os.path.splitext(os.path.basename(filename))[0]


def read_sample(filename):
    """Чтение эталонов"""
    try:
        with open(filename) as file:
            #массив данных с файла эталона
            data = [row.strip() for row in file]
    except Exception:
        raise ParseError("Невозможно открыть файл эталона {}"
                         "\nВозможно он открыт в другой программе".format(filename))

    for idx, el in enumerate(data):
        try:
            # проверка типа, флоат ли это или нет
            data[idx] = float(el)
        except ValueError:
            raise ParseError("Невозможно распознать строку {} в файле {}: убедитесь, что там записано число "
                             "(дробная часть отделяется точкой)".format(idx + 1, filename))
    return data


def read_xlsx_sample(filename):
    try:
        #для чтения xlsx
        wb = load_workbook(filename=filename)
    except Exception:
        raise ParseError("Невозможно открыть файл образца {}"
                         "\nВозможно он открыт в другой программе".format(filename))
    #инициализация листа с информацией о пациенте из xlsx
    sheet = wb.get_active_sheet()

    datas = []
    for col in range(1, 4 + 1):
        data, row = [], 1
        while sheet.cell(row, col).value is not None and sheet.cell(row, col).value.strip():
            try:
                #вытаскивает значение из очередной колонки и пишет в массив
                data.append(float(sheet.cell(row, col).value))
            except Exception:
                raise ParseError('Ошибка при обработке файла {}\nСтраница {}, ячейка {}{}'
                                 .format(filename, sheet.title, 'ABCD'[col], row))
            row += 1
        datas.append(data)
    return datas

#какая-то шляпа, которая делает график из подсчитанных данных, возвращает буффер байтов
def plot_image(plot_func, *args, **kwargs):
    figure = Figure(dpi=100)
    canvas = FigureCanvasQT(figure)
    plot_func(*args, figure)

    buffer = BytesIO()
    canvas.print_figure(buffer)
    if kwargs.get('io', False):
        buffer.seek(0)
        return buffer
    else:
        return buffer.getvalue()


if __name__ == '__main__':
    print('\n'.join(map(str, read_xlsx_sample("samples/1_3.xlsx"))))
