def create_test_data():

    data = {
        # Conjuntos básicos
        'sLineas': [1, 2],  # Dos líneas de producción
        'sPedidos': [1, 2, 3],  # Tres pedidos
        'sProcesos': [1, 2],  # Dos procesos
        'sPeriodos': list(range(1, 50)),  # 50 periodos de tiempo (1, 2, 3 ... 49 y 50)
        'sPosiciones': list(range(1, 4)),  # 4 posiciones posibles (1, 2, 3 y 4)

        # Parámetros

        'pDeltaTiempo': {None: 0.5},  # Intervalos de media hora
        'pHorizonteSemanal': {None: 37.5},  # 1 semana de trabajo = 37.5 horas (7h y 30 min x 5) de jornada semanal

        'pEsManualLinea': {
            1: 1,  # Línea 1 es manual (1)
            2: 0  # Línea 2 es automática (0)
        },

        'pMinTrabajadoresLinea': {
            1: 1,  # Mínimo 1 trabajadores en línea 1
            2: 1  # Mínimo 1 trabajador en línea 2
        },

        'pMaxTrabajadoresLinea': {
            1: 6,  # Máximo 6 trabajadores para línea 1
            2: 4,  # Máximo 4 trabajadores para línea 2
        },

        'pMaxTrabajadoresCEE': {None: 2},  # Máximo 2 trabajadores disponibles

        'pNumUnidades': {
            1: 1,  # Pedido 1: 1 unidad
            2: 2,  # Pedido 2: 2 unidades
            3: 3  # Pedido 3: 3 unidades
        },

        'pTiempoProcUnidad': {
            (1, 1): 0.5,  # Pedido 1, Proceso 1: 0.5 horas por unidad
            (1, 2): 0.5,  # Pedido 1, Proceso 2: 0.5 horas por unidad
            (2, 1): 1,  # Pedido 2, Proceso 1: 1.0 horas por unidad
            (2, 2): 1,  # Pedido 2, Proceso 2: 1.0 horas por unidad
            (3, 1): 0.5,  # Pedido 3, Proceso 1: 0.5 horas por unidad
            (3, 2): 0.5  # Pedido 3, Proceso 2: 0.5 horas por unidad
        },

        'pProcesosenPedido': {
            (1, 1): 1, (1, 2): 1,  # Pedido 1 necesita ambos procesos
            (2, 1): 1, (2, 2): 0,  # Pedido 2 solo necesita proceso 1
            (3, 1): 1, (3, 2): 1  # Pedido 3 necesita ambos procesos
        },

        'pPedidoEnLinea': {
            (1, 1, 1): 1, (1, 1, 2): 0, (1, 2, 1): 0, (1, 2, 2): 1,
            (2, 1, 1): 1, (2, 1, 2): 0,
            (3, 1, 1): 0, (3, 1, 2): 1, (3, 2, 1): 1, (3, 2, 2): 0
        },

        'pTiempoSetup': {
            (1, 1): 0, (1, 2): 1.3, (1, 3): 2.1,
            (2, 1): 0.5, (2, 2): 0, (2, 3): 0.5,
            (3, 1): 1.1, (3, 2): 0.5, (3, 3): 0
        },

        'pFechaLimite': {
            1: 3,  # Pedido 1 debe completarse antes de 3h
            2: 3,  # Pedido 2 debe completarse antes de 3h
            3: 4   # Pedido 3 debe completarse antes de 4h
        }
    }
    return data
