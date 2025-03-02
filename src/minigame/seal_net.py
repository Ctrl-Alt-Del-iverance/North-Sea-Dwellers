import pygame
import random
import time
from display import Display
from itertools import combinations

class SealNetGame:
    WIDTH, HEIGHT = 1000, 500
    NODE_RADIUS = 10
    EDGE_COLOR = (0, 0, 0)
    NODE_COLOR = (0, 0, 255)
    BACKGROUND_COLOR = (230, 230, 230)
    TIME_LIMIT = 60  # seconds

    def __init__(self, display):
        self.display = display
        pygame.display.set_caption("Untangle the Net")

        self.num_nodes = 7
        
        self.nodes = [(random.randint(50, self.WIDTH - 50), random.randint(50, self.HEIGHT - 50)) for _ in range(self.num_nodes)]
        self.edges = [(i, (i + 1) % (self.num_nodes - 1)) for i in range(self.num_nodes - 1)]
    
        # Connect the extra node (last node) to all others
        extra_node = self.num_nodes - 1
        self.edges += [(extra_node, i) for i in range(self.num_nodes - 1)]

        self.running = True
        self.dragging = None
        self.start_time = time.time()

    def check_intersections(self):
        def ccw(A, B, C):
            return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])
        
        def edges_intersect(edge1, edge2):
            A, B = self.nodes[edge1[0]], self.nodes[edge1[1]]
            C, D = self.nodes[edge2[0]], self.nodes[edge2[1]]
            return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)
        
        for e1, e2 in combinations(self.edges, 2):
            if len(set(e1) & set(e2)) == 0 and edges_intersect(e1, e2):
                return True
        return False

    def run(self):
        success = False
        while self.running:
            self.display.screen.fill(self.BACKGROUND_COLOR)
            elapsed_time = int(time.time() - self.start_time)
            remaining_time = max(0, self.TIME_LIMIT - elapsed_time)
            self.display.draw_text(f"Time Left: {remaining_time}s", (20, 20))
        
            
            if not self.check_intersections():
                self.display.draw_text("You untangled the net!", (self.WIDTH//2 - 100, self.HEIGHT//2), (0, 200, 0))
                success = True
                if self.dragging is None:
                    self.running = False
            elif remaining_time == 0:
                self.display.draw_text("Time's up! You lost.", (self.WIDTH//2 - 100, self.HEIGHT//2), (200, 0, 0))
                pygame.display.flip()
                self.running = False
            
            for edge in self.edges:
                pygame.draw.line(self.display.screen, self.EDGE_COLOR, self.nodes[edge[0]], self.nodes[edge[1]], 2)
            
            for i, (x, y) in enumerate(self.nodes):
                pygame.draw.circle(self.display.screen, self.NODE_COLOR, (x, y), self.NODE_RADIUS)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for i, (x, y) in enumerate(self.nodes):
                        if (event.pos[0] - x) ** 2 + (event.pos[1] - y) ** 2 <= self.NODE_RADIUS ** 2:
                            self.dragging = i
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.dragging = None
                elif event.type == pygame.MOUSEMOTION and self.dragging is not None:
                    self.nodes[self.dragging] = (event.pos[0], event.pos[1])
        
        pygame.time.delay(2000)
        return success

if __name__ == "__main__":
    game = SealNetGame()
    game.run()
