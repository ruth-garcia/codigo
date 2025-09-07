def create_input_data_for_pyomo(model, data):
    pyomo_data = {None: {
        'sLineas': {None: data.get('sLineas', [])},
        'sPedidos': {None: data.get('sPedidos', [])},
        'sPeriodos': {None: data.get('sPeriodos', [])},
        'sPosiciones': {None: data.get('sPosiciones', [])},
        'sProcesos': {None: data.get('sProcesos', [])},

        'pTiempoProcUnidad': data.get('pTiempoProcUnidad', {}),
        'pNumUnidades': data.get('pNumUnidades', {}),
        'pDeltaTiempo': data.get('pDeltaTiempo', {}),
        'pHorizonteSemanal': data.get('pHorizonteSemanal', {}),
        'pTiempoSetup': data.get('pTiempoSetup', {}),
        'pMaxTrabajadoresLinea': data.get('pMaxTrabajadoresLinea', {}),
        'pProcesosenPedido': data.get('pProcesosenPedido', {}),
        'pPedidoEnLinea': data.get('pPedidoEnLinea', {}),
        'pEsManualLinea': data.get('pEsManualLinea', {}),
        'pMinTrabajadoresLinea': data.get('pMinTrabajadoresLinea', {}),
        'pMaxTrabajadoresCEE': data.get('pMaxTrabajadoresCEE', {}),
        'pFechaLimite': data.get('pFechaLimite', {}),
    }}
    return pyomo_data
