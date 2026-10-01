.data
	comma: .asciiz "," 
	blank: .asciiz " " # could print \n for new line
	
.text
	j main # jumping to main

	print_blank:
		li $v0, 4 # Prints an integer
		
		la $a0, comma
		syscall
		
		la $a0, blank
		syscall
		
		jr $ra
		
	main:
		li   $t0, 0	# Using t0 as my index
		li   $t1, 5	# Number of iterations

	start_loop:
		li   $v0, 1	# Print integer syscall
		move $a0, $t0	# Copy t0 into a0 for printing
		syscall

		jal print_blank

		addi $t0, $t0, 1	# t0 = t0 + 1
		blt  $t0, $t1, start_loop