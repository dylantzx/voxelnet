if __name__ == "__main__":
    fps_ls = []
    with open("fps.txt", "r") as f:
        for line in f:
            fps_ls.append(float(line))
    
    print(f"Average FPS is {sum(fps_ls)/len(fps_ls):.2f}")