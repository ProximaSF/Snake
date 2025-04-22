import random
import pygame

class Snake():
    def __init__(self, screen_size, move_delay=150, frame=60):
        pygame.init()
        pygame.display.set_caption('Snake')

        self.screen_size = screen_size
        self.frame = frame
        self.running = True
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size))
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        self.size = 20
        self.player_pos = pygame.Vector2(screen_width/2, screen_height/2)
        self.snake_head_pos = [int(self.player_pos.x), int(self.player_pos.y)]
        self.body = [self.snake_head_pos.copy()]

        self.move_interval = 20

        self.last_moved = 0
        self.move_delay = move_delay

        self.snake_direction = '' # current move direction

        self.apple_pos = [100, 100]
        self.score = 0

    def game_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(f'game close: {event.type} == {pygame.QUIT}')
                self.running = False
            elif event.type == pygame.KEYDOWN:

                # check if snake head-within game boarder
                def check_border(key):
                    #print(self.snake_head_pos)
                    if key == 'w':
                        return self.snake_head_pos[1] > 0
                    if key == 's':
                        return self.snake_head_pos[1] < self.screen_size

                    if key == 'a':
                        return self.snake_head_pos[0] > 0
                    if key == 'd':
                        return self.snake_head_pos[0] < self.screen_size
                    else:
                        return False

                # prevent 180 turn
                def check_direction(direction):
                    opposites = {
                        'up': 'down',
                        'down': 'up',
                        'left': 'right',
                        'right': 'left'
                    }
                    if opposites[direction] == self.snake_direction:
                        return False
                    else:
                        return True

                keys = pygame.key.get_pressed()
                if keys[pygame.K_w] and check_border('w') and check_direction('up'):
                    self.snake_direction = 'up' # change snake move direction
                if keys[pygame.K_s] and check_border('s') and check_direction('down'):
                    self.snake_direction = 'down'

                if keys[pygame.K_a] and check_border('a') and check_direction('left'):
                    self.snake_direction = 'left'
                if keys[pygame.K_d] and check_border('d') and check_direction('right'):
                    self.snake_direction = 'right'

    # move snake head
    def update_head_pos(self):
        current_time = pygame.time.get_ticks()

        # update snake head pos
        def replace_first_index():
            if len(self.body) == 0:
                self.body.append(self.snake_head_pos)
            else:
                self.body[0] = self.snake_head_pos


        if current_time - self.last_moved > self.move_delay:
            if self.snake_head_pos[0] != 0 and self.snake_head_pos[0] != self.screen_size and \
                self.snake_head_pos[1] != 0 and self.snake_head_pos[1] != self.screen_size:

                for part in range(len(self.body) - 1, 0, -1):
                    self.body[part] = self.body[part-1].copy()

                if self.snake_direction == 'up':
                    replace_first_index()
                    self.snake_head_pos[1] -= self.move_interval
                elif self.snake_direction == 'down':
                    replace_first_index()
                    self.snake_head_pos[1] += self.move_interval
                elif self.snake_direction == 'left':
                    replace_first_index()
                    self.snake_head_pos[0] -= self.move_interval
                elif self.snake_direction == 'right':
                    replace_first_index()
                    self.snake_head_pos[0] += self.move_interval
            else:
                self.running = False

            self.last_moved = current_time

    # render game
    def snake(self):
        self.screen.fill('gray')
        # The rect position is top-left corner

        for segment in range(1, len(self.body)):
            pygame.draw.rect(self.screen, 'black', (self.body[segment][0], self.body[segment][1], self.size, self.size))

        pygame.draw.rect(self.screen, 'orange', (self.snake_head_pos[0], self.snake_head_pos[1], self.size, self.size))
        pygame.draw.rect(self.screen, 'red', (self.apple_pos[0], self.apple_pos[1], self.size, self.size))

    # add a segment after eating
    def add_body(self):
        last_pos = self.body[-1]

        if self.snake_direction == 'up':
            self.body.append([last_pos[0], last_pos[1] + 20])
            #running = False
        elif self.snake_direction == 'down':
            self.body.append([last_pos[0], last_pos[1] - 20])
        elif self.snake_direction == 'left':
            self.body.append([last_pos[0] + 20, last_pos[1]])
        elif self.snake_direction == 'right':
            self.body.append([last_pos[0] - 20, last_pos[1]])
        self.write_pos(f"Ate an apple: {self.body}\n")

    # generate and apple and detect apple eaten
    def eat_apple(self):
        if tuple(self.snake_head_pos) == tuple(self.apple_pos):
            self.score += 1
            self.add_body()

            max_val = int(self.screen_size / 20)
            ran_pos_x = random.randint(0, max_val) * 20
            ran_pos_y = random.randint(0, max_val) * 20

            if ran_pos_x == self.screen_size:
                ran_pos_x = self.screen_size - 20
            if ran_pos_y == self.screen_size:
                ran_pos_y = self.screen_size - 20

            self.apple_pos = [ran_pos_x, ran_pos_y]

    # check body collision
    def body_collision(self):
        if self.snake_head_pos in self.body[1:]:
            self.running = False

    # txt write up
    def write_pos(self, text):
        with open('pos.txt', 'a', encoding='UTF-8') as write_file:
            write_file.write(text)

    def startgame(self):
        while self.running:
            self.game_event()
            pygame.display.flip()
            self.update_head_pos()
            self.eat_apple()
            self.body_collision()
            self.snake()
        pygame.quit()
        print(f"SCORE: {self.score}")

if __name__ == '__main__':
    with open('pos.txt', 'w', encoding='utf-8') as f:
        pass
    game_instance = Snake(screen_size=400, move_delay=100, frame=60)
    game_instance.startgame()
