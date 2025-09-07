def _val(x, tol=1e-9):
    try:
        v = pyo.value(x)
        if v is None:
            return None
        if isinstance(v, float) and math.isnan(v):
            return None
        return float(v)
    except:
        return None

def dataframe(instance, tol=1e-6):
    # -------------------- Tabla 1: FUNCIÓN OBJETIVO --------------------
    retraso1= {}

    for p in instance.sPedidos:
        retraso1[p] = _val(instance.vRetraso[p], tol=tol) or 0.0

    filas_retraso= []

    valor_objetivo = _val(instance.f_obj)

    filas_retraso.append({
        'Concepto': 'Funcion Objetivo',
        'Valor': valor_objetivo,
        'Pedido': None
    })

    for p in instance.sPedidos:
        filas_retraso.append({
            'Concepto': 'Retraso',
            'Pedido': p,
            'Retraso': retraso1[p]
        })

    df_funcobjetivo = pd.DataFrame(filas_retraso)
    if not df_funcobjetivo.empty:
        df_funcobjetivo = df_funcobjetivo.sort_values(["Valor", "Pedido", "Retraso"]).reset_index(drop=True)

    # -------------------- Tabla 2: POSICIONES --------------------
    filas_pos = []
    for l in instance.sLineas:
        for r in instance.sPosiciones:
            # buscamos qué (p,j) ocupa esa posición r en l
            for p in instance.sPedidos:
                for j in instance.sProcesos:
                    if pyo.value(instance.pProcesosenPedido[p, j]) != 1:
                        continue
                    if pyo.value(instance.pPedidoEnLinea[p, j, l]) != 1:
                        continue
                    val = _val(instance.v01Posicion[p, j, r, l])
                    if val is not None and val > 0.5:
                        filas_pos.append({
                            "Linea": l,
                            "Posicion": r,
                            "Pedido": p,
                            "Proceso": j,
                        })
    df_posiciones = pd.DataFrame(filas_pos)
    if not df_posiciones.empty:
        # df_posiciones = df_posiciones.sort_values(["Pedido", "Proceso", "Linea", "Posicion"]).reset_index(drop=True)
        df_posiciones = df_posiciones.sort_values(["Linea", "Posicion", "Pedido", "Proceso"]).reset_index(drop=True)

    # --------- Precalcular inicios, finales y retraso por (p,j,l)/p ----------
    inicio = {}
    fin = {}
    retraso = {}
    fechalimite={}

    for p in instance.sPedidos:
        fechalimite[p] = _val(instance.pFechaLimite[p], tol=tol) or 0.0

    for p in instance.sPedidos:
        retraso[p] = _val(instance.vRetraso[p], tol=tol) or 0.0
        for j in instance.sProcesos:
            for l in instance.sLineas:
                if pyo.value(instance.pProcesosenPedido[p, j]) == 1 and pyo.value(instance.pPedidoEnLinea[p, j, l]) == 1:
                    inicio[(p, j, l)] = _val(instance.vInicio[p, j, l], tol=tol)
                    fin[(p, j, l)] = _val(instance.vFin[p, j, l], tol=tol)

    # periodos_activos = {}
    # for p in instance.sPedidos:
    #     for j in instance.sProcesos:
    #         for l in instance.sLineas:
    #             if pyo.value(instance.pProcesosenPedido[p, j]) != 1 or pyo.value(instance.pPedidoEnLinea[p, j, l]) != 1:
    #                 continue
    #             ts = []
    #             for t in instance.sPeriodos:
    #                 x = _val(instance.v01Procesando[p, j, t, l], tol=tol)
    #                 if x is not None and x > 0.5:
    #                     ts.append(int(t))
    #             if ts:
    #                 periodos_activos[(p, j, l)] = (min(ts), max(ts))

    # -------------------- Tabla 3: CRONOLOGÍA --------------------
    filas_crono = []

    # 2A) Producción (solo cuando x=1)
    for p in instance.sPedidos:
        for j in instance.sProcesos:
            for l in instance.sLineas:
                if pyo.value(instance.pProcesosenPedido[p, j]) != 1 or pyo.value(instance.pPedidoEnLinea[p, j, l]) != 1:
                    continue
                # t_min, t_max = None, None
                # if (p, j, l) in periodos_activos:
                #     t_min, t_max = periodos_activos[(p, j, l)]
                for t in instance.sPeriodos:
                    x = _val(instance.v01Procesando[p, j, t, l], tol=tol)
                    if x is None or x <= 0.5:
                        continue
                    w = _val(instance.vTrabajadoresProc[p, j, t, l], tol=tol)
                    filas_crono.append({
                        "Tipo": "Produccion",
                        "Pedido": p,
                        "PedidoDestino": None,
                        "Proceso": j,
                        "Periodo": t,
                        "Linea": l,
                        "TrabajadoresProc": 0 if w is None else w,
                        "t_inicio": inicio.get((p, j, l)),
                        "t_fin":    fin.get((p, j, l)),
                        # "PeriodoInicio": t_min,
                        # "PeriodoFin": t_max,
                        "FechaLimite": fechalimite[p],
                        "RetrasoPedido": retraso[p]
                    })

    # 2B) Setups (y > 0)
    for l in instance.sLineas:
        for t in instance.sPeriodos:
            for p in instance.sPedidos:
                for p2 in instance.sPedidos:
                    if p == p2:
                        continue
                    y = _val(instance.vTrabajadoresSetup[p, p2, t, l], tol=tol)
                    if y is not None and y > tol:
                        filas_crono.append({
                            "Tipo": "Setup",
                            "Pedido": p,
                            "PedidoDestino": p2,
                            "Proceso": None,
                            "Periodo": t,
                            "Linea": l,
                            "TrabajadoresSetup": y
                        })

    df_cronologia = pd.DataFrame(filas_crono)
    if not df_cronologia.empty:
        df_cronologia = df_cronologia.sort_values(["Pedido", "Proceso", "Periodo", "Linea", "Tipo"]).reset_index(drop=True)

    with pd.ExcelWriter("solucion_CEE.xlsx") as wr:
        df_funcobjetivo.to_excel(wr, sheet_name="funcion_objeto", index=False)
        df_posiciones.to_excel(wr, sheet_name="Posiciones", index=False)
        df_cronologia.to_excel(wr, sheet_name="Cronologia", index=False)

    # Muestra breve en consola
    print("\n=== TABLA POSICIONES (primeras filas) ===")
    print(df_posiciones.head(20).to_string(index=False))
    print("\n=== TABLA CRONOLOGIA (primeras filas) ===")
    print(df_cronologia.head(20).to_string(index=False))

    return df_posiciones, df_cronologia
\end{lstlisting}

\subsubsection{Programa principal}

\begin{lstlisting}
if __name__ == "__main__":
    instance = create_test_instance()
    solve_instance(instance)
    
    df_pos, df_crono = dataframe(instance)
    print("\nFichero guardado: 'solucion_CEE.xlsx'")
    
    print("done")
