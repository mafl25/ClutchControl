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

void setup_tmr0(int tmr0_value);

int main() {
    __delay_ms(1);
    
    setup_tmr0(65340);
    serialSetUp(BRG16_ON, BRGH_ON, 0x81); // TODO: Clean Up all code
    pmwSingleModeSetUp(PACH_PBDH, 254, TMRP_1, OUT_C | OUT_B);
    setPulseWidth(0);
    
    struct receiveBuffer data;
    int i = 0;
    unsigned char wat = 0;
    
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
        
        /*if (INTCONbits.TMR0IF){
            sendData(&wat, 0);
            TMR0H = 65340 >> 8;
            TMR0L = 65340;
            INTCONbits.TMR0IF = 0;
        }*/
    }
    
    return (0);
}

void setup_tmr0(int tmr0_value)
{
    T0CONbits.PSA = 0;
    T0CONbits.T0PS = 0x06;
    T0CONbits.T0CS = 0;
    T0CONbits.T08BIT = 0;
    INTCONbits.TMR0IF = 0;
    TMR0H = tmr0_value >> 8;
    TMR0L = tmr0_value;
    T0CONbits.TMR0ON = 1;
}