from fetch_competitions import fetch_competitions

def parse_competitions():
    raw_data = fetch_competitions()

    categories = {}
    competitions = []

    for comp in raw_data:
        category = comp.get("category", {})
        category_id = category.get("id")
        category_name = category.get("name")

        # store unique categories
        if category_id and category_id not in categories:
            categories[category_id] = category_name

        competitions.append({
            "competition_id": comp.get("id"),
            "competition_name": comp.get("name"),
            "parent_id": comp.get("parent_id"),
            "type": comp.get("type"),
            "gender": comp.get("gender"),
            "category_id": category_id
        })

    return categories, competitions


if __name__ == "__main__":
    categories, competitions = parse_competitions()

    print("✅ PARSING SUCCESSFUL")
    print("Total categories:", len(categories))
    print("Total competitions:", len(competitions))
    print("\nSample category:", list(categories.items())[0])
    print("Sample competition:", competitions[0])
