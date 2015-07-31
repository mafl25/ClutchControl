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


#define _XTAL_FREQ 20000000

bool return_false(void)
{
    return false;
}

int main() {

    struct circular_buffer pic_to_pic = {0, 0, {0}};
    struct circular_buffer pic_to_pc = {0, 0, {0}};
    
    espi_setup(SLAVE_NO_SS);
    eserial_setup(BRG16_BIT | BRGH_BIT, 0x2A);
    setup_timer3(TMR3_16BIT_MODE | TMR3_PRESCALE_1 | TMR3_TIMER_ON);
    
    uint8_t value;
    char wat[] = "UUUUU";
    
    while (1) {
        //eserial_receive(&pic_to_pc, &espi_master_rts, &set_timer3, &timer3_up);
        int i;
        
        if (buffer_empty(&pic_to_pc))
            for (i = 0; wat[i] != 0; i++)
                 buffer_push(&pic_to_pc, wat[i]);
        
        int16_t value;
        if (spi_slave_peek_receive(true, &value)) {
            serial_send_byte(value);
            if (value == RX_CHAR)
                espi_slave_send(&pic_to_pc);
            else if (value == TX_CHAR)
                espi_slave_receive(&pic_to_pic, &set_timer3, &timer3_up);
        }
        eserial_send_data(&pic_to_pic);
        //serial_send_byte(0xAA);
        
//        for (i = 0; i < 100; i++)
//            __delay_ms(10);
    }
    
    return (0);
}
