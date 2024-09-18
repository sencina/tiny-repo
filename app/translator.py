

def parse_action(action):
    return {
        "id": action["id"],
        "type": "ACTION",
        "name": action["name"]
    }

def parse_singlechoice(sc):
    return {
        "id": sc["id"],
        "type": "QUESTION",
        "name": sc["name"],
        "question_type": "SINGLECHOICE",
        "metadata": {
            "metadata": {
                "lerni_question_type": "single-choice"
            },
            "options": sc["options"]
        }
    }

def parse_multiplechoice(mc):
    return {
        "id": mc["id"],
        "type": "QUESTION",
        "name": mc["name"],
        "question_type": "MULTIPLECHOICE",
        "metadata": {
            "metadata": {
                "lerni_question_type": "multiple-choice"
            },
            "options": mc["options"]
        }
    }

def parse_relation(relation):
    return {
        "from": relation["parent"],
        "to": relation["child"]
    }

translate_map = {
    "ACTION": parse_action,
    "SINGLECHOICE": parse_singlechoice,
    "MULTIPLECHOICE": parse_multiplechoice
}

def translate(data):
    return translate_map[data["question_type"]](data)