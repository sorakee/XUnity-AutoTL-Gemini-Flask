# XUnity-AutoTL-Gemini-Flask
Host your own Flask server to translate text retrieved from Unity applications via XUnity-Auto-Translator using Gemini
I did this because default translators are so bad it makes your brain fry as you attempt to understand them.

## How to Run
1. Retrieve your API key
2. Create a *secrets.json* file in the same directory as main.py and add this:<br/>
```
{
  "GEMINI_API_KEY": "INSERT YOUR API KEY HERE",
}
```
4. `pip install -r requirements.txt`
5. `py main.py` or `python main.py`
6. Modify AutoTranslator's Config.ini<br/>
```
[Custom]
Url=http://127.0.0.1:5000/translate
```
7. Run your game with XUnity-Auto-Translator plugin enabled
8. Press ALT+0
9. Change translator to Custom
