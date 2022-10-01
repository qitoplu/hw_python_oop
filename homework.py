from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:0.3f} ч.; '
                f'Дистанция: {self.distance:0.3f} км; '
                f'Ср. скорость: {self.speed:0.3f} км/ч; '
                f'Потрачено ккал: {self.calories:0.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Метод не реализован')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    def __init__(self, action, duration, weight):
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        coeff_calorie_1: int = 18
        coeff_calorie_2: int = 20
        calories = (
            (coeff_calorie_1
             * self.get_mean_speed() - coeff_calorie_2
             )
            * self.weight / self.M_IN_KM * self.duration * self.MIN_IN_H
        )
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self, action, duration, weight, height) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        coeff_calorie_3: float = 0.035
        coeff_calorie_4: float = 0.029
        coeff_calorie_5: int = 2
        calories = (
            (
                coeff_calorie_3 * self.weight
                + (
                    self.get_mean_speed() ** coeff_calorie_5 // self.height
                ) * coeff_calorie_4 * self.weight
            ) * (self.duration * self.MIN_IN_H)
        )
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance1(self) -> float:
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        speed = (self.length_pool * self.count_pool / self.M_IN_KM
                 / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        coeff_calorie_6 = 1.1
        coeff_calorie_7 = 2
        calories = (
            (self.get_mean_speed()
                + coeff_calorie_6
             )
            * coeff_calorie_7 * self.weight
        )
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dictionary = {'SWM': Swimming,
                  'RUN': Running,
                  'WLK': SportsWalking}
    if workout_type in dictionary:
        return dictionary[workout_type](*data)
    else:
        try:
            return dictionary[workout_type](*data)
        except KeyError:
            print('Данный тип тренировок еще не добавлен '
                  'в наш фитнес-трекер :(')
            return ('Поручик Ржевский проснулся и обнаружил на подушке '
                    'малиновую косточку. '
                    'Он позвал служанку и велел выяснить, '
                    'откуда она взялась. '
                    'Служанка пришла и напомнила, '
                    'что он её сам только что позвал. '
                    'P.S. Пётр, спасибо за замечания по коду!'
                    )


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        if training == ('Поручик Ржевский проснулся и обнаружил на подушке '
                        'малиновую косточку. '
                        'Он позвал служанку и велел выяснить, '
                        'откуда она взялась. '
                        'Служанка пришла и напомнила, '
                        'что он её сам только что позвал. '
                        'P.S. Пётр, спасибо за замечания по коду!'
                        ):
            continue
        main(training)
