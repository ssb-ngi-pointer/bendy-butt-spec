with import <nixpkgs> {};

( let
    bencodepy = python38.pkgs.buildPythonPackage rec {
      pname = "bencode.py";
      version = "4.0.0";

      src = python38.pkgs.fetchPypi {
        inherit pname version;
        sha256 = "0p70lsi504wn15x6xfwrlbm5k0qkc0rbdl4k11jim9952zdcq91a";
      };

      doCheck = false;
      propagatedBuildInputs = [ python38.pkgs.pbr ];

      meta = {
        homepage = "https://pypi.org/project/bencode.py/";
        description = "List processing tools and functional utilities";
      };
    };

  in python38.withPackages (ps: [bencodepy])
).env