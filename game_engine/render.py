# game_engine/renderer.py
import pygame
import math
from .config import *


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 20, bold=True)

        # Color Palette (Stereo Madness theme)
        self.BG_COLOR = (0, 102, 204)  # Blue background
        self.BG_GRADIENT_TOP = (0, 102, 204)
        self.BG_GRADIENT_BOTTOM = (0, 51, 153)

        self.GROUND_COLOR = (0, 51, 102)
        self.GROUND_LINE_COLOR = (0, 204, 255)

        self.BLOCK_COLOR = (0, 204, 102)
        self.BLOCK_BORDER = (255, 255, 255)
        self.BLOCK_INNER = (0, 153, 76)

        self.SPIKE_COLOR = (102, 102, 255)
        self.SPIKE_BORDER = (255, 255, 255)
        self.SPIKE_GLOW = (153, 153, 255)

        self.PLAYER_COLOR = (255, 255, 0)
        self.PLAYER_BORDER = (255, 200, 0)
        self.PLAYER_INNER = (255, 150, 0)

        self.PORTAL_SHIP_COLOR = (255, 100, 255)
        self.PORTAL_CUBE_COLOR = (0, 255, 255)

        # Grid lines
        self.GRID_COLOR = (0, 77, 153)
        self.grid_offset = 0

    def draw_gradient_background(self):
        """Draw vertical gradient background"""
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(self.BG_GRADIENT_TOP[0] * (1 - ratio) + self.BG_GRADIENT_BOTTOM[0] * ratio)
            g = int(self.BG_GRADIENT_TOP[1] * (1 - ratio) + self.BG_GRADIENT_BOTTOM[1] * ratio)
            b = int(self.BG_GRADIENT_TOP[2] * (1 - ratio) + self.BG_GRADIENT_BOTTOM[2] * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))

    def draw_grid_background(self, camera_x):
        """Draw animated grid background"""
        grid_size = 40
        self.grid_offset = (camera_x * 0.3) % grid_size

        # Vertical lines
        for i in range(int(SCREEN_WIDTH / grid_size) + 2):
            x = i * grid_size - self.grid_offset
            pygame.draw.line(self.screen, self.GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT), 1)

        # Horizontal lines
        for i in range(int(SCREEN_HEIGHT / grid_size) + 1):
            y = i * grid_size
            pygame.draw.line(self.screen, self.GRID_COLOR, (0, y), (SCREEN_WIDTH, y), 1)

    def draw_ground(self):
        """Draw the ground with GD style"""
        ground_y = SCREEN_HEIGHT - FLOOR_HEIGHT

        # Main ground
        pygame.draw.rect(self.screen, self.GROUND_COLOR,
                         (0, ground_y, SCREEN_WIDTH, FLOOR_HEIGHT))

        # Top line (bright)
        pygame.draw.line(self.screen, self.GROUND_LINE_COLOR,
                         (0, ground_y), (SCREEN_WIDTH, ground_y), 3)

        # Decorative lines
        for i in range(3):
            y = ground_y + 10 + i * 10
            pygame.draw.line(self.screen, (0, 128, 204),
                             (0, y), (SCREEN_WIDTH, y), 1)

    def draw_block(self, x, y, w, h):
        """Draw a block with GD style (3D effect)"""
        # Main block
        pygame.draw.rect(self.screen, self.BLOCK_COLOR, (x, y, w, h))

        # Inner rectangle (darker)
        inner_margin = 4
        pygame.draw.rect(self.screen, self.BLOCK_INNER,
                         (x + inner_margin, y + inner_margin,
                          w - 2 * inner_margin, h - 2 * inner_margin))

        # Highlight (top-left)
        pygame.draw.line(self.screen, (150, 255, 150),
                         (x, y), (x + w, y), 2)
        pygame.draw.line(self.screen, (150, 255, 150),
                         (x, y), (x, y + h), 2)

        # Shadow (bottom-right)
        pygame.draw.line(self.screen, (0, 100, 50),
                         (x, y + h), (x + w, y + h), 2)
        pygame.draw.line(self.screen, (0, 100, 50),
                         (x + w, y), (x + w, y + h), 2)

        # Border
        pygame.draw.rect(self.screen, self.BLOCK_BORDER, (x, y, w, h), 2)

    def draw_spike(self, x, y, w, h):
        """Draw a spike with GD style (glowing effect)"""
        # Calculate triangle points
        p1 = (x, y + h)  # Bottom left
        p2 = (x + w, y + h)  # Bottom right
        p3 = (x + w / 2, y)  # Top middle

        # Glow effect (draw larger semi-transparent triangles)
        glow_surf = pygame.Surface((w + 20, h + 20), pygame.SRCALPHA)
        glow_p1 = (10, h + 10)
        glow_p2 = (w + 10, h + 10)
        glow_p3 = (w / 2 + 10, 0)

        for i in range(3):
            alpha = 30 - i * 10
            color = (*self.SPIKE_GLOW, alpha)
            offset = (3 - i) * 2
            pygame.draw.polygon(glow_surf, color, [
                (glow_p1[0] - offset, glow_p1[1] + offset),
                (glow_p2[0] + offset, glow_p2[1] + offset),
                (glow_p3[0], glow_p3[1] - offset)
            ])

        self.screen.blit(glow_surf, (x - 10, y - 10))

        # Main spike
        pygame.draw.polygon(self.screen, self.SPIKE_COLOR, [p1, p2, p3])

        # Inner gradient (lighter at top)
        inner_p1 = (x + w * 0.2, y + h)
        inner_p2 = (x + w * 0.8, y + h)
        inner_p3 = (x + w / 2, y + h * 0.3)
        pygame.draw.polygon(self.screen, (150, 150, 255), [inner_p1, inner_p2, inner_p3])

        # Border
        pygame.draw.polygon(self.screen, self.SPIKE_BORDER, [p1, p2, p3], 2)

    def draw_portal(self, x, y, w, h, portal_type):
        """Draw portals with animated effects"""
        color = self.PORTAL_SHIP_COLOR if "ship" in portal_type else self.PORTAL_CUBE_COLOR

        # Outer glow
        for i in range(3):
            alpha = 50 - i * 15
            glow_surf = pygame.Surface((w + 20, h + 20), pygame.SRCALPHA)
            glow_color = (*color, alpha)
            pygame.draw.rect(glow_surf, glow_color,
                             (10 - i * 3, 10 - i * 3, w + i * 6, h + i * 6), border_radius=5)
            self.screen.blit(glow_surf, (x - 10, y - 10))

        # Main portal frame
        pygame.draw.rect(self.screen, color, (x, y, w, h), border_radius=5)
        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, w, h), 3, border_radius=5)

        # Inner icon
        center_x, center_y = x + w // 2, y + h // 2
        if "ship" in portal_type:
            # Draw ship icon
            points = [
                (center_x - 10, center_y + 5),
                (center_x + 10, center_y),
                (center_x - 10, center_y - 5)
            ]
            pygame.draw.polygon(self.screen, (255, 255, 255), points)
        else:
            # Draw cube icon
            pygame.draw.rect(self.screen, (255, 255, 255),
                             (center_x - 8, center_y - 8, 16, 16), 2)

    def draw_player_cube(self, x, y, rotation):
        """Draw player in cube mode with rotation"""
        # Create surface for rotation
        size = PLAYER_SIZE
        surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)

        offset = size // 2
        center = (size, size)

        # Outer square
        rect = pygame.Rect(offset, offset, size, size)
        pygame.draw.rect(surf, self.PLAYER_COLOR, rect)

        # Inner square (darker)
        inner_rect = pygame.Rect(offset + 4, offset + 4, size - 8, size - 8)
        pygame.draw.rect(surf, self.PLAYER_INNER, inner_rect)

        # Border
        pygame.draw.rect(surf, self.PLAYER_BORDER, rect, 3)

        # Inner border
        pygame.draw.rect(surf, self.PLAYER_BORDER, inner_rect, 2)

        # Rotate
        rotated = pygame.transform.rotate(surf, rotation)
        new_rect = rotated.get_rect(center=(x, y))

        self.screen.blit(rotated, new_rect)

    def draw_player_ship(self, x, y, rotation):
        """Draw player in ship mode"""
        # Create surface for rotation
        size = PLAYER_SIZE
        surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)

        center = (size, size)

        # Ship shape (triangle pointing right)
        points = [
            (center[0] - size // 2, center[1] + size // 2),  # Back bottom
            (center[0] - size // 2, center[1] - size // 2),  # Back top
            (center[0] + size // 2, center[1])  # Front point
        ]

        # Glow effect
        for i in range(3):
            alpha = 40 - i * 10
            glow_points = [(p[0] + (2 - i) * 2 if j == 2 else p[0] - (2 - i) * 2,
                            p[1]) for j, p in enumerate(points)]
            pygame.draw.polygon(surf, (*self.PLAYER_COLOR, alpha), glow_points)

        # Main ship
        pygame.draw.polygon(surf, self.PLAYER_COLOR, points)

        # Inner details
        inner_points = [
            (points[0][0] + 5, points[0][1] - 5),
            (points[1][0] + 5, points[1][1] + 5),
            (points[2][0] - 5, points[2][1])
        ]
        pygame.draw.polygon(surf, self.PLAYER_INNER, inner_points)

        # Border
        pygame.draw.polygon(surf, self.PLAYER_BORDER, points, 2)

        # Rotate
        rotated = pygame.transform.rotate(surf, rotation)
        new_rect = rotated.get_rect(center=(x, y))

        self.screen.blit(rotated, new_rect)

    def draw(self, player, level, camera_x):
        # 1. Background
        self.draw_gradient_background()
        self.draw_grid_background(camera_x)

        # 2. Ground
        self.draw_ground()

        # 3. Obstacles
        for obs in level.get_obstacles():
            ox = obs['x'] - camera_x + 100

            if -100 < ox < SCREEN_WIDTH + 100:
                oy = SCREEN_HEIGHT - FLOOR_HEIGHT - obs['y'] - obs['h']

                if obs['type'] == 'block':
                    self.draw_block(ox, oy, obs['w'], obs['h'])

                elif obs['type'] == 'spike':
                    self.draw_spike(ox, oy, obs['w'], obs['h'])

                elif 'portal' in obs['type']:
                    self.draw_portal(ox, oy, obs['w'], obs['h'], obs['type'])

        # 4. Player
        px, py, rotation = player.get_render_data()
        screen_y = SCREEN_HEIGHT - FLOOR_HEIGHT - py - PLAYER_SIZE
        screen_x = 100

        center_x = screen_x + PLAYER_SIZE // 2
        center_y = screen_y + PLAYER_SIZE // 2

        if player.mode == "cube":
            self.draw_player_cube(center_x, center_y, rotation)
        else:
            self.draw_player_ship(center_x, center_y, rotation)

        # 5. UI
        distance_text = self.font.render(f"Distance: {int(player.x)}", True, (255, 255, 255))
        jumps_text = self.font.render(f"Jumps: {int(player.jump_count)}", True, (255, 255, 255))
        mode_text = self.font.render(f"Mode: {player.mode.upper()}", True, (255, 255, 0))

        self.screen.blit(distance_text, (10, 10))
        self.screen.blit(jumps_text, (10, 35))
        self.screen.blit(mode_text, (10, 60))