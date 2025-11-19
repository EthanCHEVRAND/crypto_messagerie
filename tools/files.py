def create_file(filename, content):
    f = open(filename, "x")
    
    with open(filename, "w") as f:
        f.write(content)

    f = open(filename)
    return f

