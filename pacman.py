import pygame, tasks, random, time ,sys

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)
PACMAN_COLOR = (255, 255, 0)
PACMAN_RADIUS = 30
MOVEMENT_SPEED = 10
POINTS = 0
LETTER_SIZE = 50

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Loot trial")

# Set up Pac-Man
pacman_x, pacman_y = WIDTH // 2, HEIGHT // 2
pacman_angle = 45  # Initial angle

# Access the json file that contains the words
words = tasks.read_json(f'{tasks.JS_PATH}/words')

# Generate a random index
random_index = random.randint(0, len(words))

# Pick a random word
word = words[f'{random_index}']
word_meaning=tasks.defineWord(word)

# Set up letters
split_word = list(word)
print(split_word)

# Set up letters
# Set up letters
letters = [{'x': random.randint(0, WIDTH - LETTER_SIZE), 'y': random.randint(0, HEIGHT - LETTER_SIZE), 'letter': letter}
           for letter in split_word]


# Function to check collisions
def check_collisions():
    global pacman_x, pacman_y
    for letter_info in letters:
        letter_x, letter_y = letter_info['x'], letter_info['y']
        if (pacman_x - letter_x) ** 2 + (pacman_y - letter_y) ** 2 <= (PACMAN_RADIUS + LETTER_SIZE) ** 2:
            letters.remove(letter_info)
            return letter_info['letter']
    return None

# Game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Update Pac-Man position dynamically
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pacman_x -= MOVEMENT_SPEED
            elif event.key == pygame.K_RIGHT:
                pacman_x += MOVEMENT_SPEED
            elif event.key == pygame.K_UP:
                pacman_y -= MOVEMENT_SPEED
            elif event.key == pygame.K_DOWN:
                pacman_y += MOVEMENT_SPEED

    # Check collisions
    collected_letter= check_collisions()
    if collected_letter:
        print(f"You've picked up a {collected_letter}! You have {POINTS} points")

    # Draw background
    screen.fill(BACKGROUND_COLOR)

    # Draw letters
    for letter_info in letters:
        letter_x, letter_y, letter = letter_info['x'], letter_info['y'], letter_info['letter']
        font = pygame.font.Font(None, LETTER_SIZE)
        text = font.render(letter, True, (255, 0, 0))
        screen.blit(text, (letter_x, letter_y))

    # Draw Pac-Man
    pygame.draw.circle(screen, PACMAN_COLOR, (int(pacman_x), int(pacman_y)), PACMAN_RADIUS)
    pygame.draw.polygon(screen, BACKGROUND_COLOR, [(pacman_x, pacman_y)] + [
        (pacman_x + PACMAN_RADIUS * pygame.math.Vector2(1, 0).rotate(pacman_angle + angle).x,
         pacman_y + PACMAN_RADIUS * pygame.math.Vector2(1, 0).rotate(pacman_angle + angle).y)
        for angle in range(-30, 31, 10)
    ])

    # Check if all letters are picked
    if not letters:
        font = pygame.font.SysFont("Arial", 36)
        word_text = font.render(f"Good job. You found {word.upper()}", True, (255, 255, 255))
        screen.blit(word_text, (WIDTH // 2 - word_text.get_width() // 2, HEIGHT // 2 - word_text.get_height() // 2))

        time.sleep(3)
        meaning_text = font.render(f"{word_meaning}", True, (255, 255, 255))
        screen.blit(meaning_text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - meaning_text.get_height() // 2))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(10)
