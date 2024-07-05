import sys
import os
import shutil
import json
from subprocess import PIPE,run

def compiling_games_code(new_games_paths):
    for new_game_path in new_games_paths:  #looping through the new game directories path to be the current directory for compiling
        for root,dirs,files in os.walk(new_game_path): #searching the go files inside each directory
            for file in files:
                if file.endswith(".go"): #compiling the files that ends with ".go"
                    os.chdir(new_game_path)
                    result =run(["go","build", str(os.path.join(new_game_path,file))], stdout=PIPE, stdin=PIPE,universal_newlines=True)
                    print(result)
            break    
        
   

def games_metadata_JSON(game_names,destination_path):
    information_json={'Number of games':len(game_names), 'Games names':game_names}
    with open(os.path.join(destination_path,"JSON_metadata.txt"),"w") as file: #converting the dictionary to the json file
        json.dump(information_json,file)

def copy_games_to_dest(games_dirs,new_games_dirs,source_dir,destination_dir):
    current_directory = os.getcwd()
    new_games_paths= []
    for old_game,new_game in zip(games_dirs,new_games_dirs): #zipping the old and new directory names to get their path corresponding to each other
        old_game_path = os.path.join(current_directory,source_dir,old_game)
        new_game_path = os.path.join(current_directory,destination_dir,new_game)
        new_games_paths.append(new_game_path)
        if os.path.exists(new_game_path): #checking if the new games directories exist to remove them before copying
            shutil.rmtree(new_game_path)
        
        shutil.copytree(old_game_path,new_game_path)
    return new_games_paths

def new_games_dirs(game_dirs):
    
    new_game_dirs= []
    for game_dir in game_dirs:
        new_game_dirs.append(game_dir.replace("_game","")) #Adding the game directory name to the new_game_dirs list after removing "game" from its name
        
    return new_game_dirs

def retrieve_game_dirs(source_dir):
    game_dirs = []
    current_directory = os.getcwd()    # Getting the full path of source directory for walk() method
    source_path = os.path.join(current_directory,source_dir)

    for root,dirs,files in os.walk(source_path):
        for directory in dirs:    #Searching the directories in the source directory
            if "game" in directory: # checking if each directory has the "game" in its name
                game_dirs.append(directory)  #adding the directory containing "game" in its name to the game_dirs list
        break
    return game_dirs

def create_destination_dir(dir_name):

    for root,dirs,files in os.walk("."):
        if dir_name not in dirs:
            os.mkdir(dir_name)   # Creating the new games directory if it does not exist yet.
        break


def main(source_dir, destination_dir): 
    destination_path = os.path.join(os.getcwd(),destination_dir) #the new games directory path 
    create_destination_dir(destination_dir)  #Creating the new games directory
    game_dirs = retrieve_game_dirs(source_dir) #Retrieving the required games directories names form the source directory
    new_game_dirs = new_games_dirs(game_dirs)  #Making the new games directories names
    new_games_paths = copy_games_to_dest(game_dirs,new_game_dirs,source_dir,destination_dir) #Copying the games directories from source to destination directory
    games_metadata_JSON(new_game_dirs,destination_path) #making the json file with information about games
    compiling_games_code(new_games_paths) #Compiling each game code in their directories

if __name__ =='__main__':
    arguments=sys.argv
    if len(arguments) !=3:   # Checking the number of arguments entered
        raise Exception ("Number of arguments should be 3")
    source_original = arguments[1]
    destination_original = arguments[2]

    main(source_original,destination_original) # calling main method