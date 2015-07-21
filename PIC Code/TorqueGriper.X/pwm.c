#include "pwm.h"

void pmwSingleModeSetUp(sModes polarity, unsigned char valuePR2, tmrPre scaler,
        unsigned char outputs)
{
    T2CONbits.TMR2ON = 1;
    
    switch (scaler) {
        case TMRP_1:
            T2CONbits.T2CKPS = 0x00;
            break;
        case TMRP_4:
            T2CONbits.T2CKPS = 0x01;
            break;
        case TMRP_16:
            T2CONbits.T2CKPS = 0x11;
    }
    
    CCP1CONbits.P1M = 0x00;
    
    switch (polarity) {
        case PACH_PBDH:
            CCP1CONbits.CCP1M = 0b1100;
            break;
        case PACH_PBDL:
            CCP1CONbits.CCP1M = 0b1101;
            break;
        case PACL_PBDH:
            CCP1CONbits.CCP1M = 0b1110;
            break;
        case PACL_PBDL:
            CCP1CONbits.CCP1M = 0b1111;
    }
    
    PSTRCONbits.STRSYNC = 1;
    
    if (outputs & OUT_A) { //Test this code
        P1A = 0;
        TRIS_P1A = 0;
    }
    if (outputs & OUT_B) {
        P1B = 0;
        TRIS_P1B = 0;
    }
    if (outputs & OUT_C) {
        P1C = 0;
        TRIS_P1C = 0;
    }
    if (outputs & OUT_D) {
        P1D = 0;
        TRIS_P1D = 0;
    }
    
    PR2 = valuePR2;
}

void setPulseWidth(unsigned int width)
{
    CCP1CONbits.DC1B = width;
    CCPR1L = width >> 2;
}

void selectOutput(unsigned char outputs, unsigned char toggle) 
{
    switch (outputs){
        case 0:
            PSTRCON = 0xF0;
            break;
        case OUT_A:
            PSTRCONbits.STRA = (toggle) ? 1 : 0;
            break;
        case OUT_B:
            PSTRCONbits.STRB = (toggle) ? 1 : 0;
            break;
        case OUT_C:
            PSTRCONbits.STRC = (toggle) ? 1 : 0;
            break;
        case OUT_D:
            PSTRCONbits.STRD = (toggle) ? 1 : 0;
            break;
    }
}