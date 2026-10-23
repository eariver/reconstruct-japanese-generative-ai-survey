# Frozen source pins R2 (52 intended files, full 64-char SHA, DST current with Fix1+Fix2)

HEAD: `409b292756dd1277b9dfae87679934c0d2ce251c` (detached, no new HEAD)
Commands (read-only, exits 0): `git diff --name-only | sort`, `git ls-files --others --exclude-standard | grep -v __pycache__ | grep -v \.pyc$ | grep -v ^tmpvr07sdme/ | grep -v ^tmp | sort`, `sha256sum <file> | cut -d" " -f1` (full 64-char, not truncated).

## Tracked modified (24)

- `cde4f115608ece8d74b88fac5c66f9981b5769a9ea64f1c1ccb75dfe2602358c  config/survey-production-v2.json`
- `8c779e60a6938450ba8ef9d4482a6069d23f0d6e1f4faf5b3a3ad08991cfe0ca  .github/workflows/build-special-pdf.yml`
- `82840cf5aa5ea36187ece2084d59bc65b8f0e2f18b6ef72561f53f3fc6101902  .github/workflows/build-weekly-survey.yml`
- `872f31e8879c8c7b3718e1dfcf092312a7256e1d6a60c532fb61108aaefda6fc  .github/workflows/survey-production-v2-export-publication-preview.yml`
- `2d0a9499af0456c071f88b5deb2971b7abbee838ed73cf5a5595ae418f41e9ed  schemas/publication-surface-revalidation.schema.json`
- `0d8f0e9e66ccb885131645a24abfe24b94743cb0476e94fe923eb30eca9ef4c3  schemas/reader-manuscript-v2.schema.json`
- `f10de43eb85be32559d244f77d79ff76a9d3e803072a930ed164b12361dc5cd1  schemas/reader-surface-gate-v2.schema.json`
- `e8598239d3ca00441f61110fd77a7b7edf063ac15a7a6a1c2efdb38e73d6699b  schemas/reader-surface-semantic-review-v2.schema.json`
- `c6cd195781449a0b715121c74031c98efa4b1e21b23a318c480897503c8c9a04  scripts/run_semantic_publication_v2_interactive_base.py`
- `b3e0d976e6dbb4ce956067be2c4c60dfd0a5e9104ccde6203f847237fad830cd  scripts/run_semantic_publication_v2_interactive.py`
- `12995a8415f8b2ee28fab783b1688f2b3012aadb045f03ad95cf7e5be3d8f78d  scripts/survey_agent_control_v2.py`
- `d33ddc5f6184be3442988d08db621df110ae12c08ebe4e88bb073bd89860ffa0  scripts/survey_handoff_v2.py`
- `5ea6c8d69dd675fd43cfcfc65067baa682d98d1bdd2f72d15d1cfd3b4d2cfc07  scripts/survey_human_gate_v2.py`
- `c87e693e2a91406dc6c49aee04ae9be5ceae72b81746d768f13bfebc98f6b261  scripts/survey_orchestrator_v2.py`
- `a492c5eeba94bd66c02735f64533489945af68f21b1846284c90a87b1bc3cfc8  scripts/survey_production_v2.py`
- `3c3a8ffac6f87bc949d6b82b89f6af9ccc970b4f9e8fbad2ee1f3793fb3cba19  scripts/survey_profiled_freeze_v2.py`
- `2f7691db90f8bd55bcff1efc7c4ee1fd136e7bccff8399452683550c07a752b2  scripts/survey_reader_publication_v2.py`
- `879eedd24ef76485007f5f6c3143fcf75d32b0a092a6785703155c4813e4d37c  scripts/survey_reader_surface_gate_v2.py`
- `b1462e41d35a458e47d121aad69774d550f5f5db0497f24580a050621233de15  scripts/survey_schema_v2.py`
- `ddee657794490c0d9412216bc631f098b06cf401556c8932439e5fcba7f8ffc2  scripts/survey_semantic_quality_v2.py`
- `de02bf98a98821b3ee9358c5dc7ee63d3e18e8ce9684c95b515abd3ce935cee9  scripts/survey_stage_validation_v2.py`
- `2d3be54c9f42fa73cd8c7282ebb85d9a5c66ffa8c0dfb8ab726e8fcc31bed096  scripts/survey_weekly_derivation_v2.py`
- `036601ac18b9b23639d822edd06499ccbea0b913c62b0573c6926a4ef19dba33  scripts/survey_weekly_mechanical_refresh_v2.py`
- `035645caa06eb77e5416ae7a54bc1fb7b987e0b575a02bd4b512bccb5d683aec  templates/survey/jgaisurvey.sty`

## New core (28: 10 schemas + 9 scripts + 9 tests)

- `5623c0d92e3dfc5415e1ab73c73b3d5f1b147f265f2255469cede2ec333a4607  schemas/editorial-correction-proposal-v2.schema.json`
- `043ce8a565385549265d6666642c2e3ec8ce0d8e8e5544a7eddfb32691478250  schemas/editorial-manuscript-spec-v2.schema.json`
- `b7c82476047373995cd5c4733ce2ba0b1c53fef72a84bceb26feec9078fea4ba  schemas/editorial-publication-build-record-v2.schema.json`
- `7beebcef48d7777144f7df7ce3fddc27c0d39df685fdc49cbfdd7d798c7e61e9  schemas/editorial-publication-set-v2.schema.json`
- `494a1d152c76bca810d30e743d567210f130cb4197561d82b276f24ef69441bc  schemas/editorial-publication-source-manifest-v2.schema.json`
- `347e5499259ac878e28bc66b4e9ea62af1f5eb71a3f428558120a9f5d549855c  schemas/editorial-retention-manifest-v2.schema.json`
- `4fa6172338072258f1f3c204b27331ac79a35b2af9d42ac6a2e8be7a34e32e46  schemas/editorial-staged-source-manifest-v2.schema.json`
- `50b5dc3ee05c496b2c2da13377c5ee0a883dfb52d9b9785189cb00a75d6e4db4  schemas/editorial-toolchain-spec-v2.schema.json`
- `4dadf873096f31cf564a7db4fee42a1fc8cdd8fc039dd14a7ee01cf26043e8ca  schemas/longform-publication-source-manifest-v2.schema.json`
- `7bae9d2ac753c83521165c76c9e461ce40ac4e704d9b44d3518ae7b88fbd0643  schemas/longform-reader-input-v2.schema.json`
- `79bf910d79c93768824050e92cc770ce163d235b6746f82859723b59353dd292  scripts/survey_editorial_correction_proposal_v2.py`
- `fcbeee43ceaac80d16b2b9afceee784321f7ccca2cf80e250d718eb5e4eaed5d  scripts/survey_editorial_current_authority_v2.py`
- `d57542e0e3e54a2bdbcbd957df99d738d1659e9e78f71dbb8bfab9583a87eb1f  scripts/survey_editorial_publication_v2.py`
- `036d258fa58fc876956c79cae9f51b861a731b3128a73084af921ead28a52771  scripts/survey_editorial_retention_v2.py`
- `0fb23e83caec01f7d94a80bdaaa5714741d9d8c6496a0f630d99e06c206ea355  scripts/survey_editorial_staged_source_v2.py`
- `c09c5558f9668906b7d2ed34c55281d5f6d9ed279d3237a8ffc18ac84ea41149  scripts/survey_longform_derivation_v2.py`
- `2da1da8ccd263c27f4cf0d0812d7c7d8ebe77924055e1bcfa7b43cbb016e5791  scripts/survey_longform_generated_v2.py`
- `4d235a388955dcedd34d6a7dc5ac7761f9fc91de8bc723eb11f68cec6a229195  scripts/survey_longform_semantic_publication_v2.py`
- `e897a638d9c113944185a7e7c76c4fd9f14d5a5bfbf06d3741b07b4ca387fa7d  scripts/survey_publication_set_v2.py`
- `07ede73ae117ef4c40f31ef981acf3144e793d5a418ea7801c3a6a74ecda6b5e  tests/test_group_c_editorial_consumers_v2.py`
- `f581fad0a483303f2bed1de080dd1a9e6f07928d228ef8f24d7c4a7c1242dbac  tests/test_survey_editorial_correction_proposal_v2.py`
- `c567715dfb4ffa04e7d70dfcf42072cf194d0d9239c2e5b664f7098eaa62009f  tests/test_survey_editorial_current_authority_v2.py`
- `4155baab733e8bddc0b7cbc34b83fe801def2927a716d43132321f8f083d614e  tests/test_survey_editorial_retention_v2.py`
- `a3bb0f2369ffc131e8ad645759105d165a62fa114e9b4088a2497e4a13dfa036  tests/test_survey_editorial_staged_source_v2.py`
- `ce687447539a99eb92532bc34246a271fb489b259e63b31ed6699fcc12fbf913  tests/test_survey_longform_derivation_v2.py`
- `4a03b564f8fa4dd39f2b48766ddb7612cf2d8d4dacdcc42ac39f637d2bca11a4  tests/test_survey_longform_publication_integration_v2.py`
- `0cef7a6b648a60b93bd403bef7115ff8417db3c8fd3bff925d5728bd899eeda7  tests/test_survey_publication_set_v2.py`
- `b3b8cf3947eea1798dbffcb8e22acf0a5b92588b5b160938bed9fed453be0223  tests/test_survey_schema_cache_v2.py`

Excluded (preserved, not SOURCE): `scripts/__pycache__/` (22 `.pyc`), `tests/__pycache__/` (1 `.pyc`), `tmpvr07sdme/` (43 files), `tmp*/`, `*.pyc`, fixture authority `sources/`/`surveys/`, packet `smoke/`/`diagnostic-*/`, `DIAG` copies. No `.git/` in SOURCE file list; no `objects/info/alternates` (absent); no hardlinks (inodes differ); `git remote -v` empty in fixtures.
