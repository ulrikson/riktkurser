from TargetPrice import TargetPrice


class CLI:
    def __init__(self):
        self.target = TargetPrice()

    def run(self):
        mode = input("Mode (single, all): ")

        if mode == "single":
            while True:
                stock = input("Stock: ").upper()

                if stock == "EXIT":
                    break

                self.target.output_single(stock)
        elif mode == "all":
            self.target.output_all()
        else:
            exit()
