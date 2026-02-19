import time
import random
from enum import Enum
from dataclasses import dataclass
from typing import Optional, List

class EstadoRobot(Enum):
    """Definición de los estados del robot según el diagrama"""
    PARADO = "PARADO"
    NADANDO = "NADANDO"
    TOMANDO_DATOS = "TOMANDO_DATOS"
    EXPRESANDO_RESULTADOS = "EXPRESANDO_RESULTADOS"
    RECIBIENDO_MENSAJE = "RECIBIENDO_MENSAJE"
    EXPIRACION = "EXPIRACION"

class Evento(Enum):
    """Eventos que pueden ocurrir en el sistema"""
    INICIAR = "INICIAR"
    DETENER = "DETENER"
    DATOS_LISTOS = "DATOS_LISTOS"
    MENSAJE_RECIBIDO = "MENSAJE_RECIBIDO"
    RESULTADOS_EXPRESADOS = "RESULTADOS_EXPRESADOS"
    TIMEOUT = "TIMEOUT"
    REQUERIR_DATOS = "REQUERIR_DATOS"
    FALLO = "FALLO"

@dataclass
class DatosRobot:
    """Estructura de datos del robot"""
    temperatura: float = 0.0
    presion: float = 0.0
    profundidad: float = 0.0
    salinidad: float = 0.0
    mensaje_recibido: Optional[str] = None
    resultados: List[str] = None
    
    def __post_init__(self):
        if self.resultados is None:
            self.resultados = []

class RobotExplorador:
    """Clase principal del autómata Robot Explorador"""
    
    def __init__(self, nombre: str = "Explorer-01"):
        self.nombre = nombre
        self.estado_actual = EstadoRobot.PARADO
        self.datos = DatosRobot()
        self.contador_fallos = 0
        self.tiempo_inicio_estado = time.time()
        self.tiempo_limite_estado = 30  # segundos
        
    def transicion_estado(self, nuevo_estado: EstadoRobot, evento: Evento):
        """Realiza la transición entre estados"""
        print(f"\n[{self.nombre}] {self.estado_actual.value} → {nuevo_estado.value} (Evento: {evento.value})")
        self.estado_actual = nuevo_estado
        self.tiempo_inicio_estado = time.time()
        
    def verificar_timeout(self) -> bool:
        """Verifica si el estado actual ha excedido el tiempo límite"""
        return (time.time() - self.tiempo_inicio_estado) > self.tiempo_limite_estado
    
    def ejecutar_estado_parado(self):
        """Comportamiento en estado PARADO"""
        print(f"[{self.nombre}] Robot detenido, esperando instrucciones...")
        time.sleep(2)
        
        if random.random() < 0.8:  # 80% probabilidad de iniciar
            self.transicion_estado(EstadoRobot.NADANDO, Evento.INICIAR)
        else:
            self.contador_fallos += 1
            print(f"[{self.nombre}] Fallo en arranque #{self.contador_fallos}")
            
    def ejecutar_estado_nadando(self):
        """Comportamiento en estado NADANDO"""
        print(f"[{self.nombre}] Navegando hacia punto de muestreo...")
        time.sleep(3)
        
        if random.random() < 0.7:  # 70% probabilidad de encontrar objetivo
            print(f"[{self.nombre}] Objetivo alcanzado - Iniciando muestreo")
            self.transicion_estado(EstadoRobot.TOMANDO_DATOS, Evento.REQUERIR_DATOS)
        else:
            print(f"[{self.nombre}] Continuando navegación...")
            
    def ejecutar_estado_tomando_datos(self):
        """Comportamiento en estado TOMANDO_DATOS"""
        print(f"[{self.nombre}] Tomando muestras del entorno...")
        
        # Simular lectura de sensores
        self.datos.temperatura = random.uniform(15, 30)
        self.datos.presion = random.uniform(950, 1050)
        self.datos.profundidad = random.uniform(0, 100)
        self.datos.salinidad = random.uniform(30, 40)
        
        print(f"Temperatura: {self.datos.temperatura:.1f}°C")
        print(f"Presión: {self.datos.presion:.1f} hPa")
        print(f"Profundidad: {self.datos.profundidad:.1f} m")
        print(f"Salinidad: {self.datos.salinidad:.1f} ppt")
        
        time.sleep(2)
        
        # Decidir siguiente estado
        if random.random() < 0.6:  # 60% probabilidad de expresar resultados
            self.transicion_estado(EstadoRobot.EXPRESANDO_RESULTADOS, Evento.DATOS_LISTOS)
        else:
            self.transicion_estado(EstadoRobot.RECIBIENDO_MENSAJE, Evento.MENSAJE_RECIBIDO)
            
    def ejecutar_estado_expresando_resultados(self):
        """Comportamiento en estado EXPRESANDO_RESULTADOS"""
        print(f"[{self.nombre}] Procesando y expresando resultados...")
        
        resultado = (f"Muestra {len(self.datos.resultados)+1}: "
                    f"T={self.datos.temperatura:.1f}°C, "
                    f"P={self.datos.presion:.1f}hPa, "
                    f"D={self.datos.profundidad:.1f}m, "
                    f"S={self.datos.salinidad:.1f}ppt")
        
        self.datos.resultados.append(resultado)
        print(f"{resultado}")
        
        time.sleep(2)
        self.transicion_estado(EstadoRobot.PARADO, Evento.RESULTADOS_EXPRESADOS)
        
    def ejecutar_estado_recibiendo_mensaje(self):
        """Comportamiento en estado RECIBIENDO_MENSAJE"""
        print(f"[{self.nombre}] Esperando mensaje de control...")
        time.sleep(2)
        
        mensajes = ["Continuar muestreo", "Regresar base", "Esperar instrucciones"]
        self.datos.mensaje_recibido = random.choice(mensajes)
        print(f"Mensaje recibido: {self.datos.mensaje_recibido}")
        
        if "Continuar" in self.datos.mensaje_recibido:
            self.transicion_estado(EstadoRobot.TOMANDO_DATOS, Evento.MENSAJE_RECIBIDO)
        else:
            self.transicion_estado(EstadoRobot.PARADO, Evento.MENSAJE_RECIBIDO)
            
    def ejecutar_estado_expiracion(self):
        """Comportamiento en estado EXPIRACION (manejo de fallos)"""
        print(f"[{self.nombre}] MODO SEGURIDAD - Tiempo expirado")
        print(f"Fallos detectados: {self.contador_fallos}")
        
        if self.contador_fallos < 3:
            print("    🔄 Intentando recuperación...")
            time.sleep(2)
            self.transicion_estado(EstadoRobot.PARADO, Evento.TIMEOUT)
        else:
            print("ERROR CRÍTICO - Demasiados fallos")
            print("Activando protocolo de emergencia")
            
    def ejecutar_ciclo(self):
        """Ejecuta un ciclo del autómata según el estado actual"""
        
        if self.verificar_timeout() and self.estado_actual != EstadoRobot.PARADO:
            print(f"\nTimeout en estado {self.estado_actual.value}")
            self.transicion_estado(EstadoRobot.EXPIRACION, Evento.TIMEOUT)
            return
        
        # Mapa de métodos por estado
        metodos = {
            EstadoRobot.PARADO: self.ejecutar_estado_parado,
            EstadoRobot.NADANDO: self.ejecutar_estado_nadando,
            EstadoRobot.TOMANDO_DATOS: self.ejecutar_estado_tomando_datos,
            EstadoRobot.EXPRESANDO_RESULTADOS: self.ejecutar_estado_expresando_resultados,
            EstadoRobot.RECIBIENDO_MENSAJE: self.ejecutar_estado_recibiendo_mensaje,
            EstadoRobot.EXPIRACION: self.ejecutar_estado_expiracion
        }
        
        metodos[self.estado_actual]()
            
    def mostrar_resumen(self):
        """Muestra resumen de la misión"""
        print("\n" + "="*60)
        print(f"RESUMEN DE MISIÓN - {self.nombre}")
        print("="*60)
        print(f"Estado final: {self.estado_actual.value}")
        print(f"Total de fallos: {self.contador_fallos}")
        print(f"Muestras recolectadas: {len(self.datos.resultados)}")
        print("\nResultados obtenidos:")
        for i, res in enumerate(self.datos.resultados, 1):
            print(f"  {i}. {res}")
        print("="*60)

def main():
    """Función principal de ejecución"""
    
    print("="*60)
    print("SISTEMA ROBOT EXPLORADOR SUBMARINO")
    print("="*60)
    
    robot = RobotExplorador("Deep-Sea-Explorer-01")
    
    try:
        ciclos_ejecutados = 0
        max_ciclos = 12
        
        while ciclos_ejecutados < max_ciclos:
            print(f"\n--- Ciclo {ciclos_ejecutados + 1} ---")
            robot.ejecutar_ciclo()
            
            ciclos_ejecutados += 1
            time.sleep(1)
            
            if ciclos_ejecutados >= max_ciclos or robot.contador_fallos >= 5:
                break
                
    except KeyboardInterrupt:
        print("\n\nSistema detenido por usuario")
    
    finally:
        robot.mostrar_resumen()

if __name__ == "__main__":
    main()