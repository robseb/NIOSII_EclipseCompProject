/*
    FreeRTOS V7.1.0 - Copyright (C) 2011 Real Time Engineers Ltd.
	

    ***************************************************************************
     *                                                                       *
     *    FreeRTOS tutorial books are available in pdf and paperback.        *
     *    Complete, revised, and edited pdf reference manuals are also       *
     *    available.                                                         *
     *                                                                       *
     *    Purchasing FreeRTOS documentation will not only help you, by       *
     *    ensuring you get running as quickly as possible and with an        *
     *    in-depth knowledge of how to use FreeRTOS, it will also help       *
     *    the FreeRTOS project to continue with its mission of providing     *
     *    professional grade, cross platform, de facto standard solutions    *
     *    for microcontrollers - completely free of charge!                  *
     *                                                                       *
     *    >>> See http://www.FreeRTOS.org/Documentation for details. <<<     *
     *                                                                       *
     *    Thank you for using FreeRTOS, and thank you for your support!      *
     *                                                                       *
    ***************************************************************************


    This file is part of the FreeRTOS distribution.

    FreeRTOS is free software; you can redistribute it and/or modify it under
    the terms of the GNU General Public License (version 2) as published by the
    Free Software Foundation AND MODIFIED BY the FreeRTOS exception.
    >>>NOTE<<< The modification to the GPL is included to allow you to
    distribute a combined work that includes FreeRTOS without being obliged to
    provide the source code for proprietary components outside of the FreeRTOS
    kernel.  FreeRTOS is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
    or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
    more details. You should have received a copy of the GNU General Public
    License and the FreeRTOS license exception along with FreeRTOS; if not it
    can be viewed here: http://www.freertos.org/a00114.html and also obtained
    by writing to Richard Barry, contact details for whom are available on the
    FreeRTOS WEB site.

    1 tab == 4 spaces!

    http://www.FreeRTOS.org - Documentation, latest information, license and
    contact details.

    http://www.SafeRTOS.com - A version that is certified for use in safety
    critical systems.

    http://www.OpenRTOS.com - Commercial support, development, porting,
    licensing and training services.
*/

/*
 * Creates all the demo application tasks, then starts the scheduler.
 * In addition to the standard demo tasks, the following tasks and tests are
 * defined and/or created within this file:
 *
 * "Check" task -  This only executes every five seconds but has the highest
 * priority so is guaranteed to get processor time.  Its main function is to 
 * check that all the standard demo tasks are still operational.  The check
 * task will write an error message to the console should an error be detected
 * within any of the demo tasks.  The check task also toggles the LED defined
 * by mainCHECK_LED every 5 seconds while the system is error free, with the
 * toggle rate increasing to every 500ms should an error occur.
 * 
 * "Reg test" tasks - These fill the registers with known values, then check
 * that each register still contains its expected value.  Each task uses
 * different values.  The tasks run with very low priority so get preempted very
 * frequently.  A register containing an unexpected value is indicative of an
 * error in the context switching mechanism.
 *
 * See the online documentation for this demo for more information on interrupt
 * usage.
 */

/* Standard includes. */
#include <stddef.h>
#include <stdio.h>
#include <string.h>

/* Scheduler includes. */
#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"

#include <arch/cc.h>

/*-----------------------------------------------------------*/

/* The rate at which the LED controlled by the 'check' task will toggle when no
errors have been detected. */
#define mainNO_ERROR_PERIOD	( 5000 )

/* The rate at which the LED controlled by the 'check' task will toggle when an
error has been detected. */
#define mainERROR_PERIOD 	( 500 )

/* Priority definitions for the tasks in the demo application. */
#define mainLED_TASK_PRIORITY		( tskIDLE_PRIORITY + 1 )


/* Misc. */
#define mainDONT_WAIT						( 0 )

/* The parameters passed to the reg test tasks.  This is just done to check
the parameter passing mechanism is working correctly. */
#define mainREG_TEST_1_PARAMETER    ( ( void * ) 0x12345678 )
/*-----------------------------------------------------------*/

#ifdef __cplusplus
extern "C" {
#endif


#ifdef __cplusplus
}
#endif
/*
 * The register test (or RegTest) tasks as described at the top of this file.
 */
static void prvFirstRegTestTask( void *pvParameters );


/*-----------------------------------------------------------*/

/* Counters that are incremented on each iteration of the RegTest tasks
so long as no errors have been detected. */
volatile unsigned long ulRegTest1Counter = 0UL, ulRegTest2Counter = 0UL;

/*-----------------------------------------------------------*/

/*
 * Create the demo tasks then start the scheduler.
 */
int main( void )
{
    /* The RegTest tasks as described at the top of this file. */
    xTaskCreate( prvFirstRegTestTask, "Rreg1", configMINIMAL_STACK_SIZE, mainREG_TEST_1_PARAMETER, mainLED_TASK_PRIORITY, NULL );

    /* Finally start the scheduler. */
	vTaskStartScheduler();
    
	/* Will only reach here if there is insufficient heap available to start
	the scheduler. */
	for( ;; );
}
/*-----------------------------------------------------------*/
void vApplicationStackOverflowHook(__unused xTaskHandle *pxTask, signed char *pcTaskName )
{
	printf("[free_rtos] Application stack overflow at task: %s\n", pcTaskName);
}

void vApplicationMallocFailedHook(void)
{
	printf("[free_rtos] Malloc Failed\n");
}

void _general_exception_handler( unsigned long ulCause, unsigned long ulStatus )
{
	/* This overrides the definition provided by the kernel.  Other exceptions 
	should be handled here. */
	for( ;; )
    {
		asm( "break" );
    }
}
/*-----------------------------------------------------------*/

static void prvFirstRegTestTask( void *pvParameters )
{
    /* Check the parameters are passed in as expected. */
    if( pvParameters != mainREG_TEST_1_PARAMETER )
    {
        /* Don't execute any further so an error is recognised by the check 
        task. */
        vTaskDelete( NULL );
    }
}