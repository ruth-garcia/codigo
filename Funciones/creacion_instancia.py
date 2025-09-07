def create_test_instance():

    # Creamos el modelo concreto desde el abstracto
    model = get_production_planning_model()

    # Obtenemos los datos de prueba
    test_data = create_test_data()

    # Convertimos los datos al formato de Pyomo
    pyomo_data = create_input_data_for_pyomo(model, test_data)

    # Creamos la instancia
    instance = model.create_instance(pyomo_data)

    # Comprobación rápida
    variables = list(instance.component_objects(ctype=pyo.Var))
    print('Instancia cargada OK con', len(variables), 'variables')

    # Guardamos una vista previa de la instancia
    try:
        instance.pprint(ostream=open('instance_preview.txt', 'w', encoding='utf-8'))
        print("Vista previa de la instancia guardada en 'instance_preview.txt'")
    except Exception as e:
        print(f"Error al guardar la vista previa: {e}")

    return instance
