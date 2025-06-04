import requests

def get_entity_details(entity_id: str, token: str) -> dict:
    url = f"https://api.sayari.com/v1/entity/{entity_id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        attributes = data.get("attributes", {})

        def extract_value(attr_key):
            try:
                return attributes.get(attr_key, {}).get("data", [])[0].get("properties", {}).get("value")
            except (IndexError, AttributeError):
                return "Not found"

        entity = {
            "entity_id": data.get("id", "Not found"),
            "translated_name": data.get("translated_label", "Not found"),
            "name": extract_value("name"),
            "country": extract_value("country"),
            "type": data.get("type", "Not found"),
            "degree": data.get("degree", "Not found"),
            "sanctioned": data.get("sanctioned", "Not found"),
            "related_entities_count": data.get("related_entities_count", "Not found"),
            "relationship_count": data.get("relationship_count", {}).get("linked_to", "Not found"),
        }

        # Identifiers
        identifiers = data.get("identifiers", [])
        entity["identifiers"] = ", ".join(i.get("value") for i in identifiers if i.get("value")) if identifiers else "Not found"

        # Source Count (resumo legível)
        source_count = data.get("source_count", {})
        if source_count:
            sources_summary = []
            for s in source_count.values():
                label = s.get("label", "Unknown")
                count = s.get("count", 0)
                sources_summary.append(f"{label}: {count}")
            entity["source_count"] = "; ".join(sources_summary)
        else:
            entity["source_count"] = "Not found"

        # Export Controls
        risk = data.get("risk", {})
        export_controls = risk.get("export_controls", {})
        entity["export_controls"] = export_controls.get("value", "Not found")
        entity["export_controls_level"] = export_controls.get("level", "N/A")
        sources = export_controls.get("metadata", {}).get("source", [])
        entity["export_controls_sources"] = ", ".join(sources) if sources else "None"

        # Helper functions for other risk indicators
        def extract_risk_flag(risk_key, default_value="Not found"):
            return risk.get(risk_key, {}).get("value", default_value)

        def extract_risk_level(risk_key):
            return risk.get(risk_key, {}).get("level", "N/A")

        entity["sanctioned_adjacent"] = extract_risk_flag("sanctioned_adjacent")
        entity["sanctioned_adjacent_level"] = extract_risk_level("sanctioned_adjacent")

        entity["soe_adjacent"] = extract_risk_flag("soe_adjacent")
        entity["soe_adjacent_level"] = extract_risk_level("soe_adjacent")

        entity["meu_list_contractors"] = extract_risk_flag("meu_list_contractors")
        entity["meu_list_contractors_level"] = extract_risk_level("meu_list_contractors")

        entity["basel_aml"] = extract_risk_flag("basel_aml")
        entity["basel_aml_level"] = extract_risk_level("basel_aml")

        entity["cpi_score"] = extract_risk_flag("cpi_score")
        entity["cpi_score_level"] = extract_risk_level("cpi_score")

        return entity

    except requests.exceptions.RequestException as e:
        print(f"Error fetching entity details: {e}")
        return {
            "entity_id": entity_id,
            "error": str(e)
        }
