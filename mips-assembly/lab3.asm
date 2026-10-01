.data
	# Strings modified to match Python output exactly
	question: .asciiz "How many values do you want to enter? "
	max: .word 5
	max_error: .asciiz "5 is the maximum amount allowed\n"
	ask_value: .asciiz "Enter value "
	final_values: .asciiz "The values are "
	sum_text: .asciiz "The sum of even values is "
	colon: .asciiz ": "
	new_line: .asciiz "\n"
	space: .asciiz " "
	comma: .asciiz ","
	bracket_open: .asciiz "["
	bracket_close: .asciiz "]"

.text
.globl main

main:
	#initialize # of values to 6
	li $s1, 6
	
	#initialize even sum register $s2 to 0
	li $s2, 0
	
	#load the max allowed value into $t0
	lw $t0, max

ask_for_values_start:
	#check if user's input is greater than max ($t0)
	ble $s1, $t0, list_storage_start

	#ask the user how many values
	li $v0, 4
	la $a0, question
	syscall

	#read user's input
	li $v0, 5
	syscall

	#move the result ($v0) to $s1
	move $s1, $v0

	#check if user's input is greater than max ($t0)
	ble $s1, $t0, ask_for_values_start

	#load max_error
	li $v0, 4
	la $a0, max_error
	syscall
	
	#jump back to the appropriate prompt start
	j ask_for_values_start

list_storage_start:
	#check if the count is zero or negative
	blez $s1, list_storage_skip

	#calculate total memory needed ($s1 * 4 bytes/word)
	sll $a0, $s1, 2

	#setting up dynamic memory (sbrk syscall 9)
	li $v0, 9
	syscall

	#save the list start address in $s0
	move $s0, $v0

	#jump to list setup
	j list_setup_end

list_storage_skip:
	#set pointer to 0 if list is empty or negative
	li $s0, 0

list_setup_end:
	#set index $s3 to 0 (using saved register for safety)
	li $s3, 0
	
	#set pointer $s4 to the start of the list (using saved register for safety)
	move $s4, $s0

append_list_start:
	#check if index $s3 equals total count $s1
	bge $s3, $s1, even_sum_calc_start

	#print "enter value"
	li $v0, 4
	la $a0, ask_value
	syscall

	#print the current index + 1 (for 1-based display)
	addi $a0, $s3, 1
	li $v0, 1
	syscall

	#print the colon
	li $v0, 4
	la $a0, colon
	syscall

	#print a space
	li $v0, 4
	la $a0, space
	syscall

	#read user's input
	li $v0, 5
	syscall

	#move the successful result ($v0) to $t2
	move $t2, $v0

	#store the integer ($t2) at the current list pointer ($s4)
	sw $t2, 0($s4)

	#move pointer +4 bytes (next word address)
	addi $s4, $s4, 4
	
	#increment index +1
	addi $s3, $s3, 1
	
	#loop back to ask for the next value
	j append_list_start

even_sum_calc_start:
	#reset index $s3 to 0
	li $s3, 0

	#reset pointer $s4 to start ($s0)
	move $s4, $s0

check_even_loop:
	#exit if all numbers have been checked
	bge $s3, $s1, is_even_end

	#load the current number from array at $s4 into $t2
	lw $t2, 0($s4)

	#load 2 into $t3
	li $t3, 2

	#divide $t2 by 2
	div $t2, $t3

	#move the remainder (from hi register) to $t4
	mfhi $t4

	#check if remainder ($t4) is not equal to 0 (number is odd)
	bnez $t4, skip_add

	#add the even number ($t2) to sum ($s2)
	add $s2, $s2, $t2

skip_add:
	#move pointer +4 bytes
	addi $s4, $s4, 4

	#increment index +1
	addi $s3, $s3, 1

	#loop to check next number
	j check_even_loop

is_even_end:
	#reset index $s3 to 0
	li $s3, 0

	#reset pointer $s4 to start ($s0)
	move $s4, $s0

	#print the "the values are:" text
	li $v0, 4
	la $a0, final_values
	syscall

	#print the open bracket
	li $v0, 4
	la $a0, bracket_open
	syscall

print_loop:
	#exit if all numbers printed
	bge $s3, $s1, print_final

	#load the next number to print into $a0
	lw $a0, 0($s4)

	#print the number (syscall 1)
	li $v0, 1
	syscall

	#calculate next index to check if it's the last element
	addi $t5, $s3, 1
	
	#if next index equals total count, skip printing comma
	beq $t5, $s1, skip_comma

	#print comma
	li $v0, 4
	la $a0, comma
	syscall

	#print a space
	li $v0, 4
	la $a0, space
	syscall

skip_comma:
	#move pointer +4 bytes
	addi $s4, $s4, 4

	#increment index +1
	addi $s3, $s3, 1

	#loop to print next number
	j print_loop

print_final:
	#print the close bracket
	li $v0, 4
	la $a0, bracket_close
	syscall

	#print a newline
	li $v0, 4
	la $a0, new_line
	syscall

	#print the "the sum is:" text
	li $v0, 4
	la $a0, sum_text
	syscall

	#move the final sum from $s2 to $a0
	move $a0, $s2

	#print the sum (syscall 1)
	li $v0, 1
	syscall

	#print the final newline
	li $v0, 4
	la $a0, new_line
	syscall

	#exit the program
	li $v0, 10
	syscall