class Persona:
    def __init__(self, dni: str, nombre: str, apellido: str, edad: int):
        # Validaciones simples directamente en el constructor
        if not nombre or not apellido:
            raise ValueError("El nombre y el apellido no pueden estar vacíos.")
        if edad < 0:
            raise ValueError("La edad no puede ser negativa.")
        
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad

class RegistroPersonas:
    def __init__(self, datos: list):
        self.personas = {} # Diccionario para guardar y buscar rápido por DNI
        self.cargar_datos(datos)

    def cargar_datos(self, datos: list):
        for persona_data in datos:
            # Desempaquetado clásico
            dni = persona_data[0]
            nombre = persona_data[1]
            apellido = persona_data[2]
            edad = persona_data[3]
            
            if dni in self.personas:
                # Un junior suele imprimir un aviso en lugar de romper todo el programa
                print(f"Aviso: El DNI {dni} ya está registrado. Se omitirá.")
                continue 
            
            nueva_persona = Persona(dni, nombre, apellido, edad)
            self.personas[dni] = nueva_persona

    def formatear_registros(self) -> dict:
        resultado = {}
        for dni, p in self.personas.items():
            resultado[dni] = (p.nombre, p.apellido, p.edad)
        return resultado

    def obtener_mayor_edad(self):
        if not self.personas:
            return None
        
        mayor = None
        for p in self.personas.values():
            if mayor is None or p.edad > mayor.edad:
                mayor = p
        return mayor

    def obtener_menor_edad(self):
        if not self.personas:
            return None
        
        menor = None
        for p in self.personas.values():
            if menor is None or p.edad < menor.edad:
                menor = p
        return menor

    def segmentar_por_edad(self, umbral: int = 25):
        menores = []
        mayores = []
        
        for p in self.personas.values():
            if p.edad < umbral:
                menores.append(p)
            else:
                mayores.append(p)
                
        return menores, mayores

    def promedio_edad(self) -> float:
        if len(self.personas) == 0:
            return 0.0
        
        suma = 0
        for p in self.personas.values():
            suma += p.edad
            
        return suma / len(self.personas)

    def consultar_edad_por_dni(self, dni: str):
        if dni in self.personas:
            return self.personas[dni].edad
        return None


if __name__ == "__main__":
    # Datos de prueba
    datos_crudos = [
        ('11111111', 'Pedro', 'Paez', 24),
        ('22222222', 'Maria', 'Gomez', 30),
        ('33333333', 'Juan', 'Perez', 19),
        ('44444444', 'Ana', 'Lopez', 25)
    ]

    # Probando la clase
    registro = RegistroPersonas(datos_crudos)

    print("Diccionario formateado:", registro.formatear_registros())
    
    mayor = registro.obtener_mayor_edad()
    print("Persona mayor:", mayor.nombre)
    
    menor = registro.obtener_menor_edad()
    print("Persona menor:", menor.nombre)

    menores, mayores = registro.segmentar_por_edad(25)
    print("Cantidad de menores de 25:", len(menores))
    print("Cantidad de mayores o iguales a 25:", len(mayores))

    print("Promedio de edad:", registro.promedio_edad())
    print("Edad del DNI 22222222:", registro.consultar_edad_por_dni('22222222'))
