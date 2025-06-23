// Encoder channels A (interrupt-driven)
#define ENC_A_MOTOR_A 2  // Motor A encoder A (green)
#define ENC_A_MOTOR_B 3  // Motor B encoder A (green)

// Encoder channels B (for optional direction detection)
#define ENC_B_MOTOR_A 4  // Motor A encoder B (yellow)
#define ENC_B_MOTOR_B 5  // Motor B encoder B (yellow)

// Pulse counters
volatile long pulseCountA = 0;
volatile long pulseCountB = 0;

// Motor control pins (L298N)
#define IN1 8   // Motor A
#define IN2 9
#define IN3 10  // Motor B
#define IN4 11

void setup() {
  Serial.begin(9600);

  // Encoder pins
  pinMode(ENC_A_MOTOR_A, INPUT_PULLUP);
  pinMode(ENC_A_MOTOR_B, INPUT_PULLUP);
  pinMode(ENC_B_MOTOR_A, INPUT_PULLUP);
  pinMode(ENC_B_MOTOR_B, INPUT_PULLUP);

  // Motor pins
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  // Attach encoder interrupts
  attachInterrupt(digitalPinToInterrupt(ENC_A_MOTOR_A), pulseA_ISR, RISING);
  attachInterrupt(digitalPinToInterrupt(ENC_A_MOTOR_B), pulseB_ISR, RISING);
}

void loop() {
  // --- Run motors forward ---
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW); // Motor A forward
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW); // Motor B forward
  delay(3000);

  // --- Stop ---
  digitalWrite(IN1, LOW); digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW); digitalWrite(IN4, LOW);
  delay(1000);

  // --- Run motors backward ---
  digitalWrite(IN1, LOW); digitalWrite(IN2, HIGH); // Motor A backward
  digitalWrite(IN3, LOW); digitalWrite(IN4, HIGH); // Motor B backward
  delay(3000);

  // --- Stop again ---
  digitalWrite(IN1, LOW); digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW); digitalWrite(IN4, LOW);
  delay(1000);

  // --- Print encoder counts ---
  Serial.print("Motor A Pulses: ");
  Serial.print(pulseCountA);
  Serial.print(" | Motor B Pulses: ");
  Serial.println(pulseCountB);
}

// ISR: Count pulses
void pulseA_ISR() { pulseCountA++; }
void pulseB_ISR() { pulseCountB++; }
