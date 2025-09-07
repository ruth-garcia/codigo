def get_production_planning_model():

    model = pyo.AbstractModel(name="Planning_CEE_Trefemo")

    # 1. Conjuntos
    model.sLineas = pyo.Set(doc="Líneas de producción (L)")
    model.sPedidos = pyo.Set(doc="Pedidos (P)")
    model.sPeriodos = pyo.Set(ordered=True, doc="Periodos discretos (T)")
    model.sPosiciones = pyo.Set(doc="Posiciones en la secuencia de cada línea (R)")
    model.sProcesos = pyo.Set(doc="Procesos en el pedido (J)")

    # 2. Parámetros
    model.pTiempoProcUnidad = pyo.Param(model.sPedidos, model.sProcesos, mutable=True, default= 0,
                                        doc="Tiempo de producción por unidad del proceso j del pedido p (h) (Tpj)")

    model.pNumUnidades = pyo.Param(model.sPedidos, mutable=True,
                                   doc="Número de unidades del pedido p (Np)")

    model.pDeltaTiempo = pyo.Param(initialize=0.5, mutable=True, doc="Duración del intervalo de tiempo (h)")

    model.pHorizonteSemanal = pyo.Param(mutable=True, doc="Horizonte semanal [h]")

    model.pTiempoSetup = pyo.Param(model.sPedidos, model.sPedidos, default=0, mutable=True,
                                   doc="Tiempo de preparación entre pedido p y p' (h) (Spp')")

    model.pMaxTrabajadoresLinea = pyo.Param(model.sLineas, mutable=True,
                                            doc="Máximo de operarios simultáneos por línea l (MAX_l)")

    model.pProcesosenPedido = pyo.Param(model.sPedidos, model.sProcesos, mutable=True,
                                        within=pyo.Binary, default=0, doc="1 si el pedido p tiene el proceso j (Ipj)")

    model.pPedidoEnLinea = pyo.Param(model.sPedidos, model.sProcesos, model.sLineas, mutable=True,
                                     within=pyo.Binary, default=0,
                                     doc="1 si el pedido p durante el proceso j se procesa en la línea l (Ωpjl)")

    model.pEsManualLinea = pyo.Param(model.sLineas, within=pyo.Binary, mutable=True,
                                     doc="1 si la línea es manual, 0 si es automática (M_l)")

    model.pMinTrabajadoresLinea = pyo.Param(model.sLineas, mutable=True,
                                            doc="Requisito mínimo de operarios por línea l (MIN_l)")

    model.pMaxTrabajadoresCEE = pyo.Param(mutable=True, doc="Número máximo de operarios disponibles en el CEE (Wmax)")

    model.pFechaLimite = pyo.Param(model.sPedidos, mutable=True,
                                   doc="Fecha límite (h desde t=0) del pedido p")

    # 3. Variables
    # 3.1 Continuas
    model.vTrabajadoresProc = pyo.Var(model.sPedidos, model.sProcesos, model.sPeriodos, model.sLineas,
                                      domain=pyo.NonNegativeIntegers,
                                      doc="w_{p,j,t,l}: Nº de operarios procesando p en t,l del proceso j")

    model.vRetraso = pyo.Var(model.sPedidos, domain=pyo.NonNegativeReals,
                             doc="Retraso (h) del pedido p")

    model.vTrabajadoresSetup = pyo.Var(model.sPedidos, model.sPedidos, model.sPeriodos, model.sLineas,
                                       domain=pyo.NonNegativeIntegers,
                                       doc="y_{p,p',t, l}: operarios en el cambio p→p' en t")

    model.vInicio = pyo.Var(model.sPedidos, model.sProcesos, model.sLineas,
                            domain=pyo.NonNegativeReals, doc="s_{p,j,l}: inicio de p del proceso j en l")

    model.vFin = pyo.Var(model.sPedidos, model.sProcesos, model.sLineas,
                         domain=pyo.NonNegativeReals, doc="f_{p,j,l}: fin de p del proceso j en l")

    # 3.2 Binarias
    model.v01Procesando = pyo.Var(model.sPedidos, model.sProcesos, model.sPeriodos, model.sLineas,
                                  domain=pyo.Binary, doc="x_{p,j,t,l}: 1 si p se procesa en el proceso j en t,l")

    model.v01Posicion = pyo.Var(model.sPedidos, model.sProcesos, model.sPosiciones, model.sLineas,
                                domain=pyo.Binary,
                                doc="α_{p,j,r,l}: 1 si p durante el proceso j ocupa la posición r en la secuencia de l")

    model.v01Arranque = pyo.Var(model.sPedidos, model.sProcesos, model.sPeriodos, model.sLineas, within=pyo.Binary)

    model.v01SetupAct = pyo.Var(model.sPedidos, model.sPedidos, model.sPeriodos, model.sLineas,
                                domain=pyo.Binary, doc="z_{p,p',t,l}: 1 si el setup p→p' se realiza en el periodo t (línea l)")

    model.v01Consecutivo = pyo.Var(model.sPedidos, model.sPedidos, model.sPosiciones, model.sLineas,
                                   domain=pyo.Binary, doc="β_{p,p',r,l}: 1 si p está en r y p' en r+1 en la línea l")

    # 4. Restricciones

    # 4.1 No solapamiento (Ecuaciones 1-3)

    def c1_uno_por_linea_rule(m, p, j, t, l):
        if m.pPedidoEnLinea[p, j, l].value == m.pProcesosenPedido[p, j].value == 1:
            return (sum(m.v01Procesando[p, j, t, l] for p in m.sPedidos for j in m.sProcesos) <= 1)
        else:
            return pyo.Constraint.Skip

    model.c1_uno_por_linea = pyo.Constraint(model.sPedidos, model.sProcesos, model.sPeriodos, model.sLineas,
                                             rule=c1_uno_por_linea_rule)

    def c2_uno_por_linea_rule(m, p, j, t, l):
        if m.pPedidoEnLinea[p, j, l].value == m.pProcesosenPedido[p, j].value == 1:
            return (sum(m.v01Procesando[p, j, t, l] for j in m.sProcesos for l in m.sLineas) <= 1)
        else:
            return pyo.Constraint.Skip

    model.c2_uno_por_linea = pyo.Constraint(model.sPedidos, model.sProcesos, model.sPeriodos, model.sLineas,
                                             rule=c2_uno_por_linea_rule)

    def c3_no_prod_durante_setup(m, t, l):
        prod = sum(m.v01Procesando[p, j, t, l] for p in m.sPedidos for j in m.sProcesos
                   if m.pProcesosenPedido[p, j].value == 1 and m.pPedidoEnLinea[p, j, l].value == 1)
        setup = sum(m.v01SetupAct[p, p2, t, l] for p in m.sPedidos for p2 in m.sPedidos if p != p2)
        return prod + setup <= 1

    model.c3_no_prod_durante_setup = pyo.Constraint(model.sPeriodos, model.sLineas,
                                                    rule=c3_no_prod_durante_setup)

    # 4.2 Consistencia (Ecuaciones 4-6)

    def c4_consistencia_min_rule(m, p, j, t, l):
        if m.pProcesosenPedido[p, j].value == m.pPedidoEnLinea[p, j, l].value == 1:
            return (m.v01Procesando[p, j, t, l] <= m.vTrabajadoresProc[p, j, t, l])
        else:
            return pyo.Constraint.Skip

    model.c4_consistencia_min = pyo.Constraint(model.sPedidos, model.sProcesos, model.sPeriodos, model.sLineas, rule=c4_consistencia_min_rule)

    def c5_consistencia_max_rule(m, p, j, t, l):
        if m.pProcesosenPedido[p, j].value == m.pPedidoEnLinea[p, j, l].value == 1:
            return (m.v01Procesando[p, j, t, l] * m.pMaxTrabajadoresLinea[l] >= m.vTrabajadoresProc[p, j, t, l])
        else:
            return pyo.Constraint.Skip

    model.c5_consistencia_max = pyo.Constraint(model.sPedidos, model.sProcesos, model.sPeriodos, model.sLineas, rule=c5_consistencia_max_rule)

    def c6_y_cotas_por_z_min(m, p, p2, t, l):
        if p != p2:
            return m.vTrabajadoresSetup[p, p2, t, l] >= m.v01SetupAct[p, p2, t, l]
        return pyo.Constraint.Skip

    model.c6_y_cotas_por_z_min = pyo.Constraint(model.sPedidos, model.sPedidos, model.sPeriodos, model.sLineas, rule=c6_y_cotas_por_z_min)

    # 4.3 Trabajadores necesarios (Ecuaciones 7-10)

    def c7_min_ops_rule(m, p, j, t, l):
        if m.pProcesosenPedido[p, j].value == m.pPedidoEnLinea[p, j, l].value == 1:
            return (m.pMinTrabajadoresLinea[l] * m.v01Procesando[p, j, t, l] <= m.vTrabajadoresProc[p, j, t, l])
        else:
            return pyo.Constraint.Skip

    model.c7_min_ops = pyo.Constraint(model.sPedidos, model.sProcesos, model.sPeriodos, model.sLineas, rule=c7_min_ops_rule)

    def c8_max_ops_pedido_rule(m, p, j, t, l):
        if m.pProcesosenPedido[p, j].value == m.pPedidoEnLinea[p, j, l].value == 1:
            return (m.vTrabajadoresProc[p, j, t, l] <= m.pMaxTrabajadoresLinea[l])
        else:
            return pyo.Constraint.Skip

    model.c8_max_ops_pedido = pyo.Constraint(model.sPedidos, model.sProcesos, model.sPeriodos, model.sLineas, rule=c8_max_ops_pedido_rule)

    def c9_cota_y_por_z(m, p, p2, t, l):
        return m.vTrabajadoresSetup[p, p2, t, l] <= m.pMaxTrabajadoresLinea[l] * m.v01SetupAct[p, p2, t, l]

    model.c9_cota_y_por_z = pyo.Constraint(model.sPedidos, model.sPedidos, model.sPeriodos, model.sLineas, rule=c9_cota_y_por_z)

    def c10_total_ops_rule(m, t):
        prod = sum(m.vTrabajadoresProc[p, j, t, l] for p in m.sPedidos for j in m.sProcesos for l in m.sLineas \
                   if m.pProcesosenPedido[p, j].value == m.pPedidoEnLinea[p, j, l].value == 1)
        setup = sum(m.vTrabajadoresSetup[p, p2, t, l] for p in m.sPedidos for p2 in m.sPedidos for l in m.sLineas if p != p2)
        return prod + setup <= m.pMaxTrabajadoresCEE

    model.c10_total_ops = pyo.Constraint(model.sPeriodos, rule=c10_total_ops_rule)

    # 4.4 Arranque de un pedido (Ecuaciones 11-13)

    def c11_arranque_ge_rule(m, p, j, t, l):
        x_prev = 0 if t == m.sPeriodos.first() else m.v01Procesando[p, j, m.sPeriodos.prev(t), l]
        return m.v01Arranque[p, j, t, l] >= m.v01Procesando[p, j, t, l] - x_prev

    model.c11_arranque_ge = pyo.Constraint(model.sPedidos, model.sProcesos, model.sPeriodos, model.sLineas, rule=c11_arranque_ge_rule)

    def c12_un_arranque_rule(m, p, j, l):
        if m.pPedidoEnLinea[p, j, l].value == 1 and m.pProcesosenPedido[p, j].value == 1:
            return sum(m.v01Arranque[p, j, t, l] for t in m.sPeriodos) == 1
        return pyo.Constraint.Skip

    model.c12_un_arranque = pyo.Constraint(model.sPedidos, model.sProcesos, model.sLineas, rule=c12_un_arranque_rule)

    def c13_s_igual_rule(m, p, j, l):
        if m.pPedidoEnLinea[p, j, l].value == 1 and m.pProcesosenPedido[p, j].value == 1:
            return m.vInicio[p, j, l] == sum(m.v01Arranque[p, j, t, l] * (t - 1) * m.pDeltaTiempo for t in m.sPeriodos)
        return pyo.Constraint.Skip

    model.c13_inicio_exacto = pyo.Constraint(model.sPedidos, model.sProcesos, model.sLineas, rule=c13_s_igual_rule)

    # 4.5 Tiempo de proceso del pedido (Ecuaciones 14 y c15)

    def c14_tiempo_total_manual_rule(m, p, j, l):
        if m.pEsManualLinea[l].value == 1 and m.pPedidoEnLinea[p, j, l].value == 1 and m.pProcesosenPedido[p, j].value == 1:
            return (sum(m.vTrabajadoresProc[p, j, t, l] * m.pDeltaTiempo for t in m.sPeriodos) >= \
                    m.pTiempoProcUnidad[p, j] * m.pNumUnidades[p])
        else:
            return pyo.Constraint.Skip

    model.c14_tiempo_total_manual = pyo.Constraint(model.sPedidos, model.sProcesos, model.sLineas,
                                                  rule=c14_tiempo_total_manual_rule)

    def c15_tiempo_total_auto_rule(m, p, j, l):
        if m.pEsManualLinea[l].value == 0 and m.pPedidoEnLinea[p, j, l].value == 1 and m.pProcesosenPedido[p, j].value == 1:
            return (sum(m.v01Procesando[p, j, t, l] * m.pDeltaTiempo for t in m.sPeriodos) >= \
                    m.pTiempoProcUnidad[p, j] * m.pNumUnidades[p])
        else:
            return pyo.Constraint.Skip

    model.c15_tiempo_total_auto = pyo.Constraint(model.sPedidos, model.sProcesos, model.sLineas,
                                                rule=c15_tiempo_total_auto_rule)

    # 4.6 Tiempos de preparación (Ecuaciones 16-20)

    def c16_end_link_rule(m, p, j, t, l):
        if m.pProcesosenPedido[p, j].value == m.pPedidoEnLinea[p, j, l].value == 1:
            return m.vFin[p, j, l] >= m.v01Procesando[p, j, t, l] * t * m.pDeltaTiempo
        else:
            return pyo.Constraint.Skip

    model.c16_end = pyo.Constraint(model.sPedidos, model.sProcesos, model.sPeriodos, model.sLineas, rule=c16_end_link_rule)

    def c17_start_link_rule(m, p, j, t, l):
        if m.pProcesosenPedido[p, j].value == m.pPedidoEnLinea[p, j, l].value == 1:
            return m.vInicio[p, j, l] <= (t - 1) * m.pDeltaTiempo - m.pHorizonteSemanal * (m.v01Procesando[p, j, t, l] - 1)
        else:
            return pyo.Constraint.Skip

    # model.c17_start = pyo.Constraint(model.sPedidos, model.sProcesos, model.sPeriodos, model.sLineas, rule=c17_start_link_rule)

    def c18_duracion_rule(m, p, j, l):
        if m.pProcesosenPedido[p, j].value == m.pPedidoEnLinea[p, j, l].value == 1:
            return m.vFin[p, j, l] - m.vInicio[p, j, l] == sum(m.v01Procesando[p, j, t, l] * m.pDeltaTiempo for t in m.sPeriodos)
        else:
            return pyo.Constraint.Skip

    model.c18_duracion = pyo.Constraint(model.sPedidos, model.sProcesos, model.sLineas, rule=c18_duracion_rule)

    def c19_siguiente_proceso_rule(m, p, j, l, l2):
        if (j + 1 in m.sProcesos and m.pProcesosenPedido[p, j].value == 1 and m.pProcesosenPedido[p, j + 1].value == 1 \
                and m.pPedidoEnLinea[p, j, l].value == 1 and m.pPedidoEnLinea[p, j + 1, l2].value == 1):
            return m.vInicio[p, j + 1, l2] >= m.vFin[p, j, l]
        else:
            return pyo.Constraint.Skip

    model.c19_siguiente_proceso = pyo.Constraint(model.sPedidos, model.sProcesos, model.sLineas, model.sLineas, rule=c19_siguiente_proceso_rule)

    def c20_setup_secuencia_rule(m, p, p2, j, j2, r, l):
        if p != p2 and r + 1 in m.sPosiciones and m.pPedidoEnLinea[p, j, l].value == 1 and m.pPedidoEnLinea[
            p2, j2, l].value == 1 \
                and m.pProcesosenPedido[p, j].value == 1 and m.pProcesosenPedido[p2, j2].value == 1:
            alpha1 = m.v01Posicion[p, j, r, l]
            alpha_next1 = m.v01Posicion[p2, j2, r + 1, l]
            return m.vInicio[p2, j2, l] - m.vFin[p, j, l] >= m.pTiempoSetup[p, p2] + \
                (alpha1 + alpha_next1 - 2) * (m.pHorizonteSemanal - m.pTiempoSetup[p, p2])
        return pyo.Constraint.Skip

    model.c20_setup_secuencia = pyo.Constraint(model.sPedidos, model.sPedidos, model.sProcesos, model.sProcesos, model.sPosiciones, model.sLineas, rule=c20_setup_secuencia_rule)

    # 4.7 Detección de pedidos consecutivos (Ecuaciones 21-23)

    def c21_beta_ub_p(m, p, p2, r, l):
        if p != p2 and (r + 1) in m.sPosiciones:
            return m.v01Consecutivo[p, p2, r, l] <= sum(m.v01Posicion[p, j, r, l] for j in m.sProcesos
                if m.pProcesosenPedido[p, j].value == 1 and m.pPedidoEnLinea[p, j, l].value == 1)
        return m.v01Consecutivo[p,p2,r,l] == 0

    model.c21_beta_ub_p = pyo.Constraint(model.sPedidos, model.sPedidos, model.sPosiciones, model.sLineas, rule=c21_beta_ub_p)

    def c22_beta_ub_p2(m, p, p2, r, l):
        if p != p2 and (r + 1) in m.sPosiciones:
            return m.v01Consecutivo[p, p2, r, l] <= sum(m.v01Posicion[p2, j2, r + 1, l] for j2 in m.sProcesos
                if m.pProcesosenPedido[p2, j2].value == 1 and m.pPedidoEnLinea[p2, j2, l].value == 1)
        return m.v01Consecutivo[p,p2,r,l] == 0

    model.c22_beta_ub_p2 = pyo.Constraint(model.sPedidos, model.sPedidos, model.sPosiciones, model.sLineas, rule=c22_beta_ub_p2)

    def c23_beta_lb(m, p, p2, r, l):
        if p != p2 and (r + 1) in m.sPosiciones:
            s1 = sum(m.v01Posicion[p, j, r, l] for j in m.sProcesos
                     if m.pProcesosenPedido[p, j].value == 1 and m.pPedidoEnLinea[p, j, l].value == 1)
            s2 = sum(m.v01Posicion[p2, j2, r + 1, l] for j2 in m.sProcesos
                     if m.pProcesosenPedido[p2, j2].value == 1 and m.pPedidoEnLinea[p2, j2, l].value == 1)
            return m.v01Consecutivo[p, p2, r, l] >= s1 + s2 - 1
        return pyo.Constraint.Skip

    model.c23_beta_lb = pyo.Constraint(model.sPedidos, model.sPedidos, model.sPosiciones, model.sLineas, rule=c23_beta_lb)

    # 4.8 Activación y posicionamiento del setup (Ecuaciones 24-26)

    def c24_setup_act_si_consec(m, p, p2, t, l):
        if p != p2:
            return m.v01SetupAct[p, p2, t, l] <= sum(m.v01Consecutivo[p, p2, r, l] for r in m.sPosiciones if (r + 1) in m.sPosiciones)
        return pyo.Constraint.Skip

    model.c24_setup_act_si_consec = pyo.Constraint(model.sPedidos, model.sPedidos, model.sPeriodos, model.sLineas, rule=c24_setup_act_si_consec)

    def c25_setup_antes_de_arranque(m, p, p2, t, l):
        if p != p2:
            return m.v01SetupAct[p, p2, t, l] <= sum(m.v01Arranque[p2, j2, tau, l] for j2 in m.sProcesos for tau in m.sPeriodos
                if tau >= t + 1 and m.pProcesosenPedido[p2, j2].value == 1 and m.pPedidoEnLinea[p2, j2, l].value == 1)
        return pyo.Constraint.Skip

    model.c25_setup_antes_de_arranque = pyo.Constraint(model.sPedidos, model.sPedidos, model.sPeriodos, model.sLineas, rule=c25_setup_antes_de_arranque)

    def c26_setup_despues_de_fin_p(m, p, p2, t, tau, j, l):
        if p != p2 and tau >= t and m.pProcesosenPedido[p, j].value == 1 and m.pPedidoEnLinea[p, j, l].value == 1:
            return m.v01SetupAct[p, p2, t, l] + m.v01Procesando[p, j, tau, l] <= 1
        return pyo.Constraint.Skip

    model.c26_setup_despues_de_fin_p = pyo.Constraint(model.sPedidos, model.sPedidos, model.sPeriodos, model.sPeriodos, model.sProcesos, model.sLineas, rule=c26_setup_despues_de_fin_p)

    # 4.9 Duración del setup (Ecuaciones 27 y 28)

    def c27_min_tiempo_setup(m, p, p2, l):
        if p != p2:
            return sum(m.vTrabajadoresSetup[p, p2, t, l] * m.pDeltaTiempo for t in m.sPeriodos) >= \
                m.pTiempoSetup[p, p2] * sum(m.v01Consecutivo[p, p2, r, l] for r in m.sPosiciones if (r + 1) in m.sPosiciones)
        return pyo.Constraint.Skip

    model.c27_min_tiempo_setup = pyo.Constraint(model.sPedidos, model.sPedidos, model.sLineas, rule=c27_min_tiempo_setup)

    def c28_eq_numperiodos_con_z(m, p, p2, r, l):
        if p != p2 and r+1 in m.sPosiciones:
            return sum(m.v01SetupAct[p, p2, t, l] for t in m.sPeriodos) == pyo.ceil(m.pTiempoSetup[p, p2] / m.pDeltaTiempo) * sum(m.v01Consecutivo[p, p2, r, l] for r in m.sPosiciones if r+1 in m.sPosiciones)
        return pyo.Constraint.Skip

    model.c28_eq_numperiodos_con_z = pyo.Constraint(model.sPedidos, model.sPedidos, model.sPosiciones, model.sLineas, rule=c28_eq_numperiodos_con_z)

    # 4.10 Unicidad de posición del pedido (Ecuaciones 29-33)

    def c29_pos_unica_por_pedido_rule(m, p, j, l):
        if m.pProcesosenPedido[p, j].value == 1:
            return sum(m.v01Posicion[p, j, r, l] for r in m.sPosiciones) == m.pPedidoEnLinea[p, j, l]
        else:
            return pyo.Constraint.Skip

    model.c29_pos_unica_por_pedido = pyo.Constraint(model.sPedidos, model.sProcesos, model.sLineas,
                                                    rule=c29_pos_unica_por_pedido_rule)

    def c30_pos_unica_por_pedido_rule(m, p, j, r, l):
        if m.pPedidoEnLinea[p, j, l].value == m.pProcesosenPedido[p, j].value == 1:
            return sum(m.v01Posicion[p, j, r, l] for p in m.sPedidos for j in m.sProcesos) <= 1
        else:
            return pyo.Constraint.Skip

    model.c30_pos_unica_por_pedido = pyo.Constraint(model.sPedidos, model.sProcesos, model.sPosiciones, model.sLineas,
                                                    rule=c30_pos_unica_por_pedido_rule)

    def c31_prefijo_rule(m, r, l):
        if r + 1 in m.sPosiciones:
            hay_algo = any(m.pProcesosenPedido[p, j].value == 1 and m.pPedidoEnLinea[p, j, l].value == 1
                           for p in m.sPedidos for j in m.sProcesos)
            if not hay_algo:
                return pyo.Constraint.Feasible
            else:
                return sum(m.v01Posicion[p, j, r + 1, l] for p in m.sPedidos for j in m.sProcesos if
                           m.pProcesosenPedido[p, j].value == 1 and m.pPedidoEnLinea[p, j, l].value == 1) <= \
                    sum(m.v01Posicion[p, j, r, l] for p in m.sPedidos for j in m.sProcesos if
                        m.pProcesosenPedido[p, j].value == 1 and m.pPedidoEnLinea[p, j, l].value == 1)
        return pyo.Constraint.Skip

    model.c31_prefijo = pyo.Constraint(model.sPosiciones, model.sLineas, rule=c31_prefijo_rule)

    def c32_x_implica_pos_rule(m, p, j, t, l):
        if m.pProcesosenPedido[p, j].value == 1 and m.pPedidoEnLinea[p, j, l].value == 1:
            return m.v01Procesando[p, j, t, l] <= sum(m.v01Posicion[p, j, r, l] for r in m.sPosiciones)
        return pyo.Constraint.Skip

    model.c32_x_implica_pos = pyo.Constraint(model.sPedidos, model.sProcesos, model.sPeriodos, model.sLineas, rule=c32_x_implica_pos_rule)

    # 4.11 Retraso (Ecuación 34)

    def c33_retraso_def_rule(m, p, j, l):
        if m.pPedidoEnLinea[p, j, l].value == 1:
            j_ultimo = sum(m.pProcesosenPedido[p, j].value for j in m.sProcesos if m.pProcesosenPedido[p, j].value == 1)
            if j == j_ultimo:
                return m.vRetraso[p] >= m.vFin[p, j, l] - m.pFechaLimite[p]
            else:
                return pyo.Constraint.Skip
        else:
            return pyo.Constraint.Skip

    model.c33_retraso = pyo.Constraint(model.sPedidos, model.sProcesos, model.sLineas, rule=c33_retraso_def_rule)

    # FUNCIÓN OBJETIVO
    def obj_rule(m):
        return sum(m.vRetraso[p] for p in m.sPedidos) + 1e-4 * sum(m.v01Procesando[p, j, t, l] for p in m.sPedidos for j in m.sProcesos for t in m.sPeriodos for l in m.sLineas)

    model.f_obj = pyo.Objective(rule=obj_rule, sense=pyo.minimize, doc='Min. retraso')

    return model
