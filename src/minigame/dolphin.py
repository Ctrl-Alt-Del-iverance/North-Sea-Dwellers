import pygame
import random
import sys


# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 1000, 500
CELL_SIZE = 100
GRID_GAP = 10
ROWS, COLS = 3, 3
GRID_TOP = 70
GRID_LEFT = 400
SEQUENCE_DELAY = 1000  # 1 second between cells
ACTIVE_TIME = 500      # 500ms highlight duration

# Colors
BG_COLOR = (255, 255, 255)
CELL_COLOR = (0, 119, 190)
ACTIVE_COLOR = (0, 179, 255)
TEXT_COLOR = (0, 0, 0)
BUTTON_COLOR = (200, 200, 200)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dolphin Memory Game")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)

class Game:
    def __init__(self):
        self.reset()
        self.create_grid()
        self.button_rect = pygame.Rect(80, 370, 160, 40)
        
    def reset(self):
        self.sequence = []
        self.player_sequence = []
        self.level = 1
        self.game_active = False
        self.playing_sequence = False
        self.current_step = 0
        self.last_step_time = 0
        self.show_game_over = False
        
    def create_grid(self):
        self.cells = []
        for row in range(ROWS):
            for col in range(COLS):
                x = GRID_LEFT + col * (CELL_SIZE + GRID_GAP)
                y = GRID_TOP + row * (CELL_SIZE + GRID_GAP)
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                self.cells.append({
                    'rect': rect,
                    'active': False,
                    'flash_end': 0
                })

    def start_game(self):
        self.reset()
        self.game_active = True
        self.playing_sequence = True
        self.add_to_sequence()  # Start with first step
        
    def add_to_sequence(self):
        # Only append ONE new step to existing sequence
        new_step = random.randint(0, 8)
        self.sequence.append(new_step)
        self.playing_sequence = True
        self.current_step = 0
        self.last_step_time = pygame.time.get_ticks()
        
    def play_sequence_step(self):
        now = pygame.time.get_ticks()
        if now - self.last_step_time >= SEQUENCE_DELAY:
            if self.current_step < len(self.sequence):
                # Flash current step in sequence
                cell_index = self.sequence[self.current_step]
                self.cells[cell_index]['flash_end'] = now + ACTIVE_TIME
                self.current_step += 1
                self.last_step_time = now
            else:
                # Finished showing full sequence
                self.playing_sequence = False
                self.player_sequence = []  # Reset player input

    def check_sequence(self):
        # Compare player input with current sequence
        for i in range(len(self.player_sequence)):
            if self.player_sequence[i] != self.sequence[i]:
                self.show_game_over = True
                self.game_active = False
                return False
            
        if len(self.player_sequence) == len(self.sequence):
            # Only add new step when entire sequence is matched
            self.level += 1
            self.add_to_sequence()  # Append new step to existing sequence
        return True

    def draw(self):
        screen.fill(BG_COLOR)
        
        # Draw level
        level_text = font.render(f"Level: {self.level}", True, TEXT_COLOR)
        screen.blit(level_text, (10, 10))
        
        # Draw game over text
        if self.show_game_over:
            game_over_text = font.render(f"Game Over! Level: {self.level}", True, (255, 0, 0))
            screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2))
        
        # Draw cells
        for cell in self.cells:
            color = ACTIVE_COLOR if pygame.time.get_ticks() < cell['flash_end'] else CELL_COLOR
            pygame.draw.rect(screen, color, cell['rect'], border_radius=10)
            text = font.render("🐬", True, (255, 255, 255))
            text_rect = text.get_rect(center=cell['rect'].center)
            screen.blit(text, text_rect)
        
        # Draw start button
        pygame.draw.rect(screen, BUTTON_COLOR, self.button_rect, border_radius=5)
        button_text = small_font.render("New Game", True, TEXT_COLOR)
        text_rect = button_text.get_rect(center=self.button_rect.center)
        screen.blit(button_text, text_rect)
        
        pygame.display.flip()

    def handle_click(self, pos):
        if self.button_rect.collidepoint(pos):
            self.start_game()
            return
            
        if self.game_active and not self.playing_sequence:
            for i, cell in enumerate(self.cells):
                if cell['rect'].collidepoint(pos):
                    cell['flash_end'] = pygame.time.get_ticks() + 200
                    self.player_sequence.append(i)
                    self.check_sequence()

def main():
    game = Game()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.handle_click(pygame.mouse.get_pos())
        
        if game.playing_sequence:
            game.play_sequence_step()
        
        game.draw()
        clock.tick(30)

if __name__ == "__main__":
    main()