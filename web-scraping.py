import requests
from bs4 import BeautifulSoup
from pprint import pprint


def get_category_url(category_name, city_name):
    # Get the URL of the category
    main_url = "https://forgottenrealms.fandom.com/"
    url = main_url + f"wiki/Category:{category_name}_"
    if category_name == "Inhabitants":
        url += "of"
    else:
        url += "in"
    url += "_" + city_name.replace(" ", "_")
    return url


def get_elements_from_category(url, category_name="elements"):
    elements = []
    sub_categories = []

    # For each letter in the alphabet
    for letter in range(ord("A"), ord("Z") + 1):
        letter = chr(letter)
        print(f"\nRetrieving {category_name} starting with {letter}...")
        url_letter = url + "?from=" + letter

        # Send a GET request to the URL
        response = requests.get(url_letter)

        # Verify the request was successful
        if response.status_code != 200:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
            exit()

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, "html.parser")

        # Check if letter corresponds to div first char
        div_tag = soup.find("div", class_="category-page__first-char")
        if not div_tag:
            print("No category")
            exit()
        if div_tag.text.strip() != letter:
            print(f"No {category_name} found starting with {letter}.")
            continue

        # Find ul with class category-page__members-for-char
        ul_tag = soup.find("ul", class_="category-page__members-for-char")

        # Verify if the ul tag exists
        if not ul_tag:
            print("No ul tag found on the page.")
            exit()

        # Find all li inside the ul tag
        li_tags = ul_tag.find_all("li")

        # Get the text of each li tag
        element = [li_tag.text.strip() for li_tag in li_tags]

        # Add the elements to the list
        elements.extend([e for e in element if not e.startswith("Category:")])
        sub_categories.extend([e for e in element if e.startswith("Category:")])

    return elements, sub_categories


# Save categories url
categories = ["Inhabitants", "Locations", "Organizations"]

# Set cities to scrape
cities = ["Waterdeep"]

for city in cities:
    print(f"\nScraping {city}...")
    for category in categories:
        print(f"\nRetrieving {category} in {city}...")
        category_url = get_category_url(category, city)
        elements, sub_categories = get_elements_from_category(category_url, category)
        print(
            "Found "
            + len(elements)
            + " "
            + category
            + " and "
            + len(sub_categories)
            + " subcategories in "
            + city
            + "."
        )
