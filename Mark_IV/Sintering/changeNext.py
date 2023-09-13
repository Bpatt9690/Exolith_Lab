import sys

def main():
    directory = "./Exolith_Lab/Mark_IV/Sintering/"
    pause_file_name = "pause.txt"
    num_args = len(sys.argv)
    if num_args == 2:
        if sys.argv[1] == "True":
            with open(directory + pause_file_name, "w") as f:
                f.write("1")
        if sys.argv[1] == "False":
            with open(directory + pause_file_name, "w") as f:
                f.write("0")

if __name__ == "__main__":
    main()