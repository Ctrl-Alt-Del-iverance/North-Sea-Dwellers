import pygame
import random
import time
from itertools import combinations
import math

class SealNetGame:
    def __init__(self, display):
        self.display = display
        pygame.display.set_caption("Untangle the Net")
        self.background = self.display.location_bg["Newburgh Seal Beach"]
        self.running = True
        self.num_nodes = 8
        self.nodes = self.generate_nodes()
        self.node_radius = 10
        self.edges = self.generate_edges()
        self.edge_colour = (0, 0, 0) # black :)
        self.dragging = None # node that is being dragged
        self.start_time = time.time()

    def generate_nodes(self):
        # puts some nodes at random coordinates
        nodes = []
        for i in range(self.num_nodes):
            x = random.randint(50, 950)
            y = random.randint(65, 450) # avoid overlapping with the text
            nodes.append((x, y))
        return nodes
    
    def generate_edges(self):
        # an edge is defined by (node1, node2), where node1, node2 are the indexes of the node
        # all but one of the nodes is in a circuit
        # so connect n-1 of the nodes:
        edges = []
        middle_node = self.num_nodes - 1
        for node in range(self.num_nodes - 1):
            edges.append((middle_node, node)) # connect xtra  node to all of the others
            next_node = node + 1
            if next_node == self.num_nodes - 1:  # if it's the last node in circuit
                next_node = 0  # wrap around to the first node
            edges.append((node, next_node))
            
        # the result of this is a plannar graph which is always solvable
        return edges
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # this checks to see if the user is clicking on a node
                for i, (x, y) in enumerate(self.nodes):
                    # checks if the distance of the click is within radius of the node
                    # and therefore inside that node
                    if math.sqrt((event.pos[0] - x) ** 2 + (event.pos[1] - y) ** 2) <= self.node_radius:
                        self.dragging = i # record which node is being clicked
            elif event.type == pygame.MOUSEBUTTONUP:
                self.dragging = None # player lets go of the node
            elif event.type == pygame.MOUSEMOTION and self.dragging is not None:
                # if the player is holding onto a node and moving the mouse, 
                # update position of the node
                self.nodes[self.dragging] = (event.pos[0], event.pos[1])
            if event.type == pygame.VIDEORESIZE:
                pygame.display.set_mode((self.display.width, self.display.height))

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
        # the game should end either upon winning or time running out
        time_left = 45
        while self.running:
            self.display.screen.blit(self.background, (0, 0))
            
            # if no strings of the net are overlapping:
            if not self.check_intersections():
                # green edge for untangled
                self.edge_colour = (0, 200, 0)
                # dont end until user lets go of the node
                if self.dragging is None:
                    success = True
                    self.running = False
            else: # black edge for tangled
                self.edge_colour = (0, 0, 0)

            if time_left == 0:
                self.display.draw_text("Time's up!", (self.display.width//2 - 70, 150), (200, 0, 0))
                pygame.display.flip()
                self.running = False
            
            for edge in self.edges:
                # line of width 2. going from one endpoint of the edge to the other
                # self.nodes[edge[0]] is a coordinate
                pygame.draw.line(self.display.screen, self.edge_colour, self.nodes[edge[0]], self.nodes[edge[1]], 2)
            
            for x, y in self.nodes:
                # draws the nodes
                pygame.draw.circle(self.display.screen, (0, 0, 200), (x, y), self.node_radius)
            
            # time left shouldn't go below 0, hence why we use max()
            time_left = max(0, 45 - int((time.time() - self.start_time)))
            self.display.draw_text(f"Time Left: {time_left}s", (10, 10), (0, 0, 0))
            self.display.draw_text(f"Untangle the net strings to free the seal!", (205, 10), (0, 0, 0))
            pygame.display.flip()
            self.handle_events()    
        
        pygame.time.delay(2000)
        return success # lets the main game know if the player won
    
    def show_seal_fun_fact(self):
        overlay = pygame.Surface((self.display.width, self.display.height))
        overlay.set_alpha(220)
        overlay.fill((0, 0, 0))
        self.display.screen.blit(overlay, (0, 0))
        
        fact_lines = [
            "Fun Fact: Seals in Newburgh!",
            "",
            "Newburgh Seal Beach is home to one of the largest colonies of seals in Scotland.",
            "At certain times of the year, over 400 seals can be seen basking on the sands.",
            "  ",
            "Seals are very curious creatures and often swim close to the shore to observe humans!"
            "Seals can hold their breath for 40-45 minutes"
        ]
        
        title_font = pygame.font.SysFont('Arial', 36)
        body_font = pygame.font.SysFont('Arial', 24)
        
        title = title_font.render(fact_lines[0], True, (100, 255, 100))
        title_rect = title.get_rect(center=(self.display.width // 2, self.display.height // 4))
        self.display.screen.blit(title, title_rect)

        for i, line in enumerate(fact_lines[2:], start=0):
            text = body_font.render(line, True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.display.width // 2, self.display.height // 2 + i * 30))
            self.display.screen.blit(text, text_rect)
        
        continue_text = body_font.render("Press any key to continue", True, (255, 255, 255))
        continue_rect = continue_text.get_rect(center=(self.display.width // 2, self.display.height - 50))
        self.display.screen.blit(continue_text, continue_rect)
        
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                    waiting = False

if __name__ == "__main__":
    from test_display import TestDisplay
    pygame.init()
    game = SealNetGame(TestDisplay())
    game.run()
