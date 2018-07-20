package=unbound
$(package)_version=1.7.3
$(package)_download_path=http://unbound.net/downloads/
$(package)_file_name=$(package)-$($(package)_version).tar.gz
$(package)_sha256_hash=c11de115d928a6b48b2165e0214402a7a7da313cd479203a7ce7a8b62cba602d
$(package)_dependencies=openssl

define $(package)_set_vars
  $(package)_config_opts=--with-ssl=$(host_prefix) --disable-gost --disable-ecdsa
endef

define $(package)_config_cmds
  $($(package)_autoconf)
endef

define $(package)_build_cmds
  $(MAKE)
endef

define $(package)_stage_cmds
  $(MAKE) DESTDIR=$($(package)_staging_dir) install-all
endef

define $(package)_postprocess_cmds
endef
