/* 
 * File:   main.c
 * Author: Manuel
 *
 * Created on July 10, 2015, 12:54 PM
 */

#include <xc.h>

#include "extended_serial.h"
#include "extended_spi.h"
#include "timers_pic.h"



#pragma config FOSC = HS        // Oscillator Selection bits (HS oscillator)
#pragma config LVP = OFF        // Single-Supply ICSP Enable bit (Single-Supply ICSP disabled)
#pragma config WDTEN = OFF      // Watchdog Timer Enable bit (WDT is controlled by SWDTEN bit of the WDTCON register)


#define _XTAL_FREQ 20000000

bool return_false(void)
{
    return spi_slave_peek_receive(false, NULL);
}

int main() {

    struct circular_buffer pic_to_pic = {0, 0, {0}};
    struct circular_buffer pic_to_pc = {0, 0, {0}};
    
    espi_setup(SLAVE_NO_SS);
    eserial_setup(BRG16_BIT | BRGH_BIT, 0x10);
    setup_timer3(TMR3_16BIT_MODE | TMR3_PRESCALE_1 | TMR3_TIMER_ON);
    
    uint8_t value;
    int i = 0;
    while (1) {
        
        
        eserial_receive(&pic_to_pic, &return_false, &set_timer3, &timer3_up); //If it is has data, don't receive, that may be the problem
        
        int16_t value;
        if (spi_slave_peek_receive(true, &value)) {
            if (value == RX_CHAR) {
                espi_slave_send(&pic_to_pic);
            } else if (value == TX_CHAR) {
                espi_slave_receive(&pic_to_pc);
            } else {             
                if (i > 3) {
                    SSPCON1bits.SSPEN = 0;
                    SSPCON1bits.SSPEN = 1;
                    i = 0;
                }
                i++;
            }
        }
        
        eserial_send_data(&pic_to_pc);
    }
    
    return (0);
}
