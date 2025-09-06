import json
import sys
from pathlib import Path

def clean_model_block(block):
    """Trasforma ricorsivamente i blocchi eliminando il riconoscimento per nome."""
    if isinstance(block, dict):
        if "cases" in block:
            # Raccogli i modelli interni
            cleaned = []
            for case in block.get("cases", []):
                model = case.get("model")
                if model:
                    cleaned.append(clean_model_block(model))
            # Se c'è solo un modello ritorna direttamente quello
            if len(cleaned) == 1:
                return cleaned[0]
            elif cleaned:
                return {"type": "minecraft:alternatives", "variants": cleaned}
        elif "model" in block:
            return clean_model_block(block["model"])
        else:
            return {k: clean_model_block(v) for k, v in block.items()}
    elif isinstance(block, list):
        return [clean_model_block(v) for v in block]
    else:
        return block

def convert_file(input_path, output_path=None):
    """Converte un file JSON da riconoscimento per nome a modello-only."""
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "model" in data:
        data["model"] = clean_model_block(data["model"])

    # Se non specificato, salva con _cleaned
    if output_path is None:
        output_path = Path(input_path).with_name(Path(input_path).stem + "_cleaned.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"File convertito salvato in: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python convert_pack.py <file.json> [output.json]")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        convert_file(input_file, output_file)
