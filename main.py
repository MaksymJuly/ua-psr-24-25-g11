#!/usr/bin/env python3

import argparse
from readchar import readkey
from collections import namedtuple

import random
from random_word import RandomWords

from colorama import Fore, Style, init
from pprint import pprint

from time import time, ctime
import os
import sys

init()

InputData = namedtuple('Input', ['requested', 'received', 'duration'])
results_list = []


def interruption_handel():
    print("\nGoodbye!")
    sys.exit(0)

def setup_arg():
    os.system('clear')
    parser = argparse.ArgumentParser(description=f'Definition of {Fore.BLUE}test{Style.RESET_ALL} mode',
                                     add_help=False)
    
    parser.add_argument('-h','--help',
                        action="help",
                        help=f'show this {Fore.BLUE}help{Style.RESET_ALL} message and {Fore.BLUE}exit{Style.RESET_ALL}')

    # Game mode options
    parser.add_argument('-utm', '--use_time_mode',
                        metavar=Fore.LIGHTBLACK_EX +'TIME_IN_SEC'+ Style.RESET_ALL,
                        type=int,
                        default=0,
                        help=f'Use this argument for {Fore.GREEN}time mode{Style.RESET_ALL} challange.')
    
    parser.add_argument('-uim', '--use_input_mode',
                        metavar=Fore.LIGHTBLACK_EX +'NUM_OF_INPUTS'+ Style.RESET_ALL,
                        type=int,
                        default=0,
                        help=f'Use this argument for {Fore.GREEN}input mode{Style.RESET_ALL} challange.')
    
    parser.add_argument('-uw', '--use_words',
                        metavar='',
                        default='letters',
                        help=f'Use this argument for {Fore.GREEN}random words{Style.RESET_ALL} typing challange.')
    
    arg = parser.parse_args()

    arg.use_time_mode = abs(arg.use_time_mode)
    arg.use_input_mode = abs(arg.use_input_mode)

    # Vanila mode [-uim: letters-10, words-5]
    if arg.use_time_mode == 0 and arg.use_input_mode == 0:
        arg.use_input_mode = 10 if arg.use_words == 'letters' else 5
    
    if arg.use_input_mode != 0:
        arg.mode = 'Input-based'
        arg.lim = arg.use_input_mode
    else:
        arg.mode = 'Time-based'
        arg.lim = arg.use_time_mode

    print(f'\n{Fore.YELLOW}Starting {arg.mode} Typing Game!{Fore.RESET}')
    print(f'Input Type: {arg.use_words.capitalize()}')
    lim_inf = 'inputs' if arg.mode == 'Input-based' else 'seconds'
    print(f'Limit: {arg.lim} {lim_inf}')

    input(Fore.CYAN + "Press Enter to begin..." + Fore.RESET)
    print('\n')

    return arg

def letters_game(lim, mode):
    start_time = time()
    correct_count, total_count = 0, 0
    total_time, correct_time, incorrect_time = 0, 0, 0

    while True:
        random_letter = chr(random.randint(97, 122)) # Random letter
        print(f"\nType the letter: {Fore.YELLOW}{random_letter}{Fore.RESET}")
        input_start_time = time()
        user_input = readkey()
        input_end_time = time()
        time_taken = input_end_time - input_start_time
        
        if user_input == ' ':
            interruption_handel() # Leads to the interruption when the user presses the "space"

        results_list.append(InputData(requested=random_letter, received=user_input, duration=time_taken))

        if user_input.lower() == random_letter:
            print(f'You typed letter: {Fore.GREEN}{user_input.lower()}{Fore.RESET}')
            correct_count += 1
            correct_time += time_taken
        else:
            print(f'You typed letter: {Fore.RED}{user_input.lower()}{Fore.RESET}')
            incorrect_time += time_taken

        total_count += 1
        total_time += time_taken

        # Game ending conditions
        if mode == 'Input-based' and total_count >= lim:
            break
        elif mode == 'Time-based' and (time() - start_time) >= lim:
            break

    display_result(total_count, correct_count, total_time, correct_time, incorrect_time, start_time)

def words_game(lim, mode):
    pass

def display_result(total_inputs, correct_inputs, total_duration, correct_duration, incorrect_duration, start_time):
    accuracy = (correct_inputs / total_inputs) * 100 if total_inputs > 0 else 0
    average_duration = total_duration / total_inputs if total_inputs > 0 else 0
    average_correct_duration = correct_duration / correct_inputs if correct_inputs > 0 else 0
    incorrect_count = total_inputs - correct_inputs
    average_incorrect_duration = incorrect_duration / incorrect_count if incorrect_count > 0 else 0

    result = {
        'accuracy': accuracy,
        'inputs': results_list,
        'number_of_hits': correct_inputs,
        'number_of_types': total_inputs,
        'test_duration': total_duration,
        'test_end': ctime(time()),
        'test_start': ctime(start_time),
        'type_average_duration': average_duration,
        'type_hit_average_duration': average_correct_duration,
        'type_miss_average_duration': average_incorrect_duration
    }

    print("\n" + Fore.MAGENTA + "Game Summary:" + Fore.RESET)
    pprint(result)

def main():
    arg = setup_arg()

    # Start game 
    if arg.use_words == 'letters':
        letters_game(arg.lim, arg.mode)
    else:
        words_game(arg.lim, arg.mode)


if __name__ == "__main__":
    main()