;***************************
;                                                                              *
;    Filename:    Serial.asm
;    Autor: José Eduardo Morales					
;    Description: EJEMPLO de serial y ADC                                      *
;   El código convierte un valor del adc y lo guarda en el puerto b. A la vez
;   lo envía a través del TX. También recibe un dato y este lo muestra en el 
;   puerto d. Para ver funcionar ambos se puede colocar un jumper entre rx y tx
;***************************
#include "p16f887.inc"

; CONFIG1
; __config 0xE0F4
 __CONFIG _CONFIG1, _FOSC_INTRC_NOCLKOUT & _WDTE_OFF & _PWRTE_OFF & _MCLRE_OFF & _CP_OFF & _CPD_OFF & _BOREN_OFF & _IESO_OFF & _FCMEN_OFF & _LVP_OFF
; CONFIG2
; __config 0xFFFF
 __CONFIG _CONFIG2, _BOR4V_BOR40V & _WRT_OFF
;***************************
GPR_VAR        UDATA
W_TEMP         RES        1      ; w register for context saving (ACCESS)
STATUS_TEMP    RES        1      ; status used for context saving
LEIDO	       RES	  1
PROBAR1	       RES	  1
PROBAR2	       RES	  1
DELAY1	       RES        1
DELAY2	       RES        1
POT1	       RES	  1
POT2	       RES	  1
POT3	       RES	  1
POT3S	       RES	  1
POTCONT        RES	  1	       
POT4	       RES	  1
POT4S	       RES	  1
SERVO RES 1
;***************************
; Reset Vector
;***************************

RES_VECT  CODE    0x0000            ; processor reset vector
    GOTO    START                   ; go to beginning of program

ISR_VECT  CODE    0x0004
  
    PUSH:
    MOVWF W_TEMP
    SWAPF STATUS,W
    MOVWF STATUS_TEMP
  ISR:
    BCF INTCON, T0IF
    MOVLW .242
    MOVWF TMR0
    MOVLW .4
    ADDWF POTCONT,1
    MOVF POT3,0
    SUBWF   POTCONT,0
    BTFSC STATUS,C
    BCF PORTB,0
    BTFSS STATUS,C
    BSF PORTB,0
    
    MOVF POT4,0
    SUBWF   POTCONT,0
    BTFSC STATUS,C
    BCF PORTB,1
    BTFSS STATUS,C
    BSF PORTB,1
    
    
    
  POP:
    SWAPF STATUS_TEMP,W
    MOVWF STATUS
    SWAPF W_TEMP,F
    SWAPF W_TEMP,W
    RETFIE	
    
    
;***************************
; MAIN PROGRAM
;***************************

MAIN_PROG CODE                      ; let linker place main program

START
;***************************
    CALL    CONFIG_RELOJ		; RELOJ INTERNO DE 500KHz
    CALL    CONFIG_IO
    CALL    CONFIG_PWM
    CALL    CONFIG_TX_RX		; 10417hz
    CALL    CONFIG_ADC			; canal 0, fosc/8, adc on, justificado a la izquierda, Vref interno (0-5V)
    CALL    CONFIG_TMR0
    BANKSEL PORTA
    CLRF SERVO
;***************************
   
;***************************
; CICLO INFINITO
;***************************
LOOP:
    CALL    DELAY_50MS
    BSF	    ADCON0, GO		    ; EMPIEZA LA CONVERSIÓN
CHECK_AD:
    BTFSC   ADCON0, GO			; revisa que terminó la conversión
    GOTO    $-1
    BCF	    PIR1, ADIF			; borramos la bandera del adc
    MOVF    ADRESH, W
    MOVWF LEIDO

CHECK_RCIF:			    ; RECIBE EN RX y lo muestra en PORTD
    BTFSS   PIR1, RCIF
    GOTO    CHECK_TXIF
    MOVF    RCREG, W

    MOVWF   PROBAR1
    RRF	    PROBAR1, 0
    MOVWF   PROBAR2
    RRF	    PROBAR2,0
    ANDLW   B'00111111'
    MOVWF PROBAR2
    
    MOVF SERVO,0
    ADDWF PCL,1
    
    GOTO SERVO0
    GOTO SERVO1
    GOTO SERVO2
    GOTO SERVO3
    
CHECK_TXIF: 
    MOVF    LEIDO,W		    ; ENVÍA PORTB POR EL TX
    MOVWF   TXREG
   
    BTFSS   PIR1, TXIF
    GOTO    $-1
    

GOTO LOOP
    
    
SERVO0:
    INCF SERVO
    BSF ADCON0,2
    MOVF PROBAR2,0
    MOVWF CCPR1L
    GOTO CHECK_TXIF

SERVO1:
    INCF SERVO
    BSF ADCON0,3
    BCF ADCON0,2
    MOVF PROBAR2,0
    MOVWF CCPR2L
    BSF PORTB,2
    GOTO CHECK_TXIF

SERVO2:
    INCF SERVO
    BSF ADCON0,2
    MOVF PROBAR2,0
    MOVWF POT3
    GOTO CHECK_TXIF
    
SERVO3:
    CLRF SERVO
    BCF ADCON0,2
    BCF ADCON0,3
    MOVF PROBAR2,0
    MOVWF POT4
    GOTO CHECK_TXIF
    BCF PORTB,2
    GOTO LOOP
;***************************
;*************************** 
;***************************    
CONFIG_RELOJ
    BANKSEL TRISA
    
    BSF OSCCON, IRCF2
    BCF OSCCON, IRCF1
    BCF OSCCON, IRCF0		    ; FRECUECNIA DE 1MHz

    RETURN
 
 ;--------------------------------------------------------
CONFIG_TX_RX
    BANKSEL TXSTA
    BCF	    TXSTA, SYNC		    ; ASINCRÓNO
    BSF	    TXSTA, BRGH		    ; LOW SPEED
    BANKSEL BAUDCTL
    BSF	    BAUDCTL, BRG16	    ; 8 BITS BAURD RATE GENERATOR
    BANKSEL SPBRG
    MOVLW   .25	    
    MOVWF   SPBRG		    ; CARGAMOS EL VALOR DE BAUDRATE CALCULADO
    CLRF    SPBRGH
    BANKSEL RCSTA
    BSF	    RCSTA, SPEN		    ; HABILITAR SERIAL PORT
    BCF	    RCSTA, RX9		    ; SOLO MANEJAREMOS 8BITS DE DATOS
    BSF	    RCSTA, CREN		    ; HABILITAMOS LA RECEPCIÓN 
    BANKSEL TXSTA
    BSF	    TXSTA, TXEN		    ; HABILITO LA TRANSMISION
    
    BANKSEL PORTD
    CLRF    PORTD
    RETURN
;--------------------------------------
CONFIG_IO
    BANKSEL TRISA
    CLRF    TRISA
    CLRF    TRISB
    CLRF    TRISC
    CLRF    TRISD
    CLRF    TRISE
    BANKSEL ANSEL
    CLRF    ANSEL
    CLRF    ANSELH
    BANKSEL PORTA
    CLRF    PORTA
    CLRF    PORTB
    CLRF    PORTC
    CLRF    PORTD
    CLRF    PORTE
    RETURN    
;--------------------------------------
CONFIG_PWM
    MOVLW   D'255'
    MOVWF   PR2
    CLRF    CCPR1L
    MOVLW   B'00111100'
    MOVWF   CCP1CON
    CLRF    CCPR2L
    MOVLW   B'00001111'
    MOVWF   CCP2CON
    CLRF    PORTE
    CLRF    PORTC
    MOVLW   B'01000001'
    MOVWF   ADCON0
    BANKSEL PORTC
    MOVLW   B'00000110'
    MOVWF   T2CON
    RETURN 
;-----------------------------------------------
CONFIG_ADC
    BANKSEL PORTA
    BCF ADCON0, ADCS1 
    BSF ADCON0, ADCS0		; FOSC/8 RELOJ TAD
    
    BCF ADCON0, CHS3		; CH0
    BCF ADCON0, CHS2
    BCF ADCON0, CHS1
    BCF ADCON0, CHS0	
    BANKSEL TRISA
    BCF ADCON1, ADFM		; JUSTIFICACIÓN A LA IZQUIERDA
    BCF ADCON1, VCFG1		; VSS COMO REFERENCIA VREF-
    BCF ADCON1, VCFG0		; VDD COMO REFERENCIA VREF+
    BANKSEL PORTA
    BSF ADCON0, ADON		; ENCIENDO EL MÓDULO ADC
    
    BANKSEL TRISA
    BSF	    TRISA, RA0		; RA0 COMO ENTRADA
    BSF	    TRISA, RA1
    BSF	    TRISA, RA2
    BSF	    TRISA, RA3
    BANKSEL ANSEL
    BSF	    ANSEL, 0		; ANS0 COMO ENTRADA ANALÓGICA
    
    RETURN
;-----------------------------------------------
CONFIG_TMR0
    BSF STATUS, RP0
    BCF STATUS, RP1	    ; CAMBIAMOS AL BANCO 1
    
    BCF OPTION_REG, T0CS    ; SELECCIONAMOS TMR0 COMO TEMPORIZADOR
    BCF OPTION_REG, PSA	    ; ASIGNAMOS PRESCALER A TMR0
    
    BCF OPTION_REG, PS2
    BCF OPTION_REG, PS1
    BCF OPTION_REG, PS0	    ; PRESCALER DE 2
    
    BCF STATUS, RP0
    BCF STATUS, RP1	    ; CAMBIAMOS AL BANCO 0
    
    BSF  INTCON, GIE
    BSF  INTCON, T0IE
    BCF  INTCON, PEIE
    BCF INTCON, T0IF	    ; APAGO LA BANDERA DE INTERRUPCION DEL TMR0
    
    MOVLW .242
    MOVWF TMR0	
    RETURN
    
    
    
    
    
    
;------------------------------------------------
    
DELAY_50MS
    MOVLW   .2	    ; 1US 
    MOVWF   DELAY2
    CALL    DELAY_500US
    DECFSZ  DELAY2		    ;DECREMENTA CONT1
    GOTO    $-2			    ; IR A LA POSICION DEL PC - 1
    RETURN
    
DELAY_500US
    MOVLW   .250		    ; 1US 
    MOVWF   DELAY1	    
    DECFSZ  DELAY1		    ;DECREMENTA CONT1
    GOTO    $-1			    ; IR A LA POSICION DEL PC - 1
    RETURN

    
    END