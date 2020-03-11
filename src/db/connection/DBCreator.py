import sqlite3


class DBCreator:

    def __init__(self):
        self.con = sqlite3.connect('health_weather_correlation.db')
        self.create_tables()
        self.con.commit()

    def create_tables(self):
        cur = self.con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS patients(patient_id INTEGER PRIMARY KEY AUTOINCREMENT,'
                    'name TEXT,'
                    'surname TEXT,'
                    'patronymic TEXT,'
                    'age INTEGER,'
                    'sex NUMERIC,'
                    'birthday NUMERIC,'
                    'stay_in_north INTEGER,'
                    'part_in_geliomed INTEGER,'
                    'obesity NUMERIC,'
                    'weight REAL,'
                    'height REAL,'
                    'imt REAL,'
                    'alcohol INTEGER,'
                    'physical_inactivity NUMERIC,'
                    'monitoring_point TEXT,'
                    'nationality TEXT,'
                    'birth_place TEXT,'
                    'smoking TEXT,'
                    'ag__heredity TEXT,'
                    'sss_heredity TEXT)')

        cur.execute('CREATE TABLE IF NOT EXISTS weather_measurements(weather_measurement_id '
                    'INTEGER PRIMARY KEY AUTOINCREMENT,'
                    'date NUMERIC,'
                    'surface_wind_speed REAL,'
                    'surface_temp REAL,'
                    'surface_wet REAL,'
                    'surface_press INTEGER,'
                    'bx_mmp REAL,'
                    'by_mmp REAL,'
                    'bz_mmp REAL,'
                    'b_vector_mmp REAL,'
                    'proton_density REAL,'
                    'plasma_speed INTEGER,'
                    'press_sun_wind REAL,'
                    'kp_index REAL,'
                    'radio_emission INTEGER,'
                    'xray_sun_one REAL,'
                    'xray_sun_two REAL,'
                    'ultraviolet_a REAL,'
                    'ultraviolet_b REAL,'
                    'ultraviolet_c REAL)')

        cur.execute('CREATE TABLE IF NOT EXISTS health_measurements(health_measurement_id '
                    'INTEGER PRIMARY KEY AUTOINCREMENT,'
                    'datetime NUMERIC,'
                    'upper_arterial_pressure INTEGER,'
                    'lower_arterial_pressure INTEGER,'
                    'chss REAL,'
                    'variab REAL,'
                    'angle REAL,'
                    'symmetry REAL,'
                    'patient_id INTEGER,'
                    'patients_state TEXT,'
                    'FOREIGN KEY (patient_id) REFERENCES patients(patient_id))')

        cur.execute('CREATE TABLE IF NOT EXISTS polymorphisms(polymorphism_id '
                    'INTEGER PRIMARY KEY AUTOINCREMENT,'
                    'value INTEGER,'
                    'polymorphism TEXT,'
                    'patient_id INTEGER,'
                    'FOREIGN KEY (patient_id) REFERENCES patients(patient_id))')

        cur.execute('CREATE TABLE IF NOT EXISTS patient_weather_measurements(patient_weather_measurement_id '
                    'INTEGER PRIMARY KEY AUTOINCREMENT,'
                    'weather_measurement_id INTEGER,'
                    'patient_id INTEGER,'
                    'FOREIGN KEY (patient_id) REFERENCES patients(patient_id),'
                    'FOREIGN KEY (weather_measurement_id) REFERENCES weather_measurements(weather_measurement_id))')
