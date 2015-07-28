/* 
 * File:   serial_extended.h
 * Author: Manuel
 *
 * Created on July 27, 2015, 3:35 PM
 */

#include <xc.h>

#include "serial_pic.h"
#include "circular_buffer.h"

#ifndef EXTENDED_SERIAL_H
#define	EXTENDED_SERIAL_H

void eserial_setup(uint8_t baudrate_bits, uint16_t baudrate_value);

/* If CTS is deasserted? it will stop sending data immediately. It returns
 * the number of bytes sent. That can be used to ensure that all your data 
 * is sent later. I need to include encoding.
 */
int8_t eserial_send_data(struct circular_buffer volatile *buffer);

void eserial_receive(struct circular_buffer volatile *buffer);

#endif	/* EXTENDED_SERIAL_H */

