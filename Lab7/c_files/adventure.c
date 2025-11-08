// File: adventure.c
#include <stdio.h>
#include <string.h>

#define MAX_INPUT_LENGTH 100

int main() {
    // --- Game State Variables ---
    char player_input[MAX_INPUT_LENGTH];
    int game_is_running = 1; // Main game loop condition

    // --- Player and Environment Flags ---
    // These boolean-like flags track the state of the world.
    int has_key = 0;
    int has_note = 0;
    int has_book = 0;
    int desk_drawer_open = 0;
    int safe_unlocked = 0;
    int lights_on = 1; // The lights start on
    int player_location = 0; // 0: Library, 1: Hallway

    // --- Game Introduction ---
    printf("======================================\n");
    printf("       ESCAPE THE FORGOTTEN LIBRARY\n");
    printf("======================================\n\n");
    printf("You awake with a start, your head throbbing. You are sitting in a plush armchair in a vast, dusty library.\n");
    printf("The only exit is a large oak door to the north, which appears to be locked.\n");
    printf("The air is still and silent. You need to find a way out.\n\n");
    printf("Type 'help' to see available commands.\n\n");

    // --- Main Game Loop ---
    // This loop continues as long as game_is_running is true (1).
    while (game_is_running) {
        // --- Print Location Description based on current state ---
        if (player_location == 0) { // In the Library
            printf("\n--- You are in the Library ---\n");
            printf("A grand room filled with towering bookshelves. A large **desk** sits in the center.\n");
            printf("To the north is a heavy **door**. A dim **lamp** provides the only light.\n");
            if(has_book) {
                printf("You are holding a heavy leather-bound book.\n");
            }
            if(has_note) {
                printf("You have a crumpled note in your pocket.\n");
            }
            if(has_key) {
                printf("You are holding a small, ornate brass key.\n");
            }
        } else { // In the Hallway
             printf("\n--- You are in the Hallway ---\n");
             printf("You've unlocked the door and stepped into a long, dark hallway. You are free!\n");
             game_is_running = 0; // End the game
             continue; // Skip to the next loop iteration to exit
        }


        // --- Get Player Input ---
        printf("\n> ");
        // fgets is safer than scanf for string input
        if (fgets(player_input, MAX_INPUT_LENGTH, stdin) != NULL) {
            // Remove the newline character that fgets captures
            player_input[strcspn(player_input, "\n")] = 0;
        } else {
            // Handle potential input error
            printf("Error reading input. Exiting.\n");
            break;
        }


        // --- Command Parsing using if/else if/else ---

        // -- Look Commands --
        if (strcmp(player_input, "look") == 0) {
            printf("You are in a large library. There is a desk, bookshelves, a door, and a lamp.\n");
        } else if (strcmp(player_input, "look desk") == 0) {
            printf("The desk is made of dark mahogany. It has a single drawer and a small, locked **safe** built into its side.\n");
            if (desk_drawer_open && !has_note) {
                printf("The drawer is open. Inside is a crumpled **note**.\n");
            } else if (desk_drawer_open) {
                printf("The drawer is open and empty.\n");
            } else {
                 printf("The drawer is closed.\n");
            }
        } else if (strcmp(player_input, "look bookshelves") == 0) {
            printf("Rows upon rows of books, most covered in a thick layer of dust. One **book** with a red cover seems out of place.\n");
        } else if (strcmp(player_input, "look door") == 0) {
            printf("A heavy oak door. It is firmly locked. It has a brass keyhole.\n");
        } else if (strcmp(player_input, "look lamp") == 0) {
             if(lights_on) {
                 printf("A simple desk lamp. It's currently on. You could probably 'turn off lamp'.\n");
             } else {
                  printf("The lamp is off. The room is now pitch black, but you see a faint number glowing on the safe: 852.\n");
             }
        } else if (strcmp(player_input, "look safe") == 0) {
             if(lights_on) {
                 printf("A small metal safe with a three-digit combination lock. It's too bright to see any details on the dial.\n");
             } else {
                  printf("In the dark, you can clearly see glowing numbers on the dial: 8-5-2.\n");
             }
        } 
        
        // -- Get/Take Commands --
        else if (strcmp(player_input, "get note") == 0 || strcmp(player_input, "take note") == 0) {
            if (desk_drawer_open && !has_note) {
                printf("You take the note. It reads: 'The answer reveals itself only in darkness.'\n");
                has_note = 1; // Update player state
            } else {
                printf("There is no note here.\n");
            }
        } else if (strcmp(player_input, "get book") == 0 || strcmp(player_input, "take book") == 0) {
            if (!has_book) {
                printf("You take the red book from the shelf. It's titled 'Principles of Locking Mechanisms'. It seems useless.\n");
                has_book = 1; // Update player state
            } else {
                printf("You already have the book.\n");
            }
        }
        
        // -- Use/Action Commands --
        else if (strcmp(player_input, "open drawer") == 0) {
            if (!desk_drawer_open) {
                printf("You open the desk drawer. You hear a soft click.\n");
                desk_drawer_open = 1; // Update world state
            } else {
                printf("The drawer is already open.\n");
            }
        } else if (strcmp(player_input, "turn off lamp") == 0) {
             if (lights_on) {
                 printf("You switch off the lamp. The room plunges into darkness, unsettlingly quiet.\n");
                 lights_on = 0; // Update world state
             } else {
                 printf("The lamp is already off.\n");
             }
        } else if (strcmp(player_input, "turn on lamp") == 0) {
             if (!lights_on) {
                 printf("You switch the lamp back on. The familiar, dusty room reappears.\n");
                 lights_on = 1; // Update world state
             } else {
                 printf("The lamp is already on.\n");
             }
        } else if (strcmp(player_input, "use key on door") == 0 || strcmp(player_input, "unlock door") == 0) {
            if (has_key) {
                printf("You insert the brass key into the lock. With a satisfying *CLUNK*, the door unlocks!\n");
                printf("You push the door open.\n");
                player_location = 1; // Change location
            } else {
                printf("You don't have a key.\n");
            }
        } else if (strcmp(player_input, "open safe") == 0 || strcmp(player_input, "unlock safe") == 0) {
            printf("You need to enter the combination. Type 'enter code XXX' where XXX is the 3-digit number.\n");
        } else if (strncmp(player_input, "enter code ", 11) == 0) {
            if (safe_unlocked) {
                printf("The safe is already open.\n");
            } else if (strcmp(player_input, "enter code 852") == 0) {
                printf("You dial in 8-5-2. The safe door swings open silently. Inside, you find a small brass **key**!\n");
                safe_unlocked = 1;
                has_key = 1;
            } else {
                printf("Incorrect code. The lock clicks but doesn't open.\n");
            }
        }

        // -- System Commands --
        else if (strcmp(player_input, "help") == 0) {
            printf("\n--- Available Commands ---\n");
            printf("Actions: look, get/take, open, use, enter code, turn on/off\n");
            printf("Objects: desk, bookshelves, door, lamp, note, book, safe, drawer\n");
            printf("Example: 'look desk', 'get note', 'use key on door', 'turn off lamp'\n");
            printf("System: 'help', 'quit'\n");
        } else if (strcmp(player_input, "quit") == 0) {
            printf("You give up and accept your fate as a permanent resident of the library.\n");
            game_is_running = 0; // Set condition to exit loop
        } else {
            printf("I don't understand how to '%s'. Try something else.\n", player_input);
        }
    }

    // --- Game Conclusion ---
    printf("\n======================================\n");
    printf("            THANKS FOR PLAYING!\n");
    printf("======================================\n");

    return 0;
}