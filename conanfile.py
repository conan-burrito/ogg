from conans import tools, ConanFile, CMake

import os


# Note: adapted from https://github.com/conan-io/conan-center-index/blob/master/recipes/ogg/all/conanfile.py
class OggConan(ConanFile):
    name = 'ogg'
    description = 'Reference implementation of the Ogg media container'
    homepage = 'https://github.com/xiph/ogg'
    license = 'BSD-2-Clause'
    url = 'https://github.com/conan-burrito/ogg'

    generators = 'cmake'

    settings = 'os', 'arch', 'compiler', 'build_type'
    options = {'shared': [True, False], 'fPIC': [True, False]}
    default_options = {'shared': False, 'fPIC': True}

    build_policy = 'missing'

    exports_sources = ['CMakeLists.txt', 'patches/*']

    _cmake = None

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC

        # It's a C project - remove irrelevant settings
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    @property
    def source_subfolder(self):
        return 'src'

    @property
    def build_subfolder(self):
        return "_build"

    def source(self):
        tools.get(**self.conan_data["sources"][self.version], destination=self.source_subfolder, strip_root=True)

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake

        self._cmake = CMake(self)
        self._cmake.configure(build_folder=self.build_subfolder)
        return self._cmake

    def build(self):
        for patch in self.conan_data.get("patches", {}).get(self.version, []):
            tools.patch(**patch)

        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

        self.copy("COPYING", src=self.source_subfolder, dst="licenses", keep_path=False)
        tools.rmdir(os.path.join(self.package_folder, "lib", "cmake"))
        tools.rmdir(os.path.join(self.package_folder, "lib", "pkgconfig"))
        tools.rmdir(os.path.join(self.package_folder, "share"))

    def package_info(self):
        self.cpp_info.names["cmake_find_package"] = "Ogg"
        self.cpp_info.names["cmake_find_package_multi"] = "Ogg"
        self.cpp_info.components["ogglib"].names["cmake_find_package"] = "ogg"
        self.cpp_info.components["ogglib"].names["cmake_find_package_multi"] = "ogg"
        self.cpp_info.components["ogglib"].libs = ["ogg"]
