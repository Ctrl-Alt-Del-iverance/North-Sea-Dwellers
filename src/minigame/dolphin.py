import pygame
import random
import sys
import os

class DolphinGame:
    def __init__(self, display):
        # Initialize Pygame
        # Game Constants
        self.WIDTH, self.HEIGHT = 1000, 500
        self.CELL_SIZE = 100
        self.GRID_GAP = 20
        self.ROWS, self.COLS = 3, 3
        self.GRID_TOP = 70
        self.GRID_LEFT = 325
        self.SEQUENCE_DELAY = 1000  # 1 second between cells
        self.ACTIVE_TIME = 300      # 500ms animation duration

        # Colors
        self.BG_COLOR = (255, 255, 255)
        self.TEXT_COLOR = (255, 255, 255)
        self.BUTTON_COLOR = (200, 200, 200)

        # Initialize screen
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Dolphin Memory Game ")
        self.clock = pygame.time.Clock()

        # Fonts

        self.font = pygame.font.Font("src/pixelfont.ttf", 36)
        self.small_font = pygame.font.Font("src/pixelfont.ttf", 28)

        self.frames = self.load_frames("src/dolphin_video/output_folder")
        self.current_frame = 0
        self.reset()
        self.create_grid()
        self.grey_image = pygame.image.load("src/images/animals/dolphin_poses_buttons/grey.png")
        self.grey_image = pygame.transform.scale(self.grey_image, (self.CELL_SIZE, self.CELL_SIZE))

    def load_frames(self, folder):
        frames = []
        for filename in sorted(os.listdir(folder)):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                img_path = os.path.join(folder, filename)
                img = pygame.image.load(img_path).convert()
                img = pygame.transform.scale(img, (self.WIDTH, self.HEIGHT))
                frames.append(img)
        return frames
    
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

    def reset(self):
        self.sequence = []
        self.player_sequence = []
        self.level = 1
        self.game_active = False
        self.playing_sequence = False
        self.current_step = 0
        self.last_step_time = 0
        self.show_game_over = False
        self.show_win_message = False
        
    def create_grid(self):
        self.cells = []
        images = self.load_images("src/images/animals/dolphin_poses_buttons")
        for row in range(self.ROWS):
            for col in range(self.COLS):
                x = self.GRID_LEFT + col * (self.CELL_SIZE + self.GRID_GAP)
                y = self.GRID_TOP + row * (self.CELL_SIZE + self.GRID_GAP)
                rect = pygame.Rect(x, y, self.CELL_SIZE, self.CELL_SIZE)
                self.cells.append({
                    'rect': rect,
                    'image': images[row * self.COLS + col],
                    'flash_end': 0,
                    'offset': (0, 0)
                })

    def add_to_sequence(self):
        new_step = random.randint(0, 8)
        self.sequence.append(new_step)
        self.playing_sequence = True
        self.current_step = 0
        self.last_step_time = pygame.time.get_ticks()
        
    def play_sequence_step(self):
        now = pygame.time.get_ticks()
        if now - self.last_step_time >= self.SEQUENCE_DELAY:
            if self.current_step < len(self.sequence):
                cell_index = self.sequence[self.current_step]
                self.cells[cell_index]['flash_end'] = now + self.ACTIVE_TIME
                self.current_step += 1
                self.last_step_time = now
            else:
                self.playing_sequence = False
                self.player_sequence = []

    def check_sequence(self):
        for i in range(len(self.player_sequence)):
            if self.player_sequence[i] != self.sequence[i]:
                self.show_game_over = True
                self.game_active = False
                return False
            
        if len(self.player_sequence) == len(self.sequence):
            self.level += 1
            if self.level == 10:  # Winning condition
                self.show_win_message = True
                self.game_active = False  # Stop the game
            else:
                self.add_to_sequence()
        return True

    def draw(self):
        if self.frames:
            self.screen.blit(self.frames[self.current_frame], (0, 0))
        else:
            self.screen.fill(self.BG_COLOR)
        
        level_text = self.font.render(f"Level: {self.level}", True, self.TEXT_COLOR)
        self.screen.blit(level_text, (10, 10))

        # Draw cells
        for cell in self.cells:
            #pygame.draw.rect(screen, CELL_COLOR, cell['rect'], border_radius=10)
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
        
        if self.show_game_over:
            game_over_text = self.font.render(f"Game Over! Level: {self.level}", True, (255, 0, 0))
            self.screen.blit(game_over_text, (self.WIDTH//2 - game_over_text.get_width()//2, self.HEIGHT//2))

        if self.show_win_message:
            win_text = self.font.render("You Win!", True, (0, 255, 0))
            self.screen.blit(win_text, (self.WIDTH//2 - win_text.get_width()//2, self.HEIGHT//2))
        
        pygame.display.flip()

    def handle_click(self, pos):
            
        if self.game_active and not self.playing_sequence:
            for i, cell in enumerate(self.cells):
                if cell['rect'].collidepoint(pos):
                    cell['flash_end'] = pygame.time.get_ticks() + self.ACTIVE_TIME
                    self.player_sequence.append(i)
                    self.check_sequence()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game.handle_click(pygame.mouse.get_pos())
            
            if game.playing_sequence:
                game.play_sequence_step()

            game.current_frame = (game.current_frame + 1) % len(game.frames)
            game.draw()
            self.clock.tick(30)

if __name__ == "__main__":
    from test_display import TestDisplay
    pygame.init()
    game = DolphinGame(TestDisplay())
    game.run()