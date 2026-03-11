# game_engine/core.py

import pygame

from .config import *
from .player import Player
from .level import Level
from .render import Renderer
from .victory import play_victory_animation


def run_simulation(genome, render=False):
    player = Player()
    level = Level()

    jumps_list = genome.reshape(-1, 2)
    jumps_list = jumps_list[jumps_list[:, 0].argsort()]

    valid_jumps = jumps_list[(jumps_list[:, 1] > 0) & (jumps_list[:, 0] < 40.0)]

    num_jumps = len(valid_jumps)
    current_jump_idx = 0

    renderer = None
    if render:
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("EvoDash - Optimization")
        renderer = Renderer(screen)
        clock = pygame.time.Clock()

    sim_time = 0.0
    dt = 1.0 / 60.0
    max_time = 40.0

    victory_x = 13200

    running = True
    victory_triggered = False

    while running and sim_time < max_time:
        if render:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return 0, 0

        is_pressing_jump = False

        while current_jump_idx < num_jumps:
            start_t, duration = valid_jumps[current_jump_idx]
            end_t = start_t + duration
            if start_t > sim_time:
                break

            if start_t <= sim_time <= end_t:
                is_pressing_jump = True
                break

            if sim_time > end_t:
                current_jump_idx += 1
            else:
                break

        player.update(dt, is_pressing_jump, level.get_obstacles())

        # CHECK FOR VICTORY
        if not victory_triggered and not player.dead and player.x >= victory_x:
            victory_triggered = True
            if render:
                renderer.draw(player, level, player.x)
                pygame.display.flip()
                play_victory_animation(renderer.screen, player.x, player.y)
                pygame.quit()
                return player.x, player.jump_count

        if player.dead:
            running = False

        if render:
            renderer.draw(player, level, player.x)
            pygame.display.flip()
            clock.tick(FPS)

        sim_time += dt

    if render:
        pygame.quit()

    return player.x, player.jump_count