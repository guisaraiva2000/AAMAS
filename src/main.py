from clean_waters import CleanWaters


if __name__ == "__main__":
    cw = CleanWaters()

    while cw.running:
        cw.initiate()
        cw.main_loop()
