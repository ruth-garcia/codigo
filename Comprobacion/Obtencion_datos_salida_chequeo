def get_solution_data(instance):
    solution = {
        'task_start': {},
        'task_end': {},
        'task_retraso': {},
        # 'task_trabajproc': {},
        'task_procesando': {},
        # 'task_trabajsetup': {},
        'task_posicion':{}
    }
    # Recuperamos la información de inicio y fin de cada tarea de cada pedido en cada línea
    for p in instance.sPedidos:
        for j in instance.sProcesos:
            for l in instance.sLineas:
                if instance.pPedidoEnLinea[p, j, l].value == 1:
                    solution['task_start'][p, j, l] = instance.vInicio[p, j, l].value
                    solution['task_end'][p, j, l] = instance.vFin[p, j, l].value

    # Recupero la información de retraso de cada pedido
    for p in instance.sPedidos:
        solution['task_retraso'][p] = instance.vRetraso[p].value

    # Recupero la información de trabajadores en cada línea y periodo y si está procesando
    for p in instance.sPedidos:
        for j in instance.sProcesos:
            for t in instance.sPeriodos:
                for l in instance.sLineas:
                    if instance.pPedidoEnLinea[p, j, l].value == 1 and instance.pProcesosenPedido[p, j].value == 1:
                        # solution['task_trabajproc'][p, j, t, l] = instance.vTrabajadoresProc[p, j, t, l].value
                        solution['task_procesando'][p, j, t, l] = instance.v01Procesando[p, j, t, l].value

    # Recupero la información de trabajadores de setup
    for p in instance.sPedidos:
        for p2 in instance.sPedidos:
            if p != p2:
                for t in instance.sPeriodos:
                    for l in instance.sLineas:
                        for j in instance.sProcesos:
                            for j2 in instance.sProcesos:
                                if instance.pPedidoEnLinea[p, j, l].value == 1 and instance.pPedidoEnLinea[p2, j2, l].value == 1:
                                    solution['task_trabajsetup'][p, p2, t, l] = instance.vTrabajadoresSetup[p, p2, t, l].value

    # Recupero la información de la posición del pedido en la línea
    for p in instance.sPedidos:
        for j in instance.sProcesos:
            for r in instance.sPosiciones:
                for l in instance.sLineas:
                    if instance.pPedidoEnLinea[p, j, l].value == 1:
                        solution['task_posicion'][p, j, r, l] = instance.v01Posicion[p, j, r, l].value

    return solution
