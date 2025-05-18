import argparse
import re
from pathlib import Path

PROMPT_DIR = Path(__file__).parent / 'prompts'
PAGES_PATH = PROMPT_DIR / 'pages.txt'
TOC_PATH = PROMPT_DIR / 'tableofcontents.yaml'
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
    lines = [l.rstrip('\n') for l in TOC_PATH.read_text().splitlines()]
    sections = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('* number:'):
            sec = {'chapters': []}
            sec['number'] = int(re.findall(r'\d+', line)[0])
            i += 1
            while i < len(lines):
                l = lines[i].rstrip()
                s = l.strip()
                if s.startswith('* number:'):
                    break
                if s.startswith('title:'):
                    sec['title'] = s.split(':', 1)[1].strip(' "')
                elif s.startswith('connected'):
                    sec['connected_character'] = s.split(':', 1)[1].strip(' "')
                elif s.startswith('pages:'):
                    nums = re.findall(r'\d+', s)
                    if nums:
                        sec['pages'] = (int(nums[0]), int(nums[1]))
                elif s.startswith('chapters:'):
                    pass
                elif s.startswith('* name:'):
                    ch_name = s.split(':', 1)[1].strip(' "')
                    i += 1
                    pr = lines[i].strip()
                    nums = re.findall(r'\d+', pr)
                    if len(nums) >= 2:
                        prange = (int(nums[0]), int(nums[1]))
                    else:
                        prange = (0, 0)
                    sec['chapters'].append({'name': ch_name, 'page_range': prange})
                i += 1
            sections.append(sec)
        else:
            i += 1
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
    lines = [l.rstrip('\n') for l in Path(path).read_text().splitlines()]
    data = []
    current = None
    for line in lines:
        s = line.strip()
        if s.startswith('- '):
            if current:
                data.append(current)
            current = {}
            part = s[2:]
            k, v = part.split(':', 1)
            current[k.strip()] = v.strip(' "')
        elif ':' in s and current is not None:
            k, v = s.split(':', 1)
            current[k.strip()] = v.strip(' "')
    if current:
        data.append(current)
    print(f"{key.capitalize()}:")
    for item in data:
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
