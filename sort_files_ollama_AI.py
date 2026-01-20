import ollama
from pathlib import Path


# --- NEW AI FUNCTION ---
def ask_ai_for_category(filename):
    """
    Sends the filename to Llama3 and gets a category name back.
    """
    # Define our smart categories
    categories = ["Work", "Taxes", "Study", "Finance", "Personal"]

    prompt = f"""
    Analyze the filename: '{filename}'
    Choose the best category from this list: {', '.join(categories)}.
    If you are not sure, choose 'Others'.
    Answer with ONLY ONE WORD and nothing else.
    """

    try:
        # Calling local Ollama
        response = ollama.generate(model='llama3', prompt=prompt)
        # We use .strip() to remove any accidental spaces or newlines
        return response['response'].strip()
    except Exception as e:
        print(f"Error connecting to Ollama: {e}")
        return "Others"


# --- MAIN ORGANIZER ---
def smart_ai_organizer():
    folder_to_track = Path.home() / "Downloads"

    # 1. SIMPLE MAP (for non-documents)
    # We use this to save time and CPU power
    simple_map = {
        ".jpg": "Images", ".png": "Images", ".jpeg": "Images",
        ".zip": "Zip, Rar", ".mp3": "Music", ".mp4": "Videos",
        ".rar": "Zip, Rar", ".7z": "Zip, Rar", ".ppt": "Presentations",
        ".pptx": "Presentations", ".pptm": "Presentations",
        ".xlsx": "Excel", ".xlsm": "Excel", ".py": "Scripts"
    }

    # 2. DOCUMENT EXTENSIONS (for AI analysis)
    # These files have meaningful names that AI should read
    docs_to_analyze = [".pdf", ".docx", ".doc", ".txt"]

    for item in folder_to_track.iterdir():
        if item.is_file():
            # Skip the files start with . (like .DS_Store)
            if item.name.startswith('.'): continue

            ext = item.suffix.lower()

            # Logic:
            # 1. If 'ext' is in 'simple_map' -> get category from map
            # 2. Elif 'ext' is in 'docs_to_analyze' -> call ask_ai_for_category(item.name)
            # 3. Else -> use "Others"
            if ext in simple_map:
                target_folder = simple_map.get(ext)
            elif ext in docs_to_analyze:
                target_folder = ask_ai_for_category(item.name)
            else:
                target_folder = "Others"

            # Moving logic (same as your previous version)
            target_dir = folder_to_track / target_folder
            target_dir.mkdir(exist_ok=True)
            new_path = target_dir / item.name
            item.rename(new_path)
            print(f"Processed: {item.name} -> {target_folder}")


if __name__ == "__main__":
    smart_ai_organizer()
