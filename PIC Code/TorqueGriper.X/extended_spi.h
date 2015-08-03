/* 
 * File:   extended_spi.h
 * Author: Manuel
 *
 * Created on July 30, 2015, 12:37 PM
 */

#include <xc.h>
#include <stdint.h>
#include <stdbool.h>
#include "spi_pic.h"
#include "circular_buffer.h"
#include "encoding.h"

#ifndef EXTENDED_SPI_H
#define	EXTENDED_SPI_H

#define TX_CHAR     0x10
#define RX_CHAR     0x20
#define END_CHAR    0x30
#define ERROR_CHAR  0x70


void espi_setup(uint8_t mode);

void espi_slave_receive(struct circular_buffer *buffer);
void espi_slave_send(struct circular_buffer *buffer);

void espi_master_send(struct circular_buffer *buffer,
                      void (*timer_start)(int16_t),
                      bool (*timer)(void));
void espi_master_receive(struct circular_buffer *buffer,
                        void (*timer_start)(int16_t),
                        bool (*timer)(void));

#endif	/* EXTENDED_SPI_H */

