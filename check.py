
def output_val(val_non_faulty, val_faulty):
    return{
        '00':'0',
        '01':'D',
        '0x':'x',
        '10':'D_bar',
        '11':'1',
        '1x':'x',
        'x0':'x',
        'x1':'x',
        'xx':'x',
          
		}[val_non_faulty + val_faulty]
		
	
	
def non_faulty(a):
        return{
            '0':'0',
            '1':'1',
            'x':'x',
            'D':'0',
            'D_bar':'1'
            }[a]
               
def faulty(a):
	return{
		'0':'0',
		'1':'1',
		'x':'x',
		'D':'1',
		'D_bar':'0'
		}[a]

	
def and_gate(a, b):
	a_non_faulty = non_faulty(a)
	b_non_faulty = non_faulty(b)
	val_non_faulty = and_three_valued(a_non_faulty, b_non_faulty)
	a_faulty = faulty(a)
	b_faulty = faulty(b)
	val_faulty = and_three_valued(a_faulty, b_faulty)
	return output_val(val_non_faulty, val_faulty)
