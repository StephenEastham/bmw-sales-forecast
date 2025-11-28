"""
HTML aggregator and browser automation
"""

import os
import glob
import webbrowser
from pathlib import Path
from config import OUTPUT_DIR, out_path


def create_aggregator_html():
    """Create aggregator HTML page for all outputs"""
    out_html = '07_all_outputs.html'
    # Look for generated PNGs/HTMLs inside the outputs directory
    pngs = sorted([str(p) for p in OUTPUT_DIR.glob('*.png')])
    exclude_names = {out_html, 'commit_messages-can-change-values.html'}
    htmls = sorted([str(p) for p in OUTPUT_DIR.glob('*.html') if os.path.basename(p) not in exclude_names])
    
    if not pngs and not htmls:
        print('No output PNG or HTML files found in the current directory.')
    else:
        parts = []
        parts.append('<!doctype html>')
        parts.append('<html lang="en">')
        parts.append('<head>')
        parts.append('<meta charset="utf-8"/>')
        parts.append('<meta name="viewport" content="width=device-width, initial-scale=1"/>')
        parts.append('<title>All Outputs - BMW Sales Forecast</title>')
        parts.append('<style>body{font-family:system-ui,Segoe UI,Roboto,Helvetica,Arial,sans-serif;margin:20px} h2{margin-top:1.2rem} figure{margin:12px 0} img{max-width:100%;height:auto;border:1px solid #ddd;padding:4px;background:#fff} .filelink{margin-bottom:8px;display:inline-block}</style>')
        parts.append('</head>')
        parts.append('<body>')
        parts.append('<h1>BMW Sales Forecast — Generated Outputs</h1>')
        parts.append(f'<p>Repository path: {Path().resolve()}</p>')
        
        if pngs:
            parts.append('<h2>PNG Visualizations</h2>')
            for p in pngs:
                safe = os.path.basename(p)
                parts.append(f'<figure><figcaption>{safe}</figcaption><img src="{safe}" alt="{safe}"/></figure>')
        
        if htmls:
            parts.append('<h2>Interactive HTML Outputs</h2>')
            for h in htmls:
                safe = os.path.basename(h)
                parts.append(f'<div class="filelink"><a href="{safe}" target="_blank">Open {safe} in new tab</a></div>')
                parts.append(f'<div style="margin:12px 0; border:1px solid #ccc;"><iframe src="{safe}" style="width:100%;height:640px;border:0"></iframe></div>')
        
        parts.append('</body>')
        parts.append('</html>')
        
        html_content = '\n'.join(parts)
        out_path_full = OUTPUT_DIR / out_html
        with open(out_path_full, 'w', encoding='utf-8') as f:
            f.write(html_content)

        abs_path = out_path_full.resolve()
        print(f'✅ Created aggregator: {abs_path}')

        # Automatically open the aggregator and the two interactive dashboards
        try:
            url = abs_path.as_uri()
            print(f'\n🌐 Opening {out_html} in your default browser...')
            webbrowser.open(url)
            print(f'✅ Opened aggregator: {abs_path}')

            # Open the interactive dashboards in separate tabs if they exist
            dash05 = (OUTPUT_DIR / '05_interactive_dashboard.html').resolve()
            dash06 = (OUTPUT_DIR / '06_model_heatmap_interactive.html').resolve()

            try:
                if dash05.exists():
                    print(f'🌐 Opening dashboard: {dash05.name} in a new tab...')
                    webbrowser.open_new_tab(dash05.as_uri())
                else:
                    print(f'   • {dash05} not found; skipping open for 05')
            except Exception as e2:
                print(f'⚠️ Could not open {dash05}: {e2}')

            try:
                if dash06.exists():
                    print(f'🌐 Opening dashboard: {dash06.name} in a new tab...')
                    webbrowser.open_new_tab(dash06.as_uri())
                else:
                    print(f'   • {dash06} not found; skipping open for 06')
            except Exception as e3:
                print(f'⚠️ Could not open {dash06}: {e3}')

            print('✅ Browser open actions complete.')

        except Exception as e:
            print(f'⚠️ Could not open browser automatically: {e}')
            print(f'   You can manually open: {abs_path}')
