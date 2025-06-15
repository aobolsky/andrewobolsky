TITLE Project 6     (Proj6_obolskya.asm)

; Author: Andrew Obolsky
; Last Modified: 06/08/2025
; OSU email address obolskya@oregonstate.edu
; Course number/section:   CS271 Section 400
; Project Number:  6               Due Date: 06/08/2025
;  Description: This program reads a comma-delimited list of temperatures from a file,
;  parses them into signed integers using string primitives, and prints
;  them in reverse order, separated by the same delimiter.
; 
INCLUDE Irvine32.inc

; ================================
; Constants
; ================================
DELIMITER     = ','       ; character separating temperatures
MAX_BUFFER    = 500       ; size of file read buffer
MAX_TEMPS     = 100       ; maximum number of temperatures

; ================================
; Data Section
; ================================
.data
welcomeMsg    BYTE "Welcome to the CS271 Temperature Parser!",0
guideMsg      BYTE "Enter the name of the file to read: ",0
promptErr     BYTE "Error opening file.",0
inputFilename BYTE 20 DUP(?)           ; up to 19 chars + NULL
fileBuffer    BYTE MAX_BUFFER DUP(?)   ; raw file contents
tempArray     SDWORD MAX_TEMPS DUP(?)  ; parsed integers
newline       BYTE 0Dh,0Ah,0

; ================================
; Macros
; ================================
; --------------------------------------
; Macro: mGetString
; Prompt for and read a string into buffer.
; arg1 = address of prompt string
; arg2 = address of buffer
; arg3 = max buffer length
; arg4 = address to store count of chars read
; --------------------------------------
mGetString MACRO prompt, buffer, maxlen, countAddr
    LOCAL mGetDone
    PUSH EAX
    PUSH ECX
    PUSH EDX

    mov EDX, prompt
    call WriteString
    mov EDX, buffer
    mov ECX, maxlen
    call ReadString
    mov EAX, eax        ; EAX returns length
    mov [countAddr], EAX

    POP EDX
    POP ECX
    POP EAX
mGetDone:
ENDM

; --------------------------------------
; Macro: mDisplayString
; Display a null-terminated string.
; arg = address of string
; --------------------------------------
mDisplayString MACRO strAddr
    LOCAL mDispDone
    PUSH EAX
    PUSH EDX

    mov EDX, strAddr
    call WriteString

    POP EDX
    POP EAX
mDispDone:
ENDM

; --------------------------------------
; Macro: mDisplayChar
; Display a single ASCII character.
; arg = character value in DL
; --------------------------------------
mDisplayChar MACRO charVal
    LOCAL mCharDone
    PUSH EAX

    mov DL, charVal
    mov AH, 02h
    int 21h

    POP EAX
mCharDone:
ENDM

; ================================
; Code Section
; ================================
.code

; ------------------------------------------------------
; Procedure: main
; Description: Entry point. Manages I/O, calls parser
;              and printer. Uses stack-based params.
; Preconditions: Irvine32 available.
; Postconditions: Displays reversed temperatures.
; Registers changed: EAX, EBX, ECX, EDX
; ------------------------------------------------------
main PROC
    push EBP
    mov EBP, ESP

    ; Clear screen & greet
    call Clrscr
    mDisplayString welcomeMsg
    call Crlf

    ; Get filename
    mDisplayString guideMsg
    mGetString guideMsg, OFFSET inputFilename, 20, OFFSET bytesRead

    ; Open file
    mov EDX, OFFSET inputFilename
    call OpenInputFile
    cmp EAX, INVALID_HANDLE_VALUE
    je FileError
    mov EBX, EAX           ; file handle

    ; Read entire file into buffer
    mov EDX, OFFSET fileBuffer
    mov ECX, MAX_BUFFER
    mov EBX, EBX
    call ReadFromFile

    ; Close file
    mov EAX, EBX
    call CloseFile

    ; Parse temperatures
    push OFFSET tempCount
    push OFFSET tempArray
    push OFFSET fileBuffer
    call ParseTempsFromString

    ; Announce reversed output
    mDisplayString newline
    mDisplayString welcomeMsg    ; reuse or use a new message if desired
    call Crlf

    ; Print reversed temperatures
    push DELIMITER
    push tempCount
    push OFFSET tempArray
    call WriteTempsReverse

    call Crlf
    jmp Done

FileError:
    mDisplayString promptErr
    call Crlf

Done:
    call WaitMsg
    call ExitProcess,0

    mov ESP, EBP
    pop EBP
    ret
main ENDP

; ------------------------------------------------------
; Procedure: ParseTempsFromString
; Description: Parses signed SDWORDs from BYTE buffer.
; Parameters (stdcall):
;   [ESP+12] = offset of input BYTE buffer
;   [ESP+8]  = offset of SDWORD tempArray
;   [ESP+4]  = address to store tempCount
; Postconditions: tempArray filled, tempCount set.
; Registers changed: EAX, EBX, ECX, EDX, ESI, EDI
; ------------------------------------------------------
ParseTempsFromString PROC
    push EBP
    mov EBP, ESP
    pushad

    mov ESI, [EBP+12]  ; input buffer
    mov EDI, [EBP+8]   ; tempArray base
    mov EBX, 0         ; count

NextChar:
    lodsb
    cmp AL, 0
    je DoneParse
    cmp AL, ' '
    je NextChar

    mov EDX, 0
    cmp AL, '-'
    jne NoNeg
    mov EDX, 1
    lodsb

NoNeg:
    sub AL, '0'
    cmp AL, 9
    ja SkipChar
    mov ECX, EAX

ParseDigits:
    lodsb
    cmp AL, DELIMITER
    je StoreNum
    cmp AL, 0
    je StoreNum
    sub AL, '0'
    cmp AL, 9
    ja StoreNum
    imul ECX, 10
    add ECX, EAX
    jmp ParseDigits

StoreNum:
    cmp EDX, 0
    je Positive
    neg ECX

Positive:
    mov [EDI], ECX
    add EDI, 4
    inc EBX
    cmp EBX, MAX_TEMPS
    je DoneParse
    jmp NextChar

SkipChar:
    jmp NextChar

DoneParse:
    mov EAX, [EBP+4]  ; address of tempCount
    mov [EAX], EBX

    popad
    mov ESP, EBP
    pop EBP
    ret 12
ParseTempsFromString ENDP

; ------------------------------------------------------
; Procedure: WriteTempsReverse
; Description: Prints SDWORD array in reverse order.
; Parameters (stdcall):
;   [ESP+12] = offset of SDWORD array
;   [ESP+8]  = count of elements
;   [ESP+4]  = delimiter char
; Postconditions: Values displayed on console.
; Registers changed: EAX, ECX, EDX
; ------------------------------------------------------
WriteTempsReverse PROC
    push EBP
    mov EBP, ESP
    pushad

    mov ESI, [EBP+12]   ; array base
    mov ECX, [EBP+8]    ; count
    cmp ECX, 0
    je EndPrint
    dec ECX             ; last index

PrintLoop:
    mov EAX, [ESI + ECX*4]
    call WriteInt
    mov DL, BYTE PTR [EBP+4]
    mDisplayChar DL
    call Crlf
    dec ECX
    cmp ECX, -1
    jne PrintLoop

EndPrint:
    popad
    mov ESP, EBP
    pop EBP
    ret 12
WriteTempsReverse ENDP

END main





 
