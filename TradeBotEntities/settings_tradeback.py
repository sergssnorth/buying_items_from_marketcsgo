class SettingsTradebackForBuyTm:

    def __init__(self,game,steam_week_sales,first_service,second_service,first_service_price_from,
                 first_service_count_from,first_service_procent_from,first_service_procent_before):
        self.game = game
        self.steam_week_sales = steam_week_sales
        self.first_service = first_service
        self.second_service = second_service
        self.first_service_price_from = first_service_price_from
        self.first_service_count_from = first_service_count_from
        self.first_service_procent_from = first_service_procent_from
        self.first_service_procent_before = first_service_procent_before


class SettingsTradebackForBuySteam:

    def __init__(self,game,tm_week_sales,first_service,second_service,first_service_price_from,
                 first_service_count_from,first_service_procent_from,first_service_procent_before):
        self.game = game
        self.tm_week_sales = tm_week_sales
        self.first_service = first_service
        self.second_service = second_service
        self.first_service_price_from = first_service_price_from
        self.first_service_count_from = first_service_count_from
        self.first_service_procent_from = first_service_procent_from
        self.first_service_procent_before = first_service_procent_before

