#include "stepper_motor.h"

static uint8_t current_state;
static uint8_t output_value[8] = {0x01, 0x03, 0x02, 0x06,
                                  0x04, 0x0C, 0x08, 0x09};

void stepper_motor_setup(void)
{
    STEPPER_OUT_A = 0;
    STEPPER_OUT_B = 0;
    STEPPER_OUT_C = 0;
    STEPPER_OUT_D = 0;
    
    TRIS_STEPPER_OUT_A = 0;
    TRIS_STEPPER_OUT_B = 0;
    TRIS_STEPPER_OUT_C = 0;
    TRIS_STEPPER_OUT_D = 0;
}

void step_forward(void)
{    
    current_state++;
    current_state &= 0x07;
    
    STEPPER_REG = (STEPPER_REG & 0xF0) | output_value[current_state];
}

void step_backward(void)
{
    current_state--;
    current_state &= 0x07;
    
    STEPPER_REG = (STEPPER_REG & 0xF0) | output_value[current_state];
}

void stepper_turn_off(void)
{
    STEPPER_REG = STEPPER_REG & 0xF0;
}
