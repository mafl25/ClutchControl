#include "extended_spi.h"
#include "extended_serial.h"


#define TRIS_SLAVE_SEND     TRISAbits.RA2
#define WRITE_SLAVE_SEND    LATAbits.LATA2
#define READ_SLAVE_SEND     PORTAbits.RA2
#define AN_SLAVE_SEND       ANSELbits.ANS2

#define TRIS_MASTER_SEND    TRISCbits.RC6
#define WRITE_MASTER_SEND   LATCbits.LATC6
#define READ_MASTER_SEND    PORTCbits.RC6
#define AN_MASTER_SEND      ANSELHbits.ANS8

#define WAIT_TIME       63535
#define SEND_DELAY      100
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
        INTCON2bits.INTEDG2 = 1;
        INTCON3bits.INT2E = 1; //Turn this into a separate library
                              //that configures it all
    }
        
}

bool espi_master_rts(void)
{
    return READ_MASTER_SEND;
}

void espi_slave_receive(struct circular_buffer *buffer)
{
    uint8_t value;
    int8_t received_1;
    int8_t received_2;

    WRITE_SLAVE_SEND = 1;
    WRITE_SLAVE_SEND = 0;

    while (buffer_space(buffer) > 5) {
        received_1 = spi_slave_get_byte();
        if (received_1 == END_CHAR)
            break;

        received_2 = spi_slave_get_byte();
        if (received_2 == END_CHAR)
            break;

        decode_data( &value, (uint8_t)received_1, (uint8_t)received_2);
        buffer_push(buffer, value);
    }

    if (received_1 != END_CHAR && received_2 != END_CHAR)
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
        int16_t received_2 = spi_send_get_byte(byte_2);
        
        while (received_1 != END_CHAR && received_2 != END_CHAR) { //This is wrong
            buffer_pop(buffer);
            serial_send_byte('T');
            byte_to_send = buffer_peek(buffer);
            if (byte_to_send == -1)         
                break;
            
            encode_data(byte_to_send, &byte_1, &byte_2); //If data is not encoded, send error or something
            
            received_1 = spi_send_get_byte(byte_1);
            if (received_1 == END_CHAR)
                    break;
            received_2 = spi_send_get_byte(byte_2); //This data will be lost if the buffer in the receiver is full.
            if (received_2 == END_CHAR)
                    break;
        }   

        if (received_1 != END_CHAR && received_2 != END_CHAR)
            spi_send_get_byte(END_CHAR);
    }
}

static void wait_pulse(uint8_t value, void (*timer_start)(int16_t), 
                       bool (*timer)(void))
{
    (*timer_start)(WAIT_TIME);
    while (!INT2IF) {//Change this into interrupt function
//        if ((*timer)()) { 
//            spi_send_get_byte(value);
//            (*timer_start)(WAIT_TIME);
//        }
    }
    INT2IF = 0;
}

int espi_master_send(struct circular_buffer *buffer,
                        void (*timer_start)(int16_t),
                        bool (*timer)(void))
{
    if (buffer_count(buffer)) {
        spi_send_get_byte(TX_CHAR);
        
        wait_pulse(TX_CHAR, timer_start, timer);
        
        uint16_t byte_to_send = buffer_peek(buffer);
        uint8_t byte_1;
        uint8_t byte_2;
        encode_data(byte_to_send, &byte_1, &byte_2);
        
        uint8_t received_1 = spi_send_get_byte(byte_1);
        send_delay();
        uint8_t received_2 = spi_send_get_byte(byte_2);
        send_delay();
        
        while (received_1 != END_CHAR && received_2 != END_CHAR) {
            buffer_pop(buffer);  // Maybe make a function that just deletes the next one?
            byte_to_send = buffer_peek(buffer);
            if (byte_to_send == -1)
                break;
            
            encode_data(byte_to_send, &byte_1, &byte_2);
            
            received_1 = spi_send_get_byte(byte_1);
            send_delay();
            if (received_1 == END_CHAR)
                break;
            received_2 = spi_send_get_byte(byte_2); //This data will be lost if the buffer in the receiver is full.
            send_delay();
            if (received_2 == END_CHAR)
                break;
        }   
        
        if (received_1 != END_CHAR && received_2 != END_CHAR) {
            spi_send_get_byte(END_CHAR);  //Remember, if buffer gets filled, te last byte sent gets lost
            send_delay();
        }
    }
    
    return 0;
}

int espi_master_receive(struct circular_buffer *buffer,
                        void (*timer_start)(int16_t),
                        bool (*timer)(void))
{
    if (buffer_empty(buffer)) {
        spi_send_get_byte(RX_CHAR);
        
        wait_pulse(RX_CHAR, timer_start, timer);

        uint8_t received_1;
        uint8_t received_2;
        uint8_t value;
        while (buffer_space(buffer) > 30) {
            received_1 = spi_send_get_byte(0xE0);
            if (received_1 == END_CHAR)
                break;
            send_delay();
            received_2 = spi_send_get_byte(0xE0);
            if (received_2 == END_CHAR)
                break;
            send_delay();

            decode_data(&value, received_1, received_2);
            buffer_push(buffer, value);
        }

        if (received_1 != END_CHAR && received_2 != END_CHAR) {
            spi_send_get_byte(END_CHAR);  //Remember, if buffer gets filled, te last byte sent gets lost
            send_delay();
        }
    }
    
    return 0;
}


/*
void espi_slave_send_receive(struct circular_buffer *receive, 
                       struct circular_buffer *send)
{
    if (spi_peek_receive(false, NULL) || buffer_count(send)) {
        int16_t to_send = buffer_pop(send);
        uint8_t byte_1;
        uint8_t byte_2;
        uint8_t received_byte;
        uint8_t received_bytes[2];
        uint8_t count = 0;
        bool two_received = false;
        bool send_byte_1 = false;
        bool trans_ended = false;

        if (to_send == -1) {
            byte_1 = END_BYTE;
            byte_2 = END_BYTE;
            spi_load_buffer(byte_1);
            trans_ended = true;
        } else {
            encode_data((uint8_t)to_send, &byte_1, &byte_2);
            spi_load_buffer(byte_1);
        }

        WRITE_SLAVE_SEND = 1;
        WRITE_SLAVE_SEND = 0;


        received_byte = spi_slave_get_byte();

        while (received_byte != END_BYTE || byte_1 != END_BYTE) {
            if (received_byte != END_BYTE) {
                received_bytes[count] = received_byte;
                count++;
                if (count == 2) {
                    count = 0;
                    decode_data(&received_byte, received_bytes[0], 
                                received_bytes[1]);
                    if (!buffer_push(receive, received_byte))  // Need to decode
                        break;
                }
            }

            if (byte_1 != END_BYTE) {
                if (send_byte_1 == false) {
                    spi_load_buffer(byte_2);
                    if (buffer_count(send)) {
                        to_send = buffer_pop(send);
                        encode_data((uint8_t)to_send, &byte_1, &byte_2);
                        send_byte_1 = true;
                    } else {
                        byte_1 = END_BYTE;
                        byte_2 = END_BYTE;
                    }
                } else {
                    spi_load_buffer(byte_1);
                    send_byte_1 = false;
                }
            } else {
                spi_load_buffer(byte_1);
                trans_ended = true;
            }

            WRITE_SLAVE_SEND = 1;
            WRITE_SLAVE_SEND = 0;

            received_byte = spi_slave_get_byte();
        }
        
        if (!trans_ended) {
            spi_load_buffer(byte_1);
            WRITE_SLAVE_SEND = 1;
            WRITE_SLAVE_SEND = 0;
        }
    }
}

void espi_master_send_receive(struct circular_buffer *receive,  //Maybe join these two later
                              struct circular_buffer *send)
{
    if (buffer_count(send) || INT2IF){ //Use library!!!
        INT2IF = 0;
        int16_t to_send = buffer_pop(send);
        uint8_t byte_1;
        uint8_t byte_2;
        uint8_t received_byte;
        uint8_t received_bytes[2];
        uint8_t count = 0;
        bool two_received = false;
        bool send_byte_1 = false;
        bool trans_ended = false;

        if (to_send == -1) {
               byte_1 = END_BYTE;
               byte_2 = END_BYTE;
               received_byte = spi_send_get_byte(byte_1);
               trans_ended = true;
           } else {
               encode_data((uint8_t)to_send, &byte_1, &byte_2);
               received_byte = spi_send_get_byte(byte_1);
           }
        
        while (!INT2IF);
        INT2IF = 0;
        
        while (received_byte != END_BYTE || byte_1 != END_BYTE) {
            if (received_byte != END_BYTE) {
                received_bytes[count] = received_byte;
                count++;
                if (count == 2) {
                    count = 0;
                    decode_data(&received_byte, received_bytes[0], 
                                received_bytes[1]);
                    if (!buffer_push(receive, received_byte))
                        break; //Will have to change this
                }
                
            }
            
            if (byte_1 != END_BYTE) {
                if (send_byte_1 == false) {
                    received_byte = spi_send_get_byte(byte_2);
                    if (buffer_count(send)) {
                        to_send = buffer_pop(send);
                        encode_data((uint8_t)to_send, &byte_1, &byte_2);
                        send_byte_1 = true;
                    } else {
                        byte_1 = END_BYTE;
                        byte_2 = END_BYTE;
                    }
                } else {
                    received_byte = spi_send_get_byte(byte_1);
                    send_byte_1 = false;
                }
            } else {
                received_byte = spi_send_get_byte(byte_1);
                trans_ended = true;
            }
            
            while (!INT2IF);
            INT2IF = 0;
        }
        
        if (!trans_ended)
            received_byte = spi_send_get_byte(byte_1);
    }
}*/