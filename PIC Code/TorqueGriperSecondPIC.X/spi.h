/* 
 * File:   spi.h
 * Author: Manuel
 *
 * Created on July 22, 2015, 6:06 PM
 */

#ifndef SPI_H
#define	SPI_H

#define SDI_TRIS    TRISBbits.RB4
#define SDI_AN      ANSELHbits.ANS10
#define SDO_TRIS    TRISCbits.RC7
#define SCK_TRIS    TRISBbits.RB6
#define SS_TRIS     TRISCbits.RC6  // I think this is only for the slave  

#define SPI_CTS         PORTCbits.RC6
#define SPI_CTS_TRIS    TRISCbits.RC6
#define SPI_CTS_AN      ANSELHbits.ANS8
#define SPI_RTS         LATCbits.LATC6
#define SPI_RTS_TRIS    TRISCbits.RC6  // Need to change in the slave PIC
#define RTS_CHAR    0xA0
#define CTS_CHAR    0xB0
#define CTS_ANS     0xC0
#define DUMMY_CHAR  0xD0
#define SEND_MASK   0xF0

enum spi_mode {MM_FOSC4, MM_FOSC16, MM_FOSC64, MM_TMR22, SM_SS, SM_NSS};
enum spi_clk_pol {IDLE_LOW, IDLE_HIGH};
enum spi_trans_sel {IDLE_ACTIVE, ACTIVE_IDLE};
enum spi_sampling {MIDDLE, END};

struct spi_receive_buffer
{
    unsigned char buffer[30];
    int length;
};

void set_spi(enum spi_mode mode, enum spi_clk_pol polarity,
             enum spi_trans_sel selection, enum spi_sampling sample);
unsigned char spi_write(unsigned char data);
unsigned char spi_read(void);
void send_data_spi(unsigned char *data, char size);
void master_receive_data(struct spi_receive_buffer *buffer);
void slave_receive_data(struct spi_receive_buffer *buffer);

#endif	/* SPI_H */

