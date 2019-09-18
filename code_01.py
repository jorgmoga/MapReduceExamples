
!rm -rf input output
!mkdir input

%%writefile input/transacciones.txt
1	1	1	300	a jumper
2	1	2	300	a jumper
3	1	2	300	a jumper
4	2	3	100	a rubber chicken
5	1	3	300	a jumper

%%writefile input/usuarios.txt

1	matthew@test.com	EN	US
2	matthew@test2.com	EN	GB
3	matthew@test3.com	FR	FR

%%writefile joinMapperTU.py
#!/usr/bin/env python3
import sys
if __name__ == "__main__":
	for line in sys.stdin:
		# Setting some defaults
		user_id = ""
		product_id = "-"
		location = "-"

		line = line.strip()
		splits = line.split("\t")
		#print("line " + len(splits) + ' :: ' + line)
		if len(splits) != 4: # Transactions have more columns than users
			user_id = splits[2]
			product_id = splits[1]
		else:
			user_id = splits[0]
			location = splits[3] 
		print(user_id + '\t' + product_id + '\t' + location)


!chmod +x joinMapperTU.py
		
!cat ./input/*.txt | ./joinMapperTU.py | sort



%%writefile joinReduceTU.py
#!/usr/bin/env python3
import sys
import string

if __name__ == "__main__":
	last_user_id = None
	cur_location = "-"

	for line in sys.stdin:
		line = line.strip()
		user_id,product_id,location = line.split("\t")

		if not last_user_id or last_user_id != user_id:
			last_user_id = user_id
			cur_location = location
		elif user_id == last_user_id:
			location = cur_location
			print(product_id + '\t' + location)
		
		
!chmod +x joinReduceTU.py	

cat ./input/*.txt | ./joinMapperTU.py | sort | ./joinSuffleTU.py | sort
