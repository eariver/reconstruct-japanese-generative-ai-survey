#!/usr/bin/env bash
# Toolchain setup A2 — user-space TeX Live under disposable tool root.
# Saved BEFORE execution per root selection. No global apt/sudo/system changes,
# no Docker install, no source-copy writes. Official TeX/CTAN downloads only.
# Records arch/libc/disk, resolved URL/date/digest, safe extraction,
# scheme-small + incremental package closure, kpsewhich/--version validation,
# exact env/argv for caller. Preserves counters/duration/exit per step.
set -u
TOOLROOT="/tmp/opencode/jgas-texlive-20261019T133205Z"
EVIDIR="notes/rephase-1-initial-build-integration/evidence-toolchain-20261019T133205Z"
TEXDIR="$TOOLROOT/texlive"
DL="$TOOLROOT/download/install-tl-unx.tar.gz"
INSTDIR="$TOOLROOT/installer"
PROFILE="$TOOLROOT/texlive.profile"
URL="https://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz"
export TEXMFHOME="$TOOLROOT/texmf-home"
export TEXMFVAR="$TOOLROOT/texmf-var"
export TEXMFCONFIG="$TOOLROOT/texmf-config"
export TEXMFCACHE="$TOOLROOT/texmf-var"
export TEXLIVE_ROOT="$TEXDIR"
step=0; failures=0
mark(){ step=$((step+1)); echo "=== STEP $step: $1 ==="; date -u +"--- clock %Y-%m-%dT%H:%M:%SZ"; }
ok(){ echo "STEP_EXIT:$1 DURATION_S:$2"; if [ "$1" != "0" ]; then failures=$((failures+1)); echo "STEP_FAIL_RECORDED (not hidden)"; fi; }
echo "TOOLROOT=$TOOLROOT TEXDIR=$TEXDIR"
echo "EVIDIR=$EVIDIR"
echo "SCOPE TEXMFHOME=$TEXMFHOME TEXMFVAR=$TEXMFVAR TEXMFCONFIG=$TEXMFCONFIG TEXMFCACHE=$TEXMFCACHE"
echo "URL=$URL"
echo ""
mark "platform arch/libc/disk (before installer platform select)"
t0=$SECONDS
uname -s; echo "MACHINE:$(uname -m)"; ldd --version | head -n 2; getconf LONG_BIT; echo "PERL:$(perl --version | head -n 2 | tr '\n' ' ')"; df -h /tmp | tail -n 2; free -h | head -n 2
d1=$((SECONDS-t0)); ok "$?" "$d1"
echo ""
mark "toolroot layout (must exist from preparation; no source writes)"
t0=$SECONDS
ls -ld "$TOOLROOT" "$TOOLROOT/download" "$TOOLROOT/texmf-home" "$TOOLROOT/texmf-var" "$TOOLROOT/texmf-config" "$TOOLROOT/cache"
echo "SOURCE_TOUCH_CHECK: none (this script never references candidate-partial paths)"
d1=$((SECONDS-t0)); ok "$?" "$d1"
echo ""
mark "download official install-tl over https (record resolved URL/date/digest)"
t0=$SECONDS
echo "REQUEST_URL=$URL"
echo "REQUEST_DATE_UTC=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
if [ -s "$DL" ]; then echo "NOTE: download target already exists, size $(stat -c %s "$DL"), will re-verify digest (no overwrite without record)"; fi
curl -fsSL --retry 3 --retry-delay 5 -o "$DL" -w "RESOLVED_URL:%{url_effective}\nHTTP_CODE:%{http_code}\nSIZE_DOWNLOAD:%{size_download}\n" "$URL"
rc=$?
echo "CURL_EXIT:$rc"
if [ $rc -ne 0 ]; then echo "DOWNLOAD_FAIL rc=$rc"; d1=$((SECONDS-t0)); ok "$rc" "$d1"; echo "=== SUMMARY failures=$failures (blocker path; no install attempted further without archive) ==="; exit $failures; fi
echo "DOWNLOAD_DATE_UTC=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "DOWNLOAD_BYTES=$(stat -c %s "$DL")"
echo "DOWNLOAD_SHA256=$(sha256sum "$DL" | awk '{print $1}')"
d1=$((SECONDS-t0)); ok 0 "$d1"
echo ""
mark "safe archive inspection (no absolute paths, no .. traversal)"
t0=$SECONDS
tar -tzf "$DL" | head -n 20
echo "--- full entry count ---"
tar -tzf "$DL" | wc -l
echo "--- unsafe entry scan (leading / or .. component) ---"
if tar -tzf "$DL" | grep -E -q '(^/|(^|/)\.\.(/|$))'; then echo "UNSAFE_ENTRIES_FOUND"; tar -tzf "$DL" | grep -E '(^/|(^|/)\.\.(/|$))' | head; d1=$((SECONDS-t0)); ok 1 "$d1"; echo "ABORT: unsafe archive"; exit 1; else echo "ARCHIVE_SAFE_OK (no absolute/traversal entries)"; fi
d1=$((SECONDS-t0)); ok 0 "$d1"
echo ""
mark "safe extraction to installer dir (fresh; no overwrite of prior extract without record)"
t0=$SECONDS
rm -rf "$INSTDIR"; mkdir -p "$INSTDIR"
tar -xzf "$DL" -C "$INSTDIR" --strip-components=1
rc=$?
echo "EXTRACT_EXIT:$rc"
ls -la "$INSTDIR" | head -n 30
echo "INSTALL_TL_VERSION_HINT:$(grep -m1 -E 'TeX Live|version' "$INSTDIR/install-tl" | head -c 300 || true)"
d1=$((SECONDS-t0)); ok "$rc" "$d1"
if [ $rc -ne 0 ]; then echo "=== SUMMARY failures=$failures ==="; exit $failures; fi
echo ""
mark "write unattended profile (scheme-small, TEXDIR under toolroot, no docs/src to save disk)"
t0=$SECONDS
cat > "$PROFILE" <<EOF
selected_scheme scheme-small
TEXDIR $TEXDIR
TEXMFCONFIG $TOOLROOT/texmf-config
TEXMFHOME $TOOLROOT/texmf-home
TEXMFVAR $TOOLROOT/texmf-var
binary_x86_64-linux 1
option_doc 0
option_src 0
option_autobackup 0
option_desktop_integration 0
option_file_assocs 0
option_fmt 1
option_letter 0
option_post_code 1
option_sys_bin /usr/local/bin
option_sys_info /usr/local/share/info
option_sys_man /usr/local/share/man
option_w32_multi_user 0
option_adjustrepo 1
EOF
cat "$PROFILE"
d1=$((SECONDS-t0)); ok "$?" "$d1"
echo ""
mark "run installer (user-space, no sudo, portable paths under toolroot)"
t0=$SECONDS
echo "INSTALL_START_UTC=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
perl "$INSTDIR/install-tl" --profile "$PROFILE"
rc=$?
echo "INSTALL_EXIT:$rc"
echo "INSTALL_END_UTC=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
d1=$((SECONDS-t0)); ok "$rc" "$d1"
echo "INSTALL_DURATION_S:$d1"
df -h /tmp | tail -n 1
ls -ld "$TEXDIR" "$TEXDIR/bin/x86_64-linux" 2>&1 | head
if [ $rc -ne 0 ]; then echo "=== SUMMARY failures=$failures (installer blocker; report actual mechanism) ==="; exit $failures; fi
echo ""
mark "pin installed year/version (explicit; do not spoof 2026)"
t0=$SECONDS
export PATH="$TEXDIR/bin/x86_64-linux:$PATH"
echo "PATH_HEAD=$TEXDIR/bin/x86_64-linux"
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
mark "tlmgr incremental package closure (no full all-languages; record counters)"
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
if [ $rc -ne 0 ]; then echo "INCREMENTAL_FAIL: will attempt kpsewhich validation to list exact missing before declaring blocker"; fi
echo ""
mark "dependency validation kpsewhich required cls/sty/cfg (no production build)"
t0=$SECONDS
vfail=0
for q in jlreq.cls jgaisurvey.sty luatexja.sty luatexja-preset.sty haranoaji.sty biblatex.sty tcolorbox.sty fancyhdr.sty hyperref.sty bookmark.sty xurl.sty geometry.sty xcolor.sty graphicx.sty booktabs.sty tabularx.sty array.sty multicol.sty needspace.sty rotating.sty enumitem.sty etoolbox.sty references.bib; do
  # references.bib is route-generated, not TeXLive; expect NOTFOUND here (informational)
  out=$(kpsewhich "$q" 2>&1); rcq=$?
  echo "KPSE $q rc=$rcq path=${out:-NOTFOUND}"
  case "$q" in references.bib) ;; *) if [ $rcq -ne 0 ] || [ -z "$out" ]; then vfail=$((vfail+1)); fi;; esac
done
echo "KPSE_MISSING_COUNT (excl references.bib)=$vfail"
echo "--- engine --version recheck ---"
lualatex --version | head -n 3; latexmk --version | head -n 3; biber --version | head -n 3
d1=$((SECONDS-t0)); ok "$([ $vfail -eq 0 ] && echo 0 || echo 1)" "$d1"
if [ $vfail -ne 0 ]; then echo "VALIDATION_GAP: $vfail required files unresolved; feasible alternative is targeted tlmgr install of owning packages (see tlmgr search) without full rebuild"; failures=$((failures+1)); fi
echo ""
mark "exact env/argv for caller (supported toolchain)"
t0=$SECONDS
echo "CALLER_PATH=$TEXDIR/bin/x86_64-linux:\$PATH"
echo "CALLER_TEXDIR=$TEXDIR"
echo "CALLER_TEXMFHOME=$TEXMFHOME"
echo "CALLER_TEXMFVAR=$TEXMFVAR"
echo "CALLER_TEXMFCONFIG=$TEXMFCONFIG"
echo "CALLER_TEXMFCACHE=$TEXMFCACHE"
echo "CALLER_TEXLIVE_ROOT=$TEXLIVE_ROOT"
echo 'CALLER_ARGV_LUALATEX=lualatex -synctex=1 -interaction=nonstopmode -file-line-error -halt-on-error %O %S'
echo 'CALLER_ARGV_LATEXMK=latexmk -lualatex -synctex=1 -interaction=nonstopmode -file-line-error -halt-on-error main.tex'
echo 'CALLER_ARGV_BIBER=biber %O %B'
echo "SUPPORTED: engine LuaLaTeX/latexmk/biber per .latexmkrc; schema deps jsonschema 4.23.0 + pypdf 6.16.2 already present via system python3 -m pip (not TeX); poppler pdftoppm/pdftotext for render/inspection"
d1=$((SECONDS-t0)); ok 0 "$d1"
echo ""
echo "=== SUMMARY failures=$failures (0=toolchain ready for disposable-build caller; nonzero=actual blocker with mechanism above; NOT a build PASS) ==="
exit $failures
