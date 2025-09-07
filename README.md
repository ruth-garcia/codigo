# Herramienta para la planificación de la producción (TFG)
Este repositorio contiene el modelo base del programa destinado a generar planes semanales de producción, así como las diferentes instancias analizadas y las funciones de demostración.

**El repositorio cuenta con 4 carpetas:**
- **Programa:** contiene el programa principal a ejecutar.
- **Funciones:** contiene las funciones por separado presentes en el programa principal.
- **Comprobacion:** contiene las dos funciones necesarias si se quiere comprobar la validez de las soluciones. Estas comprobaciones lanzan avisos si la solución no cumple con los requisitos.
- **Instancias:** están añadidas los datos de instancia de los 5 casos analizados. Existen dos funciones con respecto al caso real, uno es el caso real tal y como es, y en el el otro archivo se desprecian los setups tal y como se indica en su correspondiente capítulo del TFG, a partir del cual se obtiene la solución analizada. Únicamente habría que coger estos datos e intercambiar la función 'create_test_data' por la que se desee para poder obtener las soluciones del análisis computacional.

**Ejecución:** es necesario crear el entorno en Python e instalar las instancias (pyomo, pandas y openpyxl)
