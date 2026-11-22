# Importa la clase Cliente desde entidades para gestionar los clientes del sistema.
from entidades import Cliente
# Importa las excepciones personalizadas del dominio para validar y controlar errores.
from excepciones import (
    CalculoInconsistenteError,
    ErrorSistemaFJ,
    ErrorValidacionDato,
    OperacionReservaInvalidaError,
)
# Importa GestorLogs para escribir eventos y errores en un archivo sin usar base de datos.
from gestor_logs import GestorLogs
# Importa la clase Reserva para administrar el estado y ciclo de vida de cada reserva.
from reservas import Reserva
# Importa la clase base Servicio para gestionar el catálogo de servicios de Software FJ.
from servicios import Servicio


# Define la clase principal que coordina clientes, servicios, reservas y logs en memoria.
class SistemaGestionFJ:
    # Inicializa las listas internas de objetos y el gestor de logs para Software FJ.
    def __init__(self, nombre_empresa: str = "Software FJ", ruta_log: str = "software_fj.log"):
        # Guarda el nombre de la empresa.
        self.nombre_empresa = nombre_empresa
        # Lista interna en memoria para almacenar objetos Cliente (sin base de datos).
        self.clientes: list[Cliente] = []
        # Lista interna en memoria para almacenar objetos Servicio (sin base de datos).
        self.servicios: list[Servicio] = []
        # Lista interna en memoria para almacenar objetos Reserva (sin base de datos).
        self.reservas: list[Reserva] = []
        # Crea el gestor de logs encargado de registrar eventos y errores en archivo.
        self.logs = GestorLogs(ruta_archivo=ruta_log)
        # Registra en el archivo de log que el sistema inició correctamente.
        self.logs.registrar_info(f"Sistema '{self.nombre_empresa}' inicializado.")

    # Busca un cliente por su identificador dentro de la lista interna.
    def buscar_cliente(self, id_cliente: str) -> Cliente:
        # Recorre la lista de clientes registrados en memoria.
        for cliente in self.clientes:
            # Compara el identificador limpiando espacios externos.
            if cliente.id_entidad == str(id_cliente).strip():
                # Retorna el objeto Cliente encontrado.
                return cliente
        # Lanza ErrorValidacionDato si no se encuentra un cliente con ese identificador.
        raise ErrorValidacionDato(f"No se encontró un cliente con ID '{id_cliente}'.")

    # Busca un servicio por su identificador dentro de la lista interna.
    def buscar_servicio(self, id_servicio: str) -> Servicio:
        # Recorre la lista de servicios registrados en memoria.
        for servicio in self.servicios:
            # Compara el identificador del servicio limpiando espacios externos.
            if servicio.id_entidad == str(id_servicio).strip():
                # Retorna el objeto Servicio encontrado.
                return servicio
        # Lanza ErrorValidacionDato si no se encuentra un servicio con ese identificador.
        raise ErrorValidacionDato(f"No se encontró un servicio con ID '{id_servicio}'.")

    # Busca una reserva por su identificador dentro de la lista interna.
    def buscar_reserva(self, id_reserva: str) -> Reserva:
        # Recorre la lista de reservas registradas en memoria.
        for reserva in self.reservas:
            # Compara el identificador de la reserva limpiando espacios externos.
            if reserva.id_reserva == str(id_reserva).strip():
                # Retorna el objeto Reserva encontrado.
                return reserva
        # Lanza ErrorValidacionDato si no se encuentra una reserva con ese identificador.
        raise ErrorValidacionDato(f"No se encontró una reserva con ID '{id_reserva}'.")

    # Registra un nuevo cliente en la lista interna con manejo completo de excepciones.
    def registrar_cliente(self, id_entidad: str, nombre: str, correo: str, telefono: str) -> Cliente | None:
        # Intenta validar y crear el objeto Cliente.
        try:
            # Verifica que no exista previamente otro cliente con el mismo ID.
            if any(c.id_entidad == str(id_entidad).strip() for c in self.clientes):
                # Lanza ErrorValidacionDato ante un ID duplicado.
                raise ErrorValidacionDato(f"Ya existe un cliente registrado con ID '{id_entidad}'.")
            # Instancia Cliente aplicando encapsulación y validaciones estrictas.
            nuevo_cliente = Cliente(id_entidad=id_entidad, nombre=nombre, correo=correo, telefono=telefono)
        # Captura errores de validación o tipo y encadena si proviene de un error de bajo nivel.
        except (ErrorValidacionDato, TypeError, ValueError) as err:
            # Mantiene ErrorValidacionDato o encadena el error dentro de ErrorValidacionDato.
            error_encadenado = err if isinstance(err, ErrorValidacionDato) else ErrorValidacionDato(
                f"Error al crear cliente '{id_entidad}'."
            )
            # Registra el error en el archivo de log manteniendo la aplicación activa.
            self.logs.registrar_error(str(error_encadenado), f"Cliente ID: {id_entidad}")
            # Imprime el error controlado en consola.
            print(f"[ERROR CONTROLADO] {error_encadenado}")
            # Retorna None al no completarse el registro.
            return None
        # Ejecuta este bloque únicamente si no ocurrió ninguna excepción en try.
        else:
            # Añade el cliente válido a la lista interna.
            self.clientes.append(nuevo_cliente)
            # Registra el alta exitosa en el archivo de log.
            self.logs.registrar_info(f"Cliente registrado: {nuevo_cliente.resumen()}")
            # Retorna el cliente registrado.
            return nuevo_cliente
        # Ejecuta siempre al finalizar el bloque para cerrar el intento con trazabilidad.
        finally:
            # Registra en el log que el intento de registro de cliente concluyó.
            self.logs.registrar_info("Intento de registro de cliente finalizado.", f"ID: {id_entidad}")

    # Registra un servicio especializado en la lista interna con manejo de excepciones.
    def registrar_servicio(self, servicio: Servicio) -> Servicio | None:
        # Intenta validar que el objeto sea un Servicio y que su ID no esté repetido.
        try:
            # Valida que el parámetro recibido herede de Servicio.
            if not isinstance(servicio, Servicio):
                # Lanza ErrorValidacionDato si el objeto no es un servicio válido.
                raise ErrorValidacionDato("Solo se pueden registrar objetos que hereden de Servicio.")
            # Comprueba que no exista otro servicio con el mismo ID.
            if any(s.id_entidad == servicio.id_entidad for s in self.servicios):
                # Lanza ErrorValidacionDato si el ID de servicio ya existe.
                raise ErrorValidacionDato(f"Ya existe un servicio con ID '{servicio.id_entidad}'.")
        # Captura cualquier excepción del sistema.
        except ErrorSistemaFJ as err:
            # Registra el error en el archivo de log.
            self.logs.registrar_error(str(err), "Registro de servicio")
            # Muestra el error controlado en consola sin detener el sistema.
            print(f"[ERROR CONTROLADO] {err}")
            # Retorna None indicando que no se registró el servicio.
            return None
        # Ejecuta este bloque si el registro del servicio fue válido.
        else:
            # Guarda el servicio en la lista interna de servicios.
            self.servicios.append(servicio)
            # Registra el evento en el archivo de log.
            self.logs.registrar_info(f"Servicio registrado: {servicio.describir()}")
            # Retorna el servicio registrado.
            return servicio
        # Ejecuta siempre al concluir el proceso de registro de servicio.
        finally:
            # Registra en el log la finalización del intento.
            self.logs.registrar_info("Proceso de registro de servicio finalizado.")

    # Crea una reserva validando entidades, parámetros y encadenando errores de cálculo.
    def crear_reserva(
        self,
        id_reserva: str,
        id_cliente: str,
        id_servicio: str,
        duracion: int = 1,
        descuento_pct: float = 0.0,
        impuesto_pct: float = 0.0,
        **parametros_servicio,
    ) -> Reserva | None:
        # Intenta localizar cliente y servicio, validar parámetros y construir la reserva.
        try:
            # Verifica que el ID de reserva no exista ya en la lista interna.
            if any(r.id_reserva == str(id_reserva).strip() for r in self.reservas):
                # Lanza OperacionReservaInvalidaError si el ID está duplicado.
                raise OperacionReservaInvalidaError(f"Ya existe una reserva con ID '{id_reserva}'.")
            # Busca el cliente por su identificador.
            cliente = self.buscar_cliente(id_cliente)
            # Busca el servicio por su identificador.
            servicio = self.buscar_servicio(id_servicio)
            # Si se pasaron parámetros adicionales del servicio, los valida con polimorfismo.
            if parametros_servicio:
                # Llama al método validar_parametros() correspondiente al tipo de servicio.
                servicio.validar_parametros(**parametros_servicio)
            # Intenta instanciar Reserva y encadena errores aritméticos o de cálculo.
            try:
                # Crea el objeto Reserva calculando su costo inicial.
                nueva_reserva = Reserva(
                    id_reserva=id_reserva,
                    cliente=cliente,
                    servicio=servicio,
                    duracion=duracion,
                    descuento_pct=descuento_pct,
                    impuesto_pct=impuesto_pct,
                )
            # Captura errores de cálculo o tipo y los encadena con 'raise ... from'.
            except (ZeroDivisionError, ArithmeticError, TypeError) as err_aritmetico:
                # Encadena la excepción original dentro de CalculoInconsistenteError.
                raise CalculoInconsistenteError(
                    f"Fallo de cálculo al generar la reserva '{id_reserva}'."
                ) from err_aritmetico
        # Captura excepciones del sistema, de valor o de tipo.
        except (ErrorSistemaFJ, ValueError, TypeError) as err:
            # Registra el error en el archivo de log.
            self.logs.registrar_error(str(err), f"Reserva ID: {id_reserva}")
            # Muestra el error controlado en consola sin detener la ejecución.
            print(f"[ERROR CONTROLADO] {err}")
            # Retorna None ante el fallo.
            return None
        # Ejecuta este bloque únicamente si se creó la reserva sin errores.
        else:
            # Agrega la reserva a la lista interna.
            self.reservas.append(nueva_reserva)
            # Registra la creación de la reserva en el archivo de log.
            self.logs.registrar_info(f"Reserva creada: {nueva_reserva.resumen()}")
            # Retorna la reserva creada.
            return nueva_reserva
        # Ejecuta siempre al cerrar el intento de creación.
        finally:
            # Registra en el log que terminó el intento de crear la reserva.
            self.logs.registrar_info("Intento de creación de reserva finalizado.", f"Reserva: {id_reserva}")

    # Ejecuta una acción ('confirmar', 'cancelar' o 'procesar') sobre una reserva existente.
    def gestionar_reserva(self, id_reserva: str, accion: str, motivo: str = "Cancelación estándar") -> bool:
        # Intenta buscar la reserva y ejecutar la transición de estado solicitada.
        try:
            # Busca la reserva por su identificador.
            reserva = self.buscar_reserva(id_reserva)
            # Normaliza el nombre de la acción a minúsculas sin espacios.
            accion_limpia = accion.strip().lower() if isinstance(accion, str) else ""
            # Ejecuta la acción correspondiente según su nombre.
            if accion_limpia == "confirmar":
                # Confirma la reserva.
                resultado = reserva.confirmar()
            elif accion_limpia == "cancelar":
                # Cancela la reserva indicando el motivo.
                resultado = reserva.cancelar(motivo=motivo)
            elif accion_limpia == "procesar":
                # Procesa la reserva previamente confirmada.
                resultado = reserva.procesar()
            else:
                # Lanza ErrorValidacionDato si la acción solicitada no es válida.
                raise ErrorValidacionDato(f"Acción de reserva no válida: '{accion}'.")
        # Captura errores del sistema o de valor durante la operación.
        except (ErrorSistemaFJ, ValueError) as err:
            # Registra el error en el archivo de log.
            self.logs.registrar_error(str(err), f"Acción '{accion}' en reserva '{id_reserva}'")
            # Imprime el error controlado en consola.
            print(f"[ERROR CONTROLADO] {err}")
            # Retorna False indicando que la operación falló.
            return False
        # Ejecuta este bloque si la operación sobre la reserva fue exitosa.
        else:
            # Registra el resultado exitoso en el archivo de log.
            self.logs.registrar_info(resultado)
            # Muestra el mensaje de éxito en consola.
            print(f"[OK] {resultado}")
            # Retorna True indicando éxito.
            return True
        # Ejecuta siempre al finalizar la operación sobre la reserva.
        finally:
            # Registra en el log el cierre de la operación.
            self.logs.registrar_info("Operación sobre reserva finalizada.", f"ID: {id_reserva}")
