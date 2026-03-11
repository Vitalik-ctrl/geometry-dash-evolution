# game_engine/stereo_madness.py

def create_stereo_madness_data():
    obstacles = []

    def add_spike(x, y=0):
        obstacles.append({"x": x, "y": y, "w": 30, "h": 30, "type": "spike"})

    def add_block(x, y, w=40, h=40):
        obstacles.append({"x": x, "y": y, "w": w, "h": h, "type": "block"})

    def add_triple_spike(x, y=0):
        add_spike(x)
        add_spike(x + 30)
        add_spike(x + 60)

    # --- SECTION 1: CUBE INTRO ---
    add_spike(600)
    add_spike(850)

    # Staircase challenge
    add_block(1100, 0)
    add_spike(1250)
    add_spike(1280)

    # Double pillar
    add_block(1600, 0)
    add_block(1600, 40)
    add_spike(1850)
    add_spike(1900)

    # Complex stair section
    add_block(2200, 0)
    add_block(2240, 40)
    add_block(2280, 80)
    add_spike(2320, 80)
    add_block(2400, 80)
    add_block(2440, 40)
    add_block(2480, 0)

    # Spike gauntlet
    add_spike(2700)
    add_spike(2760)
    add_block(2850, 0, w=100)
    add_spike(2960)
    add_block(3100, 0, w=100)

    # --- SECTION 2: SHIP MODE ---
    obstacles.append({"x": 3500, "y": 100, "w": 50, "h": 80, "type": "portal_ship"})

    start_ship = 3800

    # Wave pattern ceiling/floor obstacles
    for i in range(6):
        x_pos = start_ship + i * 250
        if i % 2 == 0:
            # Ceiling obstacle
            add_block(x_pos, 250, w=80, h=200)
        else:
            # Floor obstacle
            add_block(x_pos, 0, w=80, h=120)

    # Narrow gates (must fly through middle)
    gate_x = start_ship + 1400
    add_block(gate_x, 0, w=50, h=100)
    add_block(gate_x, 200, w=50, h=250)

    gate_x2 = start_ship + 1700
    add_block(gate_x2, 0, w=50, h=130)
    add_block(gate_x2, 220, w=50, h=250)

    # --- SECTION 3: RETURN TO CUBE ---
    end_ship = start_ship + 2000
    obstacles.append({"x": end_ship, "y": 100, "w": 50, "h": 80, "type": "portal_cube"})

    # Triple spike boss
    ts_x = end_ship + 400
    add_triple_spike(ts_x)

    # Platform jumps
    add_block(ts_x + 400, 0, w=60)
    add_spike(ts_x + 500)
    add_block(ts_x + 600, 40, w=60)
    add_spike(ts_x + 700, 40)
    add_block(ts_x + 800, 0, w=60)

    # Spike valley
    for i in range(2):
        add_spike(ts_x + 1000 + i * 40)

    # --- SECTION 4: FINAL ---
    final_x = ts_x + 1400

    # Alternating platforms
    for i in range(6):
        x_pos = final_x + i * 200
        height = (i % 3) * 40
        add_block(x_pos, height, w=80)
        if i < 5:
            add_spike(x_pos + 120, height)

    # Second ship section (short)
    ship2_x = final_x + 1400
    obstacles.append({"x": ship2_x, "y": 100, "w": 50, "h": 80, "type": "portal_ship"})

    # Tight ship tunnel
    for i in range(6):
        x_pos = ship2_x + 300 + i * 200
        add_block(x_pos, 0, w=60, h=90)
        add_block(x_pos, 240, w=60, h=200)

    # Back to cube for finale
    cube2_x = ship2_x + 1500
    obstacles.append({"x": cube2_x, "y": 100, "w": 50, "h": 80, "type": "portal_cube"})

    # Final cube section - THE WALL
    final_section = cube2_x + 300

    # Triple spike lines
    for row in range(2):
        add_triple_spike(final_section + 200 + row * 150)

    # Platform maze
    add_block(final_section + 700, 0, w=100)
    add_block(final_section + 850, 40, w=100)
    add_block(final_section + 1000, 80, w=100)
    add_spike(final_section + 1150, 80)
    add_block(final_section + 1250, 40, w=100)
    add_block(final_section + 1400, 0, w=100)

    # Victory spikes (final challenge)
    victory_x = final_section + 1600
    for i in range(8):
        if i % 2 == 0:
            add_spike(victory_x + i * 45)

    # FINISH LINE (Platform to celebrate)
    add_block(victory_x + 500, 0, w=600, h=40)

    return obstacles