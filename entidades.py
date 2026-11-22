# Importa ABC y abstractmethod para definir clases abstractas y métodos obligatorios.
from abc import ABC, abstractmethod
# Importa ErrorValidacionDato para reportar datos inválidos o faltantes con excepciones propias.
from excepciones import ErrorValidacionDato


# Define la clase abstracta base que representa entidades generales dentro del sistema.
class EntidadSistema(ABC):
    # Inicializa una entidad con un identificador único y un estado activo por defecto.
    def __init__(self, id_entidad: str, activo: bool = True):
        # Valida que el identificador no esté vacío ni compuesto solo por espacios.
        if not isinstance(id_entidad, str) or not id_entidad.strip():
            # Lanza una excepción personalizada si el identificador es inválido.
            raise ErrorValidacionDato("El identificador de la entidad no puede estar vacío.")
        # Asigna el identificador limpio a un atributo protegido de la instancia.
        self._id_entidad = id_entidad.strip()
        # Asigna el estado booleano que indica si la entidad está activa.
        self._activo = bool(activo)

    # Expone de forma controlada el identificador de la entidad.
    @property
    def id_entidad(self) -> str:
        # Retorna el identificador almacenado.
        return self._id_entidad

    # Expone de forma controlada el estado de activación de la entidad.
    @property
    def activo(self) -> bool:
        # Retorna True o False según el estado actual.
        return self._activo

    # Permite actualizar el estado de activación validando que sea un booleano.
    @activo.setter
    def activo(self, valor: bool) -> None:
        # Verifica que el nuevo valor sea de tipo bool.
        if not isinstance(valor, bool):
            # Lanza ErrorValidacionDato si el tipo de dato no es booleano.
            raise ErrorValidacionDato("El estado 'activo' debe ser un valor booleano (True/False).")
        # Actualiza el estado interno de la entidad.
        self._activo = valor

    # Declara el método abstracto que cada entidad concreta debe implementar para resumirse.
    @abstractmethod
    def resumen(self) -> str:
        # Cuerpo vacío porque la implementación real se define en las subclases.
        pass


# Define la clase Cliente que hereda de EntidadSistema y encapsula datos personales.
class Cliente(EntidadSistema):
    # Inicializa un cliente validando identificación, nombre, correo y teléfono.
    def __init__(self, id_entidad: str, nombre: str, correo: str, telefono: str, activo: bool = True):
        # Invoca el constructor de la clase abstracta EntidadSistema.
        super().__init__(id_entidad=id_entidad, activo=activo)
        # Asigna el nombre mediante su property para ejecutar la validación estricta.
        self.nombre = nombre
        # Asigna el correo mediante su property para validar formato básico y contenido.
        self.correo = correo
        # Asigna el teléfono mediante su property para validar dígitos y longitud.
        self.telefono = telefono

    # Getter encapsulado para obtener el nombre del cliente.
    @property
    def nombre(self) -> str:
        # Retorna el atributo privado __nombre.
        return self.__nombre

    # Setter con validación estricta para el nombre del cliente.
    @nombre.setter
    def nombre(self, valor: str) -> None:
        # Comprueba que sea texto y tenga al menos 2 caracteres tras quitar espacios.
        if not isinstance(valor, str) or len(valor.strip()) < 2:
            # Lanza ErrorValidacionDato si el nombre es inválido o muy corto.
            raise ErrorValidacionDato("El nombre del cliente debe tener al menos 2 caracteres.")
        # Guarda el nombre limpio en el atributo privado __nombre.
        self.__nombre = valor.strip()

    # Getter encapsulado para obtener el correo electrónico del cliente.
    @property
    def correo(self) -> str:
        # Retorna el atributo privado __correo.
        return self.__correo

    # Setter con validación estricta para el correo electrónico.
    @correo.setter
    def correo(self, valor: str) -> None:
        # Limpia espacios y comprueba que sea cadena y contenga '@' y un punto en el dominio.
        correo_limpio = valor.strip() if isinstance(valor, str) else ""
        # Verifica presencia de '@' y dominio válido con punto después de '@'.
        if "@" not in correo_limpio or "." not in correo_limpio.split("@")[-1]:
            # Lanza ErrorValidacionDato si el correo no cumple el formato esperado.
            raise ErrorValidacionDato("El correo electrónico del cliente no es válido.")
        # Guarda el correo normalizado en minúsculas en __correo.
        self.__correo = correo_limpio.lower()

    # Getter encapsulado para obtener el teléfono del cliente.
    @property
    def telefono(self) -> str:
        # Retorna el atributo privado __telefono.
        return self.__telefono

    # Setter con validación estricta para el teléfono del cliente.
    @telefono.setter
    def telefono(self, valor: str) -> None:
        # Limpia espacios y guiones para evaluar los dígitos reales.
        telefono_limpio = valor.replace("-", "").replace(" ", "").strip() if isinstance(valor, str) else ""
        # Verifica que contenga solo dígitos y tenga entre 7 y 15 caracteres.
        if not telefono_limpio.isdigit() or not (7 <= len(telefono_limpio) <= 15):
            # Lanza ErrorValidacionDato si el teléfono no es válido.
            raise ErrorValidacionDato("El teléfono debe contener entre 7 y 15 dígitos numéricos.")
        # Guarda el teléfono limpio en __telefono.
        self.__telefono = telefono_limpio

    # Implementa el método abstracto resumen() exigido por EntidadSistema.
    def resumen(self) -> str:
        # Construye una descripción legible del cliente con sus datos encapsulados.
        estado_texto = "Activo" if self.activo else "Inactivo"
        # Retorna la cadena formateada con los datos del cliente.
        return f"Cliente [{self.id_entidad}]: {self.__nombre} | Correo: {self.__correo} | Tel: {self.__telefono} | {estado_texto}"