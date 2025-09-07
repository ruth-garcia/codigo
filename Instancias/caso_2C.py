def create_test_data():

    data = {
        'sLineas': [1, 2, 3],
        'sPedidos': [1, 2, 3, 4],
        'sProcesos': [1, 2],
        'sPeriodos': list(range(1, 79)),
        'sPosiciones': list(range(1, 4)),

        'pDeltaTiempo': {None: 0.5},
        'pHorizonteSemanal': {None: 38.75},

        'pEsManualLinea': {1: 1, 2: 0, 3: 1},  # L1 manual, L2 auto, L3 manual
        'pMinTrabajadoresLinea': {1: 1, 2: 1, 3: 1},
        'pMaxTrabajadoresLinea': {1: 4, 2: 3, 3: 3},
        'pMaxTrabajadoresCEE': {None: 8},

        'pNumUnidades': {1: 6, 2: 5, 3: 4, 4: 6},
        'pTiempoProcUnidad': {
            (1, 1): 0.6, (1, 2): 0.5,  # p1: j1 L1, j2 L2
            (2, 1): 0.8, (2, 2): 0.0,  # p2: solo j1 L3
            (3, 1): 0.5, (3, 2): 0.6,  # p3: j1 L1, j2 L2
            (4, 1): 0.7, (4, 2): 0.0  # p4: solo j2 L2
        },
        'pProcesosenPedido': {
            (1, 1): 1, (1, 2): 1,
            (2, 1): 1, (2, 2): 0,
            (3, 1): 1, (3, 2): 1,
            (4, 1): 1, (4, 2): 0
        },
        'pPedidoEnLinea': {
            (1, 1, 1): 1, (1, 2, 2): 1,  # p1: L1->L2
            (2, 1, 3): 1,  # p2: L3
            (3, 1, 1): 1, (3, 2, 2): 1,  # p3: L1->L2
            (4, 1, 2): 1  # p4: L2
        },

        'pTiempoSetup': {
            (1, 1): 0, (1, 2): 1.2, (1, 3): 0.4, (1, 4): 1.5,
            (2, 1): 1.2, (2, 2): 0, (2, 3): 1.0, (2, 4): 1.0,
            (3, 1): 0.4, (3, 2): 1.0, (3, 3): 0, (3, 4): 0.7,
            (4, 1): 1.5, (4, 2): 1.0, (4, 3): 0.7, (4, 4): 0
        },
        'pFechaLimite': {1: 5.0, 2: 2.0, 3: 3.5, 4: 13.0}
    }
    return data
