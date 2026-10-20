#!/usr/bin/env bash
# Toolchain setup A2 — ATTEMPT 4 (correct package names + HaranoAji validation).
# Attempt 3 state: TeX Live 2026 installed OK (LuaHBTeX 1.24.0); tlmgr exit 1 only
# because `array/multicol/rotating/tabularx` are not standalone packages (they
# live in `tools`, already present); kpsewhich miss only `haranoaji.sty`, which
# does not exist by design — haranoaji package ships OTF + .fontspec, resolved
# via `kpsewhich HaranoAjiMincho-Regular.otf` (verified rc=0 outside this script).
# This attempt: rerun tlmgr with corrected names (expect exit 0 / already-present),
# then corrected validation (OTF, not .sty). No reinstall, no source writes.
set -u
TOOLROOT="/tmp/opencode/jgas-texlive-20261019T133205Z"
TEXDIR="$TOOLROOT/texlive"
step=30; failures=0
mark(){ step=$((step+1)); echo "=== STEP $step: $1 ==="; date -u +"--- clock %Y-%m-%dT%H:%M:%SZ"; }
ok(){ echo "STEP_EXIT:$1 DURATION_S:$2"; if [ "$1" != "0" ]; then failures=$((failures+1)); echo "STEP_FAIL_RECORDED (not hidden)"; fi; }
export PATH="$TEXDIR/bin/x86_64-linux:$PATH"
export TEXMFHOME="$TOOLROOT/texmf-home" TEXMFVAR="$TOOLROOT/texmf-var" TEXMFCONFIG="$TOOLROOT/texmf-config" TEXMFCACHE="$TOOLROOT/texmf-var" TEXLIVE_ROOT="$TEXDIR"
echo "ATTEMPT=4 TOOLROOT=$TOOLROOT"
echo ""
mark "corrected tlmgr closure (tools covers array/tabularx/multicol; no bogus names)"
t0=$SECONDS
tlmgr option repository "$(tlmgr option repository | awk '{print $NF}' | head -n 1)"
echo "REPO_PINNED:$(tlmgr option repository)"
PKGS="latexmk luatex luaotfload luatexja jlreq haranoaji haranoaji-extra biblatex biber geometry xcolor graphics booktabs tools multirow needspace enumitem tcolorbox fancyhdr xurl hyperref bookmark etoolbox l3packages l3kernel latex-bin collection-luatex collection-latexrecommended collection-bibtexextra collection-langjapanese"
echo "REQUESTED_PKGS:$PKGS"
tlmgr install $PKGS
rc=$?
echo "TLMGR_INSTALL_EXIT:$rc"
d1=$((SECONDS-t0)); ok "$rc" "$d1"
echo "TLMGR_DURATION_S:$d1"
echo ""
mark "corrected validation (OTF for HaranoAji; all .sty/.cls; --version)"
t0=$SECONDS
vfail=0
for q in jlreq.cls luatexja.sty luatexja-preset.sty biblatex.sty tcolorbox.sty fancyhdr.sty hyperref.sty bookmark.sty xurl.sty geometry.sty xcolor.sty graphicx.sty booktabs.sty tabularx.sty array.sty multicol.sty needspace.sty rotating.sty enumitem.sty etoolbox.sty; do
  out=$(kpsewhich "$q" 2>&1); rcq=$?
  echo "KPSE $q rc=$rcq path=${out:-NOTFOUND}"
  if [ $rcq -ne 0 ] || [ -z "$out" ]; then vfail=$((vfail+1)); fi
done
for q in HaranoAjiMincho-Regular.otf HaranoAjiGothic-Regular.otf; do
  out=$(kpsewhich "$q" 2>&1); rcq=$?
  echo "KPSE-FONT $q rc=$rcq path=${out:-NOTFOUND}"
  if [ $rcq -ne 0 ] || [ -z "$out" ]; then vfail=$((vfail+1)); fi
done
echo "KPSE_MISSING_COUNT=$vfail (references.bib excluded: route-generated)"
echo "--- versions ---"
lualatex --version | head -n 3; latexmk --version | head -n 3; biber --version | head -n 2; bibtex --version | head -n 2; kpsewhich --version | head -n 2
echo "--- release ---"
cat "$TEXDIR/release-texlive.txt" 2>&1 || echo "NO_RELEASE_FILE"
d1=$((SECONDS-t0))
if [ $vfail -eq 0 ]; then ok 0 "$d1"; else ok 1 "$d1"; failures=$((failures+1)); fi
echo ""
mark "exact env/argv for caller"
t0=$SECONDS
echo "CALLER_PATH=$TEXDIR/bin/x86_64-linux:\$PATH"
echo "CALLER_TEXDIR=$TEXDIR"
echo "CALLER_TEXMFHOME=$TOOLROOT/texmf-home"
echo "CALLER_TEXMFVAR=$TOOLROOT/texmf-var"
echo "CALLER_TEXMFCONFIG=$TOOLROOT/texmf-config"
echo "CALLER_TEXMFCACHE=$TOOLROOT/texmf-var"
echo "CALLER_TEXLIVE_ROOT=$TEXDIR"
echo 'CALLER_ARGV_LUALATEX=lualatex -synctex=1 -interaction=nonstopmode -file-line-error -halt-on-error %O %S'
echo 'CALLER_ARGV_LATEXMK=latexmk -lualatex -synctex=1 -interaction=nonstopmode -file-line-error -halt-on-error main.tex'
echo 'CALLER_ARGV_BIBER=biber %O %B'
echo "SUPPORTED: TeX Live 2026 LuaHBTeX/latexmk/biber per .latexmkrc; schema deps jsonschema 4.23.0 + pypdf 6.16.2 via system python3 -m pip; poppler pdftoppm/pdftotext for inspection"
d1=$((SECONDS-t0)); ok 0 "$d1"
echo ""
echo "=== SUMMARY failures=$failures (0=toolchain ready) ==="
exit $failures
