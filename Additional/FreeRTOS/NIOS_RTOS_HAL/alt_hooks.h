#ifndef __ALT_HOOKS_H__
#define __ALT_HOOKS_H__

/******************************************************************************
*                                                                             *
* Edit by Robin Sebastian (https://github.com/robseb/)  to add support        *
* for FreeRTOS to the NIOS II Interupt controller (05-2020)                   *
*                                                                             *
******************************************************************************/
#ifndef ALT_ASM_SRC

#include "FreeRTOS.h"
#include "semphr.h"

/*
 * Semaphores used to protect the heap and environment
 */
extern xSemaphoreHandle alt_heapsem;
extern xSemaphoreHandle alt_envsem;

/*
 * Tick handler for FreeRTOS
 */
extern void vPortSysTickHandler(void);

/*
 * Thisheader provides definitions for the operating system hooks used by the HAL.
 */

#define ALT_OS_TIME_TICK	vPortSysTickHandler
#define ALT_OS_INIT()		alt_heapsem = xSemaphoreCreateRecursiveMutex();		\
							alt_envsem = xSemaphoreCreateRecursiveMutex();
#define ALT_OS_STOP()		vTaskEndScheduler();

#define ALT_OS_INT_ENTER()	
#define ALT_OS_INT_EXIT()	

#endif /* ALT_ASM_SRC */

/* These macros are used by the VIC funnel assembly code */
#define ALT_OS_INT_ENTER_ASM   
#define ALT_OS_INT_EXIT_ASM     

#endif /* __ALT_HOOKS_H__ */