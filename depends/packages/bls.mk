package=bls
$(package)_version=bls-signatures
$(package)_download_path=https://index.nav.community/depends-sources/
$(package)_file_name=$($(package)_version).tar.gz
$(package)_sha256_hash=9c1731871e44f696d1e1f751e15f80357e4692313302e6248814b93296e3ee8e
$(package)_dependencies=gmp

define $(package)_set_vars
  $(package)_config_opts=-DCMAKE_INSTALL_PREFIX=$($(package)_staging_dir)/$(host_prefix)
  $(package)_config_opts+= -DCMAKE_PREFIX_PATH=$(host_prefix)
  $(package)_config_opts+= -DSTLIB=ON -DSHLIB=OFF -DSTBIN=ON
  $(package)_config_opts_linux=-DOPSYS=LINUX -DCMAKE_SYSTEM_NAME=Linux
  $(package)_config_opts_darwin=-DOPSYS=MACOSX -DCMAKE_SYSTEM_NAME=Darwin
  $(package)_config_opts_mingw32=-DOPSYS=WINDOWS -DCMAKE_SYSTEM_NAME=Windows -DCMAKE_SHARED_LIBRARY_LINK_C_FLAGS="" -DCMAKE_SHARED_LIBRARY_LINK_CXX_FLAGS=""
  $(package)_config_opts_i686+= -DWSIZE=32
  $(package)_config_opts_x86_64+= -DWSIZE=64
  $(package)_config_opts_arm+= -DWSIZE=32
  $(package)_config_opts_debug=-DDEBUG=ON -DCMAKE_BUILD_TYPE=Debug

  ifneq ($(darwin_native_toolchain),)
    $(package)_config_opts_darwin+= -DCMAKE_AR="$(host_prefix)/native/bin/$($(package)_ar)"
    $(package)_config_opts_darwin+= -DCMAKE_RANLIB="$(host_prefix)/native/bin/$($(package)_ranlib)"
  endif
endef

define $(package)_config_cmds
  export CC="$($(package)_cc)" && \
  export CXX="$($(package)_cxx)" && \
  export CFLAGS="$($(package)_cflags) $($(package)_cppflags)" && \
  export CXXFLAGS="$($(package)_cxxflags) $($(package)_cppflags)" && \
  export LDFLAGS="$($(package)_ldflags)" && \
  mkdir build && cd build && \
  cmake ../ $($(package)_config_opts)
endef

define $(package)_build_cmds
  cd build && \
  $(MAKE) $($(package)_build_opts)
endef

define $(package)_stage_cmds
  cd build && \
  $(MAKE) install
endef
