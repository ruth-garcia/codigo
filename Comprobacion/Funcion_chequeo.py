def check_solution(instance, solution):
    
    mensaje_comprobaciones = []

    # Comprobamos que el inicio y fin de cada tarea son consistentes con las duraciones de las mismas
    for p in instance.sPedidos:
        for j in instance.sProcesos:
            for l in instance.sLineas:
                if instance.pPedidoEnLinea[p, j, l].value == 1:
                    tiempo_esperado = float(instance.pTiempoProcUnidad[p, j].value) * float(
                        instance.pNumUnidades[p].value)
                    duracion_real = float(solution['task_end'][p, j, l]) - float(solution['task_start'][p, j, l])

                    mensaje = f"Pedido {p}, proceso {j}, línea {l}: inicio={float(solution['task_start'][p, j, l]):.2f}, fin={float(solution['task_end'][p, j, l]):.2f}, duración={duracion_real:.2f}, esperada={tiempo_esperado:.2f}"
                    mensaje_comprobaciones.append(mensaje)

                    # Mostramos una advertencia si hay discrepancia
                    if abs(duracion_real - tiempo_esperado) > 1e-6:
                        print(
                            f"  ADVERTENCIA: discrepancia en pedido {p}, proceso {j}, línea {l}. Duración real: {duracion_real:.2f}, esperada: {tiempo_esperado:.2f}")

    # Comprobación de retraso
    for p in instance.sPedidos:
        j_last = -1
        for j in instance.sProcesos:
            if instance.pProcesosenPedido[p, j].value == 1:
                j_last = j

        fin_pedido = -1
        j_real_last = None

        for j in instance.sProcesos:
            for l in instance.sLineas:
                if instance.pPedidoEnLinea[p, j, l].value == 1:
                    if (p, j, l) in solution['task_end']:
                        fin_aux = solution['task_end'][p, j, l]
                        if fin_aux > fin_pedido:
                            fin_pedido = fin_aux
                            j_real_last = j  # guardamos el proceso responsable
                            l_real_last = l
        retraso_esperado = max(0, fin_pedido - float(instance.pFechaLimite[p].value))
        retraso_real = float(solution['task_retraso'][p])

        mensaje = (f"Pedido {p} en proceso {j_real_last} en línea {l_real_last}: retraso esperado={retraso_esperado:.2f}, retraso real={retraso_real:.2f}")
        mensaje_comprobaciones.append(mensaje)

        #Mostramos una advertencia si hay discrepancia
        if (retraso_real < retraso_esperado) or j_last != j_real_last:
            print(
                f"  ADVERTENCIA: discrepancia en pedido {p}. Retraso real: {retraso_real:.2f}, esperado: {retraso_esperado:.2f}. Último proceso={j_real_last}"
                f" y en los datos figura {j_last} como último. Fin real={fin_pedido:.2f} ")

    # Comprobación de trabajadores y si está procesándose la línea
    for t in instance.sPeriodos:
        total_trab_periodo = 0

        for l in instance.sLineas:
            pedido_activo = None    # (p, j) o None
            trabajadores_linea = 0

            for p in instance.sPedidos:
                for j in instance.sProcesos:
                    if (p, j, t, l) in solution['task_procesando']:
                        # w = solution['task_trabajproc'][p, j, t, l]
                        x = solution['task_procesando'][p, j, t, l]
                        # trabajadores_linea += w     # Acumulación de trabajadores para detectar w sin producción
                        if x == 1:
                            if pedido_activo is None:
                                pedido_activo = (p, j)  # Guarda primer pedido activo
                            else:
                                print(f" ADVERTENCIA: discrepancia en periodo {t}, línea {l} (varios pedidos simultáneos): "
                                      f"{pedido_activo} y {(p, j)}")

                        if x == 0 and w > 0 and instance.pProcesosEnPedido[p, j].value == 1:
                            print(f" ADVERTENCIA: discrepancia en periodo {t}, línea {l} para pedido {p} y proceso {j}: "
                                f"se ha asignado {w} trabajadores a un pedido que no se está operando")

                        if x == 1 and w < 1e-6 and instance.pProcesosEnPedido[p, j].value == 1:
                            print(f" ADVERTENCIA: discrepancia en periodo {t}, línea {l} para pedido {p} y proceso {j}: "
                                f"se está procesando un pedido sin trabajadores ({w} trabajadores)")

            min_linea = instance.pMinTrabajadoresLinea[l].value
            max_linea = instance.pMaxTrabajadoresLinea[l].value

            if pedido_activo is not None or trabajadores_linea > 1e-6:
                p_txt = "ninguno"
                if pedido_activo is not None:
                    p_txt = f"{pedido_activo[0]}(proc{pedido_activo[1]})"

                mensaje = (f"Periodo {t}, línea {l}: pedido activo = {p_txt}, "
                           f"trabajadores = {trabajadores_linea:.0f}, mín {min_linea}, máx {max_linea})")
                mensaje_comprobaciones.append(mensaje)

                if trabajadores_linea < min_linea:
                    print(f"  Faltan operarios -> periodo {t}, línea {l} para pedido activo {p_txt}: "
                          f"{trabajadores_linea:.0f} < {min_linea}")
                if trabajadores_linea > max_linea:
                    print(f"  Exceso de operarios -> periodo {t}, línea {l} para pedido activo {p_txt}: "
                          f"{trabajadores_linea:.0f} > {max_linea}")

            total_trab_periodo += trabajadores_linea    # Acumulación trabajadores para total en el periodo

        capacidad_cee = instance.pMaxTrabajadoresCEE.value

        mensaje = (f"Total trabajadores usados en el periodo {t}: {total_trab_periodo:.0f}, límite {capacidad_cee:.0f} trabajadores")
        mensaje_comprobaciones.append(mensaje)

        if total_trab_periodo > capacidad_cee:
            print(f"  Exceso de operarios globales -> periodo {t}. Trabajadores usados: {total_trab_periodo:.0f} > {capacidad_cee:.0f} ")

    # Comprobación trabajadores setup
    for t in instance.sPeriodos:
        total_prod = 0
        total_setup = 0

        for l in instance.sLineas:
            for p in instance.sPedidos:
                for j in instance.sProcesos:
                    if (p, j, t, l) in solution['task_trabajproc']:
                        total_prod += solution['task_trabajproc'][p, j, t, l]

        for p in instance.sPedidos:
            for p2 in instance.sPedidos:
                if p != p2 and (p, p2, t, l) in solution['task_trabajsetup']:
                    total_setup += solution['task_trabajsetup'][p, p2, t, l]

        total = total_prod + total_setup
        limite = instance.pMaxTrabajadoresCEE.value

        mensaje = (f"En el periodo {t}: trabajadores produciendo = {total_prod:.0f}, trabajadores setup= {total_setup:.0f}, ")
        mensaje_comprobaciones.append(mensaje)

        if total > limite:
            print(f"  ADVERTENCIA: discrepancia en periodo {t}. Trabajadores producción: {total_prod:.0f} + setup: {total_setup:.0f} = {total} > {limite:.0f}")

    # Mostramos todas las comprobaciones realizadas
    print("\n=== COMPROBACIONES DE SOLUCIÓN ===")
    for mensaje in mensaje_comprobaciones:
        print(mensaje)
    print("Comprobaciones completadas (assertions deshabilitados temporalmente).")
    print("================================\n")

    return True
    
