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

/* 
 * This library seeks to extend the functionality of "serial_pic" in order to 
 * have it work with an FTDI IC. It implements hardware flow control, uses 
 * "circular_buffer" to store data, and will need to use timers to use as 
 * timeouts in order to work properly with the FTDI chip (the user will provide
 * function pointers to implement the timeout functionality, so he/she can 
 * choose which timer use).
 */

/*
 * The function "eserial_setup" sets up a connection with an FTDI serial 
 * interface IC. As input, it simply takes the baudrate configuration bits
 * and baudrate value. See "serial_pic.h" for more information. Other than the
 * RX/TX I/O pair, this also uses RC0 as RTS and RC1 as CTS.
 */
void eserial_setup(uint8_t baudrate_bits, uint16_t baudrate_value);

/*
 * The function "eserial_send_data" takes a circular_buffer as input and sends
 * all of it. See "circular_buffer.h" for more information.
 */
int8_t eserial_send_data(struct circular_buffer *buffer);

/*
 * The function "eserial_receive" takes as input:
 * - A circular_buffer to store the received data.
 * - A function pointer to a function that will indicate the PIC to stop 
 * receiving data. If this functionality is not needed, just pass a NULL
 * pointer.
 * - A function pointer to a function with int16_t as input which will start a
 * timer. This is needed because the FTDI IC keeps sending some more bytes 
 * after having de-asserted the RTS line. This function will cause the PIC to 
 * keep receiving data for a certain amount of time after de-asserting the RTS
 * so that this bytes are not lost.
 * - A function pointer that returns true when the timer is up.
 */
void eserial_receive(struct circular_buffer *buffer, 
                     bool (*stop_function)(void), 
                     void (*timer_start)(int16_t),
                     bool (*timer_up)(void));

#endif	/* EXTENDED_SERIAL_H */

