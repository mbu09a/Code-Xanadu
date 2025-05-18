import argparse
import re
from pathlib import Path
import yaml

PROMPT_DIR = Path(__file__).parent / 'prompts'
PAGES_PATH = PROMPT_DIR / 'pages.txt'
TOC_PATH = PROMPT_DIR / 'toc.yaml'
BEHAVIOR_PATH = PROMPT_DIR / 'behavior.yaml'
MODES_PATH = PROMPT_DIR / 'modes.yaml'
SAFETY_PATH = PROMPT_DIR / 'safety.yaml'
TOOLS_PATH = PROMPT_DIR / 'tools.yaml'

# ---------------------------- data loaders

def load_pages():
    text = PAGES_PATH.read_text()
    parts = re.split(r'###Page (\d+)###\n', text)
    pages = {}
    for i in range(1, len(parts), 2):
        num = int(parts[i])
        pages[num] = parts[i+1].strip()
    return pages


def parse_toc():
    """Parse toc.yaml using yaml.safe_load."""
    text = TOC_PATH.read_text()
    fixed_lines = []
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith('* '):
            indent = len(line) - len(stripped)
            line = ' ' * indent + '- ' + stripped[2:]
        fixed_lines.append(line)
    data = yaml.safe_load('\n'.join(fixed_lines)) or {}
    sections = []
    for sec in data.get('sections', []):
        out = {
            'number': sec.get('number'),
            'title': sec.get('title'),
            'connected_character': sec.get('connected_character'),
            'pages': tuple(sec.get('pages', [])),
            'chapters': []
        }
        for ch in sec.get('chapters', []):
            out['chapters'].append({
                'name': ch.get('name'),
                'page_range': tuple(ch.get('page_range', []))
            })
        sections.append(out)
    return sections

# ---------------------------- helper

def svg_filename(character: str) -> str:
    fname = character.lower().replace(' ', '_').replace('-', '_') + '.svg'
    return f"symbols/{fname}"

# ---------------------------- query functions

def display_section(num: int, sections, pages):
    sec = next((s for s in sections if s['number'] == num), None)
    if not sec:
        print(f"Error: section {num} not found")
        return
    print(f"Section {sec['number']}: {sec['title']}")
    print(f"Connected character: {sec['connected_character']}")
    print(f"SVG: {svg_filename(sec['connected_character'])}")
    print("Chapters:")
    for ch in sec['chapters']:
        start, end = ch['page_range']
        print(f" - {ch['name']} (pages {start}-{end})")


def display_chapter(ch_name: str, sections, pages):
    for sec in sections:
        for ch in sec['chapters']:
            if ch['name'].lower() == ch_name.lower():
                start, end = ch['page_range']
                if start < 1 or end > len(pages):
                    print("Error: page range out of bounds")
                    return
                print(f"Chapter: {ch['name']}")
                print(f"Section: {sec['title']} (#{sec['number']})")
                print(f"Connected character: {sec['connected_character']}")
                print(f"SVG: {svg_filename(sec['connected_character'])}")
                print()
                for p in range(start, end + 1):
                    print(f"[Page {p}]\n{pages[p]}\n")
                return
    print("Error: chapter not found")


def display_character(character: str, sections):
    hits = []
    for sec in sections:
        if sec['connected_character'].lower() == character.lower():
            for ch in sec['chapters']:
                hits.append((sec['title'], ch['name']))
    if not hits:
        print("Character not found")
        return
    print(f"Character: {character}")
    print(f"SVG: {svg_filename(character)}")
    print("Sections/Chapters:")
    for sec_title, ch_name in hits:
        print(f" - {sec_title}: {ch_name}")


def summarize_yaml(path, key):
    """Generic YAML summarizer printing list entries."""
    data = yaml.safe_load(Path(path).read_text()) or {}
    items = data.get(key, [])
    print(f"{key.capitalize()}:")
    for item in items:
        line = ', '.join(f"{k}: {v}" for k, v in item.items())
        print(f" - {line}")


def main():
    parser = argparse.ArgumentParser(description='Xanadu metadata helper')
    parser.add_argument('--section', type=int, help='Section number')
    parser.add_argument('--chapter', type=str, help='Chapter name')
    parser.add_argument('--character', type=str, help='Character name')
    parser.add_argument('--verbs', action='store_true')
    parser.add_argument('--modes', action='store_true')
    parser.add_argument('--safety', action='store_true')
    args = parser.parse_args()

    sections = parse_toc()
    pages = load_pages()

    if args.section:
        display_section(args.section, sections, pages)
    elif args.chapter:
        display_chapter(args.chapter, sections, pages)
    elif args.character:
        display_character(args.character, sections)
    elif args.verbs:
        summarize_yaml(BEHAVIOR_PATH, 'behaviors')
    elif args.modes:
        summarize_yaml(MODES_PATH, 'modes')
    elif args.safety:
        summarize_yaml(SAFETY_PATH, 'safety')
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
