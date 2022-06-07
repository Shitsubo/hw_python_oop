from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    message = ('Тип тренировки: {training_type}; '
               'Длительность: {duration:0.3f} ч.; '
               'Дистанция: {distance:0.3f} км; '
               'Ср. скорость: {speed:0.3f} км/ч; '
               'Потрачено ккал: {calories:0.3f}.'
               )

    def get_message(self: dict) -> str:
        return self.message.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MIN_IN_HOUR: int = 60

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
        return self.LEN_STEP * self.action / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return (self.LEN_STEP
                * self.action
                / self.M_IN_KM) / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise Error

    def show_training_info(self) -> InfoMessage:
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    coeff_calorie_1: int = 18
    coeff_calorie_2: int = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ):
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        calories1 = (self.coeff_calorie_1
                     * self.get_mean_speed()
                     - self.coeff_calorie_2)
        return (calories1
                * self.weight
                / self.M_IN_KM
                * self.duration
                * self.MIN_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff_calorie_1: float = 0.035
    coeff_calorie_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        calories1 = (self.coeff_calorie_1
                     * self.weight
                     + (self.get_mean_speed() ** 2 // self.height)
                     * self.coeff_calorie_2 * self.weight)
        return calories1 * self.duration * self.MIN_IN_HOUR


class Swimming(Training):
    LEN_STEP: float = 1.38
    coeff_calorie_1: int = 1.1
    coeff_calorie_2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                 + self.coeff_calorie_1)
                * self.coeff_calorie_2
                * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_workout = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    training = type_workout[workout_type](*data)
    if 'SWM' in type_workout or 'RUN' in type_workout or 'WLK' in type_workout:
        return training
    else:
        raise EROR


def main(training: Training) -> None:
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
        main(training)
