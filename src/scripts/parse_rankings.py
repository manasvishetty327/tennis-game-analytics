from fetch_rankings import fetch_rankings


def parse_rankings():
    raw_data = fetch_rankings()

    competitors = {}
    rankings = []

    # raw_data is a list of ranking groups (ATP, WTA, etc.)
    for group in raw_data:
        competitor_rankings = group.get("competitor_rankings", [])

        for item in competitor_rankings:
            competitor = item.get("competitor", {})
            competitor_id = competitor.get("id")

            if not competitor_id:
                continue

            competitors[competitor_id] = {
                "competitor_id": competitor_id,
                "name": competitor.get("name"),
                "country": competitor.get("country"),
                "country_code": competitor.get("country_code"),
                "abbreviation": competitor.get("abbreviation"),
            }

            rankings.append(
                {
                    "rank": item.get("rank"),
                    "movement": item.get("movement", 0),
                    "points": item.get("points", 0),
                    "competitions_played": item.get("competitions_played", 0),
                    "competitor_id": competitor_id,
                }
            )

    return competitors, rankings


if __name__ == "__main__":
    competitors, rankings = parse_rankings()

    print("✅ Parsing successful")
    print("Total competitors:", len(competitors))
    print("Total rankings:", len(rankings))
    print("First competitor:", list(competitors.values())[0])
