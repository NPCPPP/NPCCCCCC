import random
import sys
from dataclasses import dataclass
from typing import List

import pygame

# Game configuration constants
WINDOW_WIDTH = 480
WINDOW_HEIGHT = 640
FPS = 60
LANE_COUNT = 3
LANE_WIDTH = WINDOW_WIDTH // LANE_COUNT
CAR_WIDTH = 50
CAR_HEIGHT = 80
OBSTACLE_MIN_GAP = 150
OBSTACLE_MAX_GAP = 250
OBSTACLE_SPEED_START = 4
OBSTACLE_SPEED_INCREMENT = 0.1


def load_or_create_surface(size: tuple[int, int], color: tuple[int, int, int]) -> pygame.Surface:
    """Return a simple colored surface used for the car and obstacles."""
    surface = pygame.Surface(size)
    surface.fill(color)
    return surface


@dataclass
class GameObject:
    rect: pygame.Rect
    surface: pygame.Surface

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.surface, self.rect)


class Player(GameObject):
    lane: int

    def __init__(self, lanes: List[int]):
        self.surface = load_or_create_surface((CAR_WIDTH, CAR_HEIGHT), (66, 135, 245))
        lane_index = lanes[len(lanes) // 2]
        x = lane_index + (LANE_WIDTH - CAR_WIDTH) // 2
        y = WINDOW_HEIGHT - CAR_HEIGHT - 20
        rect = pygame.Rect(x, y, CAR_WIDTH, CAR_HEIGHT)
        super().__init__(rect, self.surface)
        self.lane_positions = lanes
        self.current_lane_index = len(lanes) // 2

    def move_left(self) -> None:
        if self.current_lane_index > 0:
            self.current_lane_index -= 1
            self.rect.x = self.lane_positions[self.current_lane_index] + (LANE_WIDTH - CAR_WIDTH) // 2

    def move_right(self) -> None:
        if self.current_lane_index < len(self.lane_positions) - 1:
            self.current_lane_index += 1
            self.rect.x = self.lane_positions[self.current_lane_index] + (LANE_WIDTH - CAR_WIDTH) // 2


class Obstacle(GameObject):
    speed: float

    def __init__(self, lane_x: int, speed: float):
        surface = load_or_create_surface((CAR_WIDTH, CAR_HEIGHT), (217, 83, 79))
        rect = pygame.Rect(lane_x + (LANE_WIDTH - CAR_WIDTH) // 2, -CAR_HEIGHT, CAR_WIDTH, CAR_HEIGHT)
        super().__init__(rect, surface)
        self.speed = speed

    def update(self) -> None:
        self.rect.y += self.speed


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Simple Racing Game")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        self.background_color = (30, 30, 30)
        self.lane_color = (100, 100, 100)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.Font(None, 36)

        self.lanes = [i * LANE_WIDTH for i in range(LANE_COUNT)]
        self.player = Player(self.lanes)
        self.obstacles: List[Obstacle] = []
        self.score = 0
        self.high_score = 0
        self.spawn_timer = 0
        self.speed = OBSTACLE_SPEED_START

    def reset(self) -> None:
        self.player = Player(self.lanes)
        self.obstacles.clear()
        self.score = 0
        self.spawn_timer = 0
        self.speed = OBSTACLE_SPEED_START

    def run(self) -> None:
        running = True
        while running:
            delta_time = self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        self.player.move_left()
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        self.player.move_right()
                    elif event.key == pygame.K_r:
                        self.reset()

            self.update(delta_time)
            self.draw()

        pygame.quit()
        sys.exit()

    def update(self, delta_time: int) -> None:
        self.spawn_timer += delta_time
        spawn_delay = random.randint(OBSTACLE_MIN_GAP, OBSTACLE_MAX_GAP)
        if self.spawn_timer >= spawn_delay:
            lane_x = random.choice(self.lanes)
            self.obstacles.append(Obstacle(lane_x, self.speed))
            self.spawn_timer = 0
            self.speed += OBSTACLE_SPEED_INCREMENT

        for obstacle in list(self.obstacles):
            obstacle.update()
            if obstacle.rect.top > WINDOW_HEIGHT:
                self.obstacles.remove(obstacle)
                self.score += 1
                self.high_score = max(self.high_score, self.score)

        if any(obstacle.rect.colliderect(self.player.rect) for obstacle in self.obstacles):
            self.high_score = max(self.high_score, self.score)
            self.reset()

    def draw(self) -> None:
        self.screen.fill(self.background_color)

        for lane_index in range(1, LANE_COUNT):
            lane_x = lane_index * LANE_WIDTH
            pygame.draw.rect(self.screen, self.lane_color, pygame.Rect(lane_x - 5, 0, 10, WINDOW_HEIGHT))

        self.player.draw(self.screen)
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        score_surface = self.font.render(f"Score: {self.score}", True, self.text_color)
        high_score_surface = self.font.render(f"High Score: {self.high_score}", True, self.text_color)
        instructions_surface = self.font.render("Arrows/A-D to move, R to reset", True, self.text_color)

        self.screen.blit(score_surface, (10, 10))
        self.screen.blit(high_score_surface, (10, 40))
        self.screen.blit(instructions_surface, (10, WINDOW_HEIGHT - 40))

        pygame.display.flip()


if __name__ == "__main__":
    Game().run()
