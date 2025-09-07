def create_test_data():

    data = {
        'sLineas': [1, 2], # 2 líneas de producción
        'sPedidos': [1, 2, 3], # 3 pedidos
        'sProcesos': [1, 2], # 2 procesos
        'sPeriodos': list(range(1, 79)), # 79 periodos de tiempo (1, 2, 3...79)
        'sPosiciones': [1, 2, 3], # Hasta 3 posiciones por línea

        'pDeltaTiempo': {None: 0.5}, # Intervalos de media hora
        'pHorizonteSemanal': {None: 37.5}, # 1 semana de trabajo = 37.5 horas (7h y 30 min x 5) de jornada semanal

        'pEsManualLinea': {
            1: 1,  # Línea 1 manual (1)
            2: 0   # Línea 2 automática (0)
        },

        'pMinTrabajadoresLinea': {
            1: 1,  # Mínimo 1 trabajador en la línea 1
            2: 1   # Mínimo 1 trabajador en la línea 2
        },

        'pMaxTrabajadoresLinea': {
            1: 3,  # Máximo 3 trabajadores en la línea 1
            2: 2   # Máximo 2 trabajadores en la línea 1
        },

        'pMaxTrabajadoresCEE': {None: 5}, # Máximo 5 trabajadores disponibles


        'pNumUnidades': {
            1: 4,   # Pedido 1: 4 unidades
            2: 4,   # Pedido 2: 4 unidades
            3: 4    # Pedido 3: 4 unidades
        },

        'pTiempoProcUnidad': {
            (1, 1): 0.75, # Pedido 1, Proceso 1: 0.75 horas por unidad
            (1, 2): 0.5,
            (2, 1): 0.75,
            (2, 2): 0.5,  # Pedido 2, Proceso 2: 0.5 horas por unidad
            (3, 1): 0.75,
            (3, 2): 0.5
        },
        'pProcesosenPedido': {(1, 1): 1, (1, 2): 1, (2, 1): 1, (2, 2): 1, (3, 1): 1, (3, 2): 1},
        # Todos los pedidos tienen el primer proceso (j1) en L1 (manual) y j2 en L2 (auto)
        'pPedidoEnLinea': {
            (1, 1, 1): 1, (1, 2, 2): 1,
            (2, 1, 1): 1, (2, 2, 2): 1,
            (3, 1, 1): 1, (3, 2, 2): 1
        },

        'pTiempoSetup': {
            (1, 1): 0, (1, 2): 1.5, (1, 3): 0.5,
            (2, 1): 1.5, (2, 2): 0, (2, 3): 1.5,
            (3, 1): 0.5, (3, 2): 0.5, (3, 3): 0
        },
        'pFechaLimite': {
            1: 7.0, # Pedido 1 debe completarse antes de 7h
            2: 8.0, # Pedido 2 debe completarse antes de 8h
            3: 10.0 # Pedido 3 debe completarse antes de 10h
        }
    }
    return data
