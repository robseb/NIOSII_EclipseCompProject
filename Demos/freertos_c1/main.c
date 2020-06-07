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
// 					designed by Robin Sebastian (https://github.com/robseb) (git@robseb.de)
//
//

#ifdef __cplusplus
extern "C" {
#endif

///////////////////////////////////////////////////////////////////////////////////////////
//				This example shows a simple implementation of a 						 //
//			stop watch running as a FreeRTOS task and a blinking LED Task				 //
//																					     //
//							===== Stop watch Task =====								     //
//				KEY1: Start and Stop the up counting of the stop watch 					 //
//				KEY2: Reset the stop watch counting values								 //
//				LEDS: To show the counting value in binary								 //
// 7-Sigment Display: To show the counting value in hexadecimal   						 //
//																						 //
//						    ==== Blinking Task ====									     //
//							Toggles a LED every 50ms 								     //
//																						 //
//							==== Required IP for FreeRTOS ===						     //
//							--- Interval Timer Intel FPGA --- 							 //
//								     Period:       1ms 							     	 //
//									 Counter Size: 32 								 	 //
//							   No Start/Stop control bit (Y)						     //
//							          Name:   "sys_clk"									 //
//								 Interrupt line to NIOS II 							     //
//																						 //
//							 ====  IP for Demo ===						     	 		 //
//							 * for Push Buttons:										 //
//								- PIO (Parallel I/O) Intel FPGA							 //
//								   * Generate IRQ (Y)									 //
//								   * IRQ Type: EDGE										 //
//								   * Name: "pb_pio"									     //
//								   *Interrupt line to NIOS II (higher priority)		     //
//							 * for LEDs:												 //
//								- PIO (Parallel I/O) Intel FPGA							 //
//								   * Name: "led_pio"									 //
//																						 //
///////////////////////////////////////////////////////////////////////////////////////////


//
// FreeRTOS includes
//
#include "system.h"
#include "FreeRTOS.h"
#include "task.h"
#include "semphr.h"

//
// NIOS II HAL includes
//
#include <sys/alt_irq.h>
#include "io.h"


///////////////////////////////////////////////////////////////////////////////////////////
///																						 //
///								DEVELOPMENT BOARD CONFIGURATION 						 //
///																						 //
///////////////////////////////////////////////////////////////////////////////////////////

#define TERASIC_DE0_NANO    1  // Terasic DE0  NANO Board with a Intel Cyclone IV FPGA
#define TERASIC_DE10_STD    2  // Terasic DE10 STANDARD Board with a Intel Cyclone V SoC-FPGA
#define TERASIC_DE10_NANO   3  // Terasic DE10 NANO Board with a Intel Cyclone V SoC-FPGA
#define TERASIC_HAN_PILOT   4  // Terasic HAN PILOT Board with a Intel Arria 10 SoC-FPGA
#define CUSTOM_BOARD	    0  // Custom board with a custom board configuration
#define UNKOWN_BOARD	   -1

/////
///////////////////
// Select your development board
#define SELCTED_BOARD TERASIC_DE10_STD
///////////////////
/////

#if SELCTED_BOARD == UNKOWN_BOARD
	#error "Please select your development board!"
#elif SELCTED_BOARD == TERASIC_DE0_NANO
	#define BCONF_EN_SEVSIG    	     0   // Enable the 7sig Display
	#define BCONF_EN_SEVSIG_LEN      0   // Largest displayable number on 7sig Display
	#define BCONF_EN_LEDDISP         1   // Enable the LED bin Display
	#define BCONF_EN_LEDDISP_LEN     7   // LED count for the bin Display
	#define BCONF_MAX_COUNT_VALUE  126   // Max value to count for the stop watch counter
	#define BCONF_START_PBNO		 0   // Number of the Start/Stop push button
	#define BCONF_REST_PBNO		     1   // Number of the Reset push button

	#define BCONF_EN_TOGLE_LED	     1   // Enable the 50ms toogle LED task
	#define BCONF_TOOGLE_LED_NO	     8   // LED number of the toogle LED

#elif SELCTED_BOARD == TERASIC_DE0_NANO
	#define BCONF_EN_SEVSIG    	     0   // Enable the 7sig Display
	#define BCONF_EN_SEVSIG_LEN      0   // Largest displayable number on 7sig Display
	#define BCONF_EN_LEDDISP         1   // Enable the LED bin Display
	#define BCONF_EN_LEDDISP_LEN     9   // LED count for the bin Display
	#define BCONF_MAX_COUNT_VALUE  511   // Max value to count for the stop watch counter
	#define BCONF_START_PBNO		 0   // Number of the Start/Stop push button
	#define BCONF_REST_PBNO		     1   // Number of the Reset push button

	#define BCONF_EN_TOGLE_LED	     1   // Enable the 50ms toogle LED task
	#define BCONF_TOOGLE_LED_NO	     9   // LED number of the toogle LED

#elif SELCTED_BOARD == TERASIC_DE10_STD
	#define BCONF_EN_SEVSIG    	      1   // Enable the 7sig Display
	#define BCONF_EN_SEVSIG_LEN   65535   // Largest displayable number on 7sig Display
	#define BCONF_EN_LEDDISP          1   // Enable the LED bin Display
	#define BCONF_EN_LEDDISP_LEN      9   // LED count for the bin Display
	#define BCONF_MAX_COUNT_VALUE   511   // Max value to count for the stop watch counter
	#define BCONF_START_PBNO		  0   // Number of the Start/Stop push button
	#define BCONF_REST_PBNO		      1   // Number of the Reset push button

	#define BCONF_EN_TOGLE_LED	      1   // Enable the 50ms toogle LED task
	#define BCONF_TOOGLE_LED_NO	      9   // LED number of the toogle LED
#elif SELCTED_BOARD == TERASIC_HAN_PILOT
	#define BCONF_EN_SEVSIG    	      1   // Enable the 7sig Display
	#define BCONF_EN_SEVSIG_LEN     255   // Largest displayable number on 7sig Display
	#define BCONF_EN_LEDDISP          0   // Enable the LED bin Display
	#define BCONF_EN_LEDDISP_LEN      0   // LED count for the bin Display
	#define BCONF_MAX_COUNT_VALUE   255   // Max value to count for the stop watch counter
	#define BCONF_START_PBNO		  0   // Number of the Start/Stop push button
	#define BCONF_REST_PBNO		      1   // Number of the Reset push button

	#define BCONF_EN_TOGLE_LED	      1   // Enable the 50ms toogle LED task
	#define BCONF_TOOGLE_LED_NO	      0   // LED number of the toogle LED
#elif SELCTED_BOARD == CUSTOM_BOARD
	#define BCONF_EN_SEVSIG    	      ()   // Enable the 7sig Display
	#define BCONF_EN_SEVSIG_LEN       ()   // Largest displayable number on 7sig Display
	#define BCONF_EN_LEDDISP          ()   // Enable the LED bin Display
	#define BCONF_EN_LEDDISP_LEN      ()   // LED count for the bin Display
	#define BCONF_MAX_COUNT_VALUE     ()   // Max value to count for the stop watch counter
	#define BCONF_START_PBNO		  ()   // Number of the Start/Stop push button
	#define BCONF_REST_PBNO		      ()   // Number of the Reset push button

	#define BCONF_EN_TOGLE_LED	      ()   // Enable the 50ms toogle LED task
	#define BCONF_TOOGLE_LED_NO	      ()   // LED number of the toogle LED
#endif


//
/*-----------------------------------------------------------*/
// 					FreeRTOS Task definitions
//


///////////////////////////////////////////////////////////////////////////////////////////
///																						 //
///								FREERTOS TAKS DEFINITIONS		 						 //
///																						 //
///////////////////////////////////////////////////////////////////////////////////////////

#define STOPWATCH_TASK_PRIORITY		( tskIDLE_PRIORITY + 1 ) // Stop watch with 2 key inputs
#if BCONF_EN_TOGLE_LED == 1
	#define BLINKING_TASK_PRIORITY		( tskIDLE_PRIORITY + 1 ) // Blinking LED
#endif

///////////////////////////////////////////////////////////////////////////////////////////
///																						 //
///								HAL COMPONENT DEFINITIONS		 						 //
///																						 //
///////////////////////////////////////////////////////////////////////////////////////////

// Intel Parallel Port IP Register Offsets
#define PIO_INTERUPT_MASK_REG 2*4
#define PIO_EDGE_CAPTURE_REG 3*4
#define PIO_DATA_REG 0

// Push button masks
#define PB_START_STOP_MASK 	(1<<BCONF_START_PBNO)
#define PB_REST_MASK  		(1<<BCONF_REST_PBNO)


///////////////////////////////////////////////////////////////////////////////////////////

SemaphoreHandle_t SemStartStop; // Semaphore to signal Start/Stop push button was pressed
SemaphoreHandle_t SemReset;     // Semaphore to signal the Reset push button was pressed


// The Stop watch task function
static void TaskStopWatch( void);

// The toggle LED task function
#if BCONF_EN_TOGLE_LED == 1
	static void TaskBlinking (void);
#endif

void displayValue(uint16_t val);
void blinkLED(void);


/*-----------------------------------------------------------*/
static void pb_exti_irq(void *context, alt_u32 id) __attribute__ ((section (".exceptions")));
/*
 * Create the demo tasks then start the scheduler.
 */
int main( void )
{
	// Register and enable the external GPIO interrupt for the Start/Stop- and Reset buttons
	if ( -EINVAL == alt_irq_register( (alt_u32) PB_PIO_IRQ, (alt_u32) 0x0,pb_exti_irq ) )
	{
		// Register failed -> stop the debugging
		asm( "break" );
	}
	// Enable the external GPIO interrupt Start/Stop- and Reset buttons
	IOWR_32DIRECT(PB_PIO_BASE,PIO_INTERUPT_MASK_REG,PB_START_STOP_MASK | PB_REST_MASK);
	// Enable the edge detection for Start/Stop- and Reset buttons
	IOWR_32DIRECT(PB_PIO_BASE,PIO_EDGE_CAPTURE_REG,PB_START_STOP_MASK | PB_REST_MASK);

	// Reset the Display output of the
	displayValue(0);

	// Create the Semaphores as Binary (length =1)
	SemStartStop =xSemaphoreCreateBinary();
	SemReset=xSemaphoreCreateBinary();

	// Create the Stop Watch Task with a minimal Stack size
    xTaskCreate( TaskStopWatch, "Stop Watch Task", configMINIMAL_STACK_SIZE, NULL, STOPWATCH_TASK_PRIORITY, NULL );

    // Create the Toogling LED Task with a minimal Stack size
    xTaskCreate( TaskBlinking, "Blinking Task", configMINIMAL_STACK_SIZE, NULL, BLINKING_TASK_PRIORITY, NULL );

    // Staret the FreeRTOS scheduler
	vTaskStartScheduler();
    
	// This loop will never reached
	for( ;; );
}
/*-----------------------------------------------------------*/
void vApplicationStackOverflowHook( xTaskHandle *pxTask, signed char *pcTaskName )
{
	asm( "break" );
}

void vApplicationMallocFailedHook(void)
{
	asm( "break" );
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
