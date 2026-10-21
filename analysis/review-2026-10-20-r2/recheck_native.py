from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2]
review=root/'analysis/review-2026-10-20-r2'
name=sys.argv[1]
source=root/'scripts'/name
text=source.read_text().replace("'analysis/native-board.json'", "'analysis/review-2026-10-20-r2/native-board.json'").replace("P/'analysis/", "P/'analysis/review-2026-10-20-r2/").replace("review-2026-10-20-r2/review-2026-10-20-r2/", "review-2026-10-20-r2/")
exec(compile(text,str(source),'exec'),{'__file__':str(source),'__name__':'__main__'})
