"""
Snake Game with Intentional Bugs for Debugging Tutorial
This game has 2 bugs that are perfect for teaching debugging:
1. Food spawns inside the snake's body (line 87-88)
2. Score increases by wrong amount when eating food (line 126)
"""

import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
GRID_SIZE = 20
CELL_SIZE = WINDOW_WIDTH // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        # Start in the middle of the screen
        start_x = GRID_SIZE // 2
        start_y = GRID_SIZE // 2
        
        # Snake starts with 3 segments
        self.segments = [
            (start_x, start_y),
            (start_x - 1, start_y),
            (start_x - 2, start_y)
        ]
        self.direction = RIGHT
        self.grow_flag = False
        
    def move(self):
        """Move the snake in the current direction"""
        head_x, head_y = self.segments[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        
        # Add new head
        self.segments.insert(0, new_head)
        
        # Remove tail unless growing
        if not self.grow_flag:
            self.segments.pop()
        else:
            self.grow_flag = False
            
    def grow(self):
        """Set flag to grow snake on next move"""
        self.grow_flag = False
        
    def check_collision(self):
        """Check if snake has collided with walls or itself"""
        head = self.segments[0]
        
        # Check wall collision
        if (head[0] < 0 or head[0] >= GRID_SIZE or head[1] >= GRID_SIZE):
            return True
            
        # Check self collision
        if head in self.segments[1:]:
            return True
            
        return False
        
class Food:
    def __init__(self):
        self.position = None
        self.spawn()
        
    def spawn(self):
        """Spawn food at random location"""
        # BUG #1: Food can spawn inside snake body
        # This should check if position overlaps with snake
        x = random.randint(0, GRID_SIZE - 1)
        y = random.randint(0, GRID_SIZE - 1)
        self.position = (x, y)
        
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game - Debugging Tutorial")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False
        self.move_counter = 0
        self.move_delay = 10  # Frames between moves
        
    def handle_input(self):
        """Handle keyboard input"""
        keys = pygame.key.get_pressed()
        
        # Prevent snake from going back into itself
        if keys[pygame.K_UP] and self.snake.direction != DOWN:
            self.snake.direction = UP
        elif keys[pygame.K_DOWN] and self.snake.direction != UP:
            self.snake.direction = DOWN
        elif keys[pygame.K_LEFT] and self.snake.direction != RIGHT:
            self.snake.direction = LEFT
        elif keys[pygame.K_RIGHT] and self.snake.direction != LEFT:
            self.snake.direction = RIGHT
            
    def update(self):
        """Update game state"""
        if self.game_over:
            return
            
        # Control snake movement speed
        self.move_counter += 1
        if self.move_counter >= self.move_delay:
            self.move_counter = 0
            
            # Move snake
            self.snake.move()
            
            # Check if snake ate food
            if self.snake.segments[0] == self.food.position:
                self.snake.grow()
                self.food.spawn()
                # BUG #2: Score increases by 100 instead of 10
                # Students can watch the score variable change
                self.score += 100  # Should be += 10
                
            # Check collisions
            if self.snake.check_collision():
                self.game_over = True
                
    def draw_grid(self):
        """Draw grid lines for visual clarity"""
        for x in range(0, WINDOW_WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, (40, 40, 40), (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, (40, 40, 40), (0, y), (WINDOW_WIDTH, y))
            
    def draw(self):
        """Draw everything on screen"""
        self.screen.fill(BLACK)
        
        # Draw grid
        self.draw_grid()
        
        # Draw snake
        for i, segment in enumerate(self.snake.segments):
            x = segment[0] * CELL_SIZE
            y = segment[1] * CELL_SIZE
            color = GREEN if i == 0 else DARK_GREEN  # Head is brighter
            pygame.draw.rect(self.screen, color, 
                           (x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2))
            
        # Draw food
        if self.food.position:
            x = self.food.position[0] * CELL_SIZE
            y = self.food.position[1] * CELL_SIZE
            pygame.draw.rect(self.screen, RED, 
                           (x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2))
            
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw game over message
        if self.game_over:
            game_over_text = self.font.render("GAME OVER! Press R to restart", True, RED)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            self.screen.blit(game_over_text, text_rect)
            
        pygame.display.flip()
        
    def reset(self):
        """Reset the game"""
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False
        self.move_counter = 0
        
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.game_over:
                        self.reset()
                        
            # Handle continuous input
            self.handle_input()
            
            # Update game state
            self.update()
            
            # Draw everything
            self.draw()
            
            # Control frame rate
            self.clock.tick(60)
            
        pygame.quit()
        sys.exit()

def main():
    """Entry point for the game"""
    game = Game()
    game.run()

if __name__ == "__main__":
    main()