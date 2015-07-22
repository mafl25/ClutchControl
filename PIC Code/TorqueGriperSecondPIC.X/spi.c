#include <xc.h>
#include "spi.h"

static void reassemble_packet(struct spi_receive_buffer *buffer, char size)
{
    char i;
    
    for (i = 0; i < size; i += 2) {
        unsigned char byte_1 = buffer->buffer[i];
        unsigned char byte_2 = buffer->buffer[i + 1];
        buffer->buffer[i >> 1] = byte_1 << 4 | (byte_2 & 0x0F);
    }

    buffer->length = i >> 1;
}

void set_spi(enum spi_mode mode, enum spi_clk_pol polarity,
             enum spi_trans_sel selection, enum spi_sampling sample)
{
    SDO_TRIS = 0;

    SSPCON1bits.SSPM = mode;
    SSPCON1bits.CKP = polarity;
    SSPSTATbits.SMP = sample;
    
    if (mode == SM_NSS || mode == SM_SS) {
        SCK_TRIS = 1;
        if (mode == SM_SS)
            SS_TRIS = 1;
        SSPSTATbits.CKE = 0;
        SPI_RTS_TRIS = 0;
        SPI_RTS = 0;
    } else {
        SCK_TRIS = 0;
        SPI_CTS_TRIS = 1;
        SPI_CTS_AN = 0;
        SSPSTATbits.CKE = selection;
    }
    
    SDI_AN = 0;
    
    SSPCON1bits.SSPEN = 0x1;
}

unsigned char spi_write(unsigned char data)
{
    SSPBUF = data;
    while (!SSPSTATbits.BF);
    return SSPBUF;
}

unsigned char spi_read(void)
{
    while (SSPSTATbits.BF);
    return SSPBUF;   
}

void send_data_spi(unsigned char *data, char size)
{
    spi_write(RTS_CHAR | (size & 0x0F));
    
    while (!SPI_CTS);  
    
    char i;
    for (i = 0; i < size; i++) {
        unsigned char byte_1 = (data[i] >> 4) | SEND_MASK;
        unsigned char byte_2 = (data[i] & 0x0F) | SEND_MASK;
        spi_write(byte_1);
        spi_write(byte_2);
    }
}

void master_receive_data(struct spi_receive_buffer *buffer)
{
    buffer->length = 0;
    
    if (SPI_CTS){
        unsigned char response = spi_write(CTS_CHAR);
        if ((response & CTS_ANS) == CTS_ANS){
            unsigned char size = (response & 0x0F) * 2;
            char i;
            for (i = 0; i < size; i++)
                buffer->buffer[i] = spi_write(DUMMY_CHAR);
            
            reassemble_packet(buffer, size);
        }
    }
}

void slave_receive_data(struct spi_receive_buffer *buffer)
{
    if (SSPSTATbits.BF){
        unsigned char receive = SSPBUF;
        if ((receive & 0xF0) == RTS_CHAR){
            char size = (receive & 0x0F) * 2;
            char i = 0;
            for (i = 0; i < size; i++) {
                SPI_RTS = 1;
                while (!SSPSTATbits.BF);
                buffer->buffer[i] = SSPBUF;
            }
            SPI_RTS = 0;
            
            reassemble_packet(buffer, size);
        }
    }
}
