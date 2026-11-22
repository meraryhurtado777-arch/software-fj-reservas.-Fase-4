# Importa Cliente desde entidades para asociar un cliente válido a cada reserva.
from entidades import Cliente
# Importa excepciones personalizadas para validar estados, cálculos y disponibilidad.
from excepciones import CalculoInconsistenteError, ErrorValidacionDato, OperacionReservaInvalidaError
# Importa la clase base Servicio para tipado y validación del servicio reservado.
from servicios import Servicio


# Define la clase Reserva que integra cliente, servicio, duración, costo y estado.
class Reserva:
    # Define los estados válidos que puede tener una reserva durante su ciclo de vida.
    ESTADOS_VALIDOS = ("PENDIENTE", "CONFIRMADA", "CANCELADA", "PROCESADA")

    # Inicializa una reserva validando cliente, servicio y duración/cantidad.
    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion: int = 1, descuento_pct: float = 0.0, impuesto_pct: float = 0.0):
        # Valida que el identificador de reserva sea un texto no vacío.
        if not isinstance(id_reserva, str) or not id_reserva.strip():
            # Lanza ErrorValidacionDato si el ID de reserva es inválido.
            raise ErrorValidacionDato("El identificador de la reserva no puede estar vacío.")
        # Valida que el parámetro cliente sea una instancia de Cliente.
        if not isinstance(cliente, Cliente):
            # Lanza ErrorValidacionDato si no se proporciona un objeto Cliente válido.
            raise ErrorValidacionDato("La reserva requiere un objeto Cliente válido.")
        # Valida que el cliente esté activo para realizar reservas.
        if not cliente.activo:
            # Lanza OperacionReservaInvalidaError si el cliente está inactivo.
            raise OperacionReservaInvalidaError(f"El cliente '{cliente.nombre}' está inactivo y no puede reservar.")
        # Valida que el parámetro servicio sea una instancia de Servicio.
        if not isinstance(servicio, Servicio):
            # Lanza ErrorValidacionDato si no se proporciona un objeto Servicio válido.
            raise ErrorValidacionDato("La reserva requiere un objeto Servicio válido.")
        # Verifica que el servicio esté disponible antes de crear la reserva.
        servicio.verificar_disponibilidad()
        # Valida que la duración sea un número entero positivo.
        if not isinstance(duracion, int) or isinstance(duracion, bool) or duracion <= 0:
            # Lanza ErrorValidacionDato si la duración es inválida.
            raise ErrorValidacionDato("La duración de la reserva debe ser un entero mayor que cero.")
        # Guarda el identificador limpio de la reserva.
        self._id_reserva = id_reserva.strip()
        # Guarda la referencia al cliente asociado.
        self._cliente = cliente
        # Guarda la referencia al servicio reservado.
        self._servicio = servicio
        # Guarda la duración o cantidad solicitada.
        self._duracion = duracion
        # Guarda el porcentaje de descuento aplicado.
        self._descuento_pct = descuento_pct
        # Guarda el porcentaje de impuesto aplicado.
        self._impuesto_pct = impuesto_pct
        # Establece el estado inicial de la reserva en PENDIENTE.
        self._estado = "PENDIENTE"
        # Calcula el costo total inicial usando el método polimórfico del servicio.
        self._costo_total = self._calcular_costo_seguro()

    # Expone el identificador de la reserva.
    @property
    def id_reserva(self) -> str:
        # Retorna el ID de la reserva.
        return self._id_reserva

    # Expone el estado actual de la reserva.
    @property
    def estado(self) -> str:
        # Retorna el estado actual.
        return self._estado

    # Expone el costo total calculado de la reserva.
    @property
    def costo_total(self) -> float:
        # Retorna el costo total.
        return self._costo_total

    # Calcula el costo encadenando excepciones si ocurre un error de cálculo o valor.
    def _calcular_costo_seguro(self) -> float:
        # Intenta calcular el costo del servicio con duración, descuento e impuesto.
        try:
            # Invoca calcular_costo() del servicio correspondiente (polimorfismo).
            costo = self._servicio.calcular_costo(
                cantidad=self._duracion,
                descuento_pct=self._descuento_pct,
                impuesto_pct=self._impuesto_pct,
            )
            # Valida que el costo calculado sea positivo.
            if costo <= 0:
                # Lanza CalculoInconsistenteError si el resultado no es mayor que cero.
                raise CalculoInconsistenteError("El costo calculado de la reserva debe ser mayor que cero.")
            # Retorna el costo válido.
            return costo
        # Captura errores de cálculo o valor y los encadena con 'raise ... from'.
        except (CalculoInconsistenteError, ErrorValidacionDato, ValueError, TypeError) as exc:
            # Encadena la excepción original dentro de CalculoInconsistenteError.
            raise CalculoInconsistenteError(
                f"No fue posible calcular el costo de la reserva '{self._id_reserva}'."
            ) from exc

    # Confirma la reserva si se encuentra en estado PENDIENTE y el servicio está disponible.
    def confirmar(self) -> str:
        # Verifica si el estado actual permite confirmar.
        if self._estado != "PENDIENTE":
            # Lanza OperacionReservaInvalidaError si no está pendiente.
            raise OperacionReservaInvalidaError(
                f"No se puede confirmar la reserva '{self._id_reserva}' en estado '{self._estado}'."
            )
        # Revalida la disponibilidad del servicio justo antes de confirmar.
        self._servicio.verificar_disponibilidad()
        # Actualiza el estado a CONFIRMADA.
        self._estado = "CONFIRMADA"
        # Retorna mensaje de confirmación.
        return f"Reserva '{self._id_reserva}' confirmada para {self._cliente.nombre} (Total: ${self._costo_total:.2f})."

    # Cancela la reserva si no ha sido ya cancelada o procesada.
    def cancelar(self, motivo: str = "Cancelación solicitada") -> str:
        # Impide cancelar una reserva ya cancelada o ya procesada.
        if self._estado in ("CANCELADA", "PROCESADA"):
            # Lanza OperacionReservaInvalidaError ante una transición inválida.
            raise OperacionReservaInvalidaError(
                f"No se puede cancelar la reserva '{self._id_reserva}' porque está '{self._estado}'."
            )
        # Cambia el estado a CANCELADA.
        self._estado = "CANCELADA"
        # Retorna mensaje informativo con el motivo.
        return f"Reserva '{self._id_reserva}' cancelada. Motivo: {motivo}."

    # Procesa una reserva confirmada recalculando costos y marcándola como PROCESADA.
    def procesar(self) -> str:
        # Solo permite procesar reservas que estén previamente confirmadas.
        if self._estado != "CONFIRMADA":
            # Lanza OperacionReservaInvalidaError si no está confirmada.
            raise OperacionReservaInvalidaError(
                f"Solo se pueden procesar reservas CONFIRMADA; estado actual: '{self._estado}'."
            )
        # Verifica disponibilidad antes de finalizar el procesamiento.
        self._servicio.verificar_disponibilidad()
        # Recalcula el costo total para asegurar consistencia antes de procesar.
        self._costo_total = self._calcular_costo_seguro()
        # Actualiza el estado final a PROCESADA.
        self._estado = "PROCESADA"
        # Retorna confirmación del procesamiento.
        return f"Reserva '{self._id_reserva}' procesada exitosamente por un total de ${self._costo_total:.2f}."

    # Devuelve un resumen legible de la reserva y sus elementos asociados.
    def resumen(self) -> str:
        # Construye una línea descriptiva con ID, cliente, servicio, duración, total y estado.
        return (
            f"Reserva [{self._id_reserva}] | Cliente: {self._cliente.nombre} | "
            f"Servicio: {self._servicio.nombre} | Duración: {self._duracion} | "
            f"Total: ${self._costo_total:.2f} | Estado: {self._estado}"
        )