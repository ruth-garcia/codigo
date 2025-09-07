def solve_instance(instance):

    try:
        # Selección del solver
        opt = pyo.SolverFactory('gurobi')

        # Resolvemos
        results = opt.solve(instance, tee=True)

        # Verificamos el estado de la solución
        if results.solver.status == pyo.SolverStatus.ok and \
                results.solver.termination_condition == pyo.TerminationCondition.optimal:
            print("\n¡Solución óptima encontrada!")
            print(f"Función objetivo (retraso total): {pyo.value(instance.f_obj)}")

            print("\nRetrasos por pedido:")
            for p in instance.sPedidos:
                print(f"Pedido {p}: {pyo.value(instance.vRetraso[p]):.2f} horas")

        else:
            print("\nNo se encontró una solución óptima")
            print(f"Estado del solver: {results.solver.status}")
            print(f"Condición de terminación: {results.solver.termination_condition}")

    except Exception as e:
        print(f"Error al resolver el modelo: {str(e)}")
