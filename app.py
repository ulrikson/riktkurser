from statistics import mode
import requests
import datetime
import json


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


class TargetPrice:
    def __init__(self):
        self.old_analysis_count = 0
        self.analysis_count = 0

    def output_single(self, stock):
        for analysis in self.__get_stock_data(stock):
            if self.analysis_count < 20:
                text = self.__generate_text(analysis, mode="single")
                print(text)
                self.analysis_count += 1

        self.old_analysis_count = 0
        self.analysis_count = 0

    def output_all(self):
        file = open("stocks.json")
        stocks = json.load(file)["stocks"]

        print()

        for stock in stocks:
            print("##### " + stock + " #####")
            for count, analysis in enumerate(self.__get_stock_data(stock)):
                if count < 5:
                    text = self.__generate_text(analysis, "all")
                    print(text)
                
            print("\n")

    def __get_stock_data(self, stock):
        url = "https://www.borskollen.se/api/feed/targetprices/tags/" + stock

        response = requests.get(url)
        json = response.json()

        data = json["items"]

        return data

    def __generate_text(self, analysis, mode):
        date = self.__get_date(analysis, mode)
        title = self.__get_title(analysis)

        text = date + " " + title

        return text

    def __get_date(self, analysis, mode):
        date = analysis["pubDateUtc"].split(" ")[0]
        date_datetime = datetime.datetime.strptime(date, "%Y-%m-%d")

        breakpoint = datetime.datetime.now() - datetime.timedelta(days=45)
        separate_old_analysis = (
            date_datetime < breakpoint and self.old_analysis_count == 0
        )

        if separate_old_analysis and mode == "single":
            self.old_analysis_count += 1
            print("\n")

        return date

    def __get_title(self, analysis):
        title = analysis["title"]
        words_to_remove = ["FLASH:", "- BN"]

        for word in words_to_remove:
            title = title.replace(word, "")

        return title


CLI().run()
