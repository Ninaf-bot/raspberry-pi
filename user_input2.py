
while 1:
   i=input()
   if i== 'w':
     print ('w')
   elif i=='s':
     robot.backward()
   elif i=='a':
     robot.left()
   elif i=='d':
     robot.right()
   elif i=='x':
     robot.stop()
   elif i=='r':
     speed+=0.1
   elif i=='f':
     speed-=0.1
   else: 
     print ('wrong input')