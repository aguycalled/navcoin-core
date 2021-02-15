package=mcl
$(package)_version=1.33
$(package)_download_path=https://github.com/herumi/mcl/archive/
$(package)_file_name=v$($(package)_version).tar.gz
$(package)_sha256_hash=c8e5ecf30cf7d827701ab193e858171864120eb073b96b5ecbd6cfdc70022a45
$(package)_patches=include_paths.patch

define $(package)_preprocess_cmds
  patch -p1 < $($(package)_patch_dir)/include_paths.patch
endef

define $(package)_build_cmds
  $(MAKE) GMP_DIR="$($($(package)_type)_prefix)" OPENSSL_DIR="$($($(package)_type)_prefix)"
endef

define $(package)_stage_cmds
  $(MAKE) PREFIX=$($(package)_staging_dir) install
endef
