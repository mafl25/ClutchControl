#include "extended_serial.h"

#define RTS         LATCbits.LATC0
#define TRIS_RTS    TRISCbits.RC0
#define RTS_AN      ANSELbits.ANS4
#define CTS         PORTCbits.RC1
#define TRIS_CTS    TRISCbits.RC1
#define CTS_AN      ANSELbits.ANS5

#define INACTIVE 1
#define ACTIVE 0

#define BYTES_SENT_AFTER_FTDI    0x04


#define ESER_BUFFER_SIZE    0x10
#define MAX_BUFFER_EMPTY    0x05

#define FTDI_WAIT_TIME  40535

void eserial_setup(uint8_t baudrate_bits, uint16_t baudrate_value)
{
    CTS_AN = 0; //Set CTS to digital.
    RX_AN = 0; //Set RX to digital.
    
    TRIS_RTS = 0; //RTS output
    TRIS_CTS = 1; //CTS input
    
    setup_simple_serial(baudrate_bits, baudrate_value);
    
    RTS = INACTIVE;
}


int8_t eserial_send_data(struct circular_buffer *buffer)
{
    /*It checks if the FTDI is available to receive data.
     * TODO: change this.
    */
    int8_t i = 0;
    int16_t value = buffer_pop(buffer); //Might need to unable interrupts for a moment
    while (value != -1) {
        serial_send_byte((uint8_t)value);  
        value = buffer_pop(buffer);
        i++;
    }
    
    return i;
}

void eserial_receive(struct circular_buffer *buffer, 
                     bool (*stop_function)(void), 
                     void (*timer_start)(int16_t),
                     bool (*timer_up)(void))
{  
        uint8_t value;
        RTS = ACTIVE;
        
        if (stop_function == NULL) {
            while (buffer_space(buffer) > MAX_BUFFER_EMPTY) {      
                if (serial_peek_receive(true, &value)) {
                    buffer_push(buffer, value);
                }         
            }
        } else {
            bool test = false;
            while ((buffer_space(buffer) > MAX_BUFFER_EMPTY) &&
                   !test) {  
                if (serial_peek_receive(true, &value)) {
                    buffer_push(buffer, value);
                }      
                test = (*stop_function)();
            }
        }
        
        RTS = INACTIVE;
        (*timer_start)(FTDI_WAIT_TIME);
        
        while (!(*timer_up)()) {
            if (serial_peek_receive(true, &value)) {
                buffer_push(buffer, value);
            }  
        }   
}