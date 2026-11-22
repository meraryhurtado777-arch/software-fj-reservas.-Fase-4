# Importa las clases de servicios especializados para instanciar el catálogo de Software FJ.
from servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala
# Importa la clase orquestadora que maneja listas internas, excepciones y logs.
from sistema import SistemaGestionFJ


# Ejecuta una batería secuencial de pruebas funcionales y de manejo de errores.
def ejecutar_pruebas_secuenciales() -> None:
    # Crea la instancia principal del sistema sin usar base de datos.
    sistema = SistemaGestionFJ(nombre_empresa="Software FJ", ruta_log="software_fj.log")
    # Muestra un encabezado claro para el paso 1 de validación.
    print("\n--- PASO 1: Registro de clientes (válidos e inválidos) ---")
    # Registra un cliente válido con datos correctos.
    sistema.registrar_cliente("CLI-01", "Laura Gómez", "laura.gomez@correo.com", "3104567890")
    # Intenta registrar un cliente con correo inválido para comprobar manejo de error sin detener el sistema.
    sistema.registrar_cliente("CLI-02", "Carlos Ruiz", "correo_sin_arroba", "3112223344")
    # Intenta registrar un cliente con nombre vacío para validar el control de datos faltantes/inválidos.
    sistema.registrar_cliente("CLI-03", "   ", "carlos.ruiz@correo.com", "3125556677")

    # Muestra un encabezado para el paso 2 de registro de servicios especializados.
    print("\n--- PASO 2: Registro de servicios (sala, equipo, asesoría y no disponible) ---")
    # Crea un servicio de reserva de sala con tarifa por hora y capacidad máxima.
    sala_a = ReservaSala("SAL-01", "Sala de Reuniones Andes", tarifa_hora=45000, capacidad_maxima=10, disponible=True)
    # Crea un servicio de alquiler de equipos con tarifa diaria y stock disponible.
    equipo_proy = AlquilerEquipo("EQP-01", "Proyector HD y Laptop", tarifa_dia=80000, stock_unidades=5, disponible=True)
    # Crea un servicio de asesoría especializada con tarifa por sesión.
    asesoria_arq = AsesoriaEspecializada("ASE-01", "Arquitectura de Software", tarifa_sesion=120000, especialidad="Cloud & POO", disponible=True)
    # Crea un servicio marcado como no disponible para probar bloqueos de disponibilidad.
    sala_mant = ReservaSala("SAL-02", "Auditorio Principal", tarifa_hora=90000, capacidad_maxima=30, disponible=False)
    # Registra cada servicio en la lista interna del sistema.
    sistema.registrar_servicio(sala_a)
    sistema.registrar_servicio(equipo_proy)
    sistema.registrar_servicio(asesoria_arq)
    sistema.registrar_servicio(sala_mant)

    # Muestra un encabezado para el paso 3 de cálculo de costos y sobrecarga/parámetros opcionales.
    print("\n--- PASO 3: Validación de cálculo de costos con descuentos e impuestos ---")
    # Calcula costo de sala para 3 horas con 10% de descuento y 19% de impuesto.
    costo_sala = sala_a.calcular_costo(cantidad=3, descuento_pct=10.0, impuesto_pct=19.0)
    # Imprime el costo calculado de la sala.
    print(f"Costo calculado sala (3h, desc 10%, imp 19%): ${costo_sala:.2f}")
    # Prueba el método sobrecargado de ajuste adicional con un porcentaje numérico.
    ajuste_prueba = sala_a.calcular_ajuste_adicional(15)
    # Imprime el ajuste calculado sobre la tarifa base.
    print(f"Ajuste adicional (15% sobre tarifa base): ${ajuste_prueba:.2f}")

    # Muestra un encabezado para el paso 4 de creación y ciclo de vida de reservas.
    print("\n--- PASO 4: Creación, confirmación y procesamiento de reservas ---")
    # Crea una reserva válida validando asistentes dentro de la capacidad de la sala.
    res_1 = sistema.crear_reserva("RES-01", "CLI-01", "SAL-01", duracion=2, descuento_pct=5.0, impuesto_pct=19.0, horas=2, asistentes=6)
    # Confirma la reserva creada si existe.
    if res_1:
        # Ejecuta la confirmación de la reserva RES-01.
        sistema.gestionar_reserva("RES-01", "confirmar")
        # Ejecuta el procesamiento final de la reserva RES-01.
        sistema.gestionar_reserva("RES-01", "procesar")

    # Muestra un encabezado para el paso 5 de escenarios de error controlados.
    print("\n--- PASO 5: Pruebas de errores (no disponible, capacidad excedida, operación inválida) ---")
    # Intenta reservar un servicio no disponible (SAL-02).
    sistema.crear_reserva("RES-02", "CLI-01", "SAL-02", duracion=1)
    # Intenta reservar una sala superando su capacidad máxima de asistentes.
    sistema.crear_reserva("RES-03", "CLI-01", "SAL-01", duracion=1, horas=1, asistentes=25)
    # Intenta cancelar una reserva que ya fue procesada (operación no permitida).
    sistema.gestionar_reserva("RES-01", "cancelar", motivo="Intento tardío")
    # Intenta procesar una reserva inexistente.
    sistema.gestionar_reserva("RES-99", "procesar")

    # Muestra un resumen final de las listas internas en memoria.
    print("\n--- RESUMEN FINAL EN MEMORIA ---")
    # Lista los clientes almacenados en memoria.
    print(f"Total clientes registrados: {len(sistema.clientes)}")
    # Lista los servicios almacenados en memoria.
    print(f"Total servicios registrados: {len(sistema.servicios)}")
    # Lista las reservas almacenadas en memoria y muestra su estado final.
    print(f"Total reservas registradas: {len(sistema.reservas)}")
    # Recorre las reservas para imprimir su resumen actual.
    for r in sistema.reservas:
        # Imprime el resumen de cada reserva.
        print(" -", r.resumen())


# Punto de entrada estándar que ejecuta las pruebas secuenciales al correr main.py.
if __name__ == "__main__":
    # Llama a la función principal de validación secuencial.
    ejecutar_pruebas_secuenciales()