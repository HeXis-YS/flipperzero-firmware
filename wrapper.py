#!/usr/bin/env python

import os
import sys

class CompilerWrapper():
    def __init__(self, argv):
        self.argv0 = argv[0]
        self.args = argv[1:]
        self.real_compiler = None

    def set_real_compiler(self):
        compiler_path = os.path.dirname(os.path.abspath(__file__))
        if os.path.islink(__file__):
            compiler = os.path.basename(os.readlink(__file__))
        else:
            compiler = os.path.basename(os.path.abspath(__file__))
        self.real_compiler = os.path.join(
            compiler_path,
            compiler + "_")

    def parse_custom_flags(self):
        newargs = []
        if os.path.exists("/tmp/optimize") and not ("-Ofast" in self.args or "-DOs" in self.args):
                newargs += ["-O2"]
        if not "-Ofast" in self.args:
            newargs += [
                # -O3
                "-fgcse-after-reload",
                "-fipa-cp-clone",
                "-floop-interchange",
                "-floop-unroll-and-jam",
                "-fpeel-loops",
                "-fpredictive-commoning",
                "-fsplit-loops",
                "-fsplit-paths",
                "-ftree-loop-distribution",
                "-ftree-partial-pre",
                "-funswitch-loops",
                "-fvect-cost-model=dynamic",
                "-fversion-loops-for-strides",
                # -Ofast
                "-fallow-store-data-races",
                "-fassociative-math",
                "-fcx-limited-range",
                "-fexcess-precision=fast",
                "-ffinite-math-only",
                "-fno-math-errno",
                "-freciprocal-math",
                "-fno-semantic-interposition",
                "-fno-signed-zeros",
                "-fno-trapping-math",
                "-funsafe-math-optimizations",
            ]
        newargs += [
            "-fipa-pta",
            "-fdevirtualize-at-ltrans",
            # "-fno-semantic-interposition",
            "-fgraphite-identity",
            "-floop-nest-optimize",
            "-fno-common",
            "-fno-plt",
        ]
        self.args += newargs

    def invoke_compiler(self):
        self.set_real_compiler()
        self.parse_custom_flags()
        os.execv(self.real_compiler, [self.argv0] + self.args)


def main(argv):
    cw = CompilerWrapper(argv)
    cw.invoke_compiler()

if __name__ == "__main__":
    main(sys.argv)
