/* 
 * File:   pwm.h
 * Author: Manuel
 *
 * Created on July 7, 2015, 11:16 AM
 */
#include <xc.h>

#ifndef PWM_H
#define	PWM_H

#define P1A LATCbits.LATC5
#define TRIS_P1A TRISCbits.RC5
#define P1B LATCbits.LATC4
#define TRIS_P1B TRISCbits.RC4
#define P1C LATCbits.LATC3
#define TRIS_P1C TRISCbits.RC3
#define P1D LATCbits.LATC2
#define TRIS_P1D TRISCbits.RC2

#define NONE 0x00
#define OUT_A 0x01
#define OUT_B 0x02
#define OUT_C 0x04
#define OUT_D 0x08

typedef enum {PACH_PBDH,PACH_PBDL, PACL_PBDH, PACL_PBDL} sModes; //To set the polarity of outputs
typedef enum {TMRP_1, TMRP_4, TMRP_16} tmrPre;

void pmwSingleModeSetUp(sModes polarity, unsigned char valuePR2, tmrPre scaler,
        unsigned char outputs);
void setPulseWidth(unsigned int width);
void selectOutput(unsigned char outputs);

void pmwHalfBridgeSetUp();//For Later
void pmwFullBridgeSetUp();//For Later




#endif	/* PWM_H */

