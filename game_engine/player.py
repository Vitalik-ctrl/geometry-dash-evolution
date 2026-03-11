# game_engine/player.py

from .config import *

class Player:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.vy = 0.0
        self.on_ground = True
        self.dead = False
        self.jump_count = 0
        self.rotation = 0.0
        self.mode = "cube"

        self.prev_jump_command = False

    def update(self, dt, jump_command, obstacles):
        if self.dead:
            return

        self.x += PLAYER_SPEED * dt

        if self.mode == "cube":
            # gravity always
            self.vy += GRAVITY * dt

            if jump_command and self.on_ground:
                self.vy = JUMP_FORCE
                self.on_ground = False
                self.jump_count += 1

        elif self.mode == "ship":
            SHIP_GRAVITY = 800.0
            SHIP_THRUST = -1200.0

            if jump_command:
                self.vy += SHIP_THRUST * dt
            else:
                self.vy += SHIP_GRAVITY * dt

            if jump_command and not self.prev_jump_command:
                self.jump_count += 1
            self.prev_jump_command = jump_command

        if self.vy > TERMINAL_VELOCITY:
            self.vy = TERMINAL_VELOCITY
        elif self.vy < -TERMINAL_VELOCITY:
            self.vy = -TERMINAL_VELOCITY

        self.y -= self.vy * dt

        # floor
        if self.y <= 0:
            self.y = 0
            self.vy = 0
            self.on_ground = (self.mode == "cube")

        max_y = SCREEN_HEIGHT - FLOOR_HEIGHT - PLAYER_SIZE
        if self.y > max_y:
            self.dead = True
            return

        if self.mode == "cube" and self.y > 0:
            self.on_ground = False


        if self.mode == "cube":
            if not self.on_ground:
                self.rotation -= 360.0 * dt
            else:
                self.rotation = round(self.rotation / 90.0) * 90.0
        else:
            tilt = -self.vy * 0.05
            if tilt < -45:
                tilt = -45
            if tilt > 45:
                tilt = 45
            self.rotation = tilt

        px1 = self.x
        py1 = self.y
        px2 = self.x + PLAYER_SIZE
        py2 = self.y + PLAYER_SIZE

        for obs in obstacles:
            t = obs["type"]
            if t not in ("portal_ship", "portal_cube"):
                continue

            ox = obs["x"]
            ow = obs["w"]

            if (px2 > ox) and (px1 < ox + ow):
                if t == "portal_ship":
                    self.mode = "ship"
                    self.on_ground = False
                    self.prev_jump_command = False
                    # self.vy = 0
                    # print(f"[PORTAL] ship at x={self.x:.1f}")
                else:
                    self.mode = "cube"
                    self.rotation = 0.0
                    self.on_ground = False
                    self.prev_jump_command = False
                    # self.vy = 0
                    # print(f"[PORTAL] cube at x={self.x:.1f}")

        for obs in obstacles:
            t = obs["type"]
            if t in ("portal_ship", "portal_cube"):
                continue

            ox = obs["x"]
            oy = obs["y"]
            ow = obs["w"]
            oh = obs["h"]

            if ox > px2 + 200:
                continue
            if ox + ow < px1 - 200:
                continue

            if not ((px2 > ox) and (px1 < ox + ow) and (py2 > oy) and (py1 < oy + oh)):
                continue

            if t == "spike":
                self.dead = True
                return

            if t == "block":
                if self.mode == "cube":
                    top = oy + oh
                    if (self.vy >= 0) and (self.y - top > -15):
                        self.y = top
                        self.vy = 0
                        self.on_ground = True
                    else:
                        self.dead = True
                        return
                else:
                    self.dead = True
                    return

    def get_render_data(self):
        return self.x, self.y, self.rotation
