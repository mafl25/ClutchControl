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


void eserial_setup(uint8_t baudrate_bits, uint16_t baudrate_value)
{
    CTS_AN = 0; //Set CTS to digital.
    RX_AN = 0; //Set RX to digital.
    
    TRIS_RTS = 0; //RTS output
    TRIS_CTS = 1; //CTS input
    
    setup_simple_serial(baudrate_bits, baudrate_value);
    
    RTS = ACTIVE;
}


//Use a transmit buffer and a receive buffer.
//Receive will use interrupts, but also RTS/CTS, to capture the rogue
//byte sent by the ftdi chip afterwards
int8_t eserial_send_data(struct circular_buffer volatile *buffer)
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
    
    if (buffer_empty(buffer))
            RTS = ACTIVE;
    
    return i;
}

void eserial_receive(struct circular_buffer volatile *buffer)
{  
        //Push into the receive buffer. Check if it is not full first.
        //Tell the other pic that there is data available. Maybe only if 
        //There is more than a certain amount.
        /*
         *The serial receive-> interrupts and cts/rts
         *Serial send->  cts/rts if ftdi cant receive, it lets data accumulate 
         * But it is unlikely. 
         * Pic 2, SPI, if sending when this pic wants to communicate, it will 
         * stop sending. it will tell how much space it has first. To maybe let 
         * it continue sending. The receiving will assert its line, probably 
         * receive the random bytes. It will tell Pic2 that it has data only 
         * after x amount of bytes received.
         * 
         * Tomorrow, create th receive and send functions, stress test them.
         */
        
        if (buffer_space(buffer) <= MAX_BUFFER_EMPTY)
            RTS = INACTIVE;
        else
            RTS = ACTIVE;
        
        uint8_t value = serial_get_byte();
        buffer_push(buffer, value);
}