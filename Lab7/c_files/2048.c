#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h> // For usleep/system("clear")

// A single function containing the entire 2048 game logic.
int main() {
    // --- 1. SETUP AND INITIALIZATION ---
    srand(time(NULL));

    // The 4x4 game grid (using a static array for simplicity within main)
    int playGround[4][4] = {{0}}; 
    int i, j, k, row, col;
    int command;
    int moved;
    int prev_state[4][4];
    int max_tile;
    int is_valid_game;

    // Helper macro to generate a new tile value: 4 (10% chance) or 2 (90% chance)
    #define GENERATE_TILE (rand() % 10 == 0 ? 4 : 2)

    // --- Welcome Message ---
    printf("Welcome to the 2048 Monolithic C Game.\n");
    printf("Controls: 1 (Up) | 2 (Down) | 3 (Left) | 4 (Right)\n");
    printf("Press 1 to begin...");
    scanf("%d", &i); // Use i temporarily for input buffer clear
    while (getchar() != '\n'); // Clear input buffer
    system("clear");

    // --- Initial Board Setup (equivalent to init()) ---
    int coord = rand() % 16;
    int x = coord / 4; 
    int y = coord % 4; 
    playGround[x][y] = GENERATE_TILE;

    // --- MAIN GAME LOOP ---
    while (1) {

        // --- Inline printMat() Logic ---
        printf("\n\033[0;36m┌");
        for (j = 0; j < 4; j++) {
            printf("─────");
            if (j < 3) printf("┬");
        }
        printf("┐\033[0m\n");

        for (i = 0; i < 4; i++) {
            printf("\033[0;36m│\033[0m");
            for (j = 0; j < 4; j++) {
                int val = playGround[i][j];
                if (val == 0) {
                    printf("     ");
                } else {
                    // Apply color based on tile value
                    switch (val) {
                        case 2:    printf("\033[0;32m"); break;   // Green
                        case 4:    printf("\033[0;34m"); break;   // Blue
                        case 8:    printf("\033[0;33m"); break;   // Yellow
                        case 16:   printf("\033[0;35m"); break;   // Magenta
                        case 32:   printf("\033[0;36m"); break;   // Cyan
                        case 64:   printf("\033[0;31m"); break;   // Red
                        case 128:  printf("\033[1;32m"); break;   // Bright Green
                        case 256:  printf("\033[1;34m"); break;   // Bright Blue
                        case 512:  printf("\033[1;33m"); break;   // Bright Yellow
                        case 1024: printf("\033[1;35m"); break;   // Bright Magenta
                        case 2048: printf("\033[1;36m"); break;   // Bright Cyan (Win condition)
                        default:   printf("\033[0;37m"); break;   // White/Default
                    }
                    printf(" %4d", val);
                    printf("\033[0m");
                }
                printf("\033[0;36m│\033[0m");
            }
            printf("\n");
            if (i < 3) {
                printf("\033[0;36m├");
                for (j = 0; j < 4; j++) {
                    printf("─────");
                    if (j < 3) printf("┼");
                }
                printf("┤\033[0m\n");
            }
        }
        printf("\033[0;36m└");
        for (j = 0; j < 4; j++) {
            printf("─────");
            if (j < 3) printf("┴");
        }
        printf("┘\033[0m\n\n");


        // --- Inline maxElem() Logic ---
        max_tile = 0;
        for (i = 0; i < 4; i++) {
            for (j = 0; j < 4; j++) {
                if (playGround[i][j] > max_tile) {
                    max_tile = playGround[i][j];
                }
            }
        }

        // --- Inline isValid() Logic (Game Over Check) ---
        is_valid_game = 0;
        for(i = 0; i < 4; i++){
            for(j = 0; j < 4; j++){
                if(playGround[i][j] == 0) is_valid_game = 1; // Empty tile exists
                // Check right for merge
                if (j < 3 && playGround[i][j] == playGround[i][j+1]) is_valid_game = 1;
                // Check down for merge
                if (i < 3 && playGround[i][j] == playGround[i+1][j]) is_valid_game = 1;
            }
        }

        // --- Win/Loss Check ---
        if (max_tile >= 2048) {
            printf("\n\n\033[1;36m*** YOU WIN! HIT %d! ***\033[0m\n", max_tile);
            break;
        }
        if (!is_valid_game) {
            printf("\n\n\033[1;31m*** GAME OVER! No more moves possible. ***\033[0m\n");
            printf("Final Max Tile: %d\n", max_tile);
            break;
        }

        printf("Current Max Tile: %d\n", max_tile);
        printf("Enter Command: 1 MoveUp | 2 MoveDown | 3 MoveLeft | 4 MoveRight\n> ");
        
        if (scanf("%d", &command) != 1) {
            printf("\n\033[0;31mInvalid input type! Try 1, 2, 3, or 4.\033[0m\n");
            while (getchar() != '\n'); // Clear input buffer
            usleep(1000000); // 1 second pause
            system("clear");
            continue;
        }
        while (getchar() != '\n'); // Clear input buffer

        // Copy current state to detect movement
        for (i = 0; i < 4; i++) {
            for (j = 0; j < 4; j++) {
                prev_state[i][j] = playGround[i][j];
            }
        }
        moved = 0;


        // --- MOVEMENT LOGIC (Large Switch Block) ---

        switch (command) {
            case 1: // MoveUp Logic (col by col)
                for (col = 0; col < 4; col++) {
                    // Step 1: Shift non-zero values upwards
                    for (row = 0; row < 4; row++) {
                        if (playGround[row][col] == 0) {
                            for (k = row + 1; k < 4; k++) {
                                if (playGround[k][col] != 0) {
                                    playGround[row][col] = playGround[k][col];
                                    playGround[k][col] = 0;
                                    break;
                                }
                            }
                        }
                    }
                    // Step 2: Merge adjacent equal tiles
                    for (row = 0; row < 3; row++) {
                        if (playGround[row][col] != 0 && playGround[row][col] == playGround[row + 1][col]) {
                            playGround[row][col] *= 2;
                            playGround[row + 1][col] = 0;
                        }
                    }
                    // Step 3: Shift again to remove any gaps from merging
                    for (row = 0; row < 4; row++) {
                        if (playGround[row][col] == 0) {
                            for (k = row + 1; k < 4; k++) {
                                if (playGround[k][col] != 0) {
                                    playGround[row][col] = playGround[k][col];
                                    playGround[k][col] = 0;
                                    break;
                                }
                            }
                        }
                    }
                }
                break;

            case 2: // MoveDown Logic (col by col)
                for (col = 0; col < 4; col++) {
                    // Step 1: Shift non-zero values downwards
                    for (row = 3; row >= 0; row--) {
                        if (playGround[row][col] == 0) {
                            for (k = row - 1; k >= 0; k--) {
                                if (playGround[k][col] != 0) {
                                    playGround[row][col] = playGround[k][col];
                                    playGround[k][col] = 0;
                                    break;
                                }
                            }
                        }
                    }
                    // Step 2: Merge adjacent equal tiles
                    for (row = 3; row > 0; row--) {
                        if (playGround[row][col] != 0 && playGround[row][col] == playGround[row - 1][col]) {
                            playGround[row][col] *= 2;
                            playGround[row - 1][col] = 0;
                        }
                    }
                    // Step 3: Shift again to remove any gaps from merging
                    for (row = 3; row >= 0; row--) {
                        if (playGround[row][col] == 0) {
                            for (k = row - 1; k >= 0; k--) {
                                if (playGround[k][col] != 0) {
                                    playGround[row][col] = playGround[k][col];
                                    playGround[k][col] = 0;
                                    break;
                                }
                            }
                        }
                    }
                }
                break;

            case 3: // MoveLeft Logic (row by row)
                for (row = 0; row < 4; row++) {
                    // Step 1: Shift non-zero values to the left
                    for (col = 0; col < 4; col++) {
                        if (playGround[row][col] == 0) {
                            for (k = col + 1; k < 4; k++) {
                                if (playGround[row][k] != 0) {
                                    playGround[row][col] = playGround[row][k];
                                    playGround[row][k] = 0;
                                    break;
                                }
                            }
                        }
                    }
                    // Step 2: Merge adjacent equal tiles
                    for (col = 0; col < 3; col++) {
                        if (playGround[row][col] != 0 && playGround[row][col] == playGround[row][col+1]) {
                            playGround[row][col] *= 2;
                            playGround[row][col+1] = 0;
                        }
                    }
                    // Step 3: Shift again to remove any gaps from merging
                    for (col = 0; col < 4; col++) {
                        if (playGround[row][col] == 0) {
                            for (k = col + 1; k < 4; k++) {
                                if (playGround[row][k] != 0) {
                                    playGround[row][col] = playGround[row][k];
                                    playGround[row][k] = 0;
                                    break;
                                }
                            }
                        }
                    }
                }
                break;

            case 4: // MoveRight Logic (row by row)
                for (row = 0; row < 4; row++) {
                    // Step 1: Shift non-zero values to the right
                    for (col = 3; col >= 0; col--) {
                        if (playGround[row][col] == 0) {
                            for (k = col - 1; k >= 0; k--) {
                                if (playGround[row][k] != 0) {
                                    playGround[row][col] = playGround[row][k];
                                    playGround[row][k] = 0;
                                    break;
                                }
                            }
                        }
                    }
                    // Step 2: Merge adjacent equal tiles
                    for (col = 3; col > 0; col--) {
                        if (playGround[row][col] != 0 && playGround[row][col] == playGround[row][col-1]) {
                            playGround[row][col] *= 2;
                            playGround[row][col-1] = 0;
                        }
                    }
                    // Step 3: Shift again to remove any gaps from merging
                    for (col = 3; col >= 0; col--) {
                        if (playGround[row][col] == 0) {
                            for (k = col - 1; k >= 0; k--) {
                                if (playGround[row][k] != 0) {
                                    playGround[row][col] = playGround[row][k];
                                    playGround[row][k] = 0;
                                    break;
                                }
                            }
                        }
                    }
                }
                break;
            default:
                printf("\n\033[0;31mInvalid command! Please use 1, 2, 3, or 4.\033[0m\n");
                usleep(1000000); // 1 second pause
                system("clear");
                continue; // Restart the loop without processing move/new tile
        }


        // --- Check for Board Change ---
        for (i = 0; i < 4; i++) {
            for (j = 0; j < 4; j++) {
                if (prev_state[i][j] != playGround[i][j]) {
                    moved = 1;
                    break;
                }
            }
            if (moved) break;
        }
        
        // --- Inline addNewNum() Logic ---
        if (moved) {
            int empty_positions[16];
            int counter = 0;

            // Collect empty positions
            for (i = 0; i < 4; i++) {
                for (j = 0; j < 4; j++) {
                    if (playGround[i][j] == 0) {
                        empty_positions[counter] = i * 4 + j; 
                        counter++;
                    }
                }
            }

            // Place new tile if an empty spot exists
            if (counter > 0) {
                int random_index = rand() % counter;
                int random_position = empty_positions[random_index];
                x = random_position / 4; 
                y = random_position % 4; 
                playGround[x][y] = GENERATE_TILE;
            }
        } else {
             printf("\n\033[0;33mNo tiles moved or merged. Try a different direction.\033[0m\n");
             usleep(1500000); // 1.5 seconds pause
        }

        system("clear");
    }
    
    // Game is over, print the final board state one last time
    // (The printMat logic is copied here to display the final board clearly)
    // printf("\n\033[0;36m┌");
    // for (j = 0; j < 4; j++) {
    //     printf("─────");
    //     if (j < 3) printf("┬");
    // }
    // printf("┐\033[0m\n");

    // for (i = 0; i < 4; i++) {
    //     printf("\033[0;36m│\033[0m");
    //     for (j = 0; j < 4; j++) {
    //         int val = playGround[i][j];
    //         if (val == 0) {
    //             printf("     ");
    //         } else {
    //             switch (val) {
    //                 case 2:    printf("\033[0;32m"); break;
    //                 case 4:    printf("\033[0;34m"); break;
    //                 case 8:    printf("\033[0;33m"); break;
    //                 case 16:   printf("\033[0;35m"); break;
    //                 case 32:   printf("\033[0;36m"); break;
    //                 case 64:   printf("\033[0;31m"); break;
    //                 case 128:  printf("\033[1;32m"); break;
    //                 case 256:  printf("\033[1;34m"); break;
    //                 case 512:  printf("\033[1;33m"); break;
    //                 case 1024: printf("\033[1;35m"); break;
    //                 case 2048: printf("\033[1;36m"); break;
    //                 default:   printf("\033[0;37m"); break;
    //             }
    //             printf(" %4d", val);
    //             printf("\033[0m");
    //         }
    //         printf("\033[0;36m│\033[0m");
    //     }
    //     printf("\n");
    //     if (i < 3) {
    //         printf("\033[0;36m├");
    //         for (j = 0; j < 4; j++) {
    //             printf("─────");
    //             if (j < 3) printf("┼");
    //         }
    //         printf("┤\033[0m\n");
    //     }
    // }
    // printf("\033[0;36m└");
    // for (j = 0; j < 4; j++) {
    //     printf("─────");
    //     if (j < 3) printf("┴");
    // }
    // printf("┘\033[0m\n\n");

    return 0;
}