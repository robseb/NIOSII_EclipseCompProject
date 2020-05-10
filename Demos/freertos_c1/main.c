//
//
//            ########   ######     ##    ##  #######   ######  ########  #######
//            ##     ## ##    ##     ##  ##  ##     ## ##    ##    ##    ##     ##
//            ##     ## ##            ####   ##     ## ##          ##    ##     ##
//            ########   ######        ##    ##     ## ##          ##    ##     ##
//            ##   ##         ##       ##    ##     ## ##          ##    ##     ##
//            ##    ##  ##    ##       ##    ##     ## ##    ##    ##    ##     ##
//            ##     ##  ######        ##     #######   ######     ##     #######
//
//			----	Simple FreeRTOS Example for the NIOS II Processor ----
//
//	This Project with it's own HAL was automatically generate by "NIOSII_EclipseCompProject"
// 					designed by Robin Sebastian (https://github.com/robseb)
//
//


/* Standard includes. */
#include <stddef.h>
#include <stdio.h>
#include <string.h>

/* Scheduler includes. */
#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"


/*-----------------------------------------------------------*/

/* The rate at which the LED controlled by the 'check' task will toggle when no
errors have been detected. */
#define mainNO_ERROR_PERIOD	( 5000 )

/* The rate at which the LED controlled by the 'check' task will toggle when an
error has been detected. */
#define mainERROR_PERIOD 	( 500 )

/* Priority definitions for the tasks in the demo application. */
#define mainLED_TASK_PRIORITY		( tskIDLE_PRIORITY + 1 )

/*-----------------------------------------------------------*/

#ifdef __cplusplus
extern "C" {
#endif



/*
 * The register test (or RegTest) tasks as described at the top of this file.
 */
static void prvFirstRegTestTask( void);


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
    xTaskCreate( prvFirstRegTestTask, "Rreg1", configMINIMAL_STACK_SIZE, NULL, mainLED_TASK_PRIORITY, NULL );

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

static void prvFirstRegTestTask(void )
{
    /* Check the parameters are passed in as expected. */
	for( ;; )
    {
        /* Don't execute any further so an error is recognised by the check 
        task. */
    	printf("Task 1\n");
        vTaskDelete( 100 );
    }
}

#ifdef __cplusplus
}
#endif
