import os
import pygame

CELL_SIZE = 7
DELAY_DECAY = 0.8
DELAY_INIT_MS = 1000
DELAY_MIN_MS = 200
END_ANIMATION_DELAY_MS = 5000
EXTRA_FRAMES_AFTER_COMPLETION = 10
    
class Visualizable:
    REMOVAL_TIME_TO_COLOR = {
        5: (255, 0, 255),
        4: (200, 0, 200),
        3: (150, 0, 150),
        2: (100, 0, 100),
        1: (50, 0, 50),
    }

    def draw_map(map_obj, screen):
        for x in range(map_obj.height):
            for y in range(map_obj.width):
                color = (0,0,0) 
                map_cell =map_obj.get(x, y)
                if map_cell.removal_time:
                    color = Visualizable.REMOVAL_TIME_TO_COLOR.get(map_cell.removal_time, (255, 255, 255))
                    map_cell.removal_time -= 1
                elif map_cell.is_paper:
                    color = (0, 255, 0)
                
                pygame.draw.rect(screen, color,
                    (y*CELL_SIZE, x*CELL_SIZE, CELL_SIZE, CELL_SIZE))


    def visualize_pygame(map_obj, frame_action=lambda: None):
        pygame.init()
        screen = pygame.display.set_mode((map_obj.width * CELL_SIZE, map_obj.height * CELL_SIZE))

        running = True
        action_results = 0
        frame_delay = DELAY_INIT_MS
        extra_frames_after_completion = EXTRA_FRAMES_AFTER_COMPLETION

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            Visualizable.draw_map(map_obj, screen)
            pygame.display.flip()
            pygame.time.delay(frame_delay)

            if frame_delay > DELAY_MIN_MS:
                frame_delay = int(frame_delay * DELAY_DECAY)
                if frame_delay < DELAY_MIN_MS:
                    frame_delay = DELAY_MIN_MS

            action_result = frame_action()
            action_results += action_result
            if not action_result:
                while extra_frames_after_completion:
                    Visualizable.draw_map(map_obj, screen)
                    pygame.display.flip()
                    pygame.time.delay(frame_delay)
                    extra_frames_after_completion -= 1
                running = False
                pygame.time.delay(END_ANIMATION_DELAY_MS)

        pygame.quit()
        return action_results


    def console_display(map_obj):
        os.system("clear")  # or "cls" on Windows
        for x in range(map_obj.height):
            row = ""
            for y in range(map_obj.width):
                cell = map_obj.get(x, y)
                if cell.is_paper:
                    row += "\033[92m@\033[0m"   # green @
                else:
                    row += "."
            print(row)
