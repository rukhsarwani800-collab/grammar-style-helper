"""
Grammar & Style Helper
------------------------
A simple web app that takes a paragraph of text and returns:
1. Grammar mistake suggestions (using the free LanguageTool API)
2. Weak/overused word suggestions (our own custom logic)

How it works:
- Flask serves a webpage with a textarea.
- When you click "Check", JavaScript sends your text to the /check route.
- /check calls the LanguageTool API for grammar issues, and runs our own
  weak-word checker, then sends both results back to the page as JSON.
"""

from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# ---------------------------------------------------------------------
# PART 1: Weak / overused word suggestions (this is your "original" part)
# ---------------------------------------------------------------------
# A small dictionary mapping weak words to stronger alternatives.
# Feel free to expand this list - the bigger it is, the more useful
# your tool becomes, and it costs you nothing extra in complexity.
WEAK_WORD_SUGGESTIONS = {
    "good": ["excellent", "beneficial", "favorable", "solid"],
    "bad": ["poor", "detrimental", "inadequate", "flawed"],
    "very": ["extremely", "remarkably", "significantly", "highly"],
    "nice": ["pleasant", "agreeable", "delightful", "commendable"],
    "big": ["substantial", "significant", "considerable", "major"],
    "small": ["minor", "modest", "slight", "limited"],
    "important": ["crucial", "essential", "vital", "significant"],
    "a lot": ["a great deal", "substantially", "considerably"],
    "thing": ["aspect", "factor", "element", "matter"],
    "get": ["obtain", "acquire", "receive", "gain"],
    "show": ["demonstrate", "illustrate", "reveal", "indicate"],
    "use": ["utilize", "employ", "apply"],
    "make": ["create", "produce", "generate", "establish"],
    "said": ["stated", "argued", "noted", "explained"],
    "think": ["believe", "consider", "argue", "maintain"],
}


def find_weak_words(text):
    """
    Scan the text word by word and flag any that appear in our
    weak-word dictionary. Returns a list of suggestion dicts.
    """
    suggestions = []
    words = text.lower().split()
    # Strip basic punctuation so "good." still matches "good"
    cleaned_words = [w.strip(".,!?;:\"'()") for w in words]

    for word in set(cleaned_words):
        if word in WEAK_WORD_SUGGESTIONS:
            suggestions.append({
                "word": word,
                "alternatives": WEAK_WORD_SUGGESTIONS[word]
            })
    return suggestions


# ---------------------------------------------------------------------
# PART 2: Grammar checking via the free LanguageTool public API
# ---------------------------------------------------------------------
def check_grammar(text):
    """
    Sends text to the free LanguageTool API and returns a simplified
    list of grammar/spelling issues found.
    """
    try:
        response = requests.post(
            "https://api.languagetool.org/v2/check",
            data={"text": text, "language": "en-US"},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        issues = []
        for match in data.get("matches", []):
            issues.append({
                "message": match.get("message"),
                "bad_text": text[match["offset"]: match["offset"] + match["length"]],
                "suggestions": [r["value"] for r in match.get("replacements", [])[:3]]
            })
        return issues
    except requests.exceptions.RequestException as e:
        # If the API is unreachable (e.g. no internet), fail gracefully
        return [{"message": f"Grammar check unavailable right now ({e})",
                  "bad_text": "", "suggestions": []}]


# ---------------------------------------------------------------------
# ROUTES
# ---------------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/check", methods=["POST"])
def check():
    text = request.json.get("text", "")

    if not text.strip():
        return jsonify({"error": "Please enter some text."}), 400

    grammar_issues = check_grammar(text)
    weak_words = find_weak_words(text)

    return jsonify({
        "grammar_issues": grammar_issues,
        "weak_words": weak_words
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
