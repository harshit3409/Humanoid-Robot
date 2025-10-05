#include "alpha_v1.h"

alpha_v1 alpha;
int servoDeg[20];
int idx = 0;
String inputData = "";
char incomingChar;

void setup() {
Serial.begin(115200);
Serial.println("Alpha v1 Test Start");

alpha.init_alpha();
alpha.initial_position();
delay(4000);

alpha.say_hi(2, 1000);
alpha.hands_up(1, 3000);
alpha.forward(20, 500);
alpha.turn_right(5, 500);
alpha.turn_left(5, 500);
alpha.move_right(5, 800);
alpha.move_left(5, 800);
alpha.ball_kick_right(1, 1000);
alpha.ball_kick_left(1, 1000);
alpha.max_sit(1, 2000);
alpha.bow(1, 2000);
alpha.right_bow(1, 2000);
alpha.left_bow(1, 2000);
alpha.ape_move(3, 2000);
alpha.clap(3, 2000);
alpha.right_leg_up(3, 2000);
alpha.left_leg_up(3, 2000);
alpha.hip_pose(1, 2000);
alpha.right_leg_balance(1, 3000);
alpha.left_leg_balance(1, 3000);
alpha.flying_action(3, 2000);
alpha.hand_sit_zigzak(3, 2000);
alpha.side_shake(3, 1200);
alpha.hip_shake(3, 1200);
alpha.bend_up(1, 2000);
alpha.push_up(3, 3000);
}

void loop() {
// idle – waits for serial input
}

void serialEvent() {
String angleData = Serial.readString();
processInput(angleData);
}

void processInput(String data) {
int angleArr[20];
int start = 0, index = 0;

for (int i = 0; i < data.length(); i++) {
if (data.charAt(i) == ',') {
angleArr[index++] = data.substring(start, i).toInt();
start = i + 1;
}
}

for (int j = 0; j < 20; j++) {
Serial.print(angleArr[j]);
Serial.print("|");
}
Serial.println("");

alpha.move_servo(2000, angleArr);
}
