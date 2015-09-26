/* 
 * File:   stepper_motor.h
 * Author: Manuel
 *
 * Created on August 5, 2015, 3:09 PM
 */
#include <xc.h>
#include <stdint.h>

#ifndef STEPPER_MOTOR_H
#define	STEPPER_MOTOR_H

#define STEPPER_OUT_A       LATCbits.LATC0
#define TRIS_STEPPER_OUT_A  TRISCbits.RC0
#define STEPPER_OUT_B       LATCbits.LATC1
#define TRIS_STEPPER_OUT_B  TRISCbits.RC1
#define STEPPER_OUT_C       LATCbits.LATC2
#define TRIS_STEPPER_OUT_C  TRISCbits.RC2
#define STEPPER_OUT_D       LATCbits.LATC3
#define TRIS_STEPPER_OUT_D  TRISCbits.RC3
#define STEPPER_REG         LATC

void stepper_motor_setup(void);
void stepper_turn_off(void);
void step_forward(void);
void step_backward(void);

// When using the dsPIC, use microstepping Probably make a special board

#endif	/* STEPPER_MOTOR_H */

