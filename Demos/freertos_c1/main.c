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
// 			designed by Robin Sebastian (https://github.com/robseb) 
//									git@robseb.de
//
//

// Compile as C Code
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

	
#include "system.h"
//
// NIOS II HAL includes
//
#include <sys/alt_irq.h>
#include "io.h"

// Application assert macro to stop the debugging process in case of an error
#define APP_ASSERT(x) 								\
						if(x==0) {asm( "break" );	\
								  while(1); }

// Reference to the FreeRTOS capable function to register an interrupt service routine (port.c)
extern int alt_irq_register( alt_u32 id, void* context, void (*handler)(void*, alt_u32) );

///////////////////////////////////////////////////////////////////////////////////////////
///																						 //
///								DEVELOPMENT BOARD CONFIGURATION 						 //
///																						 //
///////////////////////////////////////////////////////////////////////////////////////////

#define TERASIC_DE0_NANO    1  // Terasic DE0  NANO Board with an Intel Cyclone IV FPGA
#define TERASIC_DE10_STD    2  // Terasic DE10 STANDARD Board with an Intel Cyclone V SoC-FPGA
#define TERASIC_DE10_NANO   3  // Terasic DE10 NANO Board with an Intel Cyclone V SoC-FPGA
#define TERASIC_HAN_PILOT   4  // Terasic HAN PILOT Board with an Intel Arria 10 SoC-FPGA
#define CUSTOM_BOARD	    0  // Custom board with a custom board configuration
#define UNKOWN_BOARD	   -1

/////
///////////////////
// TODO: Select your development board
#define SELCTED_BOARD UNKOWN_BOARD
///////////////////
/////

#if SELCTED_BOARD == UNKOWN_BOARD
	#error "Please select your development board!"
#elif SELCTED_BOARD == TERASIC_DE0_NANO
	#define BCONF_EN_SEVSIG    	     0   // Enable the 7sig Display
	#define BCONF_EN_SEVSIG_LEN      0   // Largest displayable number on 7sig Display
	#define BCONF_EN_LEDDISP         1   // Enable the LED bin Display
	#define BCONF_EN_LEDDISP_LEN   126   // Largest displayable on the LED bin Display
	#define BCONF_MAX_COUNT_VALUE  126   // Max value to count for the stop watch counter
	#define BCONF_COUNT_DELAY	   100   // Delay between every stop watch count in ms
	#define BCONF_START_PBNO		 0   // Number of the Start/Stop push button
	#define BCONF_REST_PBNO		     1   // Number of the Reset push button

	#define BCONF_EN_TOGLE_LED	     1   // Enable the 50ms toggle LED task
	#define BCONF_TOOGLE_LED_NO	     8   // LED number of the toggle LED

#elif SELCTED_BOARD == TERASIC_DE0_NANO
	#define BCONF_EN_SEVSIG    	     0   // Enable the 7sig Display
	#define BCONF_EN_SEVSIG_LEN      0   // Largest displayable number on 7sig Display
	#define BCONF_EN_LEDDISP         1   // Enable the LED bin Display
	#define BCONF_EN_LEDDISP_LEN   512   // Largest displayable on the LED bin Display
	#define BCONF_MAX_COUNT_VALUE  511   // Max value to count for the stop watch counter
	#define BCONF_COUNT_DELAY	   100   // Delay between every stop watch count in ms
	#define BCONF_START_PBNO		 0   // Number of the Start/Stop push button
	#define BCONF_REST_PBNO		     1   // Number of the Reset push button

	#define BCONF_EN_TOGLE_LED	     1   // Enable the 50ms toggle LED task
	#define BCONF_TOOGLE_LED_NO	     9   // LED number of the toggle LED

#elif SELCTED_BOARD == TERASIC_DE10_STD
	#define BCONF_EN_SEVSIG    	      1   // Enable the 7sig Display
	#define BCONF_EN_SEVSIG_LEN   16777215// Largest displayable number on 7sig Display
	#define BCONF_EN_LEDDISP          0   // Enable the LED bin Display
	#define BCONF_EN_LEDDISP_LEN    511   // Largest displayable on the LED bin Display
	#define BCONF_MAX_COUNT_VALUE 65535   // Max value to count for the stop watch counter
	#define BCONF_COUNT_DELAY		 10   // Delay between every stop watch count in ms
	#define BCONF_START_PBNO		  0   // Number of the Start/Stop push button
	#define BCONF_REST_PBNO		      1   // Number of the Reset push button

	#define BCONF_EN_TOGLE_LED	      1   // Enable the 50ms toggle LED task
	#define BCONF_TOOGLE_LED_NO	      9   // LED number of the toggle LED

#elif SELCTED_BOARD == TERASIC_HAN_PILOT
	#define BCONF_EN_SEVSIG    	      1   // Enable the 7sig Display
	#define BCONF_EN_SEVSIG_LEN     255   // Largest displayable number on 7sig Display
	#define BCONF_EN_LEDDISP          0   // Enable the LED bin Display
	#define BCONF_EN_LEDDISP_LEN      0   // Largest displayable on the LED bin Display
	#define BCONF_MAX_COUNT_VALUE   255   // Max value to count for the stop watch counter
	#define BCONF_COUNT_DELAY		100   // Delay between every stop watch count in ms
    #define BCONF_START_PBNO		  0   // Number of the Start/Stop push button
	#define BCONF_REST_PBNO		      1   // Number of the Reset push button

	#define BCONF_EN_TOGLE_LED	      1   // Enable the 50ms toggle LED task
	#define BCONF_TOOGLE_LED_NO	      0   // LED number of the toggle LED

#elif SELCTED_BOARD == CUSTOM_BOARD
	#define BCONF_EN_SEVSIG    	      ()   // Enable the 7sig Display
	#define BCONF_EN_SEVSIG_LEN       ()   // Largest displayable number on 7sig Display
	#define BCONF_EN_LEDDISP          ()   // Enable the LED bin Display
	#define BCONF_EN_LEDDISP_LEN      ()   // Largest displayable on the LED bin Display
	#define BCONF_MAX_COUNT_VALUE     ()   // Max value to count for the stop watch counter
	#define BCONF_COUNT_DELAY		  ()   // Delay between every stop watch count in ms
    #define BCONF_START_PBNO		  ()   // Number of the Start/Stop push button
	#define BCONF_REST_PBNO		      ()   // Number of the Reset push button

	#define BCONF_EN_TOGLE_LED	      ()   // Enable the 50ms toggle LED task
	#define BCONF_TOOGLE_LED_NO	      ()   // LED number of the toggle LED
#endif


///////////////////////////////////////////////////////////////////////////////////////////
///																						 //
///								FREERTOS TASKS DEFINITIONS		 						 //
///																						 //
///////////////////////////////////////////////////////////////////////////////////////////

#define STOPWATCH_TASK_PRIORITY		   ( tskIDLE_PRIORITY + 2 ) // Stop watch with 2 key inputs (higher priority)
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


void displayValue(uint32_t val);
void blinkLED(void);


///////////////////////////////////////////////////////////////////////////////////////////
///																						 //
///									FreeRTOS HOOKS      		 						 //
///																						 //
///////////////////////////////////////////////////////////////////////////////////////////

/*! \brief FreeRTOS application Stack Overflow hook handler
 */
void vApplicationStackOverflowHook( xTaskHandle *pxTask, signed char *pcTaskName )
{
	// Triggered in case a task runs out of stack space  -> stop the debugging progress
	APP_ASSERT(0);
}

/*! \brief FreeRTOS dynamic memory allocation hook handler
 */
void vApplicationMallocFailedHook(void)
{
	// Triggered in case dynamic memory allocation failed  -> stop the debugging progress
	APP_ASSERT(0);
}

/*! \brief NIOS II exception handler hook handler
 */
void _general_exception_handler( unsigned long ulCause, unsigned long ulStatus )
{
	// This overrides the definition provided by the kernel. Other exceptions
	// should be handled here.
	APP_ASSERT(0);
}

// Prototype of the Interrupt handler
static void pb_exti_irq(void *context, alt_u32 id) __attribute__ ((section (".exceptions")));

/*
 * Main function
 */
int main( void )
{
	// Register and enable the external GPIO interrupt for the Start/Stop- and Reset buttons
	APP_ASSERT(!(-EINVAL == alt_irq_register( (alt_u32) PB_PIO_IRQ, // Name of the Interrupt line
											  (alt_u32) 0x0,        // Interrupt handler handling over -> none
											  pb_exti_irq )));      // Reference to the interrupt service routine (ISR)

	// Enable the external GPIO interrupt Start/Stop- and Reset buttons
	IOWR_32DIRECT(PB_PIO_BASE,PIO_INTERUPT_MASK_REG,PB_START_STOP_MASK | PB_REST_MASK);
	// Enable the edge detection for Start/Stop- and Reset buttons
	IOWR_32DIRECT(PB_PIO_BASE,PIO_EDGE_CAPTURE_REG,PB_START_STOP_MASK | PB_REST_MASK);

	// Reset the Display output of the LED binary- and 7segment display
	displayValue(0);

	// Create the binary Semaphores for both stop watch buttons (length =1)
	SemStartStop =xSemaphoreCreateBinary();
	SemReset=xSemaphoreCreateBinary();

	// Create the Stop Watch Task with a minimal Stack size
    xTaskCreate(
    			(TaskFunction_t) TaskStopWatch, // Reference to task function
				"Stop Watch Task",			    // Debugging ASCI name
				configMINIMAL_STACK_SIZE,		// Stack size of task      -> minimal possible
				(void*) NULL,                   // Handing over parameters -> none
				STOPWATCH_TASK_PRIORITY,        // Priority of the task
				(void*)  NULL );			 	// Reference to task handler to start,stop... task -> disabled


#if BCONF_EN_TOGLE_LED == 1
    // Create the Toggling LED Task with a minimal Stack size
    xTaskCreate(
    			(TaskFunction_t) TaskBlinking,  // Reference to task function
				"Blinking Task",			    // Debugging ASCI name
				configMINIMAL_STACK_SIZE,       // Stack size of task      -> minimal possible
				(void*) NULL,					// Handing over parameters -> none
				BLINKING_TASK_PRIORITY,			// Priority of the task
				(void*) NULL );                 // Reference to task handler to start,stop... task -> disabled
#endif
    // Start the FreeRTOS scheduler
	vTaskStartScheduler();
    
	// This loop will never reached
	for( ;; );
}

/*! \brief Stop Watch Task
 *  \note FreeRTOS Task
 */
static void TaskStopWatch(void )
{
	// Stop watch count value
	uint32_t countValue=0;

	// States of Stop watch
	typedef enum{
		RESETED=0,
		STOPED=1,
		RUNNING=2
	}stopWachStatus_t;

	// Create a current status value
	stopWachStatus_t cur_status = RESETED;

	// Enter infinity loop
	for( ;; )
    {
		// State machine for every state
		switch(cur_status)
		{
		/*
		 * --- State RESETED ---
		 * 	Stop watch running:  NO
		 * 	Stop watch display:  0 <Reset>
		 *  waiting for:	   Start/Stop-Button pressed
		 */
		case RESETED:
			// Reset the Display and count value
			countValue =0;
			displayValue(countValue);

			// Put task to sleep until the Start/Stop semaphore is set
			// --> signals that the Start/Stop push button was pressed
			// portMAX_DELAY: wait for ever (without a timeout)
			xSemaphoreTake(SemStartStop,portMAX_DELAY);

			// Start/Stop push button was pressed -> switch state to RUNNING
			cur_status = RUNNING;
			break;
		/*
		 * --- State RUNNING ---
		 * 	Stop watch running:  YES
		 * 	Stop watch display:  <countValue>
		 *  waiting for:	   Start/Stop-Button pressed or counting overflow
		 */
		case RUNNING:
			// Check if the Start/Stop semaphore is set
			// -> signals that the Start/Stop push button was pressed again
			// 0: zero wait time -> do not call the scheduler and put the task to sleep
			// 	  instead is immediately check if the status is pdTRUE -> semaphore is set
			if(xSemaphoreTake(SemStartStop,0)==pdTRUE)
			{
				// Start/Stop semaphore is set -> switch the status to STOPED
				cur_status = STOPED;
			}
			else
			{
				// Start/Stop semaphore is not set

				// Count the stop watch up and display the value
				displayValue(countValue+=BCONF_COUNT_DELAY);

				// Put the task for BCONF_COUNT_DELAY ms to sleep
				// portTICK_RATE_MS -> const to convert ms to systicks
				// here: tick rate -> 1 tick per ms -> portTICK_RATE_MS = 1
				vTaskDelay((TickType_t) BCONF_COUNT_DELAY/portTICK_RATE_MS);

				// Check if the count value reached its maximum
				if(countValue == BCONF_MAX_COUNT_VALUE)
				{
					// Limit reached -> switch the status to STOPED
					cur_status = STOPED;
				}
			}
			break;
		/*
		 * --- State STOPED ---
		 * 	Stop watch running:  NO
		 * 	Stop watch display:  <countValue>
		 *  waiting for:	   Reset-Button pressed
		 */
		case STOPED:

			// Put task to sleep until the Reset button semaphore is set
			// --> signals that the Reset push button was pressed
			// portMAX_DELAY: wait forever (without a timeout)
			xSemaphoreTake(SemReset,portMAX_DELAY);
			// the Reset button semaphore is set -> switch the status to RESETED
			cur_status = RESETED;
			break;
		}
    }
}
#if BCONF_EN_TOGLE_LED == 1
	/*! \brief Blinking LED Task
	 *  \note FreeRTOS Task
	 */
	static void TaskBlinking (void)
	{
		// Enter infinity loop
		for( ;; )
		{
			// Toggle a LED
			blinkLED();

			// Put the task for 100ms to sleep
			// portTICK_RATE_MS -> const to convert ms to systicks
			// here: tick rate -> 1 tick per ms -> portTICK_RATE_MS = 1
			vTaskDelay((TickType_t) 100/portTICK_RATE_MS);
		}
	}
#endif

/*! \brief Display a Value on the 7sig-Display and as LED binary
 *  \param val the value to display
 */
void displayValue(uint32_t val)
{
#if BCONF_EN_SEVSIG == 1
	// Write the value to the 7segment display
	IOWR_32DIRECT(DE10STD7SIG_BASE,0,val< BCONF_EN_SEVSIG_LEN ? val: BCONF_EN_SEVSIG_LEN);
#endif
#if BCONF_EN_LEDDISP == 1
	// Write the value to the binary LED display
	IOWR_32DIRECT(LED_PIO_BASE,0,val< BCONF_EN_LEDDISP_LEN ? val :BCONF_EN_LEDDISP_LEN);
#endif
}

#if BCONF_EN_TOGLE_LED == 1
	/*! \brief Toggle a LED
	 */
	void blinkLED(void)
	{
		static uint8_t blink =1;
		blink = !blink;
		uint32_t led = IORD_32DIRECT(LED_PIO_BASE,0);
		IOWR_32DIRECT(LED_PIO_BASE,0,blink ? led| (1<<BCONF_TOOGLE_LED_NO): led& ~(1<<BCONF_TOOGLE_LED_NO));
	}
#endif

/*! \brief external (EXTI) push button interrupt handler
 *  \note: Interrupt service routine (ISR)
 */
static void pb_exti_irq(void *context, alt_u32 id)
{
	// Check witch key was pressed
	uint32_t key = (~IORD_32DIRECT(PB_PIO_BASE,PIO_DATA_REG)) & (PB_START_STOP_MASK | PB_REST_MASK);
	if( key== 1)
	{
		// The Start/Stop key was pressed -> load the semaphore
		xSemaphoreGiveFromISR(SemStartStop,NULL);
		// take other Semaphore to avoid multiple push button inputs
		xSemaphoreTakeFromISR(SemReset,NULL);
	}
	else if( key== 2)
	{
		// The Reset key was pressed
		xSemaphoreGiveFromISR(SemReset,NULL);
		// take other Semaphore to avoid multiple push button inputs
		xSemaphoreTakeFromISR(SemStartStop,NULL);
	}

	// Clear the Timer ISR Flag

	// Enable the external GPIO interrupt Start/Stop- and Reset buttons
	IOWR_32DIRECT(PB_PIO_BASE,PIO_INTERUPT_MASK_REG,PB_START_STOP_MASK | PB_REST_MASK);
	IOWR_32DIRECT(PB_PIO_BASE,PIO_EDGE_CAPTURE_REG,PB_START_STOP_MASK | PB_REST_MASK);
}


#ifdef __cplusplus
}
#endif
