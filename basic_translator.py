import re
import time
from translate import Translator
import html

def read_srt(file_path):
    """Read an SRT file and return a list of subtitle entries."""
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        content = file.read()
    
    # Split by double newline to separate subtitle entries
    subtitle_blocks = re.split(r'\n\n+', content.strip())
    subtitles = []
    
    for block in subtitle_blocks:
        lines = block.split('\n')
        if len(lines) >= 3:  # Valid subtitle block has at least 3 lines
            index = lines[0]
            time_info = lines[1]
            text = '\n'.join(lines[2:])  # Combine all text lines
            subtitles.append({
                'index': index,
                'time_info': time_info,
                'text': text
            })
    
    return subtitles

def translate_text(text, src_lang='en', dest_lang='te'):
    """Translate text from source language to destination language."""
    translator = Translator(from_lang=src_lang, to_lang=dest_lang)
    
    try:
        # Handle newlines in subtitles by splitting, translating, and rejoining
        lines = text.split('\n')
        translated_lines = []
        
        for line in lines:
            if line.strip():  # Only translate non-empty lines
                # The translate library has character limits, so we might need to break up long sentences
                if len(line) > 500:
                    # Simple splitting by punctuation
                    segments = re.split(r'([.!?])', line)
                    result = ""
                    for i in range(0, len(segments), 2):
                        # Add the sentence and its punctuation if available
                        sentence = segments[i]
                        if sentence.strip():
                            result += translator.translate(sentence)
                        if i+1 < len(segments):
                            result += segments[i+1]  # Add the punctuation
                    translated_lines.append(result)
                else:
                    result = translator.translate(line)
                    translated_lines.append(result)
            else:
                translated_lines.append('')
        
        return '\n'.join(translated_lines)
    except Exception as e:
        print(f"Translation error: {e}")
        # Return original text if translation fails
        return text

def write_srt(subtitles, output_file):
    """Write subtitles to an SRT file."""
    with open(output_file, 'w', encoding='utf-8') as file:
        for i, subtitle in enumerate(subtitles):
            if i > 0:
                file.write('\n\n')
            file.write(f"{subtitle['index']}\n")
            file.write(f"{subtitle['time_info']}\n")
            file.write(subtitle['text'])

def translate_srt(input_file, output_file, src_lang='en', dest_lang='te'):
    """Translate an SRT file from source language to destination language."""
    # Read the input SRT file
    subtitles = read_srt(input_file)
    
    # Translate each subtitle text
    total_subtitles = len(subtitles)
    for i, subtitle in enumerate(subtitles):
        print(f"Translating subtitle {i+1}/{total_subtitles}")
        subtitle['text'] = translate_text(subtitle['text'], src_lang, dest_lang)
        
        # Add a small delay to avoid hitting API rate limits
        if i % 5 == 0 and i > 0:
            time.sleep(1)
    
    # Write the translated subtitles to the output file
    write_srt(subtitles, output_file)
    print(f"Translation completed. Output saved to {output_file}")

if __name__ == "__main__":
    input_file = r"C:\Users\Bhagya\Downloads\[English] 【去有风的地方】第23集 _ 刘亦菲、李现主演 _ Meet Yourself EP23 _ Starring_ Liu Yifei, Li Xian _ ENG SUB [DownSub.com].srt"  # Change this to your input file
    output_file = "telugu_subtitles.srt"  # Change this to your desired output file
    
    translate_srt(input_file, output_file, 'en', 'te')

file_path = r"C:\Users\Bhagya\Downloads\[English] 【去有风的地方】第23集 _ 刘亦菲、李现主演 _ Meet Yourself EP23 _ Starring_ Liu Yifei, Li Xian _ ENG SUB [DownSub.com].srt"

