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
            elif command == "cd" and len(parts) == 2:
                fs.cd(parts[1])
            elif command == "ls" and len(parts) == 1:
                fs.ls()
            else:
                print("Invalid command or arguments")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()