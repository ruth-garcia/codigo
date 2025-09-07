if __name__ == "__main__":
    instance = create_test_instance()
    solve_instance(instance)
    
    df_pos, df_crono = dataframe(instance)
    print("\nFichero guardado: 'solucion_CEE.xlsx'")
    
    print("done")
