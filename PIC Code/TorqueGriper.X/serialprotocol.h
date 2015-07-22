/* 
 * File:   serialprotocol.h
 * Author: Manuel
 *
 * Created on July 10, 2015, 12:58 PM
 */

#include <xc.h>

#ifndef SERIALPROTOCOL_H
#define	SERIALPROTOCOL_H

/*
 * RTS and CTS uses inverted logic
 */
#define RTS LATCbits.LATC0
#define TRIS_RTS TRISCbits.RC0
#define CTS PORTCbits.RC1
#define TRIS_CTS TRISCbits.RC1
#define CTS_AN  ANSELbits.ANS5
#define TRIS_RX TRISBbits.RB5
#define RX_AN   ANSELHbits.ANS11
#define TRIS_TX TRISBbits.RB7

#define MAX_BUFFER_LENGTH 16
#define INACTIVE 1
#define ACTIVE 0
#define BRG16_ON 1
#define BRG16_OFF 0
#define BRGH_ON 1
#define BRGH_OFF 0

typedef char int8_t;
typedef unsigned char uint8_t;

struct receiveBuffer
{
    unsigned char buffer[MAX_BUFFER_LENGTH];
    char length;
};

void serialSetUp(unsigned char brg16_bit, unsigned char brgh_bit, 
        unsigned int spbrg16); //Use Excel file to get the right values
void toggleSerialPort(unsigned char toggle); //Turns Serial Port on or off
void toggleTransmitter(unsigned char toggle); //Turns Transmitter on or off
void toggleReceiver(unsigned char toggle); //Turns Receiver on or off
void sendChar(unsigned char toggle);
void sendData(unsigned char *string, int length);
int receiveData(struct receiveBuffer *SBuffer);

#endif	/* SERIALPROTOCOL_H */

