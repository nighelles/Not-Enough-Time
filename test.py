import time
import random
import pygame

def getreactiontime():
	a = 1
	nop = 1

	s = 0
	clock = pygame.time.Clock()
	print "This is the first time you're running the game."
	print "Please press enter, then press enter again as"
	print "fast as you can after each block of text is displayed"
	wait = raw_input()
	for i in range(0,5):
		a = 0
		nop = 0
		pygame.time.wait(random.randint(2000,5000))
		msElapsed = clock.tick(30)
		print "##############################"
		print "##############################"
		print "##############################"
		x = raw_input(); msElapsed = clock.tick(30)
		s = s + msElapsed

	s = s/5

	print "Thank you"
	return s

# define a main function

red = (255,0,0)
green= (0,255,0)
blue= (0,0,255)
white=(255,255,255)

SCREEN_WIDTH =640
SCREEN_HEIGHT=480

def main():
	ph = 20
	pw = 20
	px = 320-pw/2
	py = 480-ph
	vx = .01 # player speeds are in pixels per ms
	pml = 0
	pmr = 0
	
	ta = 0
	tb = 0
	
	ex = 0
	ey = 481
	evy = 0
	ew = 40
	eh = 20
	
	f=0
	reactiontime=0
	
	try:
		f = open('reactiontime.txt','r')
		reactiontime = float(f.readline().strip())
	except:
		print "reactiontime.txt doesn't exist"
		
	if f==0 or reactiontime==0:
		reactiontime = getreactiontime()
		f = open('reactiontime.txt','w')
		f.write(str(reactiontime))
	f.close()
	
	reaction_multiple = input("How much extra time do you want to dodge, as a multiple of your reaction time? ")
	
	# initialize the pygame module
	pygame.init()
	
	# load and set the logo
	pygame.display.set_caption("The most annoying game")
	
	screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
	
	# define a variable to control the main loop
	running = True
	
	score = -1
	# main loop
	clock = pygame.time.Clock()
	
	waiting = True
	myfont = pygame.font.SysFont("monospace", 15)
	label = myfont.render("Press any key to begin", 1, (255,255,0))
	screen.blit(label, (100, 100))
	pygame.display.update()
	
	while waiting:
		for event in pygame.event.get():
			# only do something if the event if of type QUIT
			if event.type == pygame.QUIT:
				# change the value to False, to exit the main loop
				running = False
			if event.type == pygame.KEYDOWN:
				waiting = False
			
	msElapsed = clock.tick(30)
	while running:
		if ey > 480:
			score = score + 1
			ew = random.randint(pw*2,pw*10)
			#generate new enemy
			ex = random.randint(int(px-ew),int(px+pw))
			ey = 0
			#calculate distance to go
			dodge_dist = min(abs((ex+ew)-(px)),abs((px+pw)-(ex)))
			print dodge_dist
			vert_dist = SCREEN_HEIGHT - eh
			e_time = dodge_dist/vx + reaction_multiple*reactiontime#time it will take you to move that distance
			print e_time
			print
			evy = vert_dist/e_time
			
		screen.fill(white)
		# event handling, gets all event from the eventqueue
		for event in pygame.event.get():
			# only do something if the event if of type QUIT
			if event.type == pygame.QUIT:
				# change the value to False, to exit the main loop
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RIGHT:
					pmr = 1
				if event.key == pygame.K_LEFT:
					pml = 1
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_RIGHT:
					pmr = 0
				if event.key == pygame.K_LEFT:
					pml = 0
					
		msElapsed = clock.tick(30)
		if pmr: px += vx*msElapsed
		if pml: px -= vx*msElapsed
		
		ey = ey+evy*msElapsed
		
		pygame.draw.rect(screen,blue, (px,py,pw,ph),5)
		pygame.draw.rect(screen,red, (ex,ey,ew,eh),5)
		pygame.draw.lines(screen,green,False, [(ex+ew/2,0),(ex+ew/2,480)],1)
		
		# check for player death
		if ey > 480-eh:
			if not(px > ex+ew or px+pw < ex):
				print "GAME OVER"
				print "Score: ",score
				running=False
		pygame.display.update()
	
	
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
	# call the main function
	main()