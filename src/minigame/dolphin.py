import pygame
import random
import os

class DolphinGame:
    def __init__(self, display, player_level):
        self.display = display
        self.screen = self.display.screen
        self.player_level = player_level
        self.clock = pygame.time.Clock()
        self.running = True # is pygame running
        self.state = "playing" # game is active
        self.success = False # did the player win
        self.set_game() # set the values for tracking level progress
        
        # game cells (buttons)
        self.cells = []
        self.CELL_SIZE = 100
        self.ACTIVE_TIME = 300 # 300ms animation duration

        self.TEXT_COLOR = (255, 255, 255)
        self.font = display.font

        # set graphics
        self.frames = self.display.frames
        self.current_frame = 0
        self.grey_image = self.display.scale("src/images/animals/dolphin_poses_buttons/grey.png", (self.CELL_SIZE, self.CELL_SIZE))
        self.button_images = self.load_images("src/images/animals/dolphin_poses_buttons")

    def set_game(self):
        self.max_sequence = self.get_sequence_length()
        self.sequence = []
        self.player_sequence = []
        self.did_player_guess = False
        self.level = 1
        self.dolphin_turn = True
        self.current_step = 0
        self.last_step_time = 0
        self.SEQUENCE_DELAY = 1000 # 1 second between each movement in sequence

    def load_images(self, folder):
            images = []
            for filename in sorted(os.listdir(folder)):
                if filename.endswith(('.png', '.jpg', '.jpeg')):
                    img_path = os.path.join(folder, filename)
                    img = pygame.image.load(img_path)
                    img = pygame.transform.scale(img, (self.CELL_SIZE, self.CELL_SIZE))
                    images.append(img)
                    if len(images) == 9:
                        break
            return images
        
    def create_grid(self):
        grid_gap = 20
        grid_top = 70
        grid_left = 325
        rows, cols = 3, 3
        for row in range(rows):
            for col in range(cols):
                x = grid_left + col * (self.CELL_SIZE + grid_gap)
                y = grid_top + row * (self.CELL_SIZE + grid_gap)
                rect = pygame.Rect(x, y, self.CELL_SIZE, self.CELL_SIZE)
                self.cells.append({
                    'rect': rect,
                    'image': self.button_images[row * cols + col],
                    'flash_end': 0,
                    'offset': (0, 0)
                })

    def get_sequence_length(self):
        if self.player_level < 5:
            return 6
        elif self.player_level < 10:
            return 7
        elif self.player_level < 15:
            return 8
        elif self.player_level <20:
            return 9
        return 10

    def handle_events(self):
        for event in pygame.event.get():
            if self.state == "facts":
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    self.state =  "input_recieved"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click(pygame.mouse.get_pos())  
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.VIDEORESIZE:
                pygame.display.set_mode((self.display.width, self.display.height))

    def handle_click(self, pos):
        # now accepting user answer?
        if not self.dolphin_turn:
            for i, cell in enumerate(self.cells):
                if cell['rect'].collidepoint(pos):
                    cell['flash_end'] = pygame.time.get_ticks() + self.ACTIVE_TIME
                    self.player_sequence.append(i)
                    self.did_player_guess = True

    def add_to_sequence(self):
        new_step = random.randint(0, self.max_sequence-1)
        self.sequence.append(new_step)
        self.dolphin_turn = True
        self.current_step = 0
        self.last_step_time = pygame.time.get_ticks()
        self.level = len(self.sequence) #set level to length of sequence
        
    def play_sequence_step(self):
        now = pygame.time.get_ticks()
        if self.current_step < len(self.sequence):
            if now - self.last_step_time >= self.SEQUENCE_DELAY:
                cell_index = self.sequence[self.current_step]
                self.cells[cell_index]['flash_end'] = now + self.ACTIVE_TIME
                self.current_step += 1
                self.last_step_time = now
        else:
            self.dolphin_turn = False
            self.player_sequence = []

    def check_sequence(self):
        for i in range(len(self.player_sequence)):
            if self.player_sequence[i] != self.sequence[i]:
                self.state = "facts"
                return # dont bother checking the rest
        if len(self.player_sequence) == len(self.sequence):
            if self.level == self.max_sequence:  # Winning condition
                self.state = "facts"
                self.success = True
            else:
                self.add_to_sequence()
        return True

    def draw(self):
        if self.frames:
            self.screen.blit(self.frames[self.current_frame], (0, 0))
        else:
            self.screen.fill((255, 255, 255))
        
        level_text = self.font.render(f"Level: {self.level}", True, self.TEXT_COLOR)
        self.screen.blit(level_text, (10, 10))

        # Draw cells
        for cell in self.cells:
            self.screen.blit(self.grey_image, (cell['rect'].x + 10, cell['rect'].y + 10))
            
            now = pygame.time.get_ticks()
            if now < cell['flash_end']:
                elapsed = now - (cell['flash_end'] - self.ACTIVE_TIME)
                progress = elapsed / self.ACTIVE_TIME
                if progress <= 0.5:
                    offset = int(10 * (progress / 0.5))
                else:
                    offset = int(10 * (1 - (progress - 0.5)/0.5))
                cell['offset'] = (offset, offset)
            else:
                cell['offset'] = (0, 0)
            
            self.screen.blit(cell['image'], 
                        (cell['rect'].x + cell['offset'][0], 
                         cell['rect'].y + cell['offset'][1]))
        
        self.display.draw_text("Echo the dolphin's movements!", (self.display.width//2-187, self.display.height-40), (0, 0, 0))
        pygame.display.flip()
       
    def run(self):
        pygame.display.set_caption("Dolphin Memory Game")
        self.create_grid()
        self.add_to_sequence()
        
        while self.running:
            self.handle_events()

            if self.state == "playing":
                if self.dolphin_turn:
                    self.play_sequence_step()
                # stops wasteful calls to check_sequence every frame:
                elif self.did_player_guess: 
                    self.check_sequence()
                    self.did_player_guess = False

                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.draw()
                self.clock.tick(45)

                if self.state == "facts":
                    # Show fun fact after game ends
                    self.show_dolphin_fun_fact()

            elif self.state == "input_recieved":
                return self.success

        # Return True if player wins, False if game over
        pygame.quit()
    
    def show_dolphin_fun_fact(self):
        # Create a semi-transparent overlay
        overlay = pygame.Surface((self.display.width, self.display.height))
        overlay.set_alpha(220)
        overlay.fill((0, 0, 0))  # Black color
        self.screen.blit(overlay, (0, 0))
       
        # Prepare fun fact text about dolphins
        if not self.success:
            title_text = "Game Over! You mimicked the dance wrong."
            title_colour = (255, 100, 100)
        else:
            title_text = "Congratulations! What a beautiful performance."
            title_colour = (100, 255, 100)

        fact_lines = [
            "Dolphins of Aberdeen!",
            "The waters off Aberdeen are home to a remarkable population of",
            "bottlenose dolphins in the Moray Firth, one of the best places",
            "in Europe to spot these marine mammals.",
            "Over 130 individual dolphins have been identified in this area,",
            "making it a critical habitat for these intelligent creatures.",
            "  "
        ]
       
        # Render dolphin image
        dolphin_image = pygame.image.load("src/images/animals/dolphin.png")
        scaled_dolphin = pygame.transform.scale(dolphin_image, (200, 200))
        dolphin_rect = scaled_dolphin.get_rect(center=(self.display.width // 2, self.display.height // 2 - 140))
        self.screen.blit(scaled_dolphin, dolphin_rect)
       
        # Render fact text with improved positioning
        title_font = pygame.font.SysFont('Arial', 36, bold=True)
        body_font = self.display.font
       
        # Render title separately
        title = title_font.render(title_text, True, title_colour)
        title_rect = title.get_rect(center=(self.display.width // 2, self.display.height // 2))
        self.screen.blit(title, title_rect)
       
        # Render body text
        for i, line in enumerate(fact_lines):
            text = body_font.render(line, True, (self.TEXT_COLOR))  # White color
            text_rect = text.get_rect(center=(self.display.width // 2, self.display.height // 2 + (i+1) * 30))
            self.screen.blit(text, text_rect)
       
        # Render continue instruction
        continue_text = body_font.render("Press any key to continue", True, (self.TEXT_COLOR))
        continue_rect = continue_text.get_rect(center=(self.display.width // 2, self.display.height - 30))
        self.screen.blit(continue_text, continue_rect)
       
        pygame.display.flip()

# Optional: Allow the game to be run standalone for testing
if __name__ == "__main__":
    from test_display import TestDisplay
    pygame.init()
    game = DolphinGame(TestDisplay(), 1)
    game.run()