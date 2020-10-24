class Player():

    init_x = 100
	init_y = 400

    jump_height = 250
	jump_speed = 5
	jump_speed_accel = 0

    def __init__(self, radius, images):
        self.x = init_x
        self.y = init_y
        self.image = images[0]
        self.velocity = 5
        self.score_update = pygame.time.get_ticks()
        self.score = 0
        self.jumping = False
        self.inair = False

    def update(self):

        if pygame.time.get_ticks() - self.score_update > 100:
            if not self.isDead:
                self.score_update = pygame.time.get_ticks()
                player.score += 10

        self.x += self.velocity

        if self.y >= Player.init_y:
			self.inair = False
		else:
			self.inair = True
        
        if self.jumping:
			self.y -= Player.jump_speed
			self.current_jump_speed += Player.jump_speed_accel
			if self.y <= Player.init_y - Player.jump_height:
				self.jumping=False
		else:
			self.current_jump_speed -= Player.jump_speed_accel
			if self.y <= Player.init_y:
				self.y += Player.jump_speed


    def jump(self):
        self.current_jump_speed = Player.jump_speed
		self.inair = True
		if self.y >= Player.init_y:
			self.jumping = True
