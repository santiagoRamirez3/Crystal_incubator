#include <TimerOne.h>              // Incluir Librería TimerOne
#include <OneWire.h>                
#include <DallasTemperature.h>
#include <PID_v1.h>                 // Incluir Librería PID

volatile int i = 0;                  // Variable usada por el contador.
volatile boolean cruce_cero = 0;     // variable que actúa como switch al detectar cruce por cero.
int Triac = 3;                       // Salida conectada al optoacoplador MOC 3021.
int dim;                             // Controla la intensidad de iluminación, 0 = ON ; 83 = OFF                
int T_int = 100;                     // Tiempo en el cual se producen las interrupciones en us. 
float average;

// Variables del termometro
OneWire ourWire(5);                //Se establece el pin 5 como bus OneWire
DallasTemperature sensors(&ourWire); //Se declara una variable u objeto para nuestro sensor
float temp;

// Variables PID
double Setpoint, Input, Output;
double Kp = 100, Ki = 100, Kd = 0.1;
PID myPID(&Input, &Output, &Setpoint, Kp, Ki, Kd, DIRECT);

void setup() { 
  delay(1000);
  Serial.begin(9600);
  sensors.begin();                                     //Se inicia el sensor  
  pinMode(Triac, OUTPUT);                              // Configurar como salida.
  attachInterrupt(0, deteccion_Cruce_cero, RISING);    // Realiza una interrupción al detectar el cruce por cero en el pin 2
  Timer1.initialize(T_int);                            //Inicializa la librería con el tiempo deseado.
  Timer1.attachInterrupt(Dimer, T_int);                // En cada interrupción ejecuta el código Dimer. 

  // Inicializar PID
  Setpoint = 55; // Temperatura objetivo inicial
  myPID.SetMode(AUTOMATIC);
  myPID.SetOutputLimits(0, 67); // Ajusta los límites de salida del PID para el control del dimmer
}

void deteccion_Cruce_cero() { 
  cruce_cero = true; // Si existe un cruce por cero entonces la variable "cruce_cero" cambia a TRUE...
  i = 0; 
  digitalWrite(Triac, LOW);
}   

void Dimer() {                   
  if (cruce_cero == true) {
    if (i >= dim) {
      digitalWrite(Triac, HIGH);
      i = 0;
      cruce_cero = false;
    } else {
      i++;
    }
  }
}

void loop () {
  average = 0;
  for (int i = 0; i < 10; i++) {
    sensors.requestTemperatures();   //Se envía el comando para leer la temperatura
    average += sensors.getTempCByIndex(0)/10; //Se obtiene la temperatura en ºC
    delay(1000); // Esperar un poco entre lecturas
  }
  Input = average;
  myPID.Compute(); // Calcular PID
  dim = map(Output,0,67,84,17); // Asignar la salida del PID al dimmer
  //dim = 42;
  
  // Leer el setpoint desde el puerto serie
  if (Serial.available() > 0) {
    Setpoint = Serial.parseFloat();
  }

  // Enviar la temperatura actual al PC
  Serial.println(Input);
  Serial.println(dim);

  delay(1000);
}
