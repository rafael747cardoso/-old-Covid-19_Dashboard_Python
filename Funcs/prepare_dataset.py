
import numpy as np
import pandas as pd
import COVID19Py
import pycountry

def prepare_dataset(covid19data,
                    dataset_type,
                    chosen_country):
    
    """
    Divides the original dataset of cases, deaths and recovered, into 5 different dataframes,
    with cases, deaths and recovered in daily and cumulative numbers:
        - Latest data for all countries (one country per row): latest_data_all_countries
        - Latest data for a selected country (one row): latest_data_country
        - Latest data for the world (one row): latest_data_world
        - Time series for a selected country: time_series_country
        - Time series for the world: time_series_world
    """

    # Latest data for all countries, the chosen country and the world:
    if dataset_type in ["latest_data_all_countries", 
                        "latest_data_country",
                        "latest_data_world"]:
        countries_data = covid19data.getLocations(timelines = True)        
        allcountries_latest = []
        for i in range(0, len(countries_data), 1):
            if countries_data[i]["province"] == "Repatriated Travellers":
                continue
            df_country = {"country": countries_data[i]["country"],
                          "country_code": countries_data[i]["country_code"],
                          "country_population": countries_data[i]["country_population"],
                          "latitude": float(countries_data[i]["coordinates"]["latitude"]),
                          "longitude": float(countries_data[i]["coordinates"]["longitude"]),
                          "cases_daily": (list(countries_data[i]["timelines"]["confirmed"]["timeline"].values())[-1] - 
                                          list(countries_data[i]["timelines"]["confirmed"]["timeline"].values())[-2] if
                                          len(countries_data[i]["timelines"]["confirmed"]["timeline"]) > 0 else 0),
                          "deaths_daily": (list(countries_data[i]["timelines"]["deaths"]["timeline"].values())[-1] -
                                          list(countries_data[i]["timelines"]["deaths"]["timeline"].values())[-2] if
                                          len(countries_data[i]["timelines"]["deaths"]["timeline"]) > 0 else 0),
                          "recovered_daily": (list(countries_data[i]["timelines"]["recovered"]["timeline"].values())[-1] -
                                             list(countries_data[i]["timelines"]["recovered"]["timeline"].values())[-2] if
                                             len(countries_data[i]["timelines"]["recovered"]["timeline"]) > 0 else 0),
                          "cases_cumulative": countries_data[i]["latest"]["confirmed"],
                          "deaths_cumulative": countries_data[i]["latest"]["deaths"],
                          "recovered_cumulative": countries_data[i]["latest"]["recovered"]}
            allcountries_latest += [df_country]
        allcountries_latest = pd.DataFrame(allcountries_latest)
        allcountries_latest = allcountries_latest.groupby(["country"]).agg({"country": "first",
                                                                            "country_code": "first",
                                                                            "country_population": "first",
                                                                            "latitude": "mean",
                                                                            "longitude": "mean",
                                                                            "cases_daily": "sum",
                                                                            "deaths_daily": "sum",
                                                                            "recovered_daily": "sum",
                                                                            "cases_cumulative": "sum",
                                                                            "deaths_cumulative": "sum",
                                                                            "recovered_cumulative": "sum"})
        allcountries_latest.index = list(range(0, len(allcountries_latest.values), 1))
        
        if dataset_type == "latest_data_all_countries":
            df = allcountries_latest
            popu = df["country_population"]
            m_pop = 1e6
            df["cases_daily_1e6_pop"] = df["cases_daily"]/popu*m_pop
            df["deaths_daily_1e6_pop"] = df["deaths_daily"]/popu*m_pop
            df["recovered_daily_1e6_pop"] = df["recovered_daily"]/popu*m_pop
            df["cases_cumulative_1e6_pop"] = df["cases_cumulative"]/popu*m_pop
            df["deaths_cumulative_1e6_pop"] = df["deaths_cumulative"]/popu*m_pop
            df["recovered_cumulative_1e6_pop"] = df["recovered_cumulative"]/popu*m_pop
            country_codes = []
            for i in range(0, len(list(pycountry.countries))):
                country_codes += [[list(pycountry.countries)[i].alpha_2,
                                   list(pycountry.countries)[i].alpha_3]]
            country_codes = pd.DataFrame(country_codes,
                                         columns = ["alpha_2", "alpha_3"])
            df = df.merge(country_codes,
                          how = "left",
                          left_on = "country_code",
                          right_on = "alpha_2")

            return(df)

        if dataset_type == "latest_data_country":
            country_latest = allcountries_latest.loc[allcountries_latest["country_code"] == chosen_country, :]
            country_latest.index = [1]
            df = country_latest
            return(df)

        if dataset_type == "latest_data_world":
            world_latest = allcountries_latest
            world_latest["planet"] = "Earth"
            world_latest = allcountries_latest.groupby(["planet"]).agg({"cases_daily": "sum",
                                                                        "deaths_daily": "sum",
                                                                        "recovered_daily": "sum",
                                                                        "cases_cumulative": "sum",
                                                                        "deaths_cumulative": "sum",
                                                                        "recovered_cumulative": "sum"})
            df = world_latest
            return(df)

    # Time series for the chosen country:
    if dataset_type == "time_series_country":
        country_timeseries = covid19data.getLocationByCountryCode(country_code = chosen_country,
                                                                  timelines = True)        
        df = pd.DataFrame({"date": pd.to_datetime(list(country_timeseries[0]["timelines"]["confirmed"]["timeline"].keys()))})
        df["country"] = country_timeseries[0]["country"]
        df["country_code"] = country_timeseries[0]["country_code"]
        df["country_population"] = country_timeseries[0]["country_population"]        
        cases_cum = np.zeros(df.shape[0])
        deaths_cum = np.zeros(df.shape[0])
        recovered_cum = np.zeros(df.shape[0])
        for i in range(0, len(country_timeseries), 1):
            cases_cum = cases_cum + np.array(list(country_timeseries[i]["timelines"]["confirmed"]["timeline"].values()))
            deaths_cum = deaths_cum + np.array(list(country_timeseries[i]["timelines"]["deaths"]["timeline"].values()))
            if(len(np.array(list(country_timeseries[i]["timelines"]["recovered"]["timeline"].values()))) > 0):
                recovered_cum = recovered_cum + np.array(list(country_timeseries[i]["timelines"]["recovered"]["timeline"].values()))
        df["cases_cum"] = cases_cum
        df["deaths_cum"] = deaths_cum
        df["recovered_cum"] = recovered_cum
        df["cases_daily"] = np.append(np.array(cases_cum[0]), 
                                      cases_cum[1:] - cases_cum[:-1])
        df["deaths_daily"] = np.append(np.array(deaths_cum[0]), 
                                       deaths_cum[1:] - deaths_cum[:-1])
        df["recovered_daily"] = np.append(np.array(recovered_cum[0]), 
                                          recovered_cum[1:] - recovered_cum[:-1])
        return(df)

    # Time series for the world:
    if dataset_type == "time_series_world":
        world_timeseries = covid19data.getLocations(timelines = True)
        df = pd.DataFrame({"date": pd.to_datetime(list(world_timeseries[0]["timelines"]["confirmed"]["timeline"].keys()))})
        df["planet"] = "Earth"
        cases_cum = np.zeros(df.shape[0])
        deaths_cum = np.zeros(df.shape[0])
        recovered_cum = np.zeros(df.shape[0])
        for i in range(0, len(world_timeseries), 1):
            cases_cum = cases_cum + np.array(list(world_timeseries[i]["timelines"]["confirmed"]["timeline"].values()))
            deaths_cum = deaths_cum + np.array(list(world_timeseries[i]["timelines"]["deaths"]["timeline"].values()))
            if(len(np.array(list(world_timeseries[i]["timelines"]["recovered"]["timeline"].values()))) > 0):
                recovered_cum = recovered_cum + np.array(list(world_timeseries[i]["timelines"]["recovered"]["timeline"].values()))
        df["cases_cum"] = cases_cum
        df["deaths_cum"] = deaths_cum
        df["recovered_cum"] = recovered_cum
        df["cases_daily"] = np.append(np.array(cases_cum[0]), 
                                      cases_cum[1:] - cases_cum[:-1])
        df["deaths_daily"] = np.append(np.array(deaths_cum[0]), 
                                       deaths_cum[1:] - deaths_cum[:-1])
        df["recovered_daily"] = np.append(np.array(recovered_cum[0]), 
                                          recovered_cum[1:] - recovered_cum[:-1])
        return(df)

