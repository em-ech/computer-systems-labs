	#initalize list
	#initialize byte size
	#initialize even sum
	#initialize index
	#ask for number of variables
	#check if max?
	#set the space of the list depending on the number requested
	#ask for the number
	#append the list
	#check if even, and add to even sum
	#print list
	#print if even

.data
	question: .asciiz "How many values do you want to enter? "
	value: .asciiz "5 is the maximum allowed"
	ask_value .asciiz "What is the value? "
	max: .word 5
	sum_of_even: .word $zero
	

.text
.globl main

j main

main:
	
	ask_for_values_start
	#print the string
	li $v0, 4
	la $a0, <question>
	syscall
	
	#read the user's response
	li $v0, 5
   syscall

   # copy the result to the temp register
   move $t0, $v0 
   
   # move max value to temp value
   li $t1, max
   
   check_if_max_start
   	blt $t0, $t1, append_list_start
   
   	bigger_than_max
   	la $a0, <value>
   	syscall
   	j ask_for_values_start
   
	
	make_space_in_list_start
	#left shift multiplies by powers of two
	#so sll variable, variable, 2 multiplies by 4
	sll $a0, $t0, 2
	
	# allocating memory dynamically 
	#sbrk
	li $v0, 9
	syscall
	
	# $s0 first position
	move $s0, $v0	# $s0 = base address of list
	
	# start the count
	move $s1, $t0
	
	# index is 0
	li $t2, $zero
	
	append_list_start
	
	
	append_list_end
	
	is_it_even_start
	li variable, 2
	
	div variable, var_where_2_is_stored
	
	# if $hi (where remainder is stored) == zero
	beq $hi, zero, its_even_start
	
	
	its_even_start
	
	
	is_even_end
	


	# Gracefully finish the execution of the program with the "exit" syscall
	li $v0, 10
	syscall
