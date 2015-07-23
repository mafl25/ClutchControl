/* 
 * File:   main.c
 * Author: Manuel
 *
 * Created on July 10, 2015, 12:54 PM
 */

#include <xc.h>
#include "serialprotocol.h"
#include "pwm.h"
//#include "spi.h"

// CONFIG1H
#pragma config FOSC = HS        // Oscillator Selection bits (HS oscillator)
#pragma config PLLEN = OFF      // 4 X PLL Enable bit (PLL is under software control)
#pragma config PCLKEN = ON      // Primary Clock Enable bit (Primary clock enabled)
#pragma config FCMEN = OFF      // Fail-Safe Clock Monitor Enable (Fail-Safe Clock Monitor disabled)
#pragma config IESO = OFF       // Internal/External Oscillator Switchover bit (Oscillator Switchover mode disabled)

// CONFIG2L
#pragma config PWRTEN = OFF     // Power-up Timer Enable bit (PWRT disabled)
#pragma config BOREN = SBORDIS  // Brown-out Reset Enable bits (Brown-out Reset enabled in hardware only (SBOREN is disabled))
#pragma config BORV = 19        // Brown Out Reset Voltage bits (VBOR set to 1.9 V nominal)

// CONFIG2H
#pragma config WDTEN = OFF      // Watchdog Timer Enable bit (WDT is controlled by SWDTEN bit of the WDTCON register)
#pragma config WDTPS = 32768    // Watchdog Timer Postscale Select bits (1:32768)

// CONFIG3H
#pragma config HFOFST = ON      // HFINTOSC Fast Start-up bit (HFINTOSC starts clocking the CPU without waiting for the oscillator to stablize.)
#pragma config MCLRE = ON       // MCLR Pin Enable bit (MCLR pin enabled, RA3 input pin disabled)

// CONFIG4L
#pragma config STVREN = ON      // Stack Full/Underflow Reset Enable bit (Stack full/underflow will cause Reset)
#pragma config LVP = OFF        // Single-Supply ICSP Enable bit (Single-Supply ICSP disabled)
#pragma config BBSIZ = OFF      // Boot Block Size Select bit (512W boot block size)
#pragma config XINST = OFF      // Extended Instruction Set Enable bit (Instruction set extension and Indexed Addressing mode disabled (Legacy mode))

#define _XTAL_FREQ 20000000
#define FORWARD LATCbits.LATC3 
#define TRIS_FORWARD TRISCbits.RC3
#define BACKWARD LATCbits.LATC4 
#define TRIS_BACKWARD TRISCbits.RC4 

#define TMR0VAL 65340

void interrupt com_link(void);

int main() {
    /*__delay_ms(1);
    serialSetUp(BRG16_ON, BRGH_ON, 0x81);
    
    pmwSingleModeSetUp(PACH_PBDH, 254, TMRP_1, OUT_C | OUT_B);
    setPulseWidth(0);
    
    /*T0CONbits.PSA = 0;
    T0CONbits.T0PS = 0x06;
    T0CONbits.T0CS = 0;
    T0CONbits.T08BIT = 0;
    INTCONbits.TMR0IF = 0;
    INTCONbits.TMR0IE = 1;
    INTCONbits.GIE = 1;
    TMR0H = TMR0VAL >> 8;
    TMR0L = TMR0VAL;
    T0CONbits.TMR0ON = 1;
    
        
    
    struct receiveBuffer data;
    int i = 0;
    
    while (1) {
        
        i = receiveData(&data);
        
        
        if (i) {
            if (data.buffer[0] == 0xAA) {
                selectOutput(data.buffer[1], 1); 
            } else if (data.buffer[0] == 0xAB) {
                selectOutput(data.buffer[1], 0);
            } else if (data.buffer[0] == 0xAC) {
                setPulseWidth(data.buffer[1] << 2 | data.buffer[2]);
            }
        }
    }*/
    /*serialSetUp(BRG16_ON, BRGH_ON, 0x81);
    sendChar('a');
    struct spi_receive_buffer my_data = {0, 0};
    
    set_spi(SM_NSS, IDLE_LOW, IDLE_ACTIVE, MIDDLE);
    char i = 0;
    
    while (1){
        slave_receive_data(&my_data);
        for(i = 0; i < my_data.length; i++) {
            sendChar(my_data.buffer[i]);
        }
    }*/
    
#define CTS_CHAR    0x70
#define OK_CHAR     0x60
#define NOK_CHAR    0x50
#define MAX_SIZE    6
#define TB_CHAR     0x40
#define RX_MASK     0xA0
#define RTS_MASK    0xE0
    

    serialSetUp(BRG16_ON, BRGH_ON, 0x04);
    unsigned char byte_1;
    unsigned char byte_2;
    unsigned char data[MAX_SIZE];
    char length = 0;
    char size;
    char i;
    
    while (1){
        i = 0;
        if (RCIF){
            i = 0;
            byte_1 = RCREG;
            
            if ((byte_1 & 0xF0) == RTS_MASK){
                size = byte_1 & 0x0F;
                if (size <= MAX_SIZE) {
                    sendChar(CTS_CHAR);
                    for (; i < size; i++){
                        while (!RCIF); 
                        byte_1 = RCREG;
                        while (!RCIF);
                        byte_2 = RCREG;

                        if ((byte_1 & 0xF0) == RX_MASK && (byte_2 & 0xF0) == RX_MASK){
                            data[i] = byte_1 << 4 | (byte_2 & 0x0F);
                            sendChar(OK_CHAR);
                        } else {
                            sendChar(NOK_CHAR);
                            break;
                        }
                    }
                } else {
                    sendChar(TB_CHAR);
                }
            }
            
            length = i;
        }
        
        if (i)
            sendData(data, length);
    }
    
    
    return (0);
}

void interrupt com_link(void)        // interrupt function 
 {
    if (INTCONbits.TMR0IF && INTCONbits.TMR0IE){                                     
        TMR0H = TMR0VAL >> 8;
        TMR0L = TMR0VAL;
        INTCONbits.TMR0IF = 0;
        __delay_ms(1);
    }
}