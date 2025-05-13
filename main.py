from src.filesystem import FileSystem

def main():
    fs = FileSystem()
    print("Enter commands (type 'exit' to quit):")
    while True:
        cmd = input(f"{fs.current_directory.get_path()}$ ").strip()
        if cmd == "exit":
            break
        parts = cmd.split()
        if not parts:
            continue
        command = parts[0]
        try:
            if command == "mkdir" and len(parts) == 2:
                fs.mkdir("", parts[1])
            elif command == "touch" and len(parts) == 2:
                fs.touch("", parts[1])
            elif command == "rm" and len(parts) == 2:
                fs.rm(parts[1])
            elif command == "cd" and len(parts) == 2:
                fs.cd(parts[1])
            elif command == "ls" and len(parts) == 1:
                fs.ls()
            elif command == "nwfiletxt" and len(parts) == 2:
                fs.nwfiletxt(parts[1])
            elif command == "appendtxt" and len(parts) == 2:
                fs.appendtxt(parts[1])
            elif command == "editline" and len(parts) >= 4:
                try:
                    line_num = int(parts[2])
                    text = " ".join(parts[3:])
                    fs.editline(parts[1], line_num, text)
                except ValueError:
                    print(f"Error: Invalid line number or arguments")
            elif command == "deline" and len(parts) == 3:
                fs.deline(parts[1], int(parts[2]))
            elif command == "cat" and len(parts) == 2:
                fs.cat(parts[1])
            else:
                print("Invalid command or arguments")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()