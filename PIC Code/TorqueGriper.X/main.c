/* 
 * File:   main.c
 * Author: Manuel
 *
 * Created on July 10, 2015, 12:54 PM
 */

#include <xc.h>

#include "extended_serial.h"


#pragma config FOSC = HS        // Oscillator Selection bits (HS oscillator)
#pragma config LVP = OFF        // Single-Supply ICSP Enable bit (Single-Supply ICSP disabled)


#define _XTAL_FREQ 20000000

volatile struct circular_buffer my_buffer = {0, 0, {0}};

int main() {

    eserial_setup(BRG16_BIT | BRGH_BIT, 0x13);
    
    while (1) {
        eserial_send_data(&my_buffer);
    }
     
    return (0);
}