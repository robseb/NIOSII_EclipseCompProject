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

#ifdef __cplusplus
extern "C" {
#endif

//
// Standard includes
//
#include <stddef.h>
#include <stdio.h>
#include <string.h>

//
// FreeRTOS includes
//
#include "FreeRTOS.h"
#include "task.h"
#include "semphr.h"

//
// NIOS II HAL includes
//
#include <sys/alt_irq.h>
#include "io.h"

//
/*-----------------------------------------------------------*/
// 					FreeRTOS Task definitions
//

// Priority definitions for the tasks in the demo application
#define STOPWATCH_TASK_PRIORITY		( tskIDLE_PRIORITY + 1 ) // Stop watch with 2 key inputs
#define BLINKING_TASK_PRIORITY		( tskIDLE_PRIORITY + 1 ) // Blinking LED


//
/*-----------------------------------------------------------*/
// 					HAL NIOS Component definitions
//

//
// Push Buttons (Parallel Port)
//

#define PIO_INTERUPT_MASK_REG 2*4
#define PIO_EDGE_CAPTURE_REG 3*4
#define PIO_DATA_REG 0

#define PB_START_STOP_MASK (1<<0)
#define PB_REST_MASK  (1<<1)

SemaphoreHandle_t SemStartStop;
SemaphoreHandle_t SemReset;

/*
 * The register test (or RegTest) tasks as described at the top of this file.
 */
static void TaskStopWatch( void);
static void TaskBlinking (void);

void displayValue(uint16_t val);
void blinkLED(void);

/*-----------------------------------------------------------*/

/* Counters that are incremented on each iteration of the RegTest tasks
so long as no errors have been detected. */
volatile unsigned long ulRegTest1Counter = 0UL, ulRegTest2Counter = 0UL;


/*-----------------------------------------------------------*/
static void pb_exti_irq(void *context, alt_u32 id) __attribute__ ((section (".exceptions")));
/*
 * Create the demo tasks then start the scheduler.
 */
int main( void )
{
	if ( -EINVAL == alt_irq_register( (alt_u32) PB_PIO_IRQ, (alt_u32) 0x0,pb_exti_irq ) )
	{
		/* Failed to install the Interrupt Handler. */
		asm( "break" );
	}
	else
	{
		/* Configure SysTick to interrupt at the requested rate. */
		IOWR_32DIRECT(PB_PIO_BASE,PIO_INTERUPT_MASK_REG,PB_START_STOP_MASK | PB_REST_MASK);
		IOWR_32DIRECT(PB_PIO_BASE,PIO_EDGE_CAPTURE_REG,PB_START_STOP_MASK | PB_REST_MASK);
	}

	displayValue(0);

	SemStartStop =xSemaphoreCreateBinary();
	SemReset=xSemaphoreCreateBinary();

    /* The RegTest tasks as described at the top of this file. */
    xTaskCreate( TaskStopWatch, "Stop Watch Task", configMINIMAL_STACK_SIZE, NULL, STOPWATCH_TASK_PRIORITY, NULL );
    xTaskCreate( TaskBlinking, "Blinking Task", configMINIMAL_STACK_SIZE, NULL, BLINKING_TASK_PRIORITY, NULL );

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

static void TaskStopWatch(void )
{
    /* Check the parameters are passed in as expected. */
	uint16_t countValue=0;

	typedef enum{
		RESETED=0,
		STOPED=1,
		RUNNING=2
	}stopWachStatus_t;

	stopWachStatus_t cur_status = RESETED;

	for( ;; )
    {
		switch(cur_status)
		{
		case RESETED:
			countValue =0;
			displayValue(countValue);
			// in the Reset Status wait for the Start Key
			xSemaphoreTake(SemStartStop,portMAX_DELAY);
			cur_status = RUNNING;
			break;
		case RUNNING:
			// Check if the Stop key was pressed
			if(xSemaphoreTake(SemStartStop,0)==pdTRUE)
			{
				// Stop the stop watch
				cur_status = STOPED;
			}
			else
			{
				// Count the stop watch up and display the value
				displayValue(countValue++);
				vTaskDelay((TickType_t) 100/portTICK_RATE_MS);

				if(countValue == 512)
				{
					// overdflow -> go to stop
					cur_status = STOPED;
				}
			}
			break;
		case STOPED:
			// in the Reset Status wait for the Start Key
			xSemaphoreTake(SemReset,portMAX_DELAY);
			cur_status = RESETED;
			break;
		}
    }
}

static void TaskBlinking (void)
{
	for( ;; )
    {
		blinkLED();
		vTaskDelay((TickType_t) 50/portTICK_RATE_MS);
    }

}

void displayValue(uint16_t val)
{
	IOWR_32DIRECT(DE10STD7SIG_BASE,0,val);
	IOWR_32DIRECT(LED_PIO_BASE,0,val);
}

void blinkLED(void)
{
	static uint8_t blink =1;
	blink = !blink;
	uint32_t led = IORD_32DIRECT(LED_PIO_BASE,0);
	IOWR_32DIRECT(LED_PIO_BASE,0,blink ? led| (1<<9): led& ~(1<<9));
}

static void pb_exti_irq(void *context, alt_u32 id)
{
	// Check witch key was pressed
	uint32_t key = (~IORD_32DIRECT(PB_PIO_BASE,PIO_DATA_REG)) & (PB_START_STOP_MASK | PB_REST_MASK);
	if( key== 1)
	{
		// The Start/Stop key was pressed
		xSemaphoreGiveFromISR(SemStartStop,NULL);
		// take other Semaphore to avoid multi input
		xSemaphoreTakeFromISR(SemReset,NULL);
	}
	else if( key== 2)
	{
		// The Reset key was pressed
		xSemaphoreGiveFromISR(SemReset,NULL);
		// take other Semaphore to avoid multi input
		xSemaphoreTakeFromISR(SemStartStop,NULL);
	}

	// Clear the Timer ISR Flag
	IOWR_32DIRECT(PB_PIO_BASE,PIO_INTERUPT_MASK_REG,PB_START_STOP_MASK | PB_REST_MASK);
	IOWR_32DIRECT(PB_PIO_BASE,PIO_EDGE_CAPTURE_REG,PB_START_STOP_MASK | PB_REST_MASK);

	IOWR_32DIRECT(PB_PIO_BASE,PIO_INTERUPT_MASK_REG,PB_START_STOP_MASK | PB_REST_MASK);
	IOWR_32DIRECT(PB_PIO_BASE,PIO_EDGE_CAPTURE_REG,PB_START_STOP_MASK | PB_REST_MASK);
}


#ifdef __cplusplus
}
#endif
