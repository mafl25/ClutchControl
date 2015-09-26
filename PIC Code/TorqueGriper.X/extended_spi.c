#include "extended_spi.h"
#include "extended_serial.h"


#define TRIS_SLAVE_SEND     TRISAbits.RA2
#define WRITE_SLAVE_SEND    LATAbits.LATA2  //Yellow
#define READ_SLAVE_SEND     PORTAbits.RA2
#define AN_SLAVE_SEND       ANSELbits.ANS2
#define SLAVE_INT_EDGE_SEL  INTCON2bits.INTEDG2
#define SLAVE_INT_ENABLE    INTCON3bits.INT2E
#define SLAVE_INT_FLAG      INT2IF

#define TRIS_MASTER_SEND    TRISCbits.RC6
#define WRITE_MASTER_SEND   LATCbits.LATC6
#define READ_MASTER_SEND    PORTCbits.RC6
#define AN_MASTER_SEND      ANSELHbits.ANS8

#define WAIT_TIME       54335
#define SEND_DELAY      5
#define _XTAL_FREQ      16000000

static void send_delay(void)
{
    __delay_us(SEND_DELAY);
}

void espi_setup(uint8_t mode)
{
    setup_spi(0, SPI_ENABLE | CLK_POLARITY | mode);
    
    AN_SLAVE_SEND = 0;
    AN_MASTER_SEND = 0;
    
    if (mode == SLAVE_SS || mode == SLAVE_NO_SS) {
        TRIS_SLAVE_SEND = 0;
        WRITE_SLAVE_SEND = 0;
        TRIS_MASTER_SEND = 1;
    } else {
        TRIS_SLAVE_SEND = 1;
        TRIS_MASTER_SEND = 0;
        WRITE_MASTER_SEND = 0;
        SLAVE_INT_EDGE_SEL = 1;
        SLAVE_INT_ENABLE = 1; //Turn this into a separate library
                              //that configures it all
    }
        
}

void espi_slave_receive(struct circular_buffer *buffer)
{
    uint8_t value;
    int8_t received_1;
    int8_t received_2;

    WRITE_SLAVE_SEND = 1;
    WRITE_SLAVE_SEND = 0;

    while (buffer_space(buffer)) {
        received_1 = spi_slave_get_byte();
        if (received_1 == END_CHAR || received_1 == TX_CHAR || 
            received_1 == RX_CHAR || received_1 == -1)
            return;

        received_2 = spi_slave_get_byte();
        if (received_2 == END_CHAR  || received_2 == TX_CHAR || 
            received_2 == RX_CHAR || received_2 == -1)
            return;

        decode_data( &value, (uint8_t)received_1, (uint8_t)received_2);
        buffer_push(buffer, value);
    }

    spi_send_get_byte(END_CHAR);
}

void espi_slave_send(struct circular_buffer *buffer)
{
    if (buffer_count(buffer)) {
        uint16_t byte_to_send = buffer_peek(buffer);
        uint8_t byte_1;
        uint8_t byte_2;
        
        encode_data(byte_to_send, &byte_1, &byte_2);

        WRITE_SLAVE_SEND = 1;
        WRITE_SLAVE_SEND = 0;

        int16_t received_1 = spi_send_get_byte(byte_1); //check if End_Char and get out here
        if (received_1 == END_CHAR || received_1 == TX_CHAR || 
            received_1 == RX_CHAR || received_1 == -1)
            return;
        int16_t received_2 = spi_send_get_byte(byte_2);
        if (received_2 == END_CHAR || received_2 == TX_CHAR || 
            received_2 == RX_CHAR || received_2 == -1)
            return;
        
        while (1) { 
            buffer_pop(buffer);  //Get all this in a single loop
            byte_to_send = buffer_peek(buffer);
            if (byte_to_send == -1)         
                break;
            
            encode_data(byte_to_send, &byte_1, &byte_2); //If data is not encoded, send error or something
            
            received_1 = spi_send_get_byte(byte_1);
            if (received_1 == END_CHAR || received_1 == TX_CHAR || 
                received_1 == RX_CHAR || received_1 == -1)
                    return;
            
            received_2 = spi_send_get_byte(byte_2); //This data will be lost if the buffer in the receiver is full.
            if (received_2 == END_CHAR || received_2 == TX_CHAR || 
                received_2 == RX_CHAR || received_2 == -1)  
                    return;
        }   

        spi_send_get_byte(END_CHAR);
    } else {     
        WRITE_SLAVE_SEND = 1;
        WRITE_SLAVE_SEND = 0;
        
        spi_send_get_byte(END_CHAR);
    }
}

static void wait_pulse(uint8_t value, void (*timer_start)(int16_t), 
                       bool (*timer)(void))
{
    (*timer_start)(WAIT_TIME);
    while (!SLAVE_INT_FLAG) {//Change this into interrupt function
        if ((*timer)()) { 
            spi_send_get_byte(value);
            (*timer_start)(WAIT_TIME);
        }
    }
    SLAVE_INT_FLAG = 0;
}

void espi_master_send(struct circular_buffer *buffer,
                        void (*timer_start)(int16_t),
                        bool (*timer)(void))
{
    if (buffer_count(buffer)) {
        spi_send_get_byte(TX_CHAR);
        
        wait_pulse(TX_CHAR, timer_start, timer);
        
        uint16_t byte_to_send;
        uint8_t byte_1;
        uint8_t byte_2;
        uint8_t received_1;
        uint8_t received_2;
        
        while (1) {
            byte_to_send = buffer_peek(buffer);
            if (byte_to_send == -1)
                break;
            encode_data(byte_to_send, &byte_1, &byte_2);
            
            received_1 = spi_send_get_byte(byte_1);
            send_delay();
            if (received_1 == END_CHAR)
                return;
            
            received_2 = spi_send_get_byte(byte_2); //This data will be lost if the buffer in the receiver is full.
            send_delay();
            if (received_2 == END_CHAR)
                return;
            
            buffer_pop(buffer);
        }   
        
        spi_send_get_byte(END_CHAR);  //Remember, if buffer gets filled, te last byte sent gets lost
        send_delay();
    }
}

void espi_master_receive(struct circular_buffer *buffer,
                        void (*timer_start)(int16_t),
                        bool (*timer)(void))
{
    if (!buffer_full(buffer)) {
        spi_send_get_byte(RX_CHAR);
        
        wait_pulse(RX_CHAR, timer_start, timer);

        uint8_t received_1;
        uint8_t received_2;
        uint8_t value;
        
        while (buffer_space(buffer)) {
            received_1 = spi_send_get_byte(0xE0);
            send_delay();
            if (received_1 == END_CHAR)
                return;
            
            received_2 = spi_send_get_byte(0xE0);
            send_delay();
            if (received_2 == END_CHAR)
                return;
            
            decode_data(&value, received_1, received_2);
            buffer_push(buffer, value);
        }

        spi_send_get_byte(END_CHAR);
        send_delay();
    }
}