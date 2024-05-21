import json
import asyncio
import aiohttp
from googletrans import Translator
from googletrans import LANGUAGES
import time

class TranslationGenerator:

    @classmethod
    def get_supported_languages(cls):
        supported_languages = []
        try:
            print('\033[95mGetting Supported Languages...\033[0m\n\n')
            for lang_code, lang_name in LANGUAGES.items():
                supported_languages.append(lang_code)
                print(f'\033[92m✔︎\033[0m {lang_code}: {lang_name}')
        except Exception as e:
            print('\033[91m✘ Error while getting supported languages:\033[0m', e)
        return supported_languages

    @classmethod
    async def translate_text(cls, text, target_lang):
        try:
            print(f'\033[94mTranslating to {target_lang}...\033[0m')
            start_time = time.time()
            translator = Translator()
            translated = translator.translate(text, dest=target_lang)
            elapsed_time = time.time() - start_time
            print(
                f'\033[92m✔︎\033[0m Translated in {elapsed_time:.2f} seconds\n')
            return translated.text
        except Exception as e:
            print('\033[91m✘ Error while translating text:\033[0m\n', e)
            return ''

    @classmethod
    async def translate_and_write(cls, lang, data):
        try:
            print(f'\033[94mTranslating and Writing for {lang}...\033[0m')
            start_time = time.time()

            # Translate data to the specified language
            translated_data = {key: await cls.translate_text(value, lang) for key, value in data.items()}

            # Write the translated section to the file
            with open('lang.js', 'a', encoding='utf-8') as js_file:
                js_file.write(
                    f"  {lang}: {{ // add part with the {lang} translate\n")
                for key, value in translated_data.items():
                    js_file.write(
                        f"    {json.dumps(key, ensure_ascii=False)}: {json.dumps(value, ensure_ascii=False)},\n")
                js_file.write("  },\n")

            elapsed_time = time.time() - start_time
            print(
                f'\033[92m✔︎\033[0m Elapsed Time Translated and Written in {elapsed_time:.2f} seconds\n\n')
        except Exception as e:
            print('\033[91m✘ Error while translating and writing:\033[0m', e)

    @classmethod
    def generate_translations(cls, target_languages):
        try:
            # Read the data from the .txt file (assuming it's in JSON format)
            with open('nested.json', 'r', encoding='utf-8') as txt_file:
                data_str = txt_file.read()

            # Parse the JSON data
            translations_data = json.loads(data_str)

            # Create an async session to make concurrent translation requests
            async def main():
                async with aiohttp.ClientSession() as session:
                    for lang in target_languages:
                        js_file = open('lang.js', 'w', encoding='utf-8')
                        js_file.write('const translations = {\n')
                        js_file.write(f"  '{lang}': {{\n")

                        for screen_key, screen_value in translations_data['en'].items():
                            js_file.write(f"    '{screen_key}': {{\n")

                            for key, value in screen_value.items():
                                translated_value = await cls.translate_text(value, lang)
                                js_file.write(f"      '{key}': '{translated_value}',\n")

                            js_file.write("    },\n")

                        js_file.write("  },\n")
                        js_file.write('};\n')
                        js_file.close()

            # Run the async event loop
            asyncio.run(main())

            print('\033[95mTranslation and Writing Completed!\033[0m')
        except Exception as e:
            print(
                '\033[91m✘ Error during translation and writing process:\033[0m', e)

# List of target languages
target_languages = ['ar'] # only one language

# Call the class method with the list of target languages
trans = TranslationGenerator()
trans.generate_translations(target_languages)

