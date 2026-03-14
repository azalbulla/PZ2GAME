from pokaz import TransportDecisionMaker, setup_logger

logger = setup_logger()

if __name__ == "__main__":

    A = [
        [6, 12, 20, 24],
        [9, 7, 9, 28],
        [23, 18, 15, 19],
        [27, 24, 21, 15]
    ]

    demand_names = ["П1 (10т)", "П2 (15т)", "П3 (20т)", "П4 (25т)"]

    try:
        dm = TransportDecisionMaker(A, demand_names)
        dm.print_matrix()

        risk_matrix = dm.calculate_risk_matrix()

        wald_strat, wald_val = dm.wald_criterion()
        savage_strat, savage_val = dm.savage_criterion(risk_matrix)
        hurwicz_strat, hurwicz_val = dm.hurwicz_criterion(p = 0.5)

        logger.info(f"Критерий Вальда: Стратегия {wald_strat}")
        logger.info(f"Критерий Сэвиджа: Стратегия {savage_strat}")
        logger.info(f"Критерий Гурвица: Стратегия {hurwicz_strat}")

    except Exception as e:
        logger.error("Ошибка выполнения программы", exc_info=True)
