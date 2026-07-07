# Tarea #3 - Dashboards en Python<br>"Panama-Metropolitan-Medical"
### Asignatura: Análisis de Datos y Toma de Decisiones para Computación
### Grupo: 1IL133
### Integrantes:  
- Miguel Man          8-1032-360 

- Roberto Castillo    2-758-246 

- David Roa           E-8-240914

## Descripción del Proyecto
Este proyecto, como Tarea #3, es un Dashboard basado en el Modelo-Vista-Controlador (en Flask + Dash + Plotly) elaborado en el lenguaje de programación python. 
Este, mediante filtros por ubicación y el estado de la cita (completado-cancelado), permite visualizar las estadísticas principales y más relevantes de las vista de administrador dentro de la base de datos de Panama-Metropolitan-Medical.

## Introducción al Dataset
* Nuestro dataset seleccionado se basa en el proyecto 2 del curso de Base de Datos II que fue una base de datos llamada Panamá Metropolitan Medical. Se decidió utilizar la vista creada de Administrador ya que es la más completa y nos permitirá realizar un análisis más profundo a los procesos de la clínica. 

* Los datos de esta vista fueron generados con la página Mockaroo donde se especificaron los tipos de datos, limitaciones, entre otros de las columnas a rellenar.
* El dataset contiene los datos principales de Pacientes, Médicos, Clínicas, entre otros.

## Visualizaciones Implementadas
Dentro del dashboard elaborado se muestran las siguientes gráficas, separadas en 3 secciones distintivas:

### Visión General y Tráfico Operativo

1. **Cantidad de Citas por Mes**: que visualiza el volumen total de pacientes atendidos por mes en las sucursales.
   
2. **Completados vs Cancelados**: que visualiza la proporción de citas que fueron tanto completadas como canceladas.
   
3. **Tasa de Cancelación por Sucursal**: que visualiza cuantas citas de una sucursal fueron canceladas.
   
4. **Cantidad de Pacientes por Número de Visitas**: que visualiza la distribución de recurrencia de pacientes, es decir la cantidad de pacientes que tuvieron x cantidad de visitas a una sucursal.
   
5. **Expansión Geográfica de Pacientes por Sucursal y Mes**: que visualiza la cantidad de pacientes por sucursal de una forma más dinámica por medio de un mapa interactivo.

### Desempeño Financiero
   
6. **Ingreso Total por Mes**: que visualiza la tendencia de ingresos mensuales.
   
7. **Ingreso Total por Sucursal**: que visualiza cuanta ganancia generó una sucursal en el año.

8. **Composición de Ingresos del Total de Pagos por Sucursal**: que visualiza la proporción del pago total de las citas atendidas de una sucursal, por el pacientee y la aseguradora.

9. **Dispersión y Valores Atípicos del Costo de Citas**: que visualiza mediante gráficas de caja y bigotes el rango principal del costo de una cita y algún valor atípico que haya ocurrido.

### Rendimiento del Personal Médico

10. **Pacientes Atendidos por Doctor**: que visualiza la cantidad de pacientes que han atendido los 20 doctores con más número de atendidos.

11. **Total recaudado por Doctor**: que visualiza la cantidad de ingresos que han generado los 20 doctores con más ingresos.

