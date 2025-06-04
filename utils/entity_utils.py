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
            # Pega o primeiro valor disponível para a chave
            values = attributes.get(attr_key, {}).get("data", [])
            if values and isinstance(values, list):
                return values[0].get("properties", {}).get("value", "Not found")
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
            "relationship_count": data.get("relationship_count", {}).get("linked_to", "Not found")
        }

        identifiers = data.get("identifiers", [])
        entity["identifiers"] = ", ".join(i.get("value") for i in identifiers if i.get("value")) or "Not found"

        source_count = data.get("source_count", {})
        if source_count:
            source_lines = []
            for s in source_count.values():
                label = s.get("label", "Unknown")
                count = s.get("count", 0)
                source_lines.append(f"{label}: {count}")
            entity["source_count"] = "; ".join(source_lines)
        else:
            entity["source_count"] = "Not found"

        risk = data.get("risk", {})
        export_controls = risk.get("export_controls", {})
        entity["export_controls"] = export_controls.get("value", "Not found")
        entity["export_controls_level"] = export_controls.get("level", "N/A")
        entity["export_controls_sources"] = ", ".join(
            export_controls.get("metadata", {}).get("source", [])
        ) or "None"

        def extract_flag(key, default="Not found"):
            return risk.get(key, {}).get("value", default)

        def extract_level(key):
            return risk.get(key, {}).get("level", "N/A")

        entity["sanctioned_adjacent"] = extract_flag("sanctioned_adjacent")
        entity["sanctioned_adjacent_level"] = extract_level("sanctioned_adjacent")

        entity["soe_adjacent"] = extract_flag("soe_adjacent")
        entity["soe_adjacent_level"] = extract_level("soe_adjacent")

        entity["meu_list_contractors"] = extract_flag("meu_list_contractors")
        entity["meu_list_contractors_level"] = extract_level("meu_list_contractors")

        entity["basel_aml"] = extract_flag("basel_aml")
        entity["basel_aml_level"] = extract_level("basel_aml")

        entity["cpi_score"] = extract_flag("cpi_score")
        entity["cpi_score_level"] = extract_level("cpi_score")

        return entity

    except requests.exceptions.RequestException as e:
        print(f"Failed to get entity info for ID {entity_id}: {e}")
        return {
            "entity_id": entity_id,
            "error": str(e)
        }
