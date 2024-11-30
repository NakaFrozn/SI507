import numpy as np
import json
import os
import random
import matplotlib.pyplot as plt
from matplotlib.path import Path
import requests
import pandas as pd
import re
from collections import Counter
import unittest

random.seed(17)


class DetroitDistrict:
    """
    A class representing a district in Detroit with attributes related to historical redlining.
    coordinates,holcGrade,holcColor,id,description should be load from the redLine data file
    if cache is not available

    Parameters
    ------------------------------
    coordinates : list of lists, 2D List, not list of list of list
        Coordinates defining the district boundaries from the json file
        Note that some districts are non-contiguous, which may
        effect the structure of this attribute

    holcGrade : str
        The HOLC grade of the district.

    id : str
        The identifier for the district, the HOLC ID.

    description : str, optional
        Qualitative description of the district.

    holcColor : str, optional
        A string represent the color of the holcGrade of the district

    randomLat : float, optional
        A random latitude within the district (default is None).

    randomLong : float, optional
        A random longitude within the district (default is None).

    medIncome : int, optional
        Median household income for the district, to be filled later (default is None).

    censusTract : str, optional
        Census tract code for the district (default is None).


    Attributes
    ------------------------------
    self.coordinates
    self.holcGrade
    holcColor : str
        The color representation of the HOLC grade.
        • Districts with holc grade A should be assigned the color 'darkgreen'
        • Districts with holc grade B should be assigned the color 'cornflowerblue'
        • Districts with holc grade C should be assigned the color 'gold'
        • Districts with holc grade D should be assigned the color 'maroon'
        If there is no input for holcColor, it should be generated based on the holcGrade and the rule above.

    self.id
    self.description
    self.randomLat
    self.randomLong
    self.medIncome
    self.censusTract


    """

    def __init__(
        self,
        coordinates,
        holcGrade,
        id,
        description,
        holcColor=None,
        randomLat=None,
        randomLong=None,
        medIncome=None,
        censusTract=None,
        rank=None,
        percent=None,
    ):
        self.coordinates = coordinates
        self.holcGrade = holcGrade
        self.id = id
        self.description = description
        if holcColor:
            self.holcColor = holcColor
        else:
            if holcGrade == "A":
                self.holcColor = "darkgreen"
            elif holcGrade == "B":
                self.holcColor = "cornflowerblue"
            elif holcGrade == "C":
                self.holcColor = "gold"
            elif holcGrade == "D":
                self.holcColor = "maroon"
        self.randomLat = randomLat
        self.randomLong = randomLong
        self.medIncome = medIncome
        self.censusTract = censusTract
        self.rank = rank
        self.percent = percent


class RedLines:
    """
    A class to manage and analyze redlining district data.

    Attributes
    ----------
    districts : list of DetroitDistrict
        A list to store instances of DetroitDistrict.

    """

    def __init__(self, cacheFile=None):
        """
        Initializes the RedLines class without any districts.
        assign districts attribute to an empty list
        """
        self.districts = []
        if cacheFile:
            self.loadCache(cacheFile)

    def createDistricts(self, fileName):
        """
        Creates DetroitDistrict instances from redlining data in a specified file.
        Based on the understanding in step 1, load the file,parse the json object,
        and create 238 districts instance.
        Finally, store districts instance in a list,
        and assign the list to be districts attribute of RedLines.

        Parameters
        ----------
        fileName : str
            The name of the file containing redlining data in JSON format.

        Hint
        ----------
        The data for description attribute could be from
        one of the dict key with only number.

        """
        f = open(fileName)
        data = json.load(f)
        f.close()
        features = data["features"]
        for feature in features:
            coordinates = feature["geometry"].get("coordinates")[0][0]
            holcGrade = feature["properties"].get("holc_grade")
            id = feature["properties"].get("holc_id")
            description = feature["properties"].get("area_description_data").get("8")
            holcColor = feature["properties"].get("holc_color")
            district = DetroitDistrict(coordinates, holcGrade, id, description, holcColor)
            self.districts.append(district)

    def plotDistricts(self):
        """
        Plots the districts using matplotlib, displaying each district's location and color.
        Name it redlines_graph.png and save it to the current directory.
        """
        fig, ax = plt.subplots()
        for district in self.districts:
            ax.add_patch(plt.Polygon(district.coordinates, color=district.holcColor, alpha=0.5))
            ax.autoscale()
        plt.rcParams["figure.figsize"] = (15, 15)
        plt.savefig("redlines_graph.png")

    def generateRandPoint(self):
        """
        Generates a random point within the boundaries of each district.

        This method creates a mesh grid of points covering the geographical area of interest
        and then selects a random point within the boundary of each district.

        Attributes
        ----------
        self.districts : list of DetroitDistrict
            The list of district instances in the RedLines class.

        Note
        ----
        The random point is assigned as the randomLat and randomLong  for each district.
        This method assumes the 'self.districts' attribute has been populated with DetroitDistrict instances.

        """
        xgrid = np.arange(-83.5, -82.8, 0.004)
        ygrid = np.arange(42.1, 42.6, 0.004)
        xmesh, ymesh = np.meshgrid(
            xgrid, ygrid
        )  # create a mesh grid of points to make sure x and y coordinates are paired
        points = np.vstack(
            (xmesh.flatten(), ymesh.flatten())
        ).T  # flatten the grid and stack the x and y coordinates
        for district in self.districts:
            p = Path(district.coordinates)
            grid = p.contains_points(points)  # mask the points that are within the district
            point = points[
                random.choice(list(np.where(grid)[0]))
            ]  # randomly select a point within the district
            # print(f"{district} : {point}")
            district.randomLat = point[1]
            district.randomLong = point[0]

    def fetchCensus(self):
        """
        Fetches the census tract for each district in the list of districts using the FCC API.
        """

        api = "https://geo.fcc.gov/api/census/area"
        for district in self.districts:
            lat = district.randomLat
            lon = district.randomLong
            params = {"lat": lat, "lon": lon, "censusYear": "2010", "format": "json"}
            response = requests.get(api, params)
            census = []
            while True:
                if response.status_code == 200:
                    data = response.json()
                    district.censusTract = data["results"][0]["block_fips"][2:11]
                    census.append(data)
                    break
                else:
                    response = requests.get(api, params)

    def fetch(self, params, colname=None):
        """
        Fetches data from the U.S. Census Bureau's API.

        This method sends a GET request to the specified API endpoint with the provided parameters.
        If the request is successful, the method returns the JSON response. If the request fails,
        the method retries the request until it is successful.

        Parameters
        ----------
        params : dict
            A dictionary containing the parameters to be sent with the request.

        Returns
        -------
        dict
            A dictionary containing the JSON response from the API.

        """
        api = "https://api.census.gov/data/2018/acs/acs5"
        key = "bff2ebd794e77fac281f258fe892bd1e36fe481b"
        params["key"] = key
        # print(params)
        while True:
            response = requests.get(api, params)
            if response.status_code == 200:
                response_data = response.json()
                break
            else:
                print(response.status_code)

        data = pd.DataFrame(response_data[1:], columns=response_data[0])
        data["tract_id"] = data["county"] + data["tract"]
        if colname:
            data.rename(columns={data.columns[0]: colname}, inplace=True)
        return data

    def fetchIncome(self):
        """
        Retrieves the median household income for each district based on the census tract.

        This method requests income data from the ACS 5-Year Data via the U.S. Census Bureau's API
        for the year 2018. It then maps these incomes to the corresponding census tracts and updates
        the median income attribute of each district in `self.districts`.

        Note
        ----
        The method assumes that the `censusTract` attribute for each district is already set. It updates
        the `medIncome` attribute of each district based on the fetched income data. If the income data
        is not available or is negative, the median income is set to 0.

        """
        params = {"get": "B19013_001E", "for": "tract:*", "in": "state:26"}
        data = self.fetch(params, colname="medIncome")
        for district in self.districts:
            tract = district.censusTract
            try:
                income = int(data.loc[data["tract_id"] == tract, "medIncome"])
            except:
                income = 0
            if income <= 0:
                district.medIncome = 0
            else:
                district.medIncome = income
            # print(f"{district.id} : {district.medIncome}")

    def cacheData(self, fileName):
        """
        Saves the current state of district data to a file in JSON format.
        Using the __dict__ magic method on each district instance, and save the
        result of it to a list.
        After creating the list, dump it to a json file with the inputted name.
        You should name the cache file as redlines_cache.json

        Parameters
        ----------
        filename : str
            The name of the file where the district data will be saved.
        """
        districts_data = [district.__dict__ for district in self.districts]
        with open(fileName, "w") as f:
            json.dump(districts_data, f)

    def loadCache(self, fileName):
        """
        Loads district data from a cache JSON file if it exists.

        Parameters
        ----------
        fileName : str
            The name of the file from which to load the district data.
            You should name the cache file as redlines_cache.json

        Returns
        -------
        bool
            True if the data was successfully loaded, False otherwise.
        """
        if os.path.exists(fileName):
            with open(fileName, "r") as f:
                data = json.load(f)
            for district_data in data:
                district = DetroitDistrict(**district_data)
                self.districts.append(district)
            return True
        else:
            return False

    def calcIncomeStats(self):
        """
        Use np.median and np.mean to
        Calculates the mean and median of median household incomes for each district grade (A, B, C, D).

        This method computes the mean and median incomes for districts grouped by their HOLC grades.
        The results are stored in a list following the pattern: [AMean, AMedian, BMean, BMedian, ...].
        After your calculations, you need to round the result to the closest whole int.
        Relate reading https://www.w3schools.com/python/ref_func_round.asp


        Returns
        -------
        list
            A list containing mean and median income values for each district grade in the order A, B, C, D.
        """
        grades = ["A", "B", "C", "D"]
        results = []
        for grade in grades:
            income = [
                district.medIncome for district in self.districts if district.holcGrade == grade
            ]
            if income:
                mean = round(np.mean(income))
                median = round(np.median(income))
                results.extend([mean, median])
        print(results)
        return results

    def findCommonWords(self):
        """
        Analyzes the qualitative descriptions of each district category (A, B, C, D) and identifies the
        10 most common words unique to each category.

        This method aggregates the qualitative descriptions for each district category, splits them into
        words, and computes the frequency of each word. It then identifies and returns the 10 most
        common words that are unique to each category, excluding common English filler words.

        Returns
        -------
        list of lists
            A list containing four lists, each list containing the 10 most common words for each
            district category (A, B, C, D). The first list should represent grade A, and second for grade B,etc.
            The words should be in the order of their frequency.

        Notes
        -----
        - Common English filler words such as 'the', 'of', 'and', etc., are excluded from the analysis.
        - The method ensures that the common words are unique across the categories, i.e., no word
        appears in more than one category's top 10 list.
        - Regular expressions could be used for word splitting to accurately capture words from the text.
        - Counter from collections could also be used.

        """
        # List of filter, stop words, punctuation, and numbers
        filter_words = set(["the", "of", "and", "in", "to", "a", "is", "for", "on", "that"])

        # Store the words for each grade
        words = {grade: [] for grade in ["A", "B", "C", "D"]}
        for district in self.districts:
            # Remove filter words, punctuation, numbers, and make all words lowercase
            description_text = re.sub(r"\d+", "", district.description.lower())
            description_text = re.sub(r"[^\w\s]", "", description_text)
            description = [word for word in description_text.split() if word not in filter_words]
            words[district.holcGrade].append(description)

        # count the words for each grade
        counts = {grade: Counter() for grade in ["A", "B", "C", "D"]}
        for grade in ["A", "B", "C", "D"]:
            for description in words[grade]:
                counts[grade].update(
                    description
                )  # iterate through the list of description and count the words

        # Find the 10 most common words for each grade and make sure they are unique across different lists
        common_words = {grade: [] for grade in ["A", "B", "C", "D"]}
        used_words = set()
        for grade in ["A", "B", "C", "D"]:
            for word, count in counts[grade].most_common():
                if len(common_words[grade]) == 10:
                    break
                if word in used_words:
                    continue
                else:
                    common_words[grade].append(word)
                    used_words.add(word)

        # change the dict to list of lists
        result = [common_words[grade] for grade in ["A", "B", "C", "D"]]
        # print(result)
        return result

    def calcRank(self):
        """
        Calculates and assigns a rank to each district based on median income.

        This method sorts the districts in descending order of their median income and then assigns
        a rank to each district, with 1 being the highest income district.

        Note
        ----
        The rank is assigned based on the position in the sorted list, so the district with the highest
        median income gets a rank of 1, the second-highest gets 2, and so on. Ties are not accounted for;
        each district will receive a unique rank.

        Important:
        If you do the extra credit, you need to edit the __init__ of DetroitDistrict adding another arg "rank" with
        default value to be None. Not doing so might cause the load cache method to fail if you use the ** operator in load cache.

        Attribute
        ----
        rank

        """
        sort_districts = sorted(self.districts, key=lambda x: x.medIncome, reverse=True)
        for rank, district in enumerate(sort_districts, 1):
            district.rank = rank

    def calcPopu(self):
        """
        Fetches and calculates the percentage of Black or African American residents in each district.

        This method fetch the total and Black populations for each census tract in Michigan from
        the U.S. Census Bureau's API, like the median income data.  It then calculates the percentage of Black residents in each tract
        and assigns this value to the corresponding district percent attribute.

        Note
        ----
        The method assumes that the census tract IDs in the district data match those used by the Census Bureau.
        The percentage is rounded to two decimal places. If the Black population is zero, the percentage is set to 0.
        Elif the total population is zero, the percentage is set to 1.

        Important:
        If you do the extra credit, you need to edit the __init__ of DetroitDistrict adding another arg "percent" with
        default value to be None. Not doing so might cause the load cache method to fail if you use the ** operator in load cache.


        Attribute
        ----
        percent

        """

        def _calcuate_percent(row):
            if int(row["afam_pop"]) == 0:
                return 0
            elif int(row["total_pop"]) == 0:
                return 1
            else:
                return round((int(row["afam_pop"]) / int(row["total_pop"])), 2)

        params = {"get": "B02001_003E", "for": f"tract:*", "in": f"state:26"}
        afam_data = self.fetch(params, colname="afam_pop")
        params["get"] = "B01001_001E"
        total_data = self.fetch(params, colname="total_pop")
        pop_data = pd.merge(afam_data, total_data, on="tract_id")
        pop_data["percent"] = pop_data.apply(_calcuate_percent, axis=1)
        for district in self.districts:
            district.percent = pop_data.loc[
                pop_data["tract_id"] == district.censusTract, "percent"
            ].values[0]

    def comment(self):
        """
        Look at the
        districts in each category, A, B, C and D. Are there any trends that you see? Share 1 paragraph of your
        findings. And a few sentences(more than 50 words) about how this exercise did or did not change your understanding of
        residential segregation. Print you thought in the method.
        """
        print(
            """I calculated the average percent of ratio of African-American population and median income in each census tract
            between which I found a significant negative correlation. The district graph presents a clearer pattern of residential 
            segregation where African-American residents were more likely to reside in downtown area with lower median income, while
            other residents were more likely to live in the suburbs with higher median income.
            """
        )

    def sample(self):
        """
        This is a sample method that you can use to test your implementation.
        """
        # randomly selected 5 districts
        sample = random.sample(self.districts, 5)
        for district in sample:
            print(
                district.id,
                district.holcGrade,
                district.medIncome,
                district.censusTract,
                district.rank,
                district.percent,
            )


# Test your class implementation here
# class UnitTest(unittest.TestCase):
#     def setUp(self):
#         return super().setUp()
#     def test_Cache(self):
#         myRedLines = RedLines("redlines_cache.json")
#         self.assertTrue(isinstance(myRedLines.districts, list))


# Use main function to test your class implementations.
# Feel free to modify the example main function.
def main():
    # unittest.main()
    myRedLines = RedLines()
    myRedLines.createDistricts("redlines_data.json")
    myRedLines.plotDistricts()
    myRedLines.generateRandPoint()
    myRedLines.fetchCensus()
    myRedLines.fetchIncome()
    myRedLines.calcIncomeStats()
    myRedLines.findCommonWords()
    myRedLines.calcRank()  # Assuming you have this method
    myRedLines.calcPopu()  # Assuming you have this method
    myRedLines.cacheData("redlines_cache.json")
    myRedLines.loadCache("redlines_cache.json")
    myRedLines.comment()


if __name__ == "__main__":
    main()
