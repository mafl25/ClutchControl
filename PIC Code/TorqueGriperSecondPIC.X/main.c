#include <xc.h>
#include "extended_spi.h"
#include "timers_pic.h"
#include "pwm.h"

// CONFIG1H
#pragma config FOSC = IRC       // Oscillator Selection bits (Internal RC oscillator)
#pragma config LVP = OFF        // Single-Supply ICSP Enable bit (Single-Supply ICSP disabled)

#define _XTAL_FREQ 16000000

bool load_buffer(struct circular_buffer *buffer, char *str, int size);

int main() {
    OSCCONbits.IRCF = 0x07;  //16 MHz internal oscillator
    
    espi_setup(MASTER_F4);
    setup_timer3(TMR3_16BIT_MODE | TMR3_PRESCALE_1 | TMR3_TIMER_ON);
    setup_timer0(TMR0_PRESCALE_256 | TMR0_TIMER_ON);
    pmwSingleModeSetUp(PACH_PBDH, 254, TMRP_1, OUT_A | OUT_B);
    
    struct circular_buffer send = {0, 0, {0}};
    struct circular_buffer receive = {0, 0, {0}};
    
    char name[3] = {0x55, 0xDD, 0x00};

    set_timer0(55000);
    while (1) {

        espi_master_receive(&receive, &set_timer3, &timer3_up); //TODO: Esta parte me causa problemas si no me esta mandan datos el otro pic
        int16_t value;
        
        while (buffer_count(&receive) >= 3) {
            uint8_t byte_1;
            uint8_t byte_2;
            value = buffer_pop(&receive);
            
            switch (value) {
                case 0xAC:
                    byte_1 = buffer_pop(&receive);
                    byte_2 = buffer_pop(&receive);
                    setPulseWidth(byte_1 << 2 | byte_2);
                    break;
                case 0xAA:
                    byte_1 = buffer_pop(&receive);
                    byte_2 = buffer_pop(&receive);
                    selectOutput(byte_1, byte_2);
                    break;
            }
        }
        
        //espi_master_send(&buffer, &set_timer3, &timer3_up);
            
        if (timer0_up()) {
            load_buffer(&send, name, 3);
            espi_master_send(&send, &set_timer3, &timer3_up);
            set_timer0(55000);
        }
    }
    
    return 0;
}

bool load_buffer(struct circular_buffer *buffer, char *str, int size)
{
    int i;
    if (size < 0) {
        for (i = 0; str[i] != 0; i++) {
            if (buffer_push(buffer, str[i]))
                return false;
        }
    } else {
        for (i = 0; i < size; i++) {
            if (buffer_push(buffer, str[i]))
                return false;
        }
    }
    
    return true;
}

