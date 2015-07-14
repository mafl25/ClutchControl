#include "serialprotocol.h"

static unsigned int timer3Time;

static void setTimer3(unsigned char turnOn, unsigned int TMR3Pair) {
    T3CONbits.RD16 = 0x01; //Write in one 16  bit operation
    T3CONbits.T3CKPS = 0x00; //1:1 prescale
    T3CONbits.TMR3CS = 0x00; //
    T3CONbits.TMR3ON = (turnOn) ? 1 : 0;
    timer3Time = TMR3Pair;
}

static void toggleTimer3(unsigned char toggle) {
    PIR2bits.TMR3IF = 0;
    if (toggle) {
        TMR3H = timer3Time >> 8;
        TMR3L = timer3Time;
        T3CONbits.TMR3ON = 0x01;
    } else {
        T3CONbits.TMR3ON = 0x00;
    }       
}

void serialSetUp(unsigned char brg16_bit, unsigned char brgh_bit, 
        unsigned int spbrg16) //Use Excel file to get the right values
{
    ANSELHbits.ANS9 = 0; //Set CTS to digital.
    ANSELHbits.ANS11 = 0; //Set RX to digital.
    
    TRIS_RX = 1; //RX input
    TRIS_TX = 0; //TX output
    TRIS_RTS = 0; //RTS output
    TRIS_CTS = 1; //CTS input
    
    BAUDCON = (brg16_bit) ? 0x08 : 0x00;
    TXSTA = (brgh_bit) ? 0x24: 0x20;
    SPBRGH = spbrg16 >> 8;
    SPBRG = spbrg16;
    RCSTA = 0x90;
    
    setTimer3(0x00, 65360);
    
    RTS = INACTIVE;
}

void toggleSerialPort(unsigned char toggle)
{
    RCSTAbits.SPEN = toggle != 0 ? 1 : 0;
}

void toggleTransmitter(unsigned char toggle)
{
    TXSTAbits.TXEN = toggle != 0 ? 1 : 0;
}

void toggleReceiver(unsigned char toggle)
{
    RCSTAbits.CREN = toggle != 0 ? 1 : 0;
}

void sendChar(unsigned char character)
{
    while(!TXSTAbits.TRMT);
    TXREG = character;
}

void sendData(unsigned char *string, int length)
{
    int i;

    for (i = 0; i < length; i++) 
        sendChar(string[i]);
}

int receiveData(struct receiveBuffer *buffer)
{
    
    int8_t character;
    int i = 0;
    int size = 0;
        
    if (RCSTAbits.OERR) { //In case data is sent while the MCU is not receiving
        RCSTAbits.CREN = 0; //This will clear the overrun error
        RCSTAbits.CREN = 1;
    }

    character = RCREG;//To clear the buffer of any unwanted input
    character = RCREG;
    
    if (CTS == ACTIVE) {
        RTS = ACTIVE;

        while (!RCIF);
        size = RCREG;

        if (size < MAX_BUFFER_LENGTH && size > 0) {
            while (i < size) {
                while (!RCIF); 
                buffer->buffer[i] = RCREG;
                i++;
            }
        }

        RTS = INACTIVE;
        while (CTS == ACTIVE);
    }

    buffer->length = i;
    buffer->buffer[i] = 0;
    
    return i;
}