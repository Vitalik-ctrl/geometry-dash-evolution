# game_engine/victory.py
import pygame
import math
import random


def play_victory_animation(screen, player_x, player_y):
    """
    Epic victory animation with blur, particles, and cool effects!

    Args:
        screen: pygame screen object
        player_x: player's x position
        player_y: player's y position
    """
    from .config import SCREEN_WIDTH, SCREEN_HEIGHT, FLOOR_HEIGHT

    clock = pygame.time.Clock()
    particles = []
    fireworks = []
    stars = []
    animation_time = 0.0

    print("\nVICTORY! Level Complete!")

    # Capture the current screen for blur effect
    background = screen.copy()

    # Create blurred background
    blurred_bg = pygame.transform.smoothscale(background, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4))
    blurred_bg = pygame.transform.smoothscale(blurred_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Create initial confetti burst
    for _ in range(150):
        angle = random.random() * 2 * math.pi
        speed = 200 + random.random() * 400

        vx = math.cos(angle) * speed
        vy = math.sin(angle) * speed - 300

        color = random.choice([
            (255, 100, 100), (100, 255, 100), (100, 100, 255),
            (255, 255, 100), (255, 100, 255), (100, 255, 255),
            (255, 150, 0), (255, 200, 200), (200, 255, 200)
        ])

        particles.append({
            'x': SCREEN_WIDTH // 2,
            'y': SCREEN_HEIGHT // 2,
            'vx': vx, 'vy': vy,
            'color': color,
            'lifetime': 3.0 + random.random() * 2.0,
            'max_life': 3.0 + random.random() * 2.0,
            'size': 4 + random.randint(0, 3),
            'spin': random.random() * 360
        })

    # Create floating stars
    for _ in range(20):
        stars.append({
            'x': random.randint(50, SCREEN_WIDTH - 50),
            'y': random.randint(50, SCREEN_HEIGHT - 50),
            'size': random.randint(3, 8),
            'phase': random.random() * math.pi * 2,
            'speed': 0.5 + random.random() * 1.5
        })

    # Firework spawn timer
    firework_timer = 0.0

    # Animation loop
    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        animation_time += dt
        firework_timer += dt

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    return

        # Draw blurred background
        screen.blit(blurred_bg, (0, 0))

        # Dark overlay with fade in
        overlay_alpha = min(180, int(180 * min(1.0, animation_time)))
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, overlay_alpha))
        screen.blit(overlay, (0, 0))

        # Spawn fireworks
        if firework_timer > 0.4 and animation_time < 8.0:
            firework_timer = 0.0
            fw_x = random.randint(100, SCREEN_WIDTH - 100)
            fw_y = SCREEN_HEIGHT
            fireworks.append({
                'x': fw_x, 'y': fw_y,
                'vy': -600 - random.random() * 200,
                'color': random.choice([
                    (255, 100, 100), (100, 255, 100), (100, 100, 255),
                    (255, 255, 100), (255, 100, 255)
                ]),
                'exploded': False,
                'particles': []
            })

        # Update and draw fireworks
        for fw in fireworks[:]:
            if not fw['exploded']:
                fw['y'] += fw['vy'] * dt
                fw['vy'] += 800 * dt  # Gravity

                # Draw rising firework
                for i in range(3):
                    trail_y = fw['y'] + i * 8
                    trail_alpha = 255 - i * 80
                    trail_surf = pygame.Surface((6, 6), pygame.SRCALPHA)
                    pygame.draw.circle(trail_surf, fw['color'], (3, 3), 3)
                    trail_surf.set_alpha(trail_alpha)
                    screen.blit(trail_surf, (int(fw['x'] - 3), int(trail_y - 3)))

                # Explode at peak
                if fw['vy'] > 0:
                    fw['exploded'] = True
                    # Create explosion particles
                    for _ in range(40):
                        angle = random.random() * 2 * math.pi
                        speed = 100 + random.random() * 200
                        fw['particles'].append({
                            'x': fw['x'], 'y': fw['y'],
                            'vx': math.cos(angle) * speed,
                            'vy': math.sin(angle) * speed,
                            'lifetime': 1.5 + random.random(),
                            'max_life': 1.5 + random.random(),
                            'size': 3
                        })
            else:
                # Update explosion particles
                for p in fw['particles']:
                    p['x'] += p['vx'] * dt
                    p['y'] += p['vy'] * dt
                    p['vy'] += 300 * dt  # Gravity
                    p['lifetime'] -= dt

                    if p['lifetime'] > 0:
                        alpha = int(255 * (p['lifetime'] / p['max_life']))
                        surf = pygame.Surface((p['size'] * 2, p['size'] * 2), pygame.SRCALPHA)
                        pygame.draw.circle(surf, fw['color'], (p['size'], p['size']), p['size'])
                        surf.set_alpha(alpha)
                        screen.blit(surf, (int(p['x'] - p['size']), int(p['y'] - p['size'])))

                # Remove dead firework
                fw['particles'] = [p for p in fw['particles'] if p['lifetime'] > 0]
                if not fw['particles']:
                    fireworks.remove(fw)

        # Update and draw confetti
        for p in particles:
            p['x'] += p['vx'] * dt
            p['y'] += p['vy'] * dt
            p['vy'] += 600 * dt  # Gravity
            p['vx'] *= 0.99  # Air resistance
            p['spin'] += 500 * dt
            p['lifetime'] -= dt

            if p['lifetime'] > 0:
                alpha = int(255 * (p['lifetime'] / p['max_life']))

                # Draw rotating rectangle (confetti piece)
                surf = pygame.Surface((p['size'] * 3, p['size'] * 3), pygame.SRCALPHA)
                rect_surf = pygame.Surface((p['size'] * 2, p['size']), pygame.SRCALPHA)
                pygame.draw.rect(rect_surf, p['color'], (0, 0, p['size'] * 2, p['size']))

                # Rotate
                rotated = pygame.transform.rotate(rect_surf, p['spin'])
                rotated.set_alpha(alpha)

                rect = rotated.get_rect(center=(p['size'] * 1.5, p['size'] * 1.5))
                surf.blit(rotated, rect)

                screen.blit(surf, (int(p['x'] - p['size'] * 1.5), int(p['y'] - p['size'] * 1.5)))

        # Draw floating stars
        for star in stars:
            star_alpha = int(128 + 127 * math.sin(animation_time * star['speed'] + star['phase']))

            # Draw 4-pointed star
            points = []
            for i in range(8):
                angle = (i * math.pi / 4)
                radius = star['size'] if i % 2 == 0 else star['size'] / 2
                px = star['x'] + math.cos(angle) * radius
                py = star['y'] + math.sin(angle) * radius
                points.append((px, py))

            star_surf = pygame.Surface((star['size'] * 3, star['size'] * 3), pygame.SRCALPHA)
            offset = star['size'] * 1.5
            adjusted_points = [(p[0] - star['x'] + offset, p[1] - star['y'] + offset) for p in points]
            pygame.draw.polygon(star_surf, (255, 255, 200), adjusted_points)
            star_surf.set_alpha(star_alpha)
            screen.blit(star_surf, (star['x'] - offset, star['y'] - offset))

        # Draw main VICTORY text
        if animation_time < 10.0:
            # Pulsing scale
            scale = 1.0 + 0.15 * math.sin(animation_time * 3)

            # Rainbow color effect
            hue = (animation_time * 50) % 360
            if hue < 60:
                color = (255, int(hue * 4.25), 0)
            elif hue < 120:
                color = (int(255 - (hue - 60) * 4.25), 255, 0)
            elif hue < 180:
                color = (0, 255, int((hue - 120) * 4.25))
            elif hue < 240:
                color = (0, int(255 - (hue - 180) * 4.25), 255)
            elif hue < 300:
                color = (int((hue - 240) * 4.25), 0, 255)
            else:
                color = (255, 0, int(255 - (hue - 300) * 4.25))

            # Fade in
            text_alpha = min(255, int(255 * min(1.0, animation_time / 0.5)))

            font_huge = pygame.font.SysFont("Arial", 96, bold=True)
            text = "VICTORY!"
            text_surf = font_huge.render(text, True, color)

            # Scale
            w, h = text_surf.get_size()
            scaled_surf = pygame.transform.scale(text_surf, (int(w * scale), int(h * scale)))
            scaled_surf.set_alpha(text_alpha)

            # Glow effect
            for glow_size in range(3, 0, -1):
                glow_surf = pygame.transform.scale(text_surf,
                                                   (int(w * scale * (1 + glow_size * 0.02)),
                                                    int(h * scale * (1 + glow_size * 0.02))))
                glow_surf.set_alpha(text_alpha // (glow_size * 2))
                glow_rect = glow_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
                screen.blit(glow_surf, glow_rect)

            # Main text with outline
            rect = scaled_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))

            # Thick black outline
            for dx in [-4, -2, 0, 2, 4]:
                for dy in [-4, -2, 0, 2, 4]:
                    if dx == 0 and dy == 0:
                        continue
                    outline = scaled_surf.copy()
                    outline.fill((0, 0, 0, text_alpha // 2), special_flags=pygame.BLEND_RGBA_MULT)
                    screen.blit(outline, (rect.x + dx, rect.y + dy))

            screen.blit(scaled_surf, rect)

        # Stats box
        if animation_time > 0.8:
            box_alpha = min(255, int(255 * (animation_time - 0.8) / 0.5))

            # Stats background
            stats_w, stats_h = 400, 150
            stats_surf = pygame.Surface((stats_w, stats_h), pygame.SRCALPHA)
            pygame.draw.rect(stats_surf, (20, 20, 40, 200), (0, 0, stats_w, stats_h), border_radius=15)
            pygame.draw.rect(stats_surf, (100, 200, 255, 200), (0, 0, stats_w, stats_h), 3, border_radius=15)
            stats_surf.set_alpha(box_alpha)

            stats_rect = stats_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
            screen.blit(stats_surf, stats_rect)

            # Stats text
            font_medium = pygame.font.SysFont("Arial", 32, bold=True)
            font_small = pygame.font.SysFont("Arial", 24)

            title_surf = font_small.render("LEVEL COMPLETE", True, (150, 220, 255))
            title_surf.set_alpha(box_alpha)
            title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
            screen.blit(title_surf, title_rect)

            dist_surf = font_medium.render(f"{int(player_x)} pixels", True, (255, 255, 255))
            dist_surf.set_alpha(box_alpha)
            dist_rect = dist_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
            screen.blit(dist_surf, dist_rect)

            # Star rating based on distance
            stars_earned = min(3, int(player_x / 4000))
            star_y = SCREEN_HEIGHT // 2 + 120
            for i in range(3):
                star_x = SCREEN_WIDTH // 2 - 50 + i * 50
                star_color = (255, 215, 0) if i < stars_earned else (100, 100, 100)

                # Draw star
                star_points = []
                for j in range(10):
                    angle = (j * math.pi / 5) - math.pi / 2
                    radius = 15 if j % 2 == 0 else 7
                    px = star_x + math.cos(angle) * radius
                    py = star_y + math.sin(angle) * radius
                    star_points.append((px, py))

                pygame.draw.polygon(screen, star_color, star_points)
                pygame.draw.polygon(screen, (255, 255, 255), star_points, 2)

        # Instructions
        if animation_time > 2.0:
            inst_alpha = int(128 + 127 * math.sin(animation_time * 2))
            font_tiny = pygame.font.SysFont("Arial", 18)
            inst_surf = font_tiny.render("Press ESC or ENTER to continue", True, (200, 200, 200))
            inst_surf.set_alpha(inst_alpha)
            inst_rect = inst_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
            screen.blit(inst_surf, inst_rect)

        pygame.display.flip()

    print("Victory animation closed!\n")