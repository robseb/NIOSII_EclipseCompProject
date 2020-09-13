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
// 			---       with the usage of the "socfpgaHAL" to interact  ----
//			---                    with HPS Hard-IP                   ----
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
//				This example demonstrates how a NIOS II soft-core processor  		     //
//						can interact with HPS Hard-IP modules							 //
//																					     //
//							===== Stop watch Task =====								     //
//				HPS_KEY: Start or Stop the up counting of the FPGA LED		     		 //
// 			7-Segment Display: To show the counting value in hexadecimal   		    	 //
//																						 //
//						    ==== Blinking Task ====									     //
//							Toggles the HPS_LED via the 							     //
//                           FPGA2HPS Bridge every 50ms 								 //
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
//							 ====  FPGA-to-HPS Bridge interface  ===				     //
//							 Documentation with an example Quartus Prime Project:        //
//								 https://github.com/robseb/rsyocto						 //
//																						 //
///////////////////////////////////////////////////////////////////////////////////////////


//
// FreeRTOS includes
//
#include "system.h"
#include "FreeRTOS.h"
#include "task.h"
#include "semphr.h"

// FPGA soft platform includes
#include "system.h"

//
// NIOS II HAL includes
//
#include <sys/alt_irq.h>
#include "io.h"

//
// socfpgaHAL include for
// interacting with Hard-IP
//
#include "socfpgaHAL.h"

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
	#define BCONF_EN_LEDDISP_LEN   254   // Largest displayable on the LED bin Display
	#define BCONF_MAX_COUNT_VALUE  254   // Max value to count for the stop watch counter
	#define BCONF_COUNT_DELAY	   100  // Delay between every stop watch count in ms
	#define BCONF_COUNT_ADD		     1   // Value to add to the count value after single delay
	#define BCONF_START_PBNO		 0   // Number of the Start/Stop push buttons
	#define BCONF_REST_PBNO		     1   // Number of the Reset push buttons

	#define BCONF_EN_TOGLE_LED	     1   // Enable the 50ms toggle LED task

#elif SELCTED_BOARD == TERASIC_DE10_NANO
	#define BCONF_EN_SEVSIG    	     0   // Enable the 7sig Display
	#define BCONF_EN_SEVSIG_LEN      0   // Largest displayable number on 7sig Display
	#define BCONF_EN_LEDDISP         1   // Enable the LED bin Display
	#define BCONF_EN_LEDDISP_LEN   254   // Largest displayable on the LED bin Display
	#define BCONF_MAX_COUNT_VALUE  254   // Max value to count for the stop watch counter
	#define BCONF_COUNT_DELAY	   100   // Delay between every stop watch count in ms
	#define BCONF_COUNT_ADD			 1   // Value to add to the count value after single delay
	#define BCONF_START_PBNO		 0   // Number of the Start/Stop push buttons
	#define BCONF_REST_PBNO		     1   // Number of the Reset push buttons

	#define BCONF_EN_TOGLE_LED	     1   // Enable the 50ms toggle LED task

#elif SELCTED_BOARD == TERASIC_DE10_STD
	#define BCONF_EN_SEVSIG    	      1   // Enable the 7sig Display
	#define BCONF_EN_SEVSIG_LEN   16777215// Largest displayable number on 7sig Display
	#define BCONF_EN_LEDDISP          0   // Enable the LED bin Display
	#define BCONF_EN_LEDDISP_LEN    511   // Largest displayable on the LED bin Display
	#define BCONF_MAX_COUNT_VALUE 65535   // Max value to count for the stop watch counter
	#define BCONF_COUNT_DELAY		 10   // Delay between every stop watch count in ms
	#define BCONF_COUNT_ADD		     10   // Value to add to the count value after single delay
	#define BCONF_START_PBNO		  0   // Number of the Start/Stop push buttons
	#define BCONF_REST_PBNO		      1   // Number of the Reset push buttons

	#define BCONF_EN_TOGLE_LED	      1   // Enable the 50ms toggle LED task

#elif SELCTED_BOARD == TERASIC_HAN_PILOT
	#define BCONF_EN_SEVSIG    	      1   // Enable the 7sig Display
	#define BCONF_EN_SEVSIG_LEN     255   // Largest displayable number on 7sig Display
	#define BCONF_EN_LEDDISP          0   // Enable the LED bin Display
	#define BCONF_EN_LEDDISP_LEN      0   // Largest displayable on the LED bin Display
	#define BCONF_MAX_COUNT_VALUE   255   // Max value to count for the stop watch counter
	#define BCONF_COUNT_DELAY	   1000   // Delay between every stop watch count in ms
	#define BCONF_COUNT_ADD		      1   // Value to add to the count value after single delay
    #define BCONF_START_PBNO		  0   // Number of the Start/Stop push buttons
	#define BCONF_REST_PBNO		      1   // Number of the Reset push buttons

	#define BCONF_EN_TOGLE_LED	      1   // Enable the 50ms toggle LED task

#elif SELCTED_BOARD == CUSTOM_BOARD
	#define BCONF_EN_SEVSIG    	      ()   // Enable the 7sig Display
	#define BCONF_EN_SEVSIG_LEN       ()   // Largest displayable number on 7sig Display
	#define BCONF_EN_LEDDISP          ()   // Enable the LED bin Display
	#define BCONF_EN_LEDDISP_LEN      ()   // Largest displayable on the LED bin Display
	#define BCONF_MAX_COUNT_VALUE     ()   // Max value to count for the stop watch counter
	#define BCONF_COUNT_DELAY		  ()   // Delay between every stop watch count in ms
	#define BCONF_COUNT_ADD		      ()   // Value to add to the count value after single delay
    #define BCONF_START_PBNO		  ()   // Number of the Start/Stop push buttons
	#define BCONF_REST_PBNO		      ()   // Number of the Reset push buttons

	#define BCONF_EN_TOGLE_LED	      ()   // Enable the 50ms toggle LED task
#endif


///////////////////////////////////////////////////////////////////////////////////////////
///																						 //
///								FREERTOS TASKS DEFINITIONS		 						 //
///																						 //
///////////////////////////////////////////////////////////////////////////////////////////

#define LEDCOUNTER_TASK_PRIORITY		( tskIDLE_PRIORITY + 2 ) // LED counter task (higher priority)
#if BCONF_EN_TOGLE_LED == 1
	#define BLINKING_TASK_PRIORITY		( tskIDLE_PRIORITY + 1 ) // Blinking HPS_LED
#endif

///////////////////////////////////////////////////////////////////////////////////////////

SemaphoreHandle_t SemStartStop; // Semaphore to signal that the HPS_KEY push button was pressed

// FPGA LED counter task function
static void TaskLEDcounter( void);

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

/*! \brief NIOS II exception hook handler
 */
void _general_exception_handler( unsigned long ulCause, unsigned long ulStatus )
{
	// This overrides the definition provided by the kernel. Other exceptions
	// should be handled here.
	APP_ASSERT(0);
}

// Prototype of the Interrupt handler
static void hps_key_exti_irq(void *context, alt_u32 id) __attribute__ ((section (".exceptions")));

//
// Terasic DE10 Boards HPS LED and HPS Push-button Pin assignment
//
//	Signal	|	HPS GPIO	|	Register	| socfpgaHAL Port	|	socfpgaHAL Pin
//	-------------------------------------------------------------------------------
//	HPS_LED |	 GPIO53		|	GPIO1[24]	|	GPIOB		    |	24
//	HPS_KEY |	 GPIO54		|	GPIO1[25]	|	GPIOB		    |	25
//
//

// GPIO assignment for HPS_LED
#define DEMO_LED_PORT SOC_GPIO_PORTB
#define DEMO_LED_PIN 24

// GPIO assignment for HPS_KEY
#define DEMO_KEY_PORT SOC_GPIO_PORTB
#define DEMO_KEY_PIN 25
#define DEMO_KEY_ISR_NO 4 // NIOS II interrupt input number (given by the platform designer)

/*
 * Main function
 */
int main( void )
{
	///// Configure the HPS_LED GPIO Pin as output and the HPS_KEY GPIO Pin as input ///
	soc_gpio_config_t hps_led_conf, hps_key_conf;  	     // GPIO configuration structure
	// for the HPS_LED
	hps_led_conf.port= DEMO_LED_PORT;			  	     // Name of the GPIO Module
	hps_led_conf.pin_mask=(1<<DEMO_LED_PIN);       	     // Bit mask of the pins to configure
	hps_led_conf.pin_dir= SOC_GPIO_PIN_OUTPUT;     	     // Pin direction of pins to configure -> output
	hps_led_conf.pin_pol=SOC_GPIO_PIN_ACTIVE_HIGH;       // Polarity of the pins to configure -> high
	hps_led_conf.pin_output_val=(1<<DEMO_LED_PIN);       // Init state of GPIO pins after configuration
	// for the HPS_KEY
	hps_key_conf.port= DEMO_KEY_PORT;				     // Name of the GPIO Module
	hps_key_conf.pin_mask=(1<<DEMO_KEY_PIN);		     // Bit mask of the pins to configure
	hps_key_conf.pin_dir= SOC_GPIO_PIN_INPUT;        	 // Pin direction of pins to configure <- input
	hps_key_conf.pin_pol=SOC_GPIO_PIN_ACTIVE_LOW;        // Polarity of the pins to configure <- low
	hps_key_conf.pin_deb = SOC_GPIO_PIN_DEBOUNCE;    	 // hardware debounce the pins
	hps_key_conf.isr_type= SOC_GPIO_ISR_EDGE_TRIGGERED;  // Interrupt trigger event -> Edge
	hps_key_conf.isr_mask=(1<<DEMO_KEY_PIN);		     // Interrupt mask to select the pins that should be triggered an interrupt

	// Initialization of the three GPIO controllers
	// Releasing controllers from reset
	soc_gpio_init();

	// Configuration of the HPS_LED Pin with the configuration structure
	soc_gpio_configPort(&hps_led_conf);

	// Configuration of the HPS_KEY Pin with the configuration structure
	soc_gpio_configPort(&hps_key_conf);

	// The entire GPIO configuration is actually not required: the u-boot bootloader will do it during the boot of the HPS
	// The u-boot bootloader was designed with the settings of the HPS module inside Quartus Prime Platform designer
	// Configure the HPS_KEY interrupt
	// Only the GPIO EXTI interrupt configuration is necessary

	// Configure the HPS_KEY pin as EXTI interrupt line
	soc_gpio_ISRconfig(&hps_key_conf);

	// Register and enable the HPS_KEY interrupt
	APP_ASSERT(!(-EINVAL == alt_irq_register( (alt_u32) DEMO_KEY_ISR_NO,	 // Number of the Interrupt line
											  (alt_u32) 0x0,        		 // Interrupt handler handling over -> none
											  hps_key_exti_irq )));          // Reference to the interrupt service routine (ISR)

	// Reset the LED- and 7Segment display value
	displayValue(0);

	// Create the binary Semaphores for the HPS_KEY event triggered (length =1)
	SemStartStop =xSemaphoreCreateBinary();

	// Create the FPGA LED counter started/stopped by the HPS_KEY
    xTaskCreate(
    			(TaskFunction_t) TaskLEDcounter, // Reference to task function
				"LED Counter Task",			    // Debugging ASCI name
				configMINIMAL_STACK_SIZE,		// Stack size of task      -> minimal possible
				(void*) NULL,                   // Handing over parameters -> none
				LEDCOUNTER_TASK_PRIORITY,       // Priority of the task
				(void*)  NULL );			 	// Reference to task handler to start,stop... task -> disabled


#if BCONF_EN_TOGLE_LED == 1
    // Create the Toggling of the HPS_LED Task with a minimal Stack size
    xTaskCreate(
    			(TaskFunction_t) TaskBlinking,  // Reference to task function
				"Blinking HPS Task",			// Debugging ASCI name
				configMINIMAL_STACK_SIZE,       // Stack size of task      -> minimal possible
				(void*) NULL,					// Handing over parameters -> none
				BLINKING_TASK_PRIORITY,			// Priority of the task
				(void*) NULL );                 // Reference to task handler to start,stop... task -> disabled
#endif

    // Enable the HPS_KEY interrupt
    soc_gpio_ISRenable(DEMO_KEY_PORT,(1<<DEMO_KEY_PIN),true);

    // Start the FreeRTOS scheduler
	vTaskStartScheduler();
    
	// This loop will never reached
	for( ;; );
}

/*! \brief FPGA LED counter task
 *         triggered by the HPS_KEY
 *  \note FreeRTOS Task
 */
static void TaskLEDcounter(void )
{
	// Reset the LED counter value
	uint32_t countValue=0;

	// States of the task
	typedef enum{
		STOPPED=0,
		RUNNING=1
	}ledCounterStatus_t;

	// Create a current status value
	ledCounterStatus_t cur_status = STOPPED;

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
		 *  waiting for:	  HPS_KEY pressed
		 */
		case STOPPED:
			// Reset the Display and count value
			countValue =0;
			displayValue(countValue);

			// Put task to sleep until the Start/Stop semaphore is set
			// --> signals that the HPS_KEY push button was pressed
			// portMAX_DELAY: wait for ever (without a timeout)
			xSemaphoreTake(SemStartStop,portMAX_DELAY);

			// HPS_KEY push button was pressed -> switch state to RUNNING
			cur_status = RUNNING;
			break;
		/*
		 * --- State RUNNING ---
		 * 	Stop watch running:  YES
		 * 	Stop watch display:  <countValue>
		 *  waiting for:	   HPS_KEY pressed or counting overflow
		 */
		case RUNNING:
			// Check if the Start/Stop semaphore is set
			// -> signals that the HPS_KEY push button was pressed again
			// 0: zero wait time -> do not call the scheduler and put the task to sleep
			// 	  instead of --> immediately check if the status is pdTRUE -> semaphore is set
			if(xSemaphoreTake(SemStartStop,0)==pdTRUE)
			{
				// Start/Stop semaphore is set -> switch the status to STOPPED
				cur_status = STOPPED;
			}
			else
			{
				// Start/Stop semaphore is not set

				// Count the stop watch up and display the value
				displayValue(countValue+=BCONF_COUNT_ADD);

				// Put the task for BCONF_COUNT_DELAY ms to sleep
				// portTICK_RATE_MS -> const to convert ms to systicks
				// here: tick rate -> 1 tick per ms -> portTICK_RATE_MS = 1
				vTaskDelay((TickType_t) BCONF_COUNT_DELAY/portTICK_RATE_MS);

				// Check if the count value reached its maximum
				if(countValue == BCONF_MAX_COUNT_VALUE)
				{
					// Limit reached -> switch the status to STOPPED
					cur_status = STOPPED;
				}
			}
			break;
		}
    }
}
#if BCONF_EN_TOGLE_LED == 1
	/*! \brief Blinking LED (HPS_LED) Task
	 *  \note FreeRTOS Task
	 */
	void TaskBlinking (void)
	{
		// Enter infinity loop
		for( ;; )
		{
			// Toggle the HPS_LED
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
	/*! \brief Toggle the HPS_LED via the FPGA2HPS Bridge
	 */
	void blinkLED(void)
	{
		static uint8_t blink =1;
		blink = !blink;
		if(blink)
		{
			// Turn the HPS_LED on
			soc_gpio_set(DEMO_LED_PORT,(1<<DEMO_LED_PIN));
		}
		else
		{
			// Turn the HPS_LED off
			soc_gpio_clear(DEMO_LED_PORT,(1<<DEMO_LED_PIN));
		}
	}
#endif


/*! \brief external (EXTI) push button interrupt handler
 *         Will be triggered in case the HPS_KEY is pressed
 *  \note: Interrupt service routine (ISR)
 */
static void hps_key_exti_irq(void *context, alt_u32 id)
{
	// Clear the ISR and stop it
	soc_gpio_ISRenable(DEMO_KEY_PORT,(1<<DEMO_KEY_PIN),false);

	// The StartStop key (HPS_KEY) was pressed -> load the semaphore
	// to signal this event to the FreeRTOS task
	xSemaphoreGiveFromISR(SemStartStop,NULL);

	// Enable the external HPS_ISR again
	soc_gpio_ISRenable(DEMO_KEY_PORT,(1<<DEMO_KEY_PIN),true);
}


#ifdef __cplusplus
}
#endif
