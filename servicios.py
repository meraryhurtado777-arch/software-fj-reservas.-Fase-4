# Importa ABC y abstractmethod para definir la clase abstracta Servicio y sus métodos obligatorios.
from abc import ABC, abstractmethod
# Importa functools para aplicar sobrecarga de métodos con singledispatchmethod cuando sea útil.
from functools import singledispatchmethod
# Importa EntidadSistema para que todo servicio forme parte de las entidades del sistema.
from entidades import EntidadSistema
# Importa excepciones personalizadas para validar parámetros, disponibilidad y cálculos.
from excepciones import CalculoInconsistenteError, ErrorValidacionDato, ServicioNoDisponibleError


# Define la clase abstracta Servicio que hereda de EntidadSistema.
class Servicio(EntidadSistema, ABC):
    # Inicializa un servicio con id, nombre, tarifa base, disponibilidad y estado activo.
    def __init__(self, id_entidad: str, nombre: str, tarifa_base: float, disponible: bool = True, activo: bool = True):
        # Invoca el constructor de EntidadSistema para validar id_entidad y activo.
        super().__init__(id_entidad=id_entidad, activo=activo)
        # Valida que el nombre del servicio sea un texto no vacío.
        if not isinstance(nombre, str) or not nombre.strip():
            # Lanza ErrorValidacionDato si el nombre del servicio es inválido.
            raise ErrorValidacionDato("El nombre del servicio es obligatorio y no puede estar vacío.")
        # Valida que la tarifa base sea numérica y mayor que cero.
        if not isinstance(tarifa_base, (int, float)) or isinstance(tarifa_base, bool) or tarifa_base <= 0:
            # Lanza CalculoInconsistenteError si la tarifa base es menor o igual a cero o no numérica.
            raise CalculoInconsistenteError("La tarifa base del servicio debe ser un número mayor que cero.")
        # Guarda el nombre limpio del servicio en un atributo protegido.
        self._nombre = nombre.strip()
        # Guarda la tarifa base en formato flotante en un atributo protegido.
        self._tarifa_base = float(tarifa_base)
        # Guarda la disponibilidad actual del servicio.
        self._disponible = bool(disponible)

    # Expone el nombre del servicio de forma controlada.
    @property
    def nombre(self) -> str:
        # Retorna el nombre del servicio.
        return self._nombre

    # Expone la tarifa base del servicio.
    @property
    def tarifa_base(self) -> float:
        # Retorna la tarifa base en float.
        return self._tarifa_base

    # Expone si el servicio está disponible para ser reservado.
    @property
    def disponible(self) -> bool:
        # Retorna True si está disponible y activo, de lo contrario False.
        return self._disponible and self.activo

    # Permite actualizar la disponibilidad del servicio con validación estricta.
    @disponible.setter
    def disponible(self, valor: bool) -> None:
        # Comprueba que el valor recibido sea booleano.
        if not isinstance(valor, bool):
            # Lanza ErrorValidacionDato si no es booleano.
            raise ErrorValidacionDato("La disponibilidad debe ser un valor booleano (True/False).")
        # Actualiza el atributo de disponibilidad.
        self._disponible = valor

    # Verifica que el servicio esté activo y disponible antes de operar sobre él.
    def verificar_disponibilidad(self) -> None:
        # Revisa si la entidad está inactiva o marcada como no disponible.
        if not self.activo or not self._disponible:
            # Lanza ServicioNoDisponibleError si no se puede prestar el servicio.
            raise ServicioNoDisponibleError(f"El servicio '{self._nombre}' ({self.id_entidad}) no está disponible.")

    # Método abstracto que cada servicio especializado debe sobrescribir para validar parámetros.
    @abstractmethod
    def validar_parametros(self, **kwargs) -> None:
        # Implementación obligatoria en cada subclase de Servicio.
        pass

    # Método abstracto que cada servicio especializado debe sobrescribir para describirse.
    @abstractmethod
    def describir(self) -> str:
        # Implementación obligatoria en cada subclase de Servicio.
        pass

    # Método abstracto que calcula el costo base según duración o unidades.
    @abstractmethod
    def calcular_costo(self, cantidad: float = 1, descuento_pct: float = 0.0, impuesto_pct: float = 0.0) -> float:
        # Implementación obligatoria en cada subclase de Servicio.
        pass

    # Método sobrecargado con singledispatchmethod para calcular ajustes según tipo de dato.
    @singledispatchmethod
    def calcular_ajuste_adicional(self, valor) -> float:
        # Si se recibe un tipo no soportado, lanza ErrorValidacionDato.
        raise ErrorValidacionDato(f"Tipo no soportado para ajuste adicional: {type(valor).__name__}")

    # Variante sobrecargada cuando se pasa un porcentaje numérico (int o float).
    @calcular_ajuste_adicional.register(int)
    @calcular_ajuste_adicional.register(float)
    def _(self, valor: float) -> float:
        # Evita booleanos y valida que el porcentaje esté entre 0 y 100.
        if isinstance(valor, bool) or valor < 0 or valor > 100:
            # Lanza CalculoInconsistenteError si el porcentaje está fuera de rango.
            raise CalculoInconsistenteError("El porcentaje de ajuste debe estar entre 0 y 100.")
        # Calcula el monto equivalente sobre la tarifa base.
        return round(self._tarifa_base * (valor / 100.0), 2)

    # Método auxiliar común para aplicar descuento e impuesto sobre un subtotal.
    def _aplicar_descuento_e_impuesto(self, subtotal: float, descuento_pct: float, impuesto_pct: float) -> float:
        # Valida que el subtotal sea positivo.
        if subtotal < 0:
            # Lanza CalculoInconsistenteError si el subtotal es negativo.
            raise CalculoInconsistenteError("El subtotal no puede ser negativo.")
        # Valida que los porcentajes de descuento e impuesto no sean booleanos ni estén fuera de [0, 100].
        if isinstance(descuento_pct, bool) or isinstance(impuesto_pct, bool):
            # Lanza ErrorValidacionDato si se pasan booleanos como porcentaje.
            raise ErrorValidacionDato("Los porcentajes de descuento e impuesto deben ser numéricos.")
        # Comprueba rangos válidos de porcentajes.
        if not (0 <= descuento_pct <= 100) or not (0 <= impuesto_pct <= 100):
            # Lanza CalculoInconsistenteError si algún porcentaje es inválido.
            raise CalculoInconsistenteError("Los porcentajes deben estar entre 0 y 100.")
        # Calcula el valor descontado sobre el subtotal.
        monto_descuento = subtotal * (descuento_pct / 100.0)
        # Calcula la base gravable tras descontar.
        base_con_descuento = subtotal - monto_descuento
        # Calcula el impuesto sobre la base ya descontada.
        monto_impuesto = base_con_descuento * (impuesto_pct / 100.0)
        # Calcula el total final redondeado a dos decimales.
        total_final = base_con_descuento + monto_impuesto
        # Verifica que el resultado final no sea negativo.
        if total_final < 0:
            # Lanza CalculoInconsistenteError ante un resultado inconsistente.
            raise CalculoInconsistenteError("El cálculo final del costo resultó negativo.")
        # Retorna el costo total redondeado.
        return round(total_final, 2)

    # Implementa resumen() de EntidadSistema reutilizando describir().
    def resumen(self) -> str:
        # Retorna la descripción detallada del servicio.
        return self.describir()


# Define el servicio especializado de reserva de salas para Software FJ.
class ReservaSala(Servicio):
    # Inicializa la reserva de sala con capacidad máxima de personas.
    def __init__(self, id_entidad: str, nombre: str, tarifa_hora: float, capacidad_maxima: int, disponible: bool = True):
        # Valida que la capacidad máxima sea un entero positivo.
        if not isinstance(capacidad_maxima, int) or isinstance(capacidad_maxima, bool) or capacidad_maxima <= 0:
            # Lanza ErrorValidacionDato si la capacidad no es válida.
            raise ErrorValidacionDato("La capacidad máxima de la sala debe ser un entero mayor que cero.")
        # Llama al constructor de Servicio usando tarifa_hora como tarifa_base.
        super().__init__(id_entidad=id_entidad, nombre=nombre, tarifa_base=tarifa_hora, disponible=disponible)
        # Guarda la capacidad máxima de personas de la sala.
        self.capacidad_maxima = capacidad_maxima

    # Sobrescribe validar_parametros para revisar horas y asistentes de la sala.
    def validar_parametros(self, horas: int = 1, asistentes: int = 1) -> None:
        # Valida que las horas sean un entero positivo.
        if not isinstance(horas, int) or isinstance(horas, bool) or horas <= 0:
            # Lanza ErrorValidacionDato si las horas son inválidas.
            raise ErrorValidacionDato("La duración en horas para reservar la sala debe ser un entero mayor que cero.")
        # Valida que el número de asistentes no supere la capacidad máxima de la sala.
        if not isinstance(asistentes, int) or isinstance(asistentes, bool) or asistentes <= 0 or asistentes > self.capacidad_maxima:
            # Lanza ErrorValidacionDato si los asistentes no son válidos o exceden la capacidad.
            raise ErrorValidacionDato(
                f"El número de asistentes ({asistentes}) debe estar entre 1 y {self.capacidad_maxima}."
            )

    # Sobrescribe describir() con los detalles propios de una sala.
    def describir(self) -> str:
        # Construye la descripción de la sala incluyendo capacidad y tarifa por hora.
        estado = "Disponible" if self.disponible else "No disponible"
        # Retorna el texto descriptivo del servicio.
        return f"Sala [{self.id_entidad}] '{self.nombre}' | Capacidad: {self.capacidad_maxima} pax | Tarifa/h: ${self.tarifa_base:.2f} | {estado}"

    # Sobrescribe calcular_costo() con parámetros opcionales de horas, descuento e impuesto.
    def calcular_costo(self, cantidad: int = 1, descuento_pct: float = 0.0, impuesto_pct: float = 0.0) -> float:
        # Valida que la cantidad de horas sea un entero positivo.
        if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad <= 0:
            # Lanza CalculoInconsistenteError si la cantidad de horas es inválida.
            raise CalculoInconsistenteError("La cantidad de horas para la sala debe ser mayor que cero.")
        # Calcula el subtotal multiplicando tarifa por hora por número de horas.
        subtotal = self._tarifa_base * cantidad
        # Aplica descuento e impuesto usando el método común de Servicio.
        return self._aplicar_descuento_e_impuesto(subtotal, descuento_pct, impuesto_pct)


# Define el servicio especializado de alquiler de equipos tecnológicos.
class AlquilerEquipo(Servicio):
    # Inicializa el alquiler de equipo con tipo de equipo y stock disponible.
    def __init__(self, id_entidad: str, nombre: str, tarifa_dia: float, stock_unidades: int, disponible: bool = True):
        # Valida que el stock inicial sea un entero no negativo.
        if not isinstance(stock_unidades, int) or isinstance(stock_unidades, bool) or stock_unidades < 0:
            # Lanza ErrorValidacionDato si el stock es inválido.
            raise ErrorValidacionDato("El stock de unidades debe ser un número entero igual o mayor que cero.")
        # Llama al constructor de Servicio usando tarifa_dia como tarifa_base.
        super().__init__(id_entidad=id_entidad, nombre=nombre, tarifa_base=tarifa_dia, disponible=disponible)
        # Guarda la cantidad de unidades disponibles en inventario.
        self.stock_unidades = stock_unidades

    # Sobrescribe validar_parametros para verificar días y unidades solicitadas.
    def validar_parametros(self, dias: int = 1, unidades: int = 1) -> None:
        # Valida que los días sean un entero positivo.
        if not isinstance(dias, int) or isinstance(dias, bool) or dias <= 0:
            # Lanza ErrorValidacionDato si los días son inválidos.
            raise ErrorValidacionDato("Los días de alquiler deben ser un entero mayor que cero.")
        # Valida que las unidades solicitadas no superen el stock disponible.
        if not isinstance(unidades, int) or isinstance(unidades, bool) or unidades <= 0 or unidades > self.stock_unidades:
            # Lanza ErrorValidacionDato si las unidades son inválidas o superan el stock.
            raise ErrorValidacionDato(
                f"Las unidades solicitadas ({unidades}) deben estar entre 1 y el stock disponible ({self.stock_unidades})."
            )

    # Sobrescribe describir() con información del alquiler de equipos.
    def describir(self) -> str:
        # Determina el estado actual del servicio.
        estado = "Disponible" if self.disponible else "No disponible"
        # Retorna la descripción del equipo en alquiler.
        return f"Equipo [{self.id_entidad}] '{self.nombre}' | Stock: {self.stock_unidades} und. | Tarifa/día: ${self.tarifa_base:.2f} | {estado}"

    # Sobrescribe calcular_costo() multiplicando tarifa diaria por cantidad de días y opcionalmente unidades.
    def calcular_costo(self, cantidad: int = 1, descuento_pct: float = 0.0, impuesto_pct: float = 0.0, unidades: int = 1) -> float:
        # Valida que cantidad (días) y unidades sean enteros positivos.
        if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad <= 0:
            # Lanza CalculoInconsistenteError si la cantidad de días es inválida.
            raise CalculoInconsistenteError("La cantidad de días de alquiler debe ser mayor que cero.")
        # Valida que las unidades sean válidas.
        if not isinstance(unidades, int) or isinstance(unidades, bool) or unidades <= 0:
            # Lanza CalculoInconsistenteError si las unidades son inválidas.
            raise CalculoInconsistenteError("La cantidad de unidades debe ser mayor que cero.")
        # Calcula el subtotal considerando días y unidades.
        subtotal = self._tarifa_base * cantidad * unidades
        # Aplica descuento e impuesto y devuelve el total.
        return self._aplicar_descuento_e_impuesto(subtotal, descuento_pct, impuesto_pct)


# Define el servicio especializado de asesorías técnicas o de software.
class AsesoriaEspecializada(Servicio):
    # Inicializa la asesoría con especialidad y nivel (básico, intermedio, avanzado).
    def __init__(self, id_entidad: str, nombre: str, tarifa_sesion: float, especialidad: str, disponible: bool = True):
        # Valida que la especialidad sea un texto no vacío.
        if not isinstance(especialidad, str) or not especialidad.strip():
            # Lanza ErrorValidacionDato si la especialidad está vacía.
            raise ErrorValidacionDato("La especialidad de la asesoría es obligatoria.")
        # Llama al constructor de Servicio usando tarifa_sesion como tarifa_base.
        super().__init__(id_entidad=id_entidad, nombre=nombre, tarifa_base=tarifa_sesion, disponible=disponible)
        # Guarda la especialidad de la asesoría.
        self.especialidad = especialidad.strip()

    # Sobrescribe validar_parametros para revisar la cantidad de sesiones.
    def validar_parametros(self, sesiones: int = 1) -> None:
        # Valida que el número de sesiones sea un entero positivo.
        if not isinstance(sesiones, int) or isinstance(sesiones, bool) or sesiones <= 0:
            # Lanza ErrorValidacionDato si el número de sesiones no es válido.
            raise ErrorValidacionDato("El número de sesiones de asesoría debe ser un entero mayor que cero.")

    # Sobrescribe describir() con los datos de la asesoría especializada.
    def describir(self) -> str:
        # Obtiene el estado legible del servicio.
        estado = "Disponible" if self.disponible else "No disponible"
        # Retorna la descripción de la asesoría.
        return f"Asesoría [{self.id_entidad}] '{self.nombre}' | Especialidad: {self.especialidad} | Tarifa/sesión: ${self.tarifa_base:.2f} | {estado}"

    # Sobrescribe calcular_costo() con parámetros opcionales de sesiones, descuento e impuesto.
    def calcular_costo(self, cantidad: int = 1, descuento_pct: float = 0.0, impuesto_pct: float = 0.0) -> float:
        # Valida que la cantidad de sesiones sea un entero positivo.
        if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad <= 0:
            # Lanza CalculoInconsistenteError si la cantidad de sesiones es inválida.
            raise CalculoInconsistenteError("La cantidad de sesiones debe ser mayor que cero.")
        # Calcula el subtotal según sesiones contratadas.
        subtotal = self._tarifa_base * cantidad
        # Aplica descuento e impuesto y retorna el costo final.
        return self._aplicar_descuento_e_impuesto(subtotal, descuento_pct, impuesto_pct)
