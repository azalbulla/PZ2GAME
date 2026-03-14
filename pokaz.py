import logging

def setup_logger():
    logger = logging.getLogger('TransportStrategyLogger')
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%H:%M:%S"
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        file_handler = logging.FileHandler('transport_decision.log', encoding='utf-8', mode='w')
        file_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        datefmt = "%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger
logger = setup_logger()

class TransportDecisionMaker:

    def __init__(self, matrix, demand_names=None):
        '''
        Класс для решения задачи выбора оптимальной стратегии
        строки - стратегии предприятия
        столбцы - спрос
        :param matrix: матрица затрат
        :param demand_names: название состояний спроса
        '''
        if not matrix:
            raise ValueError("Матрица не может быть пустой")

        self.matrix = matrix
        self.strategies_count = len(matrix)
        self.demand_count = len(matrix[0])

        self.demand_names = demand_names or [f"П{j+1}" for j in range(self.demand_count)]

        for row in matrix:
            if len(row) != self.demand_count:
                raise ValueError("Все строки матрицы должны быть одной длины")

        logger.info(
            f"Стратегий: {self.strategies_count}, сценариев спроса: {self.demand_count}"
        )

        logger.debug(f"Матрица затрат: {self.matrix}")

    def calculate_risk_matrix(self):
        min_by_demand = []
        logger.info("Минимальные затраты по столбцам:")
        for j in range(self.demand_count):
            col_values = [self.matrix[i][j] for i in range(self.strategies_count)]
            min_val = min(col_values)
            min_by_demand.append(min_val)
            logger.info(f"  {self.demand_names[j]}: min = {min_val}")


        risk_matrix = [[0] * self.demand_count for _ in range(self.strategies_count)]

        for i in range(self.strategies_count):
            for j in range(self.demand_count):
                risk = self.matrix[i][j] - min_by_demand[j]
                risk_matrix[i][j] = risk

        logger.info(f"Матрица рисков: {risk_matrix}")

        return risk_matrix

    def wald_criterion(self):
        logger.info("Расчёт по критерию Вальда")
        max_costs = []
        for i, row in enumerate(self.matrix):
            max_val = max(row)
            max_costs.append(max_val)
            logger.info(f"Стратегия {i + 1}: max({row}) = {max_val}")

        min_max = min(max_costs)
        optimal_index = max_costs.index(min_max)

        logger.info(f"РЕЗУЛЬТАТ: min{max_costs} = {min_max}")
        logger.info(f"Оптимальная стратегия: {optimal_index + 1}")

        return optimal_index + 1, min_max

    def savage_criterion(self, risk_matrix = None):
        logger.info("Критерий Сэвиджа")

        if risk_matrix is None:
            risk_matrix = self.calculate_risk_matrix()

        max_risks = []
        for i, row in enumerate(risk_matrix):
            max_val = max(row)
            max_risks.append(max_val)
            logger.info(f"Стратегия {i + 1}: max риск {row} = {max_val}")

        min_max_risk = min(max_risks)
        optimal_index = max_risks.index(min_max_risk)

        logger.info(f"РЕЗУЛЬТАТ: min{max_risks} = {min_max_risk}")
        logger.info(f"Оптимальная стратегия: {optimal_index + 1}")

        return optimal_index + 1, min_max_risk

    def hurwicz_criterion(self, p = 0.5):
        logger.info("Критерий Гурвица")

        if not (0 <= p <= 1):
            raise ValueError("p должен быть в диапазоне [0; 1]")

        values = []
        logger.info("Расчет значений:")
        for i, row in enumerate(self.matrix):
            min_val = min(row)
            max_val = max(row)
            h_val = p * min_val + (1 - p) * max_val
            values.append(h_val)
            logger.info(f"Стратегия {i + 1}: {p}*{min_val} + {1 - p}*{max_val} = {h_val:.2f}")

        min_h = min(values)
        optimal_index = values.index(min_h)

        logger.info(f"РЕЗУЛЬТАТ: min{[round(v, 2) for v in values]} = {min_h:.2f}")
        logger.info(f"Оптимальная стратегия: {optimal_index + 1}")

        return optimal_index + 1, min_h


    def print_matrix(self):
        logger.info("Вывод матрицы затрат")
        for i, row in enumerate(self.matrix):
            logger.info(f"Стратегия {i+1}: {row}")


