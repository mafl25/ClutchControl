#include <xc.h>
#include "extended_spi.h"
#include "timers_pic.h"

// CONFIG1H
#pragma config FOSC = IRC       // Oscillator Selection bits (Internal RC oscillator)
#pragma config LVP = OFF        // Single-Supply ICSP Enable bit (Single-Supply ICSP disabled)

#define _XTAL_FREQ 16000000

int main() {
    OSCCONbits.IRCF = 0x07;  //16 MHz internal oscillator
    
    espi_setup(MASTER_F4);
    setup_timer3(TMR3_16BIT_MODE | TMR3_PRESCALE_1 | TMR3_TIMER_ON);
    
    struct circular_buffer buffer = {0, 0, {0}};
    

    while (1) {

        espi_master_receive(&buffer, &set_timer3, &timer3_up);
        espi_master_send(&buffer, &set_timer3, &timer3_up);

    }
    
    return 0;
}

