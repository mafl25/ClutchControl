#include <xc.h>
#include "spi.h"

// CONFIG1H
#pragma config FOSC = IRC       // Oscillator Selection bits (Internal RC oscillator)
#pragma config LVP = OFF        // Single-Supply ICSP Enable bit (Single-Supply ICSP disabled)

#define _XTAL_FREQ 16000000

int main() {
    OSCCONbits.IRCF = 0x07;  //16 MHz internal oscillator
    
    struct spi_receive_buffer my_data = {0, 0};
    
    set_spi(MM_FOSC4, IDLE_LOW, IDLE_ACTIVE, MIDDLE);
    
    char data[] = "Manuel";
    
    while (1) {
        send_data_spi(&data, 6);
    }
    
    return 0;
}

