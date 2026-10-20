#!/usr/bin/env bash
# Toolchain setup A2 — ATTEMPT 2 (fix SYS paths under toolroot).
# Attempt 1 blocker: profile omitted TEXMFLOCAL/TEXMFSYSVAR/TEXMFSYSCONFIG;
# installer defaulted SYSVAR to /usr/local/texlive/2026/texmf-var -> mkdir
# permission denied (stderr preserved in attempt-1 evidence). No global change made.
# This attempt: explicit SYS/LOCAL paths under toolroot, unset TEXMF* env for
# installer invocation (profile is sole path source), reuse verified download
# (digest re-checked), fresh TEXDIR skeleton, same scheme-small + incremental closure.
set -u
TOOLROOT="/tmp/opencode/jgas-texlive-20261019T133205Z"
TEXDIR="$TOOLROOT/texlive"
DL="$TOOLROOT/download/install-tl-unx.tar.gz"
INSTDIR="$TOOLROOT/installer"
PROFILE="$TOOLROOT/texlive.profile"
EXPECTED_DL_SHA="5d9c826900a1d7a18479c3d37f60524eb78479214e03c88c055cc4c5dff2bd9c"
step=10; failures=0
mark(){ step=$((step+1)); echo "=== STEP $step: $1 ==="; date -u +"--- clock %Y-%m-%dT%H:%M:%SZ"; }
ok(){ echo "STEP_EXIT:$1 DURATION_S:$2"; if [ "$1" != "0" ]; then failures=$((failures+1)); echo "STEP_FAIL_RECORDED (not hidden)"; fi; }
echo "ATTEMPT=2 TOOLROOT=$TOOLROOT TEXDIR=$TEXDIR"
echo "PRIOR_FAIL=attempt1 SYSVAR defaulted to /usr/local/texlive (profile omitted SYS paths)"
echo ""
mark "re-verify reused download digest (no re-download without record)"
t0=$SECONDS
echo "DL_BYTES=$(stat -c %s "$DL")"
echo "DL_SHA256=$(sha256sum "$DL" | awk '{print $1}')"
if [ "$(sha256sum "$DL" | awk '{print $1}')" = "$EXPECTED_DL_SHA" ]; then echo "DL_DIGEST_REUSE_OK"; else echo "DL_DIGEST_MISMATCH_ABORT"; d1=$((SECONDS-t0)); ok 1 "$d1"; exit 1; fi
d1=$((SECONDS-t0)); ok 0 "$d1"
echo ""
mark "fresh TEXDIR skeleton (remove partial empty dir from failed attempt)"
t0=$SECONDS
rm -rf "$TEXDIR"; mkdir -p "$TEXDIR" "$TOOLROOT/texmf-home" "$TOOLROOT/texmf-var" "$TOOLROOT/texmf-config"
ls -ld "$TEXDIR" "$TOOLROOT/texmf-home" "$TOOLROOT/texmf-var" "$TOOLROOT/texmf-config"
d1=$((SECONDS-t0)); ok "$?" "$d1"
echo ""
mark "write corrected unattended profile (ALL paths under toolroot)"
t0=$SECONDS
cat > "$PROFILE" <<EOF
selected_scheme scheme-small
TEXDIR $TEXDIR
TEXMFLOCAL $TEXDIR/texmf-local
TEXMFSYSVAR $TEXDIR/texmf-var
TEXMFSYSCONFIG $TEXDIR/texmf-config
TEXMFHOME $TOOLROOT/texmf-home
TEXMFVAR $TOOLROOT/texmf-var
TEXMFCONFIG $TOOLROOT/texmf-config
binary_x86_64-linux 1
option_doc 0
option_src 0
option_autobackup 0
option_desktop_integration 0
option_file_assocs 0
option_fmt 1
option_letter 0
option_post_code 1
option_adjustpath 0
option_w32_multi_user 0
option_adjustrepo 1
EOF
cat "$PROFILE"
d1=$((SECONDS-t0)); ok "$?" "$d1"
echo ""
mark "run installer with TEXMF* env UNSET (profile sole source; no sudo)"
t0=$SECONDS
echo "INSTALL_START_UTC=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
env -u TEXMFHOME -u TEXMFVAR -u TEXMFCONFIG -u TEXMFCACHE -u TEXMFSYSVAR -u TEXMFSYSCONFIG -u TEXMFLOCAL -u TEXLIVE_INSTALL_PREFIX -u TEXLIVE_INSTALL_TEXMFSYSVAR -u TEXLIVE_INSTALL_TEXMFSYSCONFIG -u TEXLIVE_INSTALL_TEXMFLOCAL perl "$INSTDIR/install-tl" --profile "$PROFILE"
rc=$?
echo "INSTALL_EXIT:$rc"
echo "INSTALL_END_UTC=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
d1=$((SECONDS-t0)); ok "$rc" "$d1"
echo "INSTALL_DURATION_S:$d1"
df -h /tmp | tail -n 1
ls -ld "$TEXDIR" "$TEXDIR/bin/x86_64-linux" 2>&1 | head
if [ $rc -ne 0 ]; then echo "=== SUMMARY failures=$failures (installer still blocked; mechanism above) ==="; exit $failures; fi
echo ""
mark "pin installed year/version (explicit; do not spoof 2026)"
t0=$SECONDS
export PATH="$TEXDIR/bin/x86_64-linux:$PATH"
export TEXMFHOME="$TOOLROOT/texmf-home" TEXMFVAR="$TOOLROOT/texmf-var" TEXMFCONFIG="$TOOLROOT/texmf-config" TEXMFCACHE="$TOOLROOT/texmf-var" TEXLIVE_ROOT="$TEXDIR"
which -a lualatex latexmk biber bibtex kpsewhich tlmgr 2>&1
lualatex --version 2>&1 | head -n 5 || echo "LUALATEX_VERSION_FAIL rc=$?"
latexmk --version 2>&1 | head -n 5 || echo "LATEXMK_VERSION_FAIL rc=$?"
biber --version 2>&1 | head -n 5 || echo "BIBER_VERSION_FAIL rc=$?"
bibtex --version 2>&1 | head -n 5 || echo "BIBTEX_VERSION_FAIL rc=$?"
kpsewhich --version 2>&1 | head -n 5 || echo "KPSEWHICH_VERSION_FAIL rc=$?"
tlmgr --version 2>&1 | head -n 10 || echo "TLMGR_VERSION_FAIL rc=$?"
echo "--- release file ---"
cat "$TEXDIR/release-texlive.txt" 2>&1 || echo "NO_RELEASE_FILE"
d1=$((SECONDS-t0)); ok 0 "$d1"
echo ""
mark "tlmgr incremental package closure (no full all-languages)"
t0=$SECONDS
tlmgr option repository "$(tlmgr option repository | awk '{print $NF}' | head -n 1)"
echo "REPO_PINNED:$(tlmgr option repository)"
PKGS="latexmk luatex luaotfload luatexja jlreq haranoaji haranoaji-extra biblatex biber geometry xcolor graphics booktabs tabularx tools array multirow multicol needspace rotating enumitem tcolorbox fancyhdr xurl hyperref bookmark etoolbox l3packages l3kernel latex-bin collection-luatex collection-latexrecommended collection-bibtexextra collection-langjapanese"
echo "REQUESTED_PKGS:$PKGS"
tlmgr install $PKGS
rc=$?
echo "TLMGR_INSTALL_EXIT:$rc"
d1=$((SECONDS-t0)); ok "$rc" "$d1"
echo "TLMGR_DURATION_S:$d1"
if [ $rc -ne 0 ]; then echo "INCREMENTAL_FAIL: kpsewhich validation below lists exact missing"; fi
echo ""
mark "dependency validation kpsewhich required cls/sty (no production build)"
t0=$SECONDS
export PATH="$TEXDIR/bin/x86_64-linux:$PATH"
vfail=0
for q in jlreq.cls luatexja.sty luatexja-preset.sty haranoaji.sty biblatex.sty tcolorbox.sty fancyhdr.sty hyperref.sty bookmark.sty xurl.sty geometry.sty xcolor.sty graphicx.sty booktabs.sty tabularx.sty array.sty multicol.sty needspace.sty rotating.sty enumitem.sty etoolbox.sty; do
  out=$(kpsewhich "$q" 2>&1); rcq=$?
  echo "KPSE $q rc=$rcq path=${out:-NOTFOUND}"
  if [ $rcq -ne 0 ] || [ -z "$out" ]; then vfail=$((vfail+1)); fi
done
echo "KPSE_MISSING_COUNT=$vfail (references.bib excluded: route-generated, not TeXLive)"
echo "--- engine recheck ---"
lualatex --version | head -n 3; latexmk --version | head -n 3; biber --version | head -n 3
d1=$((SECONDS-t0))
if [ $vfail -eq 0 ]; then ok 0 "$d1"; else ok 1 "$d1"; echo "VALIDATION_GAP: $vfail files unresolved; alternative is targeted tlmgr install of owning packages"; failures=$((failures+1)); fi
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
echo "SUPPORTED: engine LuaLaTeX/latexmk/biber per .latexmkrc; schema deps jsonschema 4.23.0 + pypdf 6.16.2 via system python3 -m pip; poppler pdftoppm/pdftotext for inspection"
d1=$((SECONDS-t0)); ok 0 "$d1"
echo ""
echo "=== SUMMARY failures=$failures (0=toolchain ready; nonzero=actual blocker with mechanism above) ==="
exit $failures
