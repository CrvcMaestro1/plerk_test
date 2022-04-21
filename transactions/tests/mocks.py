from transactions import models


class MockSummary(models.Summary):

    def company_highest_sales(self):
        return {"name": "Rappi", "sales": 564}

    def company_least_sales(self):
        return {"name": "Supercell videogame", "sales": 1}

    def number_cashed_transactions(self):
        return 1842

    def number_not_cashed_transactions(self):
        return 849

    def company_most_rejections(self):
        return {"name": "Uber eats", "rejections": 205}

    def get_summary(self):
        return {
            "highest_sales": self.company_highest_sales(),
            "least_sales": self.company_least_sales(),
            "number_cashed_transactions": self.number_cashed_transactions(),
            "number_not_cashed_transactions": self.number_not_cashed_transactions(),
            "most_rejections": self.company_most_rejections(),
        }
