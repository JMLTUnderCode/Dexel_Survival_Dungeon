import sys
import re

def update_html(html_path, tag, win_url, linux_url):
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    html = re.sub(r"const releaseTag = '[^']*';", f"const releaseTag = '{tag}';", html)
    html = re.sub(r"const winExe = '[^']*';", f"const winExe = '{win_url}';", html)
    html = re.sub(r"const linuxExe = '[^']*';", f"const linuxExe = '{linux_url}';", html)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    # Uso: python update_web_links.py <tag> <win_url> <linux_url>
    if len(sys.argv) != 4:
        print('Uso: python update_web_links.py <tag> <win_url> <linux_url>')
        sys.exit(1)
    tag, win_url, linux_url = sys.argv[1:]
    update_html('web/index.html', tag, win_url, linux_url)
