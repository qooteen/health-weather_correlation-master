import sqlite3
from datetime import datetime
class Service:

    @staticmethod
    def add_main_patients_params(params):
        con = sqlite3.connect('health_weather_correlation.db')
        cur = con.cursor()
        cur.execute('INSERT INTO patients(name, surname, patronymic, age, sex, birthday, stay_in_north'
                    ', part_in_geliomed, obesity, weight, height, imt, alcohol, physical_inactivity, monitoring_point'
                    ', nationality, birth_place, smoking, ag_heredity, sss_heredity) '
                    'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (params['name'], params['surname'], params['patronymic'], params['age'], params['sex']
                     , params['birthday'], params['stay_in_north'], params['part_in_geliomed'], params['obesity']
                     , params['weight'], params['height'], params['imt'], params['alcohol']
                     , params['physical_inactivity'], params['monitoring_point'], params['nationality']
                     , params['birth_place'], params['smoking'], params['ag_heredity'], params['sss_heredity']))
        con.commit()
        con.close()


    @staticmethod
    def add_health_measurements_params(params, patient_id):
        con = sqlite3.connect('health_weather_correlation.db')
        cur = con.cursor()
        cur.execute('INSERT INTO health_measurements(date, upper_arterial_pressure, lower_arterial_pressure, chss,'
                    'variab, angle, symmetry, patient_id, patients_state) '
                    'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (params[0], params[1], params[2], params[3], params[4], params[5], params[6], patient_id, params[7]))
        con.commit()
        con.close()


    @staticmethod
    def add_weather_measurements_params(params):
        con = sqlite3.connect('health_weather_correlation.db')
        cur = con.cursor()
        cur.execute('INSERT INTO weather_measurements(date, surface_wind_speed, surface_temp, surface_wet'
                    ', surface_press, bx_mmp, by_mmp, bz_mmp, b_vector_mmp, proton_density, plasma_speed'
                    ', press_sun_wind, kp_index, radio_emission, xray_sun_one, xray_sun_two, ultraviolet_a'
                    ', ultraviolet_b, ultraviolet_c) '
                    'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (params[0], params[1], params[2], params[3], params[4], params[5], params[6], params[7]
                     , params[8], params[9], params[10], params[11], params[12], params[13], params[14], params[15]
                     , params[16], params[17], params[18]))
        con.commit()
        con.close()

    @staticmethod
    def get_all_weather_measurements_params():
        con = sqlite3.connect('health_weather_correlation.db')
        cur = con.cursor()
        cur.execute('SELECT * FROM weather_measurements')
        print(cur.fetchall())
        con.close()

    @staticmethod
    def get_all_patients_full_name():
        con = sqlite3.connect('health_weather_correlation.db')
        cur = con.cursor()
        cur.execute('SELECT surname, name, patronymic, patient_id FROM patients')
        data = cur.fetchall()
        con.close()
        result = []
        for data in data:
            result.append(data[0] + ' ' + data[1] + ' ' + data[2] + ' (' + str(data[3]) + ')')
        return result

    @staticmethod
    def get_all_patients_full_name_date_filter(from_date, to_date):
        con = sqlite3.connect('health_weather_correlation.db')
        cur = con.cursor()
        dt_from = datetime.strptime(from_date, '%d.%m.%Y')
        dt_to = datetime.strptime(to_date, '%d.%m.%Y')

        cur.execute('SELECT DISTINCT(p.patient_id), p.surname, p.name, p.patronymic FROM patients p,'
                    ' health_measurements h where p.patient_id = h.patient_id and h.date >= ? and h.date <= ?'
                    , (dt_from, dt_to))
        data = cur.fetchall()
        con.close()
        result = []
        for data in data:
            result.append('(' + str(data[0]) + ') ' + data[1] + ' ' + data[2] + ' ' + data[3])
        return result

    @staticmethod
    def get_all_patients_params_date_filter(patients_id, from_date, to_date, patients_state):
        con = sqlite3.connect('health_weather_correlation.db')
        cur = con.cursor()
        dt_from = datetime.strptime(from_date, '%d.%m.%Y')
        dt_to = datetime.strptime(to_date, '%d.%m.%Y')

        cur.execute('SELECT symmetry FROM'
                    ' health_measurements where patient_id = ? and date >= ? and date <= ? and patients_state = ?'
                    , (patients_id, dt_from, dt_to, patients_state))
        data = cur.fetchall()
        con.close()
        result = []
        for d in data:
            result.append(d[0])
        return result

    @staticmethod
    def get_all_weather_date_filter_count(from_date, to_date):
        con = sqlite3.connect('health_weather_correlation.db')
        cur = con.cursor()
        dt_from = datetime.strptime(from_date, '%d.%m.%Y')
        dt_to = datetime.strptime(to_date, '%d.%m.%Y')

        cur.execute('SELECT count(*) FROM weather_measurements where date >= ? and date <= ?'
                    , (dt_from, dt_to))
        data = cur.fetchone()[0]
        con.close()
        return data

    @staticmethod
    def get_weather_measurement(from_date, to_date, parameter):
        con = sqlite3.connect('health_weather_correlation.db')
        cur = con.cursor()
        dt_from = datetime.strptime(from_date, '%d.%m.%Y')
        dt_to = datetime.strptime(to_date, '%d.%m.%Y')

        cur.execute('SELECT {} FROM weather_measurements where date >= ? and date <= ?'.format(parameter)
                    , (dt_from, dt_to))
        data = cur.fetchall()
        con.close()
        result = []
        for d in data:
            result.append(d[0])
        return result

    @staticmethod
    def get_max_date():
        con = sqlite3.connect('health_weather_correlation.db')
        cur = con.cursor()

        cur.execute('SELECT max(date) FROM weather_measurements')
        date_weather = cur.fetchone()[0]
        cur.execute('SELECT max(date) FROM health_measurements')
        date_health = cur.fetchone()[0]
        con.close()
        mini = min(date_health, date_weather)
        return datetime.strptime(mini, '%Y-%m-%d %H:%M:%S')

    @staticmethod
    def get_min_date():
        con = sqlite3.connect('health_weather_correlation.db')
        cur = con.cursor()

        cur.execute('SELECT min(date) FROM weather_measurements')
        date_weather = cur.fetchone()[0]
        cur.execute('SELECT min(date) FROM health_measurements')
        date_health = cur.fetchone()[0]
        con.close()
        maxi = max(date_health, date_weather)
        return datetime.strptime(maxi, '%Y-%m-%d %H:%M:%S')
